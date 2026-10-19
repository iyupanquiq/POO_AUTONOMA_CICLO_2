"""Patrones de diseño: Singleton (GestorInventario) y Factory Method (UsuarioFactory)."""
from modelos import Gerente, Vendedor


class GestorInventario:
    """SINGLETON: una sola instancia que guarda productos, clientes y ventas."""
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.productos = []
            cls._instancia.clientes = []
            cls._instancia.ventas = []
        return cls._instancia

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def buscar_producto(self, nombre):
        return next((p for p in self.productos if p.nombre.lower() == nombre.lower()), None)

    def registrar_venta(self, venta):
        self.ventas.append(venta)


class UsuarioFactory:
    """FACTORY METHOD: crea el tipo de usuario según el rol."""
    @staticmethod
    def crear(rol, id_usuario, nombre, contrasena):
        roles = {"gerente": Gerente, "vendedor": Vendedor}
        if rol.lower() not in roles:
            raise ValueError(f"Rol desconocido: {rol}")
        return roles[rol.lower()](id_usuario, nombre, contrasena)
