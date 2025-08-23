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

    @GetMapping("/scrape/man")
    public ResponseEntity<String> scrapeProductsMan() {
        System.out.println("--------------Scraping products...");
        List<Product> products = scraperService.fetchProducts("man");
        productService.setAllProduct(products);
        return ResponseEntity.ok("Scraping completed. " + products.size() + " products fetched.");
    }

    @GetMapping("/scrape/woman")
    public ResponseEntity<String> scrapeProductsWoman() {
        System.out.println("--------------Scraping products...");
        List<Product> products = scraperService.fetchProducts("woman");
        productService.setAllProduct(products);
        return ResponseEntity.ok("Scraping completed. " + products.size() + " products fetched.");
    }

    @GetMapping("/scrape/kid")
    public ResponseEntity<String> scrapeProductsKid() {
        System.out.println("-Scraping products...");
        List<Product> products = scraperService.fetchProducts("kid");
        productService.setAllProduct(products);
        return ResponseEntity.ok("Scraping completed. " + products.size() + " products fetched.");
    }

    @GetMapping("/all")
    public List<Product> getProducts() {
        return productService.getTask();
    }

    @PostMapping("/add")
    public Product addProduct(Product product) {
        return productService.seProduct(product);
    }
}