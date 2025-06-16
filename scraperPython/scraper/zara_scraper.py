import random
import re
import time
from scraper.zara_image_scraper import ZaraScraperImage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from domain.product import Product
from bs4 import BeautifulSoup


class ZaraScraper:
    def __init__(self, url, headless=True):
        self.url = url
        self.options = Options()
        self.options.add_argument("--disable-blink-features=AutomationControlled")  # Evita detección como bot
        self.options.add_argument("--enable-unsafe-swiftshader") # Permite renderizado SwiftShader 
        self.options.add_argument("--incognito")  # Modo incógnito
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
        if headless:
            self.options.add_argument("--headless=new")  # Nueva implementación de headless en Chrome
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--window-size=1920x1080")
        self.options.add_argument("--no-sandbox")  # Requerido para algunos entornos

        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        except Exception as e:
            print("Error al iniciar ChromeDriver:", e)

    def scrape(self,total_productos):
        productos = self.fetch_and_parse(total_productos)
        if productos is None:
            return None
        for producto in productos:
            if producto.precioNodisc =="Sin precio":
                productos.remove(producto)  
        return productos
    
    def fetch_and_parse(self,total_productos):
        try:
            self.driver.get(self.url)
            time.sleep(5)
            seen_ids = {product.productId for product in total_productos}
            objetos = []

            self.scroll_to_bottom_with_lazy_loading()
            items = self.extraer_objetos()
            objetosRonda = self.procesar_items(items, seen_ids)
            zaraScraperImage=ZaraScraperImage()
            objetosRonda=zaraScraperImage.batch_get_colors_image(objetosRonda)
            objetos += objetosRonda
            print(f"[✓] Se han encontrado {len(objetos)} productos nuevos.")
            return objetos
        except Exception as e:
            print("Error al cargar la página:", e)
            return None

        
    def extraer_objetos(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return soup.find_all("li", attrs={"data-productid": True})
    
    def procesar_items(self, items, seen_ids):
        resultados = []

        for item in items:
            id = item["data-productid"]
            if id in seen_ids:
                continue
            seen_ids.add(id)
            resultados.append(self.extraer_info(item))
            print(id)

        return resultados

    
    def extraer_imagen(self, item):
        tag = item.find("img")
        url = tag["src"] if tag else None
        return None if not url or "static.zara.net/stdstatic" in url else url

    def extraer_info(self, item):
        info = item.find("div", "product-grid-product-info__main-info")
        ref = info.find("a")["href"] if info and info.find("a") else None
        nombre = info.text if info else "Sin nombre"
        precio = item.find("div", "product-grid-product-info__product-price price")
        precio_text = precio.text if precio else "Sin precio"
        predisc = self.get_discount(precio_text)
        product = Product(
            item["data-productid"],
            ref,
            nombre,
            predisc[0],
            predisc[1],
            predisc[2],
            "img_url"
        )
        return product
    

    def scroll_to_bottom_with_lazy_loading(self, wait_time=2, max_retries=5):
        retries = 0
        last_height = self.scroll_height()

        while retries < max_retries:
            # Scroll directo al final
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(wait_time)  # Esperar que cargue lazy loading

            new_height = self.scroll_height()
            if new_height == last_height:
                retries += 1
                print(f"Scroll detenido, intento {retries}/{max_retries}")
            else:
                retries = 0
                last_height = new_height

    def scroll_height(self):
        return self.driver.execute_script("return document.body.scrollHeight")

    
    def get_discount(self, precio_texto: str):

        texto = precio_texto.replace(",", ".")
        
        precios = re.findall(r"(\d+\.\d+\s*EUR)", texto)
        if len(precios) != 2:
            return precio_texto, "NODISC", "NODISC"
        
        precio_original, precio_desc = precios
        
        try:
            orig = float(precio_original.split()[0])
            desc = float(precio_desc.split()[0])
            porcentaje = f"{int(round((orig - desc) / orig * 100))}%"
        except Exception:
            porcentaje = "NODISC"
        
        return precio_original, precio_desc, porcentaje
    
        