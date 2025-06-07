import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


class WeightInputDialog(ctk.CTkToplevel):
    def __init__(self, parent, product_name):
        """Создаёт модальное окно для ввода веса товара."""
        super().__init__(parent)
        self.title("Вес товара")
        self.geometry("280x170+950+400")
        self.resizable(False, False)
        self.product_name = product_name
        self.weight = None  # сюда запишем результат

        label = ctk.CTkLabel(self, text=f"Введите вес для {product_name}, кг:")
        label.pack(pady=(20, 10), padx=20)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(padx=20)
        self.entry.focus()

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=15)

        ok_btn = ctk.CTkButton(btn_frame, text="ОК", width=110, command=self.on_ok)
        ok_btn.pack(side="left", padx=5, pady=5)
        cancel_btn = ctk.CTkButton(btn_frame, text="Отмена", width=110, command=self.on_cancel)
        cancel_btn.pack(side="right", padx=5, pady=5)

        # Чтобы окно было модальным
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def on_ok(self):
        """Обрабатывает нажатие кнопки 'ОК':
                проверяет корректность введённого веса и сохраняет результат."""
        val = self.entry.get()
        try:
            weight = float(val)
            if weight <= 0:
                CTkMessagebox(title="Ошибка", message="Вес должен быть больше 0 кг")
                return
            self.weight = weight
            self.destroy()
        except ValueError:
            CTkMessagebox(title="Ошибка", message="Введите корректное число")

    def on_cancel(self):
        """Обрабатывает нажатие кнопки 'Отмена':
                закрывает окно без сохранения веса."""
        self.weight = None
        self.destroy()
