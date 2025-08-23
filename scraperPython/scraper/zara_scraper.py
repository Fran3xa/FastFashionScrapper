import requests
import time
from domain.product import Product 

class ZaraApiScraper:
    BASE_URL = "https://www.zara.com/itxrest/1/search/store/10701/query"
    MARCA = "Zara"

    def __init__(self, query: str, section: str, language: str , country_code: str ):
        self.language = language
        self.query = query
        self.section = section.upper()
        self.locale = f"{language}_{country_code}"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        })

    def scrape(self):
        processed_products = {}
        
        params = {
            'query': self.query,
            'locale': self.locale,
            'section': self.section,
            'filter': f'searchSection:{self.section}',
            'deviceType': 'mobile',
            'deviceOS': 'Windows',
            'deviceOSVersion': '10',
            'catalogue': '25551',
            'warehouse': '18563',
            'scope': 'mobileweb',
            'origin': 'default',
            'ajax': 'true',
            'offset': 0,
            'limit': 100,
        }

        while True:
            print(f"🔍 Pidiendo productos... Query: '{params['query']}', Offset: {params['offset']}")
            try:
                response = self.session.get(self.BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()
            except requests.RequestException as e:
                print(f"❌ Error en la petición a la API: {e}")
                break

            results_data = data.get("results", [])
            if not results_data:
                print("✅ No hay más productos en la respuesta. Fin.")
                break

            for result in results_data:
                product_content = result.get("content")
                if product_content:
                    products_from_item = self._parse_item_content(product_content)
                    
                    for new_product in products_from_item:
                        if not new_product or not new_product.productId:
                            continue

                        product_id_str = str(new_product.productId)

                        if product_id_str in processed_products:
                            existing_product = processed_products[product_id_str]
                            self._merge_products(existing_product, new_product)
                        else:
                            processed_products[product_id_str] = new_product

            next_cursor = data.get("cursor")
            if next_cursor:
                params['offset'] += params['limit']
                params['cursor'] = next_cursor
                time.sleep(0.5)
            else:
                print("✅ Fin de la paginación.")
                break
        
        print(f"[✓] Se han procesado {len(processed_products)} productos únicos para '{self.query}'.")
        return list(processed_products.values())

    def _merge_products(self, existing_product: Product, new_product: Product):
        """
        Fusiona la información del nuevo producto en el existente.
        Da prioridad a la información más completa.
        """
        if (hasattr(existing_product, 'imageUrl') and existing_product.imageUrl == "NO_IMAGE" and 
            hasattr(new_product, 'imageUrl') and new_product.imageUrl != "NO_IMAGE"):
            print(f"🔄 Actualizando imagen para el producto {existing_product.productId}")
            existing_product.imageUrl = new_product.imageUrl
        
        if (hasattr(existing_product, 'categoria') and existing_product.categoria == "Sin categoría" and
            hasattr(new_product, 'categoria') and new_product.categoria != "Sin categoría"):
             print(f"🔄 Actualizando categoría para el producto {existing_product.productId}")
             existing_product.categoria = new_product.categoria

    def _parse_item_content(self, item_content: dict):
        """
        Función central que determina si un item es un bundle o un producto estándar
        y delega el parseo a la función correspondiente.
        """
        if "bundleProducts" in item_content and item_content["bundleProducts"]:
            return self._parse_bundle_product(item_content)
        else:
            return self._parse_standard_product(item_content)

    def _parse_bundle_product(self, item_content: dict):
        """
        Parsea un producto de tipo "bundle", creando un producto principal
        y productos individuales para cada uno de sus componentes.
        """
        all_related_products = []
        component_ids = []
        
        main_seo = item_content.get("seo", {})
        main_product_id = item_content.get("id", 0) 

        for component in item_content.get("bundleProducts", []):
            comp_id_str = str(component.get("id"))
            component_ids.append(comp_id_str)
            
            price = component.get("price", 0) / 100
            old_price = component.get("oldPrice", 0) / 100

            if old_price > 0 and old_price > price:
                precio_original = f"{old_price:.2f} EUR"
                precio_desc = f"{price:.2f} EUR"
                descuento_pct = f"{int(round((old_price - price) / old_price * 100))}%"
            else:
                precio_original = f"{price:.2f} EUR"
                precio_desc = "NODISC"
                descuento_pct = "NODISC"

            keyword = main_seo.get("keyword", "product")
            seo_product_id = main_seo.get("seoProductId")
            ref_url = f"https://www.zara.com/es/es/{keyword}-p{seo_product_id}.html?v1={comp_id_str}"
            
            image_url = "NO_IMAGE"
            colors = item_content.get("detail", {}).get("colors", [])

            color_value = colors[0] if colors else None
            if isinstance(color_value, dict):
                color_value = color_value.get("name", str(color_value))
            elif color_value is not None:
                color_value = str(color_value)

            component_product = Product(
                productId=comp_id_str,
                ref=ref_url,
                genero=self.section,
                nombre=component.get("name", "Componente sin nombre"),
                precioNodisc=precio_original,
                precioDisc=precio_desc,
                discount=descuento_pct,
                imageUrl=image_url,
                marca=self.MARCA,
                color=color_value,
                language=self.language
            )
            all_related_products.append(component_product)

        # 2. Crear el producto "padre" que representa el bundle completo
        category= 'bundle' if component.get("type") == 'bundle' else component.get("familyName")

        if main_product_id and component_ids:
            main_name = item_content.get("name", "Bundle sin nombre")
            main_image = self._construct_image_url(item_content.get("detail", {}).get("colors", [{}])[0].get("xmedia", [{}])[0])
            main_ref_url = f"https://www.zara.com/es/es/{main_seo.get('keyword', 'product')}-p{main_seo.get('seoProductId')}.html?v1={main_product_id}"
            colors = item_content.get("detail", {}).get("colors", [])

            color_value = colors[0] if colors else None
            if isinstance(color_value, dict):
                color_value = color_value.get("name", str(color_value))
            elif color_value is not None:
                color_value = str(color_value)

            bundle_product = Product(
                productId=str(main_product_id),
                ref=main_ref_url,
                genero=self.section,
                nombre=f"[CONJUNTO] {main_name}", 
                precioNodisc="NODISC", 
                precioDisc="NODISC",
                discount="NODISC",
                imageUrl=main_image,
                categoria=category,
                marca=self.MARCA,
                component_ids=component_ids,
                color=color_value,
                language=self.language

            )
            all_related_products.insert(0, bundle_product)
        
        print(f"📦 Detectado bundle '{item_content.get('name')}' con {len(component_ids)} componentes.")
        return all_related_products

    def _parse_standard_product(self, item_content: dict):
        """
        Parsea un único item estándar de la API y genera un producto por cada variante de color.
        (Lógica original movida a esta función)
        """
        products = []
        main_name = item_content.get("name", "Sin nombre")
        main_price = item_content.get("price", 0)
        main_old_price = item_content.get("oldPrice", 0)
        seo_data = item_content.get("seo", {})

        colors = item_content.get("detail", {}).get("colors", [])
        if not colors:
            colors = [{'productId': item_content.get('id'), 'name': '', 'price': main_price, 'oldPrice': main_old_price, 'xmedia': []}]
        
        for color_data in colors:
            try:
                product_id = str(color_data.get("productId"))
                if not product_id or product_id == 'None': continue 

                color_name = color_data.get("name", "")
                full_name = f"{main_name} - {color_name}" if color_name else main_name
                
                price = color_data.get("price", main_price) / 100
                old_price = color_data.get("oldPrice", main_old_price) / 100

                if old_price > 0 and old_price > price:
                    precio_original = f"{old_price:.2f} EUR"
                    precio_desc = f"{price:.2f} EUR"
                    descuento_pct = f"{int(round((old_price - price) / old_price * 100))}%"
                else:
                    precio_original = f"{price:.2f} EUR"
                    precio_desc = "NODISC"
                    descuento_pct = "NODISC"
                
                category= item_content.get("familyName") if item_content.get("type") == 'Product' else item_content.get("familyName")

                image_url = "NO_IMAGE"
                if color_data.get("xmedia"):
                    image_url = self._construct_image_url(color_data["xmedia"][0])

                keyword = seo_data.get("keyword", "product")
                seo_product_id = seo_data.get("seoProductId")
                ref_url = f"https://www.zara.com/es/es/{keyword}-p{seo_product_id}.html?v1={product_id}"

                products.append(Product(
                    product_id,
                    ref_url,
                    self.section,
                    full_name,
                    precio_original,
                    precio_desc,
                    descuento_pct,
                    image_url,
                    self.MARCA,
                    self.language,
                    color_name,
                    category
                ))
            except (KeyError, TypeError) as e:
                print(f"❌ Error al parsear variante de color: {e} - Data: {color_data}")
                continue
        return products
    
    def _construct_image_url(self, xmedia_item: dict):
        """
        Construye la URL de la imagen a partir del objeto xmedia.
        Ahora usa la URL directa que provee la API, que es más fiable.
        """
        if not xmedia_item or "url" not in xmedia_item:
            return "NO_IMAGE"
        
        return xmedia_item["url"].replace("{width}", "563")