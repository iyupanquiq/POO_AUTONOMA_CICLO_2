"""Demo del 50%: ejecuta con  python main.py"""
from datetime import date, timedelta
from modelos import Categoria, Producto, ProductoPerecible, Cliente, Venta
from patrones import GestorInventario, UsuarioFactory

print("1. USUARIOS")
gerente = UsuarioFactory.crear("gerente", 1, "Ana", "1234")
vendedor = UsuarioFactory.crear("vendedor", 2, "Luis", "abcd")
for u in (gerente, vendedor):
    print(u.descripcion())
print("Login correcto?", gerente.iniciar_sesion("1234"), "| Login incorrecto?", gerente.iniciar_sesion("x"))

print("\n2. SINGLETON")
g1, g2 = GestorInventario(), GestorInventario()
print("Misma instancia?", g1 is g2)

print("\n3. PRODUCTOS")
bebidas = Categoria(1, "Bebidas")
gaseosa = Producto(1, "Gaseosa", 3.50, 50)
yogurt = ProductoPerecible(2, "Yogurt", 5.00, 20, date.today() + timedelta(days=3))
for p in (gaseosa, yogurt):
    bebidas.agregar_producto(p)
    g1.agregar_producto(p)
    print(p)

print("\n4. VENTA")
cliente = Cliente(1, "Carlos Ruiz", "12345678")
venta = Venta(1, cliente, vendedor)
venta.agregar_detalle(gaseosa, 5)
venta.agregar_detalle(yogurt, 4)
g1.registrar_venta(venta)
for d in venta.detalles:
    print(f"  {d.producto.nombre} x{d.cantidad} = S/ {d.calcular_subtotal():.2f}")
print(f"TOTAL: S/ {venta.calcular_total():.2f}")
print("Stock actual ->", gaseosa.stock, "gaseosas,", yogurt.stock, "yogures")

print("\n5. ENCAPSULAMIENTO")
try:
    venta.agregar_detalle(gaseosa, 999)
except ValueError as e:
    print("Error controlado:", e)
