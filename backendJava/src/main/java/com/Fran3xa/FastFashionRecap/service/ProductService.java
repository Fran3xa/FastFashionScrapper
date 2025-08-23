package com.Fran3xa.FastFashionRecap.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.Fran3xa.FastFashionRecap.model.dao.IProductDao;
import com.Fran3xa.FastFashionRecap.model.entitys.Product;

@Service
public class ProductService {
	
	@Autowired
	private IProductDao productDao;
	
	public List<Product> getTask(String section, String language, String marca) {
		return (List<Product>) productDao.findByGeneroAndLanguageAndMarca(	section, language, marca);
	}

	public List<Product> getProducts() {
		return (List<Product>) productDao.findAll();
	}

	public Iterable<Product> setAllProduct(List<Product> product) {
		return productDao.saveAll(product);
	}
}