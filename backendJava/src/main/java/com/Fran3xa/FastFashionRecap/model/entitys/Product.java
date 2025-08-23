package com.Fran3xa.FastFashionRecap.model.entitys;

import java.io.Serializable;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Product implements Serializable{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private long productId;
    private String nombre;
    private String categoria;
    private String subcategoria;
    private String discount;
    private String imageUrl;
    private String ref;
    private String precioDisc;
    private String precioNodisc;

    // Getters y setters
}