from models.customer import Customer, Wallet, BonusCard
from controllers.shop_controller import ShopController
from views.interface import ShopInterface

if __name__ == "__main__":
    # Инициализация покупателя
    wallet = Wallet(cash=1500, debit=1000)
    bonus_card = BonusCard(bonus=300)
    customer = Customer(wallet=wallet, bonus_card=bonus_card)

    # Контроллер магазина
    controller = ShopController(customer, product_file="data/products.json")

    # Запуск GUI
    app = ShopInterface(controller)
    app.mainloop()
