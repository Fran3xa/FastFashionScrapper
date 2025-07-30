from flask import Flask, jsonify, Response
from concurrent.futures import ThreadPoolExecutor
import threading
from scraper.zara_scraper import ZaraApiScraper

app = Flask(__name__)

SEARCH_CONFIG = {
    "kid": [
        # Niña
        "ropa niña", "vestidos niña", "camisetas niña", "pantalones niña", "faldas niña", 
        "leggings niña", "monos niña", "abrigos niña", "chaquetas niña", "sudaderas niña",
        # Niño
        "ropa niño", "camisas niño", "camisetas niño", "pantalones niño", "bermudas niño", 
        "sudaderas niño", "abrigos niño", "chaquetas niño", "jeans niño",
        # Bebé (unisex, niño y niña)
        "ropa bebé", "conjuntos bebé", "bodys bebé", "pijamas bebé", "petos bebé", 
        "abrigos bebé", "chaquetas bebé",
        # Calzado y Accesorios generales
        "calzado infantil", "zapatos niña", "zapatos niño", "zapatillas niño", "zapatillas niña", 
        "botas niño", "botas niña", "sandalias niño", "sandalias niña", "patucos bebé",
        "accesorios infantil", "gorros niño", "gorros niña", "calcetines niño", "calcetines niña"
    ],
    "woman": [
        # Partes de arriba
        "mujer tops", "mujer camisetas", "mujer bodies", "mujer camisas", "mujer blusas", 
        "mujer jerséis", "mujer cárdigans", "mujer sudaderas", "mujer chalecos",
        # Prendas de abrigo
        "mujer abrigos", "mujer gabardinas", "mujer parkas", "mujer chaquetas", "mujer cazadoras", 
        "mujer blazers",
        # Partes de abajo
        "mujer pantalones", "mujer jeans", "mujer vaqueros", "mujer faldas", "mujer pantalones cortos", 
        "mujer shorts", "mujer leggings",
        # Prendas completas
        "mujer vestidos", "mujer monos",
        # Lencería y Pijamas
        "mujer lencería", "mujer sujetadores", "mujer braguitas", "mujer pijamas", "mujer batas","mujer ropa interior",
        # Ropa de baño
        "mujer bikinis", "mujer bañadores",
        # Calzado
        "mujer zapatos de tacón", "mujer zapatos planos", "mujer sandalias", "mujer zapatillas", 
        "mujer deportivas", "mujer botas", "mujer botines", "mujer mocasines",
        # Accesorios
        "mujer accesorios", "mujer bolsos", "mujer mochilas", "mujer cinturones", "mujer carteras", 
        "mujer monederos", "mujer gorros", "mujer sombreros", "mujer bufandas", "mujer pañuelos", 
        "mujer fulares", "mujer gafas de sol", "mujer joyas", "mujer bisutería",
        # Especiales
        "mujer ropa deportiva"
    ],
    "man": [
        # Partes de arriba
        "hombre camisas", "hombre camisetas", "hombre polos", "hombre jerséis", "hombre cárdigans", 
        "hombre sudaderas", "hombre chalecos",
        # Prendas de abrigo
        "hombre abrigos", "hombre gabardinas", "hombre parkas", "hombre chaquetas", "hombre cazadoras", 
        "hombre bombers", "hombre blazers", "hombre americanas",
        # Partes de abajo
        "hombre pantalones", "hombre pantalones chinos", "hombre pantalones cargo", "hombre pantalones de vestir", 
        "hombre jeans", "hombre vaqueros", "hombre bermudas",
        # Prendas completas
        "hombre trajes", "hombre monos",
        # Ropa interior y de estar por casa
        "hombre ropa interior", "hombre boxers", "hombre calcetines", "hombre pijamas",
        # Ropa de baño
        "hombre bañadores",
        # Calzado
        "hombre zapatos", "hombre zapatillas", "hombre deportivas", "hombre botas", "hombre botines", 
        "hombre mocasines", "hombre náuticos", "hombre sandalias",
        # Accesorios
        "hombre accesorios", "hombre bolsos", "hombre mochilas", "hombre riñoneras", "hombre cinturones", 
        "hombre carteras", "hombre gorros", "hombre gorras", "hombre sombreros", "hombre bufandas", 
        "hombre pañuelos", "hombre gafas de sol", "hombre corbatas",
        # Especiales
        "hombre ropa deportiva"
    ]
}


def run_scrape_for_term(term: str, section: str, language: str, marca: str):
    """
    Función auxiliar simplificada. Ya no necesita gestionar IDs compartidos.
    """
    print(f"🚀 Iniciando scraping para: '{term}' en la sección '{section.upper()}' (Lang: {language})")
    try:
        if(marca == "zara"):
            scraper = ZaraApiScraper(query=term, section=section.upper(), language=language, country_code='ES')
            products = scraper.scrape()
        
        if products:
            print(f"✅ Finalizado: '{term}'. Encontrados {len(products)} productos.")
        else:
            print(f"⚪️ Finalizado: '{term}'. No se encontraron productos.")
        return products
    except Exception as e:
        print(f"❌ Error en el scraping de '{term}': {e}")
        return []

def _merge_product_lists(list_of_lists):
    """
    Función auxiliar para fusionar listas de productos de diferentes hilos,
    evitando duplicados y actualizando con la información más completa.
    """
    final_products = {}
    
    for product_list in list_of_lists:
        for product in product_list:
            product_id = str(product.productId)
            if product_id not in final_products:
                final_products[product_id] = product
            else:
                existing_product = final_products[product_id]
                if (hasattr(existing_product, 'imageUrl') and existing_product.imageUrl == "NO_IMAGE" and 
                    hasattr(product, 'imageUrl') and product.imageUrl != "NO_IMAGE"):
                    existing_product.imageUrl = product.imageUrl

    
    return list(final_products.values())


def scrape_section_task(section: str, language: str, marca: str):
    """
    La tarea de scraping completa. Ahora fusiona los resultados al final.
    """
    print(f"\n--- Iniciando tarea de scraping para la sección: {section.upper()} (Lang: {language}, Marca: {marca}) ---")
    search_terms = SEARCH_CONFIG.get(section, [])
    if not search_terms:
        print(f"Sección '{section}' no encontrada. Abortando.")
        return []
    all_results_from_threads = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(run_scrape_for_term, term, section, language, marca) for term in search_terms]
        for future in futures:
            all_results_from_threads.append(future.result())
    print("\n--- Fusionando resultados de todos los hilos... ---")
    total_productos = _merge_product_lists(all_results_from_threads)
    print(f"--- Tarea de scraping para '{section.upper()}' completada. Total de productos únicos encontrados: {len(total_productos)} ---")
    return total_productos

@app.route('/api/<marca>/products/scrape/<section>/<language>', methods=['POST'])
def trigger_scrape(marca: str, section: str, language: str):
    section = section.lower()
    language = language.lower()
    marca = marca.lower()
    
    if section not in SEARCH_CONFIG:
        return jsonify({"error": "Sección no válida. Usar 'kid', 'woman' o 'man'."}), 400

    print(f"\nRecibida petición para iniciar scraping: Sección='{section}', Idioma='{language}', Marca='{marca}'")
    productos = scrape_section_task(section, language, marca)
    # Convierte los objetos Product a diccionarios si es necesario
    productos_dict = [p.__dict__ if hasattr(p, '__dict__') else p for p in productos]
    return jsonify(productos_dict), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)