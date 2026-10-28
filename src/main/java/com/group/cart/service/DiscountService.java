package com.group.cart.service;

public class DiscountService {

    // HÀM TRỌNG TÂM SỐ 1: Dùng để vẽ CFG 1, tính V(G) và cài bẫy lỗi "Implicit Else"
    public double calculateDiscountAmount(double subtotal, String customerTier, String couponCode, boolean isFlashSale) {
        if (subtotal <= 0) {
            return 0.0; // Nhánh 1
        }

        double discountRate = 0.0;

        // Cấu trúc rẽ nhánh phức tạp
        if ("VIP".equals(customerTier)) {
            if (subtotal >= 1000.0) {
                discountRate = 0.15; // 15% cho VIP mua lớn
            } else {
                discountRate = 0.10; // 10% cho VIP mua nhỏ
            }
        } else if ("MEMBER".equals(customerTier)) {
            discountRate = 0.05; // 5% cho thành viên thông thường
        } else {
            discountRate = 0.0;  // Không giảm giá hạng khách
        }

        double totalDiscount = subtotal * discountRate;

        // Áp dụng mã giảm giá cố định
        if ("SALE50".equals(couponCode)) {
            totalDiscount += 50.0;
        }

        // --- CÀI BẪY LỖI: IMPLICIT ELSE TRAP (Trả lời câu hỏi chính) ---
        double maxCap = 0.0; // Khởi tạo mặc định
        if (!isFlashSale) {
            maxCap = subtotal * 0.30; // Giới hạn mức giảm tối đa 30% khi ngày thường
        } 
        // [LỖI CỐ Ý]: Khi isFlashSale == true, nhánh else ngầm định không gán lại maxCap, 
        // dẫn đến maxCap = 0.0, làm lệnh if bên dưới ép totalDiscount về 0.0!
        
        if (totalDiscount > maxCap) {
            totalDiscount = maxCap;
        }

        return totalDiscount;
    }
}
