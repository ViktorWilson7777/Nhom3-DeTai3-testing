package com.group.cart.model;

public class CartItem {
    private String id;
    private String name;
    private double price;
    private int quantity;

    public CartItem(String id, String name, double price, int quantity) {
        this.id = id; this.name = name; this.price = price; this.quantity = quantity;
    }
    public String getId() { return id; }
    public double getPrice() { return price; }
    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) { this.quantity = quantity; }
}