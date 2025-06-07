import json

# from models.product import Product, Service
from models.cart import Cart
from models.payment import CashPayment, DebitCardPayment, BonusPayment
from models.product import Product


class ShopController:
    """Контроллер магазина: управляет товарами, корзиной и оплатой."""

    def __init__(self, customer, product_file="data/products.json"):
        """Инициализирует контроллер с покупателем, корзиной и загрузкой товаров из файла."""
        self.customer = customer
        self.cart = Cart(self)
        self.products = self.load_products(product_file)

    def load_products(self, filename):
        """Загружает список товаров из JSON-файла и создает объекты Product."""
        products = []
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                if item["type"] == "product":
                    # Считываем остаток из JSON (если его нет — по умолчанию 0)
                    stock = item.get("stock", 0)
                    products.append(
                        Product(
                            item["name"],
                            item["price"],
                            item.get("needs_weighing", False),
                            stock  # ← передаём stock в конструктор
                        )
                    )
        return products

    def list_products(self):
        """Возвращает список всех доступных товаров."""
        return self.products  # список объектов Product / Service

    def add_product_to_cart(self, product_index, weight=None):
        """Добавляет товар в корзину по индексу, указывая вес при необходимости."""
        product = self.products[product_index]
        if product.needs_weighing:
            if weight is None:
                raise ValueError("Необходим вес для взвешиваемого товара.")
            product.weigh(weight)
        self.cart.add_item(product)

    def remove_product_from_cart(self, product_name):
        """Удаляет товар из корзины по его названию."""
        self.cart.remove_item(product_name)

    def get_cart_total(self):
        """Возвращает итоговую стоимость всех товаров в корзине."""
        return self.cart.get_total()

    def list_cart_items(self):
        """Возвращает список товаров в корзине."""
        return self.cart.list_items()

    def try_payment(self, amount, strategies):
        """Выполняет оплату заданной суммой с использованием последовательности стратегий."""
        remaining = amount
        for strategy in strategies:
            if remaining <= 0:
                break
            paid = strategy.pay(remaining, self.customer)
            if paid:
                remaining = 0
            else:
                # Попробовать оплатить частично
                available = self._get_available(strategy)
                strategy.pay(available, self.customer)
                remaining -= available
        return remaining <= 0

    def _get_available(self, strategy):
        """Определяет доступные средства покупателя по заданной стратегии оплаты."""
        if isinstance(strategy, CashPayment):
            return self.customer.wallet.cash
        elif isinstance(strategy, DebitCardPayment):
            return self.customer.wallet.debit
        elif isinstance(strategy, BonusPayment):
            return self.customer.bonus_card.bonus
        return 0

    def checkout(self, use_cash=False, use_card=False, use_bonus=False):
        """
        Выполняет финальную оплату корзины, используя выбранные способы оплаты.
        Возвращает кортеж: (успех оплаты, сообщение).
        """
        total = self.cart.get_total()
        remaining = total

        # Подсчёт доступных средств
        available = 0
        if use_card:
            available += self.customer.wallet.debit
        if use_cash:
            available += self.customer.wallet.cash
        if use_bonus:
            available += self.customer.bonus_card.bonus

        if available < total:
            return False, "Недостаточно средств"

        # Если денег хватает — теперь списываем по порядку
        if use_card and remaining > 0:
            strategy = DebitCardPayment()
            paid = min(remaining, self.customer.wallet.debit)
            strategy.pay(paid, self.customer)
            remaining -= paid

        if use_cash and remaining > 0:
            strategy = CashPayment()
            paid = min(remaining, self.customer.wallet.cash)
            strategy.pay(paid, self.customer)
            remaining -= paid

        if use_bonus and remaining > 0:
            strategy = BonusPayment()
            paid = min(remaining, self.customer.bonus_card.bonus)
            strategy.pay(paid, self.customer)
            remaining -= paid

        self.cart.clear()
        return True, f"Покупка на {total}₽ совершена успешно!"

    def _strategy_from_name(self, name):
        """Возвращает стратегию оплаты по её названию."""
        if name == "cash":
            return CashPayment()
        elif name == "debit":
            return DebitCardPayment()
        elif name == "bonus":
            return BonusPayment()
        else:
            raise ValueError("Неизвестный способ оплаты.")
