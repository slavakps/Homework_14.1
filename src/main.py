from abc import ABC, abstractmethod

class ProductMixinLog:
    def __init__(self, *args, **kwargs):
        print(f"Создан объект: {repr(self)}")

    def __repr__(self):
        name = getattr(self, 'name', 'неизвестно')
        description = getattr(self, 'description', 'нет описания')
        price = getattr(self, 'price', 0)
        quantity = getattr(self, 'quantity', 0)
        return f"{self.__class__.__name__}({name}, {description}, {price}, {quantity})"

class BaseProduct(ABC):

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.quantity = quantity
        self.price = price
        self.description = description
        self.name = name

class Product(BaseProduct, ProductMixinLog):
    def __init__(self, name, description, price, quantity):
        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        super().__init__(name=name, description=description, price=price, quantity=quantity)

    @property
    def price(self) -> float:
        """Геттер для цены"""
        return self.__price

    @price.setter
    def price(self, new_price: float):
        """Сеттер для цены с проверкой"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data) -> "Product":
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    @property
    def product_info(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError("Нельзя складывать товары разных классов")
        return self.price * self.quantity + other.price * other.quantity


class Category:
    name: str
    description: str
    __products: list[Product]
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = products
        type(self).category_count += 1
        type(self).product_count += len(products)

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        return self.__products.copy()

    @property
    def total_quantity(self) -> int:
        return sum(product.quantity for product in self.__products)

    def middle_price(self):
        """Метод для расчета средней цены товаров в категории"""
        try:
            total_price = sum(product.price for product in self.__products)
            return total_price / len(self.__products)
        except ZeroDivisionError:
            print("В категории нет товаров")
            return 0
        except Exception as e:
            print(f"Ошибка при вычислении средней цены: {e}")
            return 0

    @property
    def products_info(self) -> str:
        return "\n".join(str(product) for product in self.__products)

    def __str__(self):
        return f"{self.name}, количество продуктов: {self.total_quantity} шт."


class Smartphone(Product):
    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


if __name__ == '__main__':
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством")
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])

    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())
