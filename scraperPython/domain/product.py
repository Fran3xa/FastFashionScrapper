class Product:

    def __init__(self, productId, ref, nombre, precioNodisc, precioDisc, discount, imageUrl):  
        self.productId = productId
        self.ref = ref
        self.nombre = nombre
        self.precioNodisc = precioNodisc
        self.precioDisc = precioDisc
        self.discount = discount
        self.imageUrl = imageUrl
        self.categoria = None
        self.subcategoria = None
        self.color = None  # Añade el campo si vas a usarlo luego

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        # Extrae solo los argumentos del constructor
        product = cls(
            productId=data['productId'],
            ref=data['ref'],
            nombre=data['nombre'],
            precioNodisc=data['precioNodisc'],
            precioDisc=data['precioDisc'],
            discount=data['discount'],
            imageUrl=data['imageUrl']
        )
        # Asigna los atributos opcionales
        product.categoria = data.get('categoria')
        product.subcategoria = data.get('subcategoria')
        product.color = data.get('color')
        return product