import pytest
from src.main import Product, Category, LawnGrass, Smartphone


@pytest.fixture
def product_samsung():
    return Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)


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


class TestProduct:
    @pytest.fixture
    def sample_products(self):
        product1 = Product("Телефон", "Смартфон", 50000.0, 10)
        product2 = Product("Ноутбук", "Игровой", 100000.0, 5)
        zero_product = Product("Аксессуар", "Чехол", 1000.0, 0)
        return product1, product2, zero_product

    def test_str_representation(self, sample_products):
        """Тест строкового представления продукта"""
        product1, product2, _ = sample_products
        assert str(product1) == "Телефон, 50000.0 руб. Остаток: 10 шт."
        assert str(product2) == "Ноутбук, 100000.0 руб. Остаток: 5 шт."

    def test_addition_of_products(self, sample_products):
        """Тест сложения продуктов"""
        product1, product2, _ = sample_products
        assert product1 + product2 == 50000.0 * 10 + 100000.0 * 5
        assert product2 + product1 == product1 + product2  # коммутативность

    def test_addition_with_zero_quantity(self, sample_products):
        """Тест сложения с нулевым количеством"""
        product1, _, zero_product = sample_products
        assert product1 + zero_product == 50000.0 * 10 + 1000.0 * 0


@pytest.fixture
def smartphone():
    return Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
        95.5,
        "S23 Ultra",
        256,
        "Серый"
    )

def test_create_smartphone(smartphone):
    assert smartphone.name == "Samsung Galaxy S23 Ultra"
    assert smartphone.description == "256GB, Серый цвет, 200MP камера"
    assert smartphone.price == 180000.0
    assert smartphone.quantity == 5
    assert smartphone.efficiency == 95.5
    assert smartphone.model == "S23 Ultra"
    assert smartphone.memory == 256
    assert smartphone.color == "Серый"

@pytest.fixture
def lawngrass():
    return LawnGrass(
        "Газонная трава",
        "Элитная трава для газона",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый"
    )


def test_create_lawngrass(lawngrass):
    assert lawngrass.name == "Газонная трава"
    assert lawngrass.description == "Элитная трава для газона"
    assert lawngrass.price == 500.0
    assert lawngrass.quantity == 20
    assert lawngrass.country == "Россия"
    assert lawngrass.germination_period == "7 дней"
    assert lawngrass.color == "Зеленый"

# Тесты для базового класса Product
class TestProduct:
    def test_initialization(self, product_samsung):
        assert product_samsung.name == "Samsung Galaxy S23 Ultra"
        assert product_samsung.description == "256GB, Серый цвет, 200MP камера"
        assert product_samsung.price == 180000.0
        assert product_samsung.quantity == 5

    def test_price_setter_valid(self, product_samsung):
        product_samsung.price = 190000.0
        assert product_samsung.price == 190000.0

    def test_price_setter_invalid(self, product_samsung, capsys):
        original_price = product_samsung.price
        product_samsung.price = -100
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product_samsung.price == original_price

    def test_product_info(self, product_samsung):
        assert product_samsung.product_info == "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."

    def test_str_representation(self, product_samsung):
        assert str(product_samsung) == "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."

    def test_addition(self, product_samsung, product_iphone):
        total = product_samsung + product_iphone
        assert total == 180000.0*5 + 210000.0*8

    def test_invalid_addition(self, product_samsung, smartphone):
        with pytest.raises(TypeError, match="Нельзя складывать товары разных классов"):
            product_samsung + smartphone

# Тесты для класса Category
class TestCategory:
    def test_initialization(self, smartphone_category):
        assert smartphone_category.name == "Смартфоны"
        assert len(smartphone_category.products) == 2

    def test_counters(self, smartphone_category, tv_category):
        assert Category.category_count == 2
        assert Category.product_count == 3

    def test_add_product(self, smartphone_category, product_xiaomi):
        initial_count = len(smartphone_category.products)
        smartphone_category.add_product(product_xiaomi)
        assert len(smartphone_category.products) == initial_count + 1
        assert Category.product_count == 4

    def test_products_info(self, smartphone_category):
        info = smartphone_category.products_info
        assert "Samsung Galaxy S23 Ultra" in info
        assert "iPhone 15" in info

    def test_total_quantity(self, smartphone_category):
        assert smartphone_category.total_quantity == 13  # 5 + 8

    def test_products_copy(self, smartphone_category):
        products_copy = smartphone_category.products
        products_copy.append("invalid")
        assert "invalid" not in smartphone_category.products

# Тесты для класса Smartphone
class TestSmartphone:
    def test_initialization(self, smartphone):
        assert smartphone.name == "Samsung Galaxy S23 Ultra"
        assert smartphone.efficiency == 95.5
        assert smartphone.model == "S23 Ultra"
        assert smartphone.memory == 256
        assert smartphone.color == "Серый"

    def test_inheritance(self, smartphone):
        assert isinstance(smartphone, Product)
        assert smartphone.price == 180000.0
        assert smartphone.quantity == 5

    def test_addition(self, smartphone):
        other = Smartphone("iPhone", "Pro", 200000, 3, "A15", "15", 512, "Black")
        total = smartphone + other
        assert total == 180000.0*5 + 200000*3

# Тесты для класса LawnGrass
class TestLawnGrass:
    def test_initialization(self, lawngrass):
        assert lawngrass.name == "Газонная трава"
        assert lawngrass.country == "Россия"
        assert lawngrass.germination_period == "7 дней"
        assert lawngrass.color == "Зеленый"

    def test_inheritance(self, lawngrass):
        assert isinstance(lawngrass, Product)
        assert lawngrass.price == 500.0
        assert lawngrass.quantity == 20

    def test_addition(self, lawngrass):
        other = LawnGrass("Трава", "Обычная", 300, 30, "Беларусь", "10 дней", "Зеленый")
        total = lawngrass + other
        assert total == 500.0*20 + 300*30