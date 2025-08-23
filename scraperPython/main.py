from flask import Flask, jsonify,  Response
from scraper.zara_scraper import ZaraScraper
app = Flask(__name__)


@app.route('/api/products/scrape/kid', methods=['GET'])
def scrapeKid():
    total_productos = []
    search_terms = [
        "niño ropa", "niña ropa", "bebé ropa", "niño calzado", "niña calzado", "accesorios niño", "accesorios niña",
    ]

    search_urls = [f"https://www.zara.com/es/es/search?searchTerm={term.replace(' ', '%20')}&section=KID" for term in search_terms]
    for url in search_urls:
        scraper = ZaraScraper(url)
        productos = scraper.scrape(total_productos)
        if productos:
            total_productos.extend(productos)
    
    return jsonify([p.to_dict() for p in productos])


@app.route('/api/products/scrape/woman', methods=['GET'])
def scrapeWoman():
    total_productos = []
    search_terms = [
        "mujer gorras", "mujer abrigos", "mujer chaquetas", "mujer camisas", "mujer blusas", 
        "mujer jerséis", "mujer sudaderas", "mujer pantalones", "mujer jeans", "mujer faldas", 
        "mujer vestidos", "mujer monos", "mujer tops", "mujer ropa interior", "mujer pijamas", 
        "mujer bikinis", "mujer calzado", "mujer botas", "mujer deportivas", "mujer bolsos", 
        "mujer accesorios", "mujer joyas", "mujer maquillaje", "mujer perfumes", "mujer gafas", 
        "mujer ropa"
    ]

    search_urls = [f"https://www.zara.com/es/es/search?searchTerm={term.replace(' ', '%20')}&section=WOMAN" for term in search_terms]
    for url in search_urls:
        scraper = ZaraScraper(url)
        productos = scraper.scrape(total_productos)
        if productos:
            total_productos.extend(productos)
    
    return jsonify([p.to_dict() for p in productos])

@app.route('/api/products/scrape/man', methods=['GET'])
def scrapeMan():

    total_productos = []
    search_terms = [
        #"hombre gafas", "hombre camisas", "hombre camisetas", "hombre jerséis", 
        #"hombre sudaderas", "hombre chaquetas", "hombre abrigos", 
        "hombre jeans","hombre pantalones"
        #,"hombre trajes", "hombre ropa interior", "hombre pijamas", "hombre calzado", "hombre deportivas", 
        #"hombre botas", "hombre bolsos", "hombre accesorios", "hombre perfumes", "hombre gorros", 
        #"hombre ropa"
    ]

    search_urls = [f"https://www.zara.com/es/es/search?searchTerm={term.replace(' ', '%20')}&section=MAN" for term in search_terms]
    for url in search_urls:
        print("-------------")
        print("total_productos")
        print(f"{total_productos}")
        scraper = ZaraScraper(url)
        productos = scraper.scrape(total_productos)
        if productos:
            total_productos.extend(productos)
    
    return jsonify([p.to_dict() for p in total_productos])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)