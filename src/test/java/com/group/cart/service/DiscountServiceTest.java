package com.group.cart.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class DiscountServiceTest {

    private DiscountService discountService;

    @BeforeEach
    public void setUp() {
        discountService = new DiscountService();
    }

    // =========================================================================
    // PHẦN 1: BỘ KIỂM THỬ ĐẠT 100% STATEMENT COVERAGE NHƯNG BỎ SÓT LỖI
    // Tất cả các dòng lệnh đều được chạy qua khi isFlashSale = false.
    // Kết quả: JaCoCo báo 100% Line Coverage, toàn bộ test đều PASS
    // nhưng KHÔNG hề phát hiện bẫy lỗi "Implicit Else Trap".
    // =========================================================================
    @Nested
    @DisplayName("Suite 1: Statement Coverage 100% (Bỏ sót bẫy lỗi Implicit Else)")
    class StatementCoverageSuite {

        @Test
        @DisplayName("TC-ST-01: Kiểm tra đơn hàng có subtotal <= 0 trả về 0.0")
        public void testSubtotalLessThanOrEqualToZero() {
            double discount = discountService.calculateDiscountAmount(0.0, "VIP", null, false);
            assertEquals(0.0, discount, 0.001);

            double discountNegative = discountService.calculateDiscountAmount(-50.0, "MEMBER", null, false);
            assertEquals(0.0, discountNegative, 0.001);
        }

        @Test
        @DisplayName("TC-ST-02: VIP mua lớn (>= 1000), có mã SALE50, ngày thường, bị giới hạn maxCap 30%")
        public void testVipLargePurchaseWithCouponCappedByMaxDiscount() {
            // subtotal = 1000.0, tier = VIP -> rate = 0.15 -> discount = 150.0
            // coupon SALE50 -> discount = 150.0 + 50.0 = 200.0
            // maxCap = 1000.0 * 0.30 = 300.0
            // totalDiscount = 200.0 <= 300.0 -> trả về 200.0
            double discount = discountService.calculateDiscountAmount(1000.0, "VIP", "SALE50", false);
            assertEquals(200.0, discount, 0.001);
        }

        @Test
        @DisplayName("TC-ST-03: VIP mua nhỏ (< 1000), không coupon, ngày thường")
        public void testVipSmallPurchaseWithoutCoupon() {
            // subtotal = 500.0, tier = VIP -> rate = 0.10 -> discount = 50.0
            // maxCap = 500.0 * 0.30 = 150.0
            // totalDiscount = 50.0 <= 150.0 -> trả về 50.0
            double discount = discountService.calculateDiscountAmount(500.0, "VIP", null, false);
            assertEquals(50.0, discount, 0.001);
        }

        @Test
        @DisplayName("TC-ST-04: Thành viên thông thường MEMBER, không coupon, ngày thường")
        public void testMemberWithoutCoupon() {
            // subtotal = 400.0, tier = MEMBER -> rate = 0.05 -> discount = 20.0
            // maxCap = 400.0 * 0.30 = 120.0 -> trả về 20.0
            double discount = discountService.calculateDiscountAmount(400.0, "MEMBER", null, false);
            assertEquals(20.0, discount, 0.001);
        }

        @Test
        @DisplayName("TC-ST-05: Khách vãng lai OTHER, có mã SALE50 nhưng subtotal nhỏ dẫn đến vượt trần maxCap")
        public void testGuestWithCouponExceedingMaxCap() {
            // subtotal = 100.0, tier = OTHER -> rate = 0.0 -> discount = 0.0
            // coupon SALE50 -> discount = 50.0
            // maxCap = 100.0 * 0.30 = 30.0
            // totalDiscount (50.0) > maxCap (30.0) -> bị cắt về maxCap = 30.0
            double discount = discountService.calculateDiscountAmount(100.0, "GUEST", "SALE50", false);
            assertEquals(30.0, discount, 0.001);
        }
    }

    // =========================================================================
    // PHẦN 2: BỘ KIỂM THỬ ĐẠT DECISION / BRANCH COVERAGE (BẮT ĐƯỢC LỖI)
    // Khi kiểm thử nhánh isFlashSale == true (nhánh False của !isFlashSale),
    // nhánh Implicit Else không gán maxCap khiến maxCap = 0.0, ép totalDiscount về 0.0!
    // =========================================================================
    @Nested
    @DisplayName("Suite 2: Decision Coverage (Kích hoạt nhánh ngầm định & Bắt bẫy lỗi Implicit Else)")
    class DecisionCoverageSuite {

        @Test
        @DisplayName("TC-DC-01: VIP mua lớn trong đợt Flash Sale - Minh chứng bẫy lỗi Implicit Else")
        public void testFlashSaleRevealsImplicitElseBug() {
            // Yêu cầu nghiệp vụ (Business Requirement):
            // Khách VIP mua 1000.0 trong ngày Flash Sale phải được giảm 15% = 150.0 (hoặc không bị giới hạn trần).
            double subtotal = 1000.0;
            double actualDiscount = discountService.calculateDiscountAmount(subtotal, "VIP", null, true);

            // PHÂN TÍCH THỰC NGHIỆM:
            // 1. Nếu hệ thống đúng: actualDiscount phải là 150.0.
            // 2. Tuy nhiên, do bẫy lỗi "Implicit Else Trap" trong code:
            //    double maxCap = 0.0;
            //    if (!isFlashSale) { maxCap = subtotal * 0.30; } // isFlashSale=true nên bỏ qua!
            //    if (totalDiscount > maxCap) { totalDiscount = maxCap; } // 150.0 > 0.0 -> ép về 0.0!
            
            // Bắt được lỗi (Bug caught): Giá trị thực tế KHÔNG ĐẠT mức giảm giá mong đợi 150.0!
            assertNotEquals(150.0, actualDiscount, 
                "DECISION COVERAGE BẮT ĐƯỢC BUG: Thực tế khách hàng bị ép chiết khấu về 0 do thiếu nhánh else!");

            // Kiểm chứng chính xác hiện tượng bẫy lỗi trả về 0.0:
            assertEquals(0.0, actualDiscount, 
                "Minh chứng Implicit Else: maxCap giữ giá trị mặc định 0.0 làm mất hoàn toàn chiết khấu!");
        }

        @Test
        @DisplayName("TC-DC-02: Khách vãng lai trong đợt Flash Sale không có giảm giá")
        public void testGuestInFlashSaleWithoutDiscount() {
            // Khách thường không có giảm giá và không có coupon -> totalDiscount = 0.0
            // maxCap = 0.0, totalDiscount > maxCap (0.0 > 0.0 là False) -> trả về 0.0
            double discount = discountService.calculateDiscountAmount(200.0, "REGULAR", null, true);
            assertEquals(0.0, discount, 0.001);
        }
    }
}
