import random

class MenuItem:
    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_price(self):
        return self._price

    def set_price(self, price):
        self._price = price

    def total_price(self, quantity: int) -> float:
        return self._price * quantity


class Beverage(MenuItem):
    def __init__(self, name: str, price: float, size_ml: int):
        super().__init__(name, price)
        self._size_ml = size_ml

    def get_size_ml(self):
        return self._size_ml

    def set_size_ml(self, size_ml: int):
        self._size_ml = size_ml

    def total_price(self, quantity: int, has_main_course: bool = False) -> float:
        tax = 0.1  # 10% impuesto
        discount = 0.1 if has_main_course else 0
        return super().total_price(quantity) * (1 + tax) * (1 - discount)


class Appetizer(MenuItem):
    def __init__(self, name: str, price: float, is_fried: bool):
        super().__init__(name, price)
        self._is_fried = is_fried

    def get_is_fried(self):
        return self._is_fried

    def set_is_fried(self, is_fried: bool):
        self._is_fried = is_fried


class MainCourse(MenuItem):
    def __init__(self, name: str, price: float, origin: str):
        super().__init__(name, price)
        self._origin = origin

    def get_origin(self):
        return self._origin

    def set_origin(self, origin: str):
        self._origin = origin


class Order:
    def __init__(self):
        self.order_number = random.randint(1000, 9999)
        self.items = []

    def add(self, item: MenuItem, quantity: int):
        self.items.append((item, quantity))

    def has_main_course(self):
        return any(isinstance(item, MainCourse) for item, _ in self.items)

    def total(self) -> float:
        has_main = self.has_main_course()
        total = 0
        for item, qty in self.items:
            if isinstance(item, Beverage):
                total += item.total_price(qty, has_main)
            else:
                total += item.total_price(qty)
        return total

    def apply_discount(self) -> float:
        subtotal = self.total()
        discount = 0.0
        if subtotal > 80000:
            discount = 0.15
        elif subtotal > 50000:
            discount = 0.10
        elif subtotal > 30000:
            discount = 0.05
        return subtotal * (1 - discount)

    def summary(self):
        print(f"\nPedido #{self.order_number}")
        print("Resumen del pedido:")
        has_main = self.has_main_course()
        for item, qty in self.items:
            if isinstance(item, Beverage):
                price = item.total_price(qty, has_main)
            else:
                price = item.total_price(qty)
            print(f" - {item.get_name()} x{qty} = ${price:,.2f}")
        print(f"\nSubtotal: ${self.total():,.2f}")
        print(f"Total con descuento: ${self.apply_discount():,.2f}")


# Sistema de pagos
class MedioPago:
    def __init__(self):
        pass

    def pagar(self, monto):
        raise NotImplementedError("Subclases deben implementar pagar()")


class Tarjeta(MedioPago):
    def __init__(self, numero, cvv):
        super().__init__()
        self.numero = numero
        self.cvv = cvv

    def pagar(self, monto):
        print(f"Pagando {monto} con tarjeta {self.numero[-4:]}")


class Efectivo(MedioPago):
    def __init__(self, monto_entregado):
        super().__init__()
        self.monto_entregado = monto_entregado

    def pagar(self, monto):
        if self.monto_entregado >= monto:
            print(f"Pago realizado en efectivo. Cambio: {self.monto_entregado - monto}")
        else:
            print(f"Fondos insuficientes. Faltan {monto - self.monto_entregado} para completar el pago.")


# ---------- Elementos del Menú ----------
coca_cola = Beverage("CocaCola", 5000, 350)
lemonade = Beverage("Limonada", 4000, 300)
beer = Beverage("Cerveza", 7000, 330)
water = Beverage("Agua", 2000, 500)

arepa_rellena = Appetizer("Arepa Rellena", 6000, True)
empanada = Appetizer("Empanada", 2500, True)
patacon = Appetizer("Patacón", 3000, True)
nachos = Appetizer("Nachos", 5500, False)

spaguetti = MainCourse("Spaguetti", 18000, "Italiana")
beef = MainCourse("Carne Asada", 25000, "Colombiana")
pork_loin = MainCourse("Lomo de Cerdo", 23000, "Internacional")
hamburger = MainCourse("Hamburguesa", 20000, "Americana")
bandeja_paisa = MainCourse("Bandeja Paisa", 30000, "Colombiana")

# ---------- Ejecución ----------
if __name__ == "__main__":
    order = Order()
    order.add(coca_cola, 2)
    order.add(nachos, 1)
    order.add(spaguetti, 1)
    order.add(bandeja_paisa, 1)
    order.add(empanada, 3)
    order.summary()

    print("\n--- Pago ---")
    total = order.apply_discount()
    pago = Tarjeta("1234567890123456", 123)
    pago.pagar(total)
