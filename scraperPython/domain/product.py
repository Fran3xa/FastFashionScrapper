class Product:
    def __init__(self, productId, ref, genero, nombre, precioNodisc, precioDisc, discount, imageUrl, marca, language, color=None, categoria=None, component_ids=None):
        """
        Inicializa un producto.
        Args:
            component_ids (list, optional): Lista de IDs de los productos que componen un bundle. Defaults to None.
        """
        self.productId = productId
        self.ref = ref
        self.genero = genero
        self.nombre = nombre
        self.precioNodisc = precioNodisc
        self.precioDisc = precioDisc
        self.discount = discount
        self.imageUrl = imageUrl
        self.component_ids = component_ids if component_ids is not None else []
        self.marca=marca
        self.categoria = categoria
        self.color = color
        self.language = language

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
    
        product = cls(
            productId=data['productId'],
            ref=data['ref'],
            genero=data['genero'],
            nombre=data['nombre'],
            precioNodisc=data['precioNodisc'],
            precioDisc=data['precioDisc'],
            discount=data['discount'],
            imageUrl=data['imageUrl'],
            marca=data['marca'],
            component_ids=data.get('component_ids'), 
            categoria=data['categoria'],
            color=data['color'],
            language=data['language']
        )
        return product