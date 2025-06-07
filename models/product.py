class Product:
    """Класс представляет товар в магазине, включая цену, необходимость взвешивания и остаток на складе."""

    def __init__(self, name: str, price: float, needs_weighing: bool = False, stock: float = 0):
        """Инициализирует товар с названием, ценой, признаком взвешивания и остатком на складе."""
        self.name = name
        self.price = price
        self.needs_weighing = needs_weighing
        self.weight = None  # None означает, что не взвешен
        self.stock = stock  # остаток: кг для взвеш., шт. для штучных

    def weigh(self, weight: float):
        """Устанавливает вес для взвешиваемого товара. Если товар не требует взвешивания — вызывает ошибку."""
        if not self.needs_weighing:
            raise ValueError(f"Продукт {self.name} не требует взвешивания.")
        self.weight = weight

    def total_price(self):
        """Вычисляет итоговую стоимость товара с учётом веса (если требуется)."""
        if self.needs_weighing:
            if self.weight is None:
                raise ValueError(f"Продукт {self.name} должен быть взвешен.")
            return self.price * self.weight
        return self.price

    def clone(self):
        """Создаёт копию товара без остатка на складе, передаёт вес и сохраняет ссылку на оригинал."""
        copy = Product(self.name, self.price, self.needs_weighing, stock=0)
        copy.weight = self.weight
        # запоминаем, откуда клонировали
        copy._orig = self
        return copy
