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
	
	public List<Product> getTask() {
		return (List<Product>) productDao.findAll();
	}

	public Product seProduct(Product product) {
		return productDao.save(product);
	}

	public Iterable<Product> setAllProduct(List<Product> product) {
		return productDao.saveAll(product);
	}
}