from main import Product, Category


def test_product_init():
    product = Product("Книга", "Толстая", 350.0, 100)
    assert product.name == "Книга"
    assert product.description == "Толстая"
    assert product.price == 350.0
    assert product.quantity == 100


def test_category_init():
    product1 = Product("Книга", "Толстая", 350.0, 100)
    product2 = Product("Смартфон", "Android", 50000.0, 5)
    category = Category("Электроника", "Гаджеты", [product1, product2])
    assert category.name == "Электроника"
    assert category.description == "Гаджеты"
    assert category.products[0].name == "Книга"
    assert len(category.products) == 2


def test_category_counters():
    p1 = Product("A", "Описание", 100, 1)
    p2 = Product("B", "Описание", 200, 1)
    cat1 = Category("Кат1", "Описание", [p1, p2])
    assert Category.category_count == 1
    assert Category.product_count == 2

    p3 = Product("C", "Описание", 300, 1)
    p4 = Product("D", "Описание", 400, 1)
    p5 = Product("E", "Описание", 500, 1)
    cat2 = Category("Кат2", "Описание", [p3, p4, p5])
    assert Category.category_count == 2
    assert Category.product_count == 5