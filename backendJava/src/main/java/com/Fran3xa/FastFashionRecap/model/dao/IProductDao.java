package com.Fran3xa.FastFashionRecap.model.dao;

import org.springframework.data.repository.CrudRepository;

import com.Fran3xa.FastFashionRecap.model.entitys.Product;

public interface IProductDao extends CrudRepository<Product, Long> {

}