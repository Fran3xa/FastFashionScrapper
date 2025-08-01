# Guía de Ejecución y Endpoints de Scrapper de marcas FastFashion

Este documento proporciona las instrucciones necesarias para ejecutar el backend de Java y el scraper de Python, junto con una descripción de los endpoints disponibles.

## Ejecución de las Aplicaciones

### 1. Backend de Java (Spring Boot)

Para iniciar el servidor de backend, navega hasta el directorio raíz del proyecto Java y ejecuta el siguiente comando:

```bash
mvn spring-boot:run
```

### 2. Scraper de Python

Para ejecutar el script de scraping, asegúrate de estar en el directorio del proyecto de Python y lanza el siguiente comando:

```bash
py main.py
```

## Descripción del Proyecto

Actualmente, el proyecto consta de los siguientes componentes:

- **Scraper en Python**: Se ha implementado únicamente el scraper para la tienda Zara. Este componente es responsable de extraer la información de los productos.
- **Backend en Spring Boot**: Se ha desarrollado un backend de ejemplo para demostrar cómo se podrían recoger y gestionar los objetos (productos) obtenidos por el scraper.

## Endpoints de la API

A continuación se detallan los endpoints disponibles en cada servicio.

### Endpoints del Backend (Spring Boot)

#### Endpoints para Iniciar el Scraping (POST)

- `/scrape/zara/man/es`
- `/scrape/zara/woman/es`
- `/scrape/zara/kid/es`

#### Endpoints para Obtener Productos (GET)

- `/zara/man/es`
- `/zara/woman/es`
- `/zara/kid/es/all`

### Endpoint del Scraper (Python/Flask)

#### Endpoint genérico de scraping (POST)

```
/api/<marca>/products/scrape/<section>/<language>
```

**Parámetros de la URL**:

- `marca`: La marca de la tienda. Por ahora, solo está implementado `zara`.
- `section`: La sección a la que pertenecen los productos (`man`, `woman`, `kid`).
- `language`: El idioma/país de la tienda (`es`, `en`, `fr`, etc.).
