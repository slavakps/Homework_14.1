import pytest
from src.main import Product, Category


@pytest.fixture
def product_samsung():
    return Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера",
                   180000.0, 5)


@pytest.fixture
def product_iphone():
    return Product("iPhone 15", "512GB, Gray space", 210000.0, 8)


@pytest.fixture
def product_xiaomi():
    return Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)


@pytest.fixture(autouse=True)
def reset_counters():
    """Сбрасываем счетчики перед каждым тестом"""
    Category.category_count = 0
    Category.product_count = 0
    yield
    # Дополнительные действия после теста (если нужны)


def test_product_initialization(product_samsung):
    """Тест корректности инициализации продукта"""
    assert product_samsung.name == "Samsung Galaxy S23 Ultra"
    assert product_samsung.description == "256GB, Серый цвет, 200MP камера"
    assert product_samsung.price == 180000.0
    assert product_samsung.quantity == 5


@pytest.fixture
def smartphone_category(product_samsung, product_iphone):
    return Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации,"
        " но и получения дополнительных функций для удобства жизни",
        [product_samsung, product_iphone],
    )


@pytest.fixture
def tv_category(product_xiaomi):
    return Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром",
        [product_xiaomi],
    )


def test_category_initialization(smartphone_category, product_samsung, product_iphone):
    """Тест корректности инициализации категории"""
    assert smartphone_category.name == "Смартфоны"
    assert smartphone_category.description == (
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
    )
    assert len(smartphone_category.products) == 2
    assert product_samsung in smartphone_category.products
    assert product_iphone in smartphone_category.products


def test_category_count(smartphone_category, tv_category):
    """Тест подсчета количества категорий"""
    assert Category.category_count == 2


def test_product_count(smartphone_category, tv_category):
    """Тест подсчета общего количества продуктов"""
    assert Category.product_count == 3


def test_product_price_setter_valid(product_samsung):
    """Тест корректного изменения цены через сеттер"""
    product_samsung.price = 190000.0
    assert product_samsung.price == 190000.0


def test_product_price_setter_negative(product_samsung, capsys):
    """Тест реакции на отрицательную цену"""
    original_price = product_samsung.price
    product_samsung.price = -100
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product_samsung.price == original_price  # Цена не изменилась


def test_product_price_setter_zero(product_samsung, capsys):
    """Тест реакции на нулевую цену"""
    original_price = product_samsung.price
    product_samsung.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product_samsung.price == original_price  # Цена не изменилась


def test_product_private_price_attribute(product_samsung):
    """Тест недоступности приватного атрибута цены"""
    with pytest.raises(AttributeError):
        product_samsung.__price


def test_product_info_format(product_samsung):
    """Тест формата вывода информации о продукте"""
    assert product_samsung.product_info == (
        "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."
    )


def test_category_products_info(smartphone_category):
    """Тест вывода информации о продуктах категории"""
    expected_output = (
        "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n"
        "iPhone 15, 210000.0 руб. Остаток: 8 шт."
    )
    assert smartphone_category.products_info == expected_output


def test_category_add_product(smartphone_category, product_xiaomi):
    """Тест добавления продукта в категорию"""
    initial_count = len(smartphone_category.products)
    smartphone_category.add_product(product_xiaomi)
    assert len(smartphone_category.products) == initial_count + 1
    assert product_xiaomi in smartphone_category.products
    assert Category.product_count == 3  # Учитываем продукты из других фикстур


def test_category_products_copy(smartphone_category):
    """Тест, что products возвращает копию списка"""
    products_copy = smartphone_category.products
    products_copy.append("invalid product")
    assert "invalid product" not in smartphone_category.products
