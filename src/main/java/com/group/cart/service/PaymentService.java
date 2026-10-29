package com.group.cart.service;

import com.group.cart.model.PaymentReceipt;
import java.util.UUID;

public class PaymentService {
    private PaymentGateway paymentGateway;
    private DiscountService discountService; // Bổ sung để tích hợp với Module 2

    public PaymentService() {
    }

    public PaymentService(PaymentGateway paymentGateway) {
        this.paymentGateway = paymentGateway;
    }

    // Constructor phục vụ Kiểm thử tích hợp (Integration Testing) giữa PaymentService và DiscountService
    public PaymentService(DiscountService discountService, PaymentGateway paymentGateway) {
        this.discountService = discountService;
        this.paymentGateway = paymentGateway;
    }

    // HÀM TRỌNG TÂM SỐ 2: Dùng để vẽ CFG 2 và tính V(G) 2 (Giữ nguyên 100% để khớp với CFG 2)
    public PaymentReceipt processPayment(double amount, String paymentMethod, boolean isInternational) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Payment amount must be greater than zero");
        }

        double fee = 0.0;
        // Chú thích: Toán tử ba ngôi paymentMethod != null ? ... : "" tạo ra 1 điểm rẽ nhánh trong bytecode
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

        // Chú thích: Toán tử ba ngôi isSuccess ? ... : ... tạo ra 1 điểm rẽ nhánh trong bytecode
        String status = isSuccess ? "SUCCESS" : "FAILED";
        return new PaymentReceipt(transactionId, totalAmount, fee, method, status);
    }

    // HÀM TÍCH HỢP MODULE (Dành cho Thành viên 4 kiểm thử tích hợp bằng Stub/Driver & bắt lỗi giao tiếp)
    public PaymentReceipt checkout(CartService cart, String customerTier, String couponCode, 
                                   boolean isFlashSale, String paymentMethod, boolean isInternational) {
        if (cart == null || cart.calculateSubtotal() <= 0) {
            throw new IllegalArgumentException("Cart cannot be null or empty");
        }

        double subtotal = cart.calculateSubtotal();
        double discount = 0.0;

        if (discountService != null) {
            // [BẪY LỖI GIAO TIẾP - INTERFACE DEFECT]: 
            // Hàm calculateDiscountAmount yêu cầu (subtotal, customerTier, couponCode, isFlashSale)
            // Nhưng ở bản tích hợp đầu tiên, lập trình viên truyền nhầm thứ tự (subtotal, couponCode, customerTier, isFlashSale)
            discount = discountService.calculateDiscountAmount(subtotal, customerTier, couponCode, isFlashSale);
        }

        double finalAmountToPay = subtotal - discount;
        return processPayment(finalAmountToPay, paymentMethod, isInternational);
    }

    public PaymentGateway getPaymentGateway() {
        return paymentGateway;
    }

    public DiscountService getDiscountService() {
        return discountService;
    }
}

