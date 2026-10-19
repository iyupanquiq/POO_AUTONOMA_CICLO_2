"""Modelos del Sistema de Gestión de Ventas e Inventario."""
from datetime import date


# ───────────── USUARIOS (herencia + polimorfismo + encapsulamiento) ─────────────
class Usuario:
    def __init__(self, id_usuario, nombre, contrasena):
        self._id = id_usuario               # protegido
        self._nombre = nombre               # protegido
        self.__contrasena = contrasena      # privado

    @property
    def nombre(self):
        return self._nombre

    def iniciar_sesion(self, contrasena):
        return self.__contrasena == contrasena

    def permisos(self):                     # se redefine en las hijas
        return []

    def descripcion(self):
        return f"{self._nombre} ({self.__class__.__name__}) - permisos: {', '.join(self.permisos())}"


class Gerente(Usuario):
    def permisos(self):
        return ["ver_stock", "registrar_venta", "agregar_producto", "eliminar_producto", "ver_reportes"]


class Vendedor(Usuario):
    def permisos(self):
        return ["ver_stock", "registrar_venta"]


# ───────────── PRODUCTOS ─────────────
class Categoria:
    def __init__(self, id_categoria, nombre):
        self.id = id_categoria
        self.nombre = nombre
        self.productos = []                 # agregación: la categoría agrupa productos

    def agregar_producto(self, producto):
        self.productos.append(producto)
        producto.categoria = self


class Producto:
    def __init__(self, id_producto, nombre, precio, stock, categoria=None):
        self.id = id_producto
        self.nombre = nombre
        self.precio = precio
        self.__stock = 0
        self.stock = stock                  # pasa por el setter (valida)
        self.categoria = categoria

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, valor):
        if valor < 0:
            raise ValueError(f"Stock insuficiente para '{self.nombre}'")
        self.__stock = valor

    def precio_final(self):                 # se redefine en la hija
        return self.precio

    def __str__(self):
        return f"{self.nombre} | S/ {self.precio_final():.2f} | stock: {self.stock}"


class ProductoPerecible(Producto):
    """Producto con fecha de vencimiento: tiene 30% de descuento si vence en <= 7 días."""
    def __init__(self, id_producto, nombre, precio, stock, vencimiento, categoria=None):
        super().__init__(id_producto, nombre, precio, stock, categoria)
        self.vencimiento = vencimiento

    def precio_final(self):
        dias = (self.vencimiento - date.today()).days
        return self.precio * 0.7 if dias <= 7 else self.precio


# ───────────── CLIENTE Y VENTAS ─────────────
class Cliente:
    def __init__(self, id_cliente, nombre, documento, telefono=""):
        self.id = id_cliente
        self.nombre = nombre
        self.documento = documento
        self.telefono = telefono


class DetalleVenta:
    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad
        self.precio_unitario = producto.precio_final()

    def calcular_subtotal(self):
        return self.precio_unitario * self.cantidad


class Venta:
    def __init__(self, id_venta, cliente, vendedor):
        self.id = id_venta
        self.fecha = date.today()
        self.cliente = cliente              # asociación
        self.vendedor = vendedor            # asociación
        self.detalles = []                  # composición: los detalles no existen sin la venta

    def agregar_detalle(self, producto, cantidad):
        producto.stock -= cantidad          # valida y descuenta stock
        self.detalles.append(DetalleVenta(producto, cantidad))

    def calcular_total(self):
        return sum(d.calcular_subtotal() for d in self.detalles)
