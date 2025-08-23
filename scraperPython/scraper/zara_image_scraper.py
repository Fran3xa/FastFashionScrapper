from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Pool
import re
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from domain.product import Product
from util.chrome_pool import ChromeDriverPool
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_color(product_dict):
    pool = ChromeDriverPool.get_instance()
    driver = pool.acquire()
    try:
        ref = product_dict['ref']
        driver.get(f"{ref}?v1={product_dict['productId']}")
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='product-color-extended-name']")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        color_elements = soup.find_all("p", class_=re.compile(r".*product-color-extended-name.*"))
        if color_elements:
            color_text = color_elements[0].text.strip()
            color = color_text.split('|')[0].strip()
        else:
            color = "NO_COLOR"
        image_url=scrape_image(soup)

    except Exception as e:
        print(f"[✗] Error en {ref}: {e}")
        print(traceback.format_exc())
        color = "ERROR"
        image_url=scrape_image(soup)
    finally:
        pool.release(driver)

    product_dict['color'] = color
    product_dict['imageUrl'] = image_url
    return product_dict

def scrape_image(soup):
    image_elements = soup.find_all("img", class_=re.compile(r"^media-image__image"))
    if image_elements:
        return image_elements[0]['src']
    else:
        return "NO_IMAGE"



class ZaraScraperImage:
    def chunks(self,lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def batch_get_colors_image(self, products, batch_size=16, max_workers=8):
        updated_products = []
        print(f"[✓] Iniciando la actualización de colores e imágenes para {len(products)} productos.")
        for batch in self.chunks(products, batch_size):
            product_dicts = [p.to_dict() for p in batch]

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(scrape_color, pd) for pd in product_dicts]
                results = [f.result() for f in as_completed(futures)]

            updated_batch = [Product.from_dict(d) for d in results]
            updated_products.extend(updated_batch)
            print(f"[✓] Procesados {len(updated_batch)} productos en este lote.")

        print(f"[✓] Total de productos actualizados con colores: {len(updated_products)}")
        return updated_products

