class Product:
    __slots__ = ('brand', 'title', 'price', 'discount', 'link')

    def __init__(self, brand: str, title: str, price: str, discount: str, link: str):
        self.brand = brand
        self.title = title
        self.price = price
        self.discount = discount
        self.link = link

    def to_dict(self):
        return self.__dict__