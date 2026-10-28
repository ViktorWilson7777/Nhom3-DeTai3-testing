package com.group.cart.service;

import com.group.cart.model.PaymentReceipt;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
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
}
