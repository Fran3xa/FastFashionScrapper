package com.Fran3xa.FastFashionRecap.service;

import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.Fran3xa.FastFashionRecap.model.entitys.Product;

import java.util.Arrays;
import java.util.List;

@Service
public class ScraperService {
    private static final String SCRAPER_URL = "http://localhost:5000/api/{marca}/products/scrape/{section}/{language}";

    public List<Product> fetchProducts(String section, String language, String marca) {
        System.out.println("------------------------Fetching products from scraper...");
        RestTemplate restTemplate = new RestTemplate();
        ResponseEntity<Product[]> response = restTemplate.postForEntity(SCRAPER_URL, null, Product[].class, marca, section, language);
        return Arrays.asList(response.getBody());
    }
}