package com.group.cart.service;

public interface PaymentGateway {
    boolean charge(String transactionId, double amount);
}
