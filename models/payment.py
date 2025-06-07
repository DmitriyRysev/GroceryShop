from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    """Абстрактная стратегия оплаты. Определяет интерфейс для всех видов оплаты."""

    @abstractmethod
    def pay(self, amount: float, customer) -> bool:
        """Выполняет оплату на заданную сумму от имени клиента."""
        pass


class CashPayment(PaymentStrategy):
    """Выполняет оплату на заданную сумму от имени клиента. Возвращает True при успешной оплате."""

    def pay(self, amount: float, customer) -> bool:
        """Списывает сумму с наличных, если достаточно средств."""
        if customer.wallet.cash >= amount:
            customer.wallet.cash -= amount
            return True
        return False


class DebitCardPayment(PaymentStrategy):
    """Оплата с дебетовой карты. Проверяет и списывает сумму с карты клиента."""

    def pay(self, amount: float, customer) -> bool:
        """Списывает сумму с карты, если достаточно средств."""
        if customer.wallet.debit >= amount:
            customer.wallet.debit -= amount
            return True
        return False


class BonusPayment(PaymentStrategy):
    """Оплата бонусами. Проверяет и списывает сумму с бонусной карты клиента."""

    def pay(self, amount: float, customer) -> bool:
        """Списывает сумму с бонусной карты, если достаточно бонусов."""
        if customer.bonus_card.bonus >= amount:
            customer.bonus_card.bonus -= amount
            return True
        return False
