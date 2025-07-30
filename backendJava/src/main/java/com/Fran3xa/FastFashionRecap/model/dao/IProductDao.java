package com.Fran3xa.FastFashionRecap.model.dao;

import java.util.List;

import org.springframework.data.repository.CrudRepository;

import com.Fran3xa.FastFashionRecap.model.entitys.Product;

public interface IProductDao extends CrudRepository<Product, Long> {

    List<Product> findByGeneroAndLanguageAndMarca(String genero, String language, String marca);


}
