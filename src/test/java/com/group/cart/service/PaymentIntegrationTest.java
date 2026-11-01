package com.group.cart.service;

import com.group.cart.model.CartItem;
import com.group.cart.model.PaymentReceipt;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class PaymentIntegrationTest {

    @Mock
    private PaymentGateway paymentGateway;

    private PaymentService paymentServiceWithGateway;
    private PaymentService paymentServiceStandalone;

    @BeforeEach
    public void setUp() {
        paymentServiceWithGateway = new PaymentService(paymentGateway);
        paymentServiceStandalone = new PaymentService();
    }

    // =========================================================================
    // SUITE 1: UNIT & STANDALONE PAYMENT GATEWAY VERIFICATION (processPayment)
    // =========================================================================
    @Test
    @DisplayName("TC-PAY-01: Thanh toán thẻ tín dụng nội địa thành công qua cổng thanh toán (Mockito Stub)")
    public void testCreditCardDomesticPayment_Success() {
        when(paymentGateway.charge(anyString(), eq(1020.0))).thenReturn(true);

        PaymentReceipt receipt = paymentServiceWithGateway.processPayment(1000.0, "CREDIT_CARD", false);

        assertNotNull(receipt);
        assertEquals(20.0, receipt.getFee(), 0.001); // 2% của 1000 = 20
        assertEquals(1020.0, receipt.getTotalAmount(), 0.001);
        assertEquals("CREDIT_CARD", receipt.getPaymentMethod());
        assertEquals("SUCCESS", receipt.getStatus());
        assertTrue(receipt.getTransactionId().startsWith("TXN-"));

        // Xác thực tương tác với Mock object
        verify(paymentGateway, times(1)).charge(receipt.getTransactionId(), 1020.0);
    }

    @Test
    @DisplayName("TC-PAY-02: Thanh toán thẻ tín dụng quốc tế cộng thêm 5.0 phụ phí")
    public void testCreditCardInternationalPayment_AddsInternationalFee() {
        when(paymentGateway.charge(anyString(), eq(1025.0))).thenReturn(true);

        PaymentReceipt receipt = paymentServiceWithGateway.processPayment(1000.0, "CREDIT_CARD", true);

        assertEquals(25.0, receipt.getFee(), 0.001); // 20 + 5 phụ phí
        assertEquals(1025.0, receipt.getTotalAmount(), 0.001);
        assertEquals("SUCCESS", receipt.getStatus());
        verify(paymentGateway).charge(anyString(), eq(1025.0));
    }

    @Test
    @DisplayName("TC-PAY-03: Ví điện tử MOMO đơn hàng nhỏ (<= 1000) chịu phí 2.0")
    public void testMomoPayment_LowAmount() {
        when(paymentGateway.charge(anyString(), eq(502.0))).thenReturn(true);

        PaymentReceipt receipt = paymentServiceWithGateway.processPayment(500.0, "MOMO", false);

        assertEquals(2.0, receipt.getFee(), 0.001);
        assertEquals(502.0, receipt.getTotalAmount(), 0.001);
        assertEquals("SUCCESS", receipt.getStatus());
    }

    @Test
    @DisplayName("TC-PAY-04: Ví điện tử MOMO đơn hàng lớn (> 1000) chịu phí 5.0")
    public void testMomoPayment_HighAmount() {
        when(paymentGateway.charge(anyString(), eq(1505.0))).thenReturn(true);

        PaymentReceipt receipt = paymentServiceWithGateway.processPayment(1500.0, "MOMO", false);

        assertEquals(5.0, receipt.getFee(), 0.001);
        assertEquals(1505.0, receipt.getTotalAmount(), 0.001);
        assertEquals("SUCCESS", receipt.getStatus());
    }

    @Test
    @DisplayName("TC-PAY-05: Chuyển khoản ngân hàng BANK_TRANSFER miễn phí giao dịch (fee = 0)")
    public void testBankTransfer_ZeroFee() {
        when(paymentGateway.charge(anyString(), eq(2000.0))).thenReturn(true);

        PaymentReceipt receipt = paymentServiceWithGateway.processPayment(2000.0, "BANK_TRANSFER", false);

        assertEquals(0.0, receipt.getFee(), 0.001);
        assertEquals(2000.0, receipt.getTotalAmount(), 0.001);
        assertEquals("SUCCESS", receipt.getStatus());
    }

    @Test
    @DisplayName("TC-PAY-06: COD số tiền hợp lệ (<= 5000) chịu phí cố định 10.0")
    public void testCodPayment_ValidAmount() {
        when(paymentGateway.charge(anyString(), eq(3010.0))).thenReturn(true);

        PaymentReceipt receipt = paymentServiceWithGateway.processPayment(3000.0, "COD", false);

        assertEquals(10.0, receipt.getFee(), 0.001);
        assertEquals(3010.0, receipt.getTotalAmount(), 0.001);
        assertEquals("SUCCESS", receipt.getStatus());
    }

    @Test
    @DisplayName("TC-PAY-07: COD số tiền vượt hạn mức (> 5000) ném ngoại lệ IllegalArgumentException")
    public void testCodPayment_ExceedsLimitThrowsException() {
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> {
            paymentServiceWithGateway.processPayment(5001.0, "COD", false);
        });

        assertEquals("COD is not supported for amounts over 5000", ex.getMessage());
        verifyNoInteractions(paymentGateway);
    }

    @Test
    @DisplayName("TC-PAY-08: Số tiền thanh toán âm hoặc bằng 0 ném ngoại lệ IllegalArgumentException")
    public void testInvalidAmount_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> {
            paymentServiceWithGateway.processPayment(0.0, "CREDIT_CARD", false);
        });

        assertThrows(IllegalArgumentException.class, () -> {
            paymentServiceWithGateway.processPayment(-100.0, "MOMO", false);
        });

        verifyNoInteractions(paymentGateway);
    }

    @Test
    @DisplayName("TC-PAY-09: Phương thức thanh toán không hỗ trợ ném ngoại lệ")
    public void testUnsupportedPaymentMethod_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> {
            paymentServiceWithGateway.processPayment(500.0, "CRYPTO_BITCOIN", false);
        });
    }

    @Test
    @DisplayName("TC-PAY-10: Cổng thanh toán phản hồi thất bại (charge = false) trả về hóa đơn FAILED")
    public void testPaymentGatewayFailure_ReturnsFailedReceipt() {
        when(paymentGateway.charge(anyString(), anyDouble())).thenReturn(false);

        PaymentReceipt receipt = paymentServiceWithGateway.processPayment(100.0, "BANK_TRANSFER", false);

        assertEquals("FAILED", receipt.getStatus());
        assertEquals(100.0, receipt.getTotalAmount(), 0.001);
        verify(paymentGateway).charge(anyString(), eq(100.0));
    }

    @Test
    @DisplayName("TC-PAY-11: Thanh toán không có cổng ngoại vi (standalone) mặc định thành công")
    public void testStandalonePayment_WithoutGateway_Success() {
        PaymentReceipt receipt = paymentServiceStandalone.processPayment(800.0, "MOMO", false);

        assertEquals("SUCCESS", receipt.getStatus());
        assertEquals(802.0, receipt.getTotalAmount(), 0.001);
    }

    @Test
    @DisplayName("TC-PAY-12: Phương thức thanh toán null ném ngoại lệ IllegalArgumentException")
    public void testNullPaymentMethod_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> {
            paymentServiceWithGateway.processPayment(500.0, null, false);
        });
    }

    @Test
    @DisplayName("TC-PAY-13: Kiểm tra getter getPaymentGateway trả về đối tượng gateway được inject")
    public void testGetPaymentGateway() {
        assertSame(paymentGateway, paymentServiceWithGateway.getPaymentGateway());
    }

    // =========================================================================
    // PHẦN BỔ SUNG CHO THÀNH VIÊN 4:
    // KIỂM THỬ TÍCH HỢP TOP-DOWN (CartService + DiscountService Stub + PaymentService)
    // VÀ PHÁT HIỆN LỖI GIAO TIẾP (INTERFACE DEFECTS)
    // =========================================================================
    @Nested
    @DisplayName("Suite 2: Top-Down Component Integration Testing & Interface Defects (checkout)")
    class CheckoutModuleIntegrationSuite {

        @Mock
        private DiscountService discountServiceStub;

        private CartService cartService;
        private PaymentService integratedPaymentService;

        @BeforeEach
        public void setUpIntegration() {
            // Module 1: Khởi tạo giỏ hàng thực tế (đã được kiểm thử TDD ở bước trước)
            cartService = new CartService();
            cartService.addItem(new CartItem("P01", "Gaming Laptop", 1000.0, 1)); // Subtotal = 1000.0

            // Tích hợp Top-Down: Tiêm Stub của DiscountService (Module 2) và PaymentGateway vào PaymentService (Module 3)
            integratedPaymentService = new PaymentService(discountServiceStub, paymentGateway);
        }

        @Test
        @DisplayName("TC-INT-01: Tích hợp Top-Down dùng Mockito Stub (Canned Response) cho DiscountService")
        public void testTopDownIntegration_WithDiscountStub_Success() {
            // Giả lập Stub (Tier 2 - Hardcoded/Computed Reply theo Slide SWT2):
            // Khi PaymentService gọi xuống DiscountService với đúng thứ tự tham số (1000.0, "VIP", "SALE50", false),
            // Stub trả về mức giảm giá định sẵn là 200.0
            when(discountServiceStub.calculateDiscountAmount(1000.0, "VIP", "SALE50", false))
                    .thenReturn(200.0);
            when(paymentGateway.charge(anyString(), eq(816.0))).thenReturn(true);

            // Thực thi hàm tích hợp checkout
            PaymentReceipt receipt = integratedPaymentService.checkout(
                    cartService, "VIP", "SALE50", false, "CREDIT_CARD", false
            );

            // Kiểm chứng sự phối hợp dữ liệu giữa các module:
            // Subtotal (1000.0) - Discount từ Stub (200.0) = 800.0
            // Phí CREDIT_CARD nội địa 2% của 800.0 = 16.0 -> Tổng thanh toán = 816.0
            assertNotNull(receipt);
            assertEquals(16.0, receipt.getFee(), 0.001);
            assertEquals(816.0, receipt.getTotalAmount(), 0.001);
            assertEquals("SUCCESS", receipt.getStatus());
            assertEquals("CREDIT_CARD", receipt.getPaymentMethod());

            // Xác thực giao tiếp (Interface Verification): Đảm bảo tham số truyền qua giao diện đúng thứ tự
            verify(discountServiceStub, times(1))
                    .calculateDiscountAmount(eq(1000.0), eq("VIP"), eq("SALE50"), eq(false));
            verify(paymentGateway, times(1)).charge(receipt.getTransactionId(), 816.0);
        }

        @Test
        @DisplayName("TC-INT-02: Phát hiện Lỗi Giao tiếp 1 (Parameter Ordering Defect) khi truyền ngược customerTier và couponCode")
        public void testInterfaceDefect_ParameterOrderingMismatch() {
            // Tích hợp thực tế với DiscountService thật để kiểm tra tương tác dữ liệu
            DiscountService realDiscountService = new DiscountService();
            PaymentService realIntegratedService = new PaymentService(realDiscountService, paymentGateway);
            when(paymentGateway.charge(anyString(), anyDouble())).thenReturn(true);

            // Kịch bản lỗi giao tiếp (Interface Defect):
            // Giả sử ở phía gọi hoặc trong hàm tích hợp, thứ tự 2 tham số String bị truyền ngược:
            // truyền ("SALE50", "VIP") thay vì ("VIP", "SALE50").
            // Khi đó: customerTier nhận giá trị "SALE50" (rơi vào nhánh else -> rate = 0.0)
            //         couponCode nhận giá trị "VIP" (không khớp "SALE50" -> cộng 0.0)
            // Hậu quả: Tổng giảm giá bằng 0.0 thay vì 200.0, khiến khách bị thu 1020.0 thay vì 816.0!
            PaymentReceipt receiptWithSwappedArgs = realIntegratedService.checkout(
                    cartService, "SALE50", "VIP", false, "CREDIT_CARD", false
            );

            // Ghi nhận hiện tượng lỗi giao tiếp làm sai lệch số tiền thanh toán:
            assertNotEquals(816.0, receiptWithSwappedArgs.getTotalAmount(),
                    "INTERFACE DEFECT: Truyền ngược thứ tự 2 tham số String (customerTier, couponCode) làm mất toàn bộ giảm giá!");
            assertEquals(1020.0, receiptWithSwappedArgs.getTotalAmount(), 0.001);
        }

        @Test
        @DisplayName("TC-INT-03: Kiểm thử biên giao tiếp (Boundary Interface Contract) khi giỏ hàng rỗng hoặc null")
        public void testCheckoutIntegration_EmptyOrNullCart_ThrowsException() {
            CartService emptyCart = new CartService();
            assertThrows(IllegalArgumentException.class, () -> {
                integratedPaymentService.checkout(emptyCart, "VIP", "SALE50", false, "CREDIT_CARD", false);
            });
            assertThrows(IllegalArgumentException.class, () -> {
                integratedPaymentService.checkout(null, "VIP", "SALE50", false, "CREDIT_CARD", false);
            });

            // Đảm bảo khi vi phạm hợp đồng đầu vào từ CartService, hệ thống ngắt ngay và không gọi xuống các module dưới
            verifyNoInteractions(discountServiceStub);
            verifyNoInteractions(paymentGateway);
        }
    }
}
