import queue
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class ChromeDriverPool:
    _instance = None
    _lock = threading.Lock()

    @staticmethod
    def get_instance(size=8):
        if ChromeDriverPool._instance is None:
            with ChromeDriverPool._lock:
                if ChromeDriverPool._instance is None:
                    ChromeDriverPool(size)
        return ChromeDriverPool._instance

    def __init__(self, size=8,headless=True):
        if ChromeDriverPool._instance is not None:
            return

        self.pool = queue.Queue(maxsize=size)
        for _ in range(size):
            options = Options()
            options.add_argument("--disable-blink-features=AutomationControlled")  # Evita detección como bot
            options.add_argument("--enable-unsafe-swiftshader") # Permite renderizado SwiftShader 
            options.add_argument("--incognito")  # Modo incógnito
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
            if headless:
                options.add_argument("--headless=new")  # Nueva implementación de headless en Chrome
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920x1080")
            options.add_argument("--no-sandbox")  # Requerido para algunos entornos
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.pool.put(driver)


        ChromeDriverPool._instance = self

    def acquire(self):
        driver = self.pool.get()  # bloquea hasta que haya uno libre
        print(f"[POOL] Driver {id(driver)} adquirido")
        return driver

    def release(self, driver):
        print(f"[POOL] Driver {id(driver)} liberado")
        self.pool.put(driver)

    def close_all(self):
        while not self.pool.empty():
            driver = self.pool.get()
            driver.quit()