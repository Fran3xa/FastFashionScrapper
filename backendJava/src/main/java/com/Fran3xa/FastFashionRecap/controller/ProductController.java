package com.Fran3xa.FastFashionRecap.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.Fran3xa.FastFashionRecap.model.entitys.Product;
import com.Fran3xa.FastFashionRecap.service.ProductService;
import com.Fran3xa.FastFashionRecap.service.ScraperService;

import java.util.List;

@RestController
@RequestMapping("/api/products")
public class ProductController {

    @Autowired
    private ScraperService scraperService;

    @Autowired
	private ProductService productService;

    @PostMapping("/scrape/zara/man/es")
    public ResponseEntity<String> scrapeProductsZaraMan() {
        System.out.println("--------------Scraping products...");
        List<Product> products = scraperService.fetchProducts("man", "es", "zara");
        productService.setAllProduct(products);
        return ResponseEntity.ok("Scraping completed. " + products.size() + " products fetched.");
    }

    @PostMapping("/scrape/zara/woman/es")
    public ResponseEntity<String> scrapeProductsZaraWoman() {
        System.out.println("--------------Scraping products...");
        List<Product> products = scraperService.fetchProducts("woman", "es", "zara");
        productService.setAllProduct(products);
        return ResponseEntity.ok("Scraping completed. " + products.size() + " products fetched.");
    }

    @PostMapping("/scrape/zara/kid/es")
    public ResponseEntity<String> scrapeProductsZaraKid() {
        System.out.println("--------------Scraping products...");
        List<Product> products = scraperService.fetchProducts("kid", "es", "zara");
        productService.setAllProduct(products);
        return ResponseEntity.ok("Scraping completed. " + products.size() + " products fetched.");
    }

    @GetMapping("/zara/man/es")
    public List<Product> getProductsZaraMan() {
        return productService.getTask("MAN", "es", "Zara");
    }

    @GetMapping("/zara/woman/es")
    public List<Product> getProductsZaraWoman() {
        return productService.getTask("WOMAN", "es", "Zara");
    }

    @GetMapping("/zara/kid/es")
    public List<Product> getProductsZaraKid() {
        return productService.getTask("KID", "es", "Zara");
    }
    @GetMapping("/all")
    public List<Product> getAllProducts() {
        return productService.getProducts();
    }

}