class Wallet:
    """Кошелёк покупателя: хранит информацию о наличных и средствах на карте."""

    def __init__(self, cash: float, debit: float):
        self.cash = cash
        self.debit = debit


class BonusCard:
    """Бонусная карта покупателя: хранит количество накопленных бонусов."""

    def __init__(self, bonus: float):
        self.bonus = bonus


class Customer:
    """Класс покупателя: объединяет кошелёк и бонусную карту."""

    def __init__(self, wallet: Wallet, bonus_card: BonusCard):
        self.wallet = wallet
        self.bonus_card = bonus_card
