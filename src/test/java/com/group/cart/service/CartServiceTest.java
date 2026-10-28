package com.group.cart.service;

import com.group.cart.model.CartItem;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CartServiceTest {
    private CartService cartService;

    @BeforeEach
    public void setUp() {
        cartService = new CartService();
    }

    @Test
    public void testAddValidItem() {
        CartItem item = new CartItem("P01", "Laptop", 1200.0, 1);
        cartService.addItem(item);
        assertEquals(1, cartService.getItems().size());
        assertEquals(1200.0, cartService.calculateSubtotal());
    }

    @Test
    public void testAddDuplicateItemAccumulatesQuantity() {
        cartService.addItem(new CartItem("P01", "Laptop", 1200.0, 1));
        cartService.addItem(new CartItem("P01", "Laptop", 1200.0, 2));
        assertEquals(1, cartService.getItems().size());
        assertEquals(3, cartService.getItems().get(0).getQuantity());
        assertEquals(3600.0, cartService.calculateSubtotal());
    }

    @Test
    public void testAddInvalidItemThrowsException() {
        CartItem invalidItem = new CartItem("P02", "Mouse", -10.0, 2);
        assertThrows(IllegalArgumentException.class, () -> {
            cartService.addItem(invalidItem);
        });
    }

    @Test
    public void testRemoveItem() {
        cartService.addItem(new CartItem("P01", "Laptop", 1200.0, 1));
        cartService.removeItem("P01");
        assertTrue(cartService.getItems().isEmpty());
        assertEquals(0.0, cartService.calculateSubtotal());
    }
}