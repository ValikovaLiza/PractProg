from playwright.sync_api import Page

class ProductsPage:
    def __init__(self, page: Page):
        self.page = page
        self.add_to_cart_button = '.inventory_item:first-of-type button'
        self.cart_badge = '.shopping_cart_badge'

    def add_first_product_to_cart(self):
        self.page.click(self.add_to_cart_button)

    def get_cart_count(self) -> str:
        return self.page.inner_text(self.cart_badge)