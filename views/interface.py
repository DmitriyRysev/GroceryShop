import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from views.dialogs import WeightInputDialog


class ShopInterface(ctk.CTk):
    def __init__(self, controller):
        """Инициализирует интерфейс магазина: создаёт виджеты, сетку, стили и загружает данные."""
        super().__init__()

        self.controller = controller
        self.title("Магазин")
        self.geometry("800x660+400+20")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        ctk.set_widget_scaling(1.1)  # ← уменьшает все виджеты

        # Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ————————————————————————————— Баланс —————————————————————————————
        self.balance_frame = ctk.CTkFrame(self, fg_color="gray13")
        self.balance_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.balance_frame.grid_columnconfigure((0, 1, 2), weight=1)  # растягивает три колонки

        self.cash_label = ctk.CTkLabel(self.balance_frame, text="", anchor="w",
                                       font=ctk.CTkFont(family="Courier New", size=14))
        self.cash_label.grid(row=0, column=0, sticky="w", padx=10)

        self.card_label = ctk.CTkLabel(self.balance_frame, text="", anchor="center",
                                       font=ctk.CTkFont(family="Courier New", size=14))
        self.card_label.grid(row=0, column=1, sticky="n", padx=10)

        self.bonus_label = ctk.CTkLabel(self.balance_frame, text="", anchor="e",
                                        font=ctk.CTkFont(family="Courier New", size=14))
        self.bonus_label.grid(row=0, column=2, sticky="e", padx=10)

        # ————————————————————————————— Левый сайдбар (продукты) —————————————————————————————
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.grid(row=1, column=0, sticky="nsw", padx=10, pady=10)
        self.product_list = ctk.CTkScrollableFrame(self.sidebar, width=200, height=310)
        self.product_list.pack(pady=10, padx=10)

        self.clear_cart_button = ctk.CTkButton(self.sidebar, font=ctk.CTkFont(family="Courier New", size=14), height=30,
                                               width=207, text="Очистить корзину",
                                               command=self.clear_cart)
        self.clear_cart_button.pack(pady=5)
        self.remove_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=[],  # значения будут обновляться в refresh_cart()
            width=200,
            font=ctk.CTkFont(family="Courier New", size=14)
        )
        self.remove_menu.set("Продукт для удаления")  # <-- плейсхолдер
        self.remove_menu.pack(pady=(0, 3), padx=10)

        self.remove_selected_btn = ctk.CTkButton(
            self.sidebar,
            height=30,
            width=207,
            text="Удалить выбранное",
            fg_color="#bb3d3d",  # цвет фона кнопки
            hover_color="#943131",  # цвет при наведении
            text_color="white",
            command=self.remove_selected_dropdown,
            font=ctk.CTkFont(family="Courier New", size=14)
        )
        self.remove_selected_btn.pack(pady=(2, 10))

        # ————————————————————————————— Правый фрейм (корзина) —————————————————————————————
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Даем в main_frame свободно растягиваться
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)  # строка 1 — под label

        # Заголовок
        self.cart_label = ctk.CTkLabel(
            self.main_frame,
            text="Корзина",
            font=ctk.CTkFont(family="Courier New", size=24)
        )
        self.cart_label.grid(row=0, column=0, sticky="n", pady=(10, 5))

        # Текстовое поле корзины
        self.cart_list = ctk.CTkTextbox(
            self.main_frame,
            font=ctk.CTkFont(family="Courier New", size=14)
        )
        self.cart_list.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.cart_list.configure(state="disabled")

        # ————————————————————————————— Способы оплаты —————————————————————————————
        self.pay_frame = ctk.CTkFrame(self)
        self.pay_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        # чекбоксы
        self.use_card_var = ctk.BooleanVar(value=True)
        self.use_cash_var = ctk.BooleanVar(value=True)
        self.use_bonus_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.pay_frame, text="Наличные", variable=self.use_cash_var,
                        font=(ctk.CTkFont(family="Courier New", size=14))).pack(side="left", padx=10)
        ctk.CTkCheckBox(self.pay_frame, text="Карта", variable=self.use_card_var,
                        font=(ctk.CTkFont(family="Courier New", size=14))).pack(side="left", padx=10)
        ctk.CTkCheckBox(self.pay_frame, text="Бонусы", variable=self.use_bonus_var,
                        font=(ctk.CTkFont(family="Courier New", size=14))).pack(side="left", padx=10)

        self.total_label = ctk.CTkLabel(self.pay_frame, text="Итого: 0.00₽",
                                        font=ctk.CTkFont(family="Courier New", size=14))
        self.total_label.pack(side="left", padx=10)
        self.checkout_button = ctk.CTkButton(self.pay_frame,
                                             height=35,
                                             width=170,
                                             text="Оформить покупку",
                                             font=(ctk.CTkFont(family="Courier New", size=14)),
                                             fg_color="#3b8c3a",  # цвет фона кнопки
                                             hover_color="#2d5e2c",  # цвет при наведении
                                             text_color="white",  # цвет текста
                                             command=self.checkout)
        self.checkout_button.pack(side="right", padx=10, pady=10)

        # Инициализировать
        self.refresh_products()
        self.refresh_cart()
        self.update_balance_labels()

    def refresh_products(self):
        """Обновляет список продуктов в интерфейсе: удаляет старые кнопки и создает новые."""
        for w in self.product_list.winfo_children():
            w.destroy()
        for idx, prod in enumerate(self.controller.list_products()):
            text = f"{prod.name} — {prod.price}₽ {'(вес)' if prod.needs_weighing else ''}"
            btn = ctk.CTkButton(
                self.product_list,
                width=190, height=30,
                text=text,
                font=ctk.CTkFont(family="Courier New", size=14),
                fg_color="#6d9e6d",  # цвет фона кнопки
                hover_color="#486848",  # цвет при наведении
                text_color="white",  # цвет текста
                command=lambda i=idx: self.select_product(i)
            )
            btn.pack(pady=2)

    def refresh_cart(self):
        """Обновляет отображение корзины и итоговой суммы. Также обновляет меню удаления."""
        self.cart_list.configure(state="normal")
        self.cart_list.delete("1.0", "end")
        total = 0

        for product, count, display in self.controller.cart.list_items():
            line_price = product.total_price() * count
            self.cart_list.insert("end", f"{display} x{count}: {line_price:.2f}₽\n")
            total += line_price

        self.cart_list.insert("end", "\n")
        self.cart_list.configure(state="disabled")
        self.total_label.configure(text=f"Итого: {total:.2f}₽")

        # Обновление OptionMenu
        current = self.remove_menu.get()
        new_values = [display for _, _, display in self.controller.cart.list_items()]
        self.remove_menu.configure(values=new_values)

        # Если пользователь ещё ничего не выбирал (т.е. установлен плейсхолдер)
        if current == "Продукт для удаления" or current not in new_values:
            self.remove_menu.set("Продукт для удаления")
        else:
            self.remove_menu.set(current)

    def remove_selected_dropdown(self):
        """Удаляет выбранный из выпадающего списка продукт из корзины."""
        display = self.remove_menu.get()
        if not display:
            return
        # ключ в корзине хранится либо как name, либо as name_weight
        # найдём ключ по совпадению display
        for key, (product, count) in list(self.controller.cart.items.items()):
            d = f"{product.name} ({product.weight}кг)" if product.needs_weighing else product.name
            if d == display:
                self.controller.cart.remove_item(key)
                break
        self.refresh_cart()
        self.update_balance_labels()

    def update_balance_labels(self):
        """Обновляет отображение баланса: наличные, карта, бонусы."""
        w = self.controller.customer.wallet
        b = self.controller.customer.bonus_card
        self.cash_label.configure(text=f"Наличные: {w.cash:.2f} ₽")
        self.card_label.configure(text=f"Карта:   {w.debit:.2f} ₽")
        self.bonus_label.configure(text=f"Бонусы: {b.bonus:} бонусов")

    def select_product(self, idx):
        """Обрабатывает добавление выбранного продукта в корзину.
           Если товар взвешиваемый — запрашивает вес.
           Проверяет наличие на складе и добавляет в корзину."""
        orig = self.controller.list_products()[idx]  # оригинальный товар из self.products

        try:
            if orig.needs_weighing:
                dialog = WeightInputDialog(self, orig.name)
                weight = dialog.weight
                if weight is None:
                    return
                qty = weight
            else:
                qty = 1

            # проверяем остаток в оригинале
            if qty > orig.stock:
                raise ValueError(f"Недостаточно {orig.name}: осталось {orig.stock}")

            # уменьшаем оригинальный запас
            orig.stock -= qty

            # теперь создаём клон для корзины и задаём вес
            prod = orig.clone()
            if orig.needs_weighing:
                prod.weigh(qty)

            self.controller.cart.add_item(prod)

        except ValueError as e:
            CTkMessagebox(title="Ошибка", message=str(e), icon="cancel")
            return

        # обновляем после успешного добавления
        self.refresh_cart()
        self.refresh_products()

    def clear_cart(self):
        """Очищает корзину, обновляет отображение и обнуляет сумму."""
        # очистить корзину у контроллера
        self.controller.cart.clear()
        # обновить отображение корзины
        self.refresh_cart()
        # можно обновить итоговую сумму и баланс, если нужно
        self.update_balance_labels()
        self.total_label.configure(text="Итого: 0.00₽")

    def checkout(self):
        """Проверяет выбранные способы оплаты и наличие товаров в корзине.
           Пытается оформить покупку через контроллер.
           Показывает результат и обновляет интерфейс."""
        use_cash = self.use_cash_var.get()
        use_card = self.use_card_var.get()
        use_bonus = self.use_bonus_var.get()

        # ❗️ Проверка: выбран ли хотя бы один способ оплаты
        if not (use_cash or use_card or use_bonus):
            CTkMessagebox(title="Ошибка", message="Выберите хотя бы один способ оплаты!", icon="cancel")
            return

        # ❗️ Проверка: есть ли товары в корзине
        if not self.controller.cart.items:
            CTkMessagebox(title="Корзина пуста", message="Добавьте товары перед оформлением покупки.", icon="warning")
            return

        # ✅ Если всё в порядке — пробуем оплату
        success, message = self.controller.checkout(
            use_cash=use_cash,
            use_card=use_card,
            use_bonus=use_bonus
        )

        # Показываем результат
        if success:
            CTkMessagebox(title="Успешно", message=message, icon="check")
        else:
            CTkMessagebox(title="Ошибка", message=message, icon="cancel")

        # Обновляем интерфейс
        self.update_balance_labels()
        self.refresh_cart()
