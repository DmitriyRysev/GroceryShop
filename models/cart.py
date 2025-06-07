class Cart:
    """Класс корзины: управляет добавлением, удалением и списком товаров для покупки."""
    def __init__(self, controller):
        """Инициализирует корзину, связывая её с контроллером магазина."""
        self.controller = controller
        self.items = {}

    def add_item(self, product):
        """Добавляет товар в корзину. Учитывает вес, если товар взвешиваемый."""
        key = f"{product.name}_{product.weight}" if product.needs_weighing else product.name
        if key in self.items:
            self.items[key][1] += 1
        else:
            self.items[key] = [product, 1]

    def find_original_product(self, product):
        """Ищет оригинальный товар по имени в списке товаров магазина."""
        for p in self.controller.list_products():
            if p.name == product.name:
                return p
        return None

    def remove_item(self, key):
        """Удаляет одну единицу товара из корзины. Возвращает соответствующее количество обратно на склад."""
        if key not in self.items:
            return

        product, count = self.items[key]
        qty = product.weight if product.needs_weighing else 1

        # Найдём оригинальный продукт (а не клон), чтобы восстановить остаток
        original = self.find_original_product(product)
        if original:
            original.stock += qty

        # уменьшаем в корзине
        self.items[key][1] -= 1
        if self.items[key][1] <= 0:
            del self.items[key]

    def list_items(self):
        """Возвращает список товаров в корзине с количеством и текстовым описанием."""
        result = []
        for key, (product, count) in self.items.items():
            display = f"{product.name} ({product.weight}кг)" if product.needs_weighing else product.name
            result.append((product, count, display))
        return result

    def get_total(self):
        """Подсчитывает итоговую стоимость всех товаров в корзине."""
        return sum(product.total_price() * count for product, count in self.items.values())

    def clear(self):
        """Очищает корзину и возвращает все товары обратно на склад."""
        # возвращаем остатки всех позиций в корзине
        for product, count in self.items.values():
            # находим оригинал (если есть), иначе — сам объект
            orig = getattr(product, "_orig", product)
            qty = product.weight if product.needs_weighing else 1
            orig.stock += qty * count

        # очищаем корзину
        self.items.clear()
