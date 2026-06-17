class Product:
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    # 1. Общие атрибуты класса
    category_count = 0
    product_count = 0

    # 2. Обычные атрибуты с типами
    name: str
    description: str
    products: list

    def __init__(self, name, description, products):
        # 3. Личные атрибуты
        self.name = name
        self.description = description
        self.products = products


        Category.category_count += 1
        Category.product_count += len(self.products)