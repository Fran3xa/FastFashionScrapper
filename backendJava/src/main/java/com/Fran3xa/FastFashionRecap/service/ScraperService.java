package com.Fran3xa.FastFashionRecap.service;

import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.Fran3xa.FastFashionRecap.model.entitys.Product;

import java.util.Arrays;
import java.util.List;

@Service
public class ScraperService {
    private static final String SCRAPER_URL_MAN = "http://localhost:5000/api/products/scrape/man";
    private static final String SCRAPER_URL_WOMAN = "http://localhost:5000/api/products/scrape/woman";
    private static final String SCRAPER_URL_KID = "http://localhost:5000/api/products/scrape/kid";


    public List<Product> fetchProducts(String category) {
        System.out.println("------Fetching products from scraper...");
        RestTemplate restTemplate = new RestTemplate();
        String url;
        switch (category) {
            case "man":
                url = SCRAPER_URL_MAN;
                break;
            case "woman":
                url = SCRAPER_URL_WOMAN;
                break;
            case "kid":
                url = SCRAPER_URL_KID;
                break;
            default:
                throw new IllegalArgumentException("Invalid category: " + category);
        }
        ResponseEntity<Product[]> response = restTemplate.getForEntity(url, Product[].class);
        return Arrays.asList(response.getBody());
    }
}