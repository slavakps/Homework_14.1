import pytest
from src.main import Product, Category


@pytest.fixture
def product_samsung():
    return Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )


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
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
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
