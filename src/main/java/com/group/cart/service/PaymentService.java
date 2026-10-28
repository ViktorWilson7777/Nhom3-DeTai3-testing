package com.group.cart.service;

import com.group.cart.model.PaymentReceipt;
import java.util.UUID;

public class PaymentService {
    private PaymentGateway paymentGateway;

    public PaymentService() {
    }

    public PaymentService(PaymentGateway paymentGateway) {
        this.paymentGateway = paymentGateway;
    }

    // HÀM TRỌNG TÂM SỐ 2: Dùng để vẽ CFG 2 và tính V(G) 2
    public PaymentReceipt processPayment(double amount, String paymentMethod, boolean isInternational) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Payment amount must be greater than zero");
        }

        double fee = 0.0;
        String method = (paymentMethod != null) ? paymentMethod.toUpperCase() : "";

        switch (method) {
            case "CREDIT_CARD":
                fee = amount * 0.02; // 2% phí cơ bản
                if (isInternational) {
                    fee += 5.0; // Phụ phí giao dịch quốc tế
                }
                break;
            case "MOMO":
                if (amount > 1000.0) {
                    fee = 5.0;
                } else {
                    fee = 2.0;
                }
                break;
            case "BANK_TRANSFER":
                fee = 0.0; // Miễn phí chuyển khoản
                break;
            case "COD":
                if (amount > 5000.0) {
                    throw new IllegalArgumentException("COD is not supported for amounts over 5000");
                }
                fee = 10.0; // Phí thu hộ COD
                break;
            default:
                throw new IllegalArgumentException("Unsupported payment method: " + paymentMethod);
        }

        double totalAmount = amount + fee;
        String transactionId = "TXN-" + UUID.randomUUID().toString().substring(0, 8);

        boolean isSuccess = true;
        if (paymentGateway != null) {
            isSuccess = paymentGateway.charge(transactionId, totalAmount);
        }

        String status = isSuccess ? "SUCCESS" : "FAILED";
        return new PaymentReceipt(transactionId, totalAmount, fee, method, status);
    }

    public PaymentGateway getPaymentGateway() {
        return paymentGateway;
    }
}
