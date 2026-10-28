package com.group.cart.service;

import com.group.cart.model.CartItem;
import java.util.ArrayList;
import java.util.List;

public class CartService {
    private List<CartItem> items = new ArrayList<>();

    public void addItem(CartItem newItem) {
        if (newItem.getPrice() <= 0 || newItem.getQuantity() <= 0) {
            throw new IllegalArgumentException("Price and quantity must be greater than zero");
        }
        for (CartItem item : items) {
            if (item.getId().equals(newItem.getId())) {
                item.setQuantity(item.getQuantity() + newItem.getQuantity());
                return;
            }
        }
        items.add(newItem);
    }

    public void removeItem(String productId) {
        items.removeIf(item -> item.getId().equals(productId));
    }

    public double calculateSubtotal() {
        double subtotal = 0.0;
        for (CartItem item : items) {
            subtotal += item.getPrice() * item.getQuantity();
        }
        return subtotal;
    }

    public List<CartItem> getItems() { return items; }
}