package com.group.cart.model;

public class PaymentReceipt {
    private String transactionId;
    private double totalAmount;
    private double fee;
    private String paymentMethod;
    private String status;

    public PaymentReceipt(String transactionId, double totalAmount, double fee, String paymentMethod, String status) {
        this.transactionId = transactionId;
        this.totalAmount = totalAmount;
        this.fee = fee;
        this.paymentMethod = paymentMethod;
        this.status = status;
    }

    public String getTransactionId() {
        return transactionId;
    }

    public double getTotalAmount() {
        return totalAmount;
    }

    public double getFee() {
        return fee;
    }

    public String getPaymentMethod() {
        return paymentMethod;
    }

    public String getStatus() {
        return status;
    }
}
