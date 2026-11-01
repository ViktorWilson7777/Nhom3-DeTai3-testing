package com.group.cart.service;

import com.group.cart.model.PaymentReceipt;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.anyDouble;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

/**
 * Unit Test Suite cho Hàm số 2: PaymentService.processPayment
 * Phục vụ Thành viên 3 đo độ bao phủ JaCoCo cho Hàm 2 đã vẽ CFG 2 (V(G) = 12)
 * Đạt 100% Statement Coverage và 100% Decision Coverage
 */
public class PaymentServiceTest {

    @Test
    @DisplayName("TC-PM-01: Số tiền <= 0 ném ngoại lệ IllegalArgumentException (Node 2)")
    public void testInvalidAmountThrowsException() {
        PaymentService service = new PaymentService();
        assertThrows(IllegalArgumentException.class, () -> {
            service.processPayment(0.0, "CREDIT_CARD", false);
        });
    }

    @Test
    @DisplayName("TC-PM-02: CREDIT_CARD quốc tế (isInternational = true) & Gateway = null (Standalone)")
    public void testCreditCardInternationalWithoutGateway() {
        PaymentService service = new PaymentService();
        PaymentReceipt receipt = service.processPayment(1000.0, "CREDIT_CARD", true);
        // Phí 2% (20.0) + phụ phí quốc tế (5.0) = 25.0 -> Tổng = 1025.0
        assertEquals(25.0, receipt.getFee(), 0.001);
        assertEquals(1025.0, receipt.getTotalAmount(), 0.001);
        assertEquals("SUCCESS", receipt.getStatus());
    }

    @Test
    @DisplayName("TC-PM-03: CREDIT_CARD nội địa (isInternational = false) & Gateway trả về SUCCESS")
    public void testCreditCardDomesticWithGatewaySuccess() {
        PaymentGateway gatewayMock = Mockito.mock(PaymentGateway.class);
        when(gatewayMock.charge(anyString(), anyDouble())).thenReturn(true);
        PaymentService service = new PaymentService(gatewayMock);
        PaymentReceipt receipt = service.processPayment(1000.0, "CREDIT_CARD", false);
        assertEquals(20.0, receipt.getFee(), 0.001);
        assertEquals("SUCCESS", receipt.getStatus());
    }

    @Test
    @DisplayName("TC-PM-04: MOMO giao dịch lớn (> 1000) & Gateway trả về FAILED")
    public void testMomoLargeAmountWithGatewayFailed() {
        PaymentGateway gatewayMock = Mockito.mock(PaymentGateway.class);
        when(gatewayMock.charge(anyString(), anyDouble())).thenReturn(false);
        PaymentService service = new PaymentService(gatewayMock);
        PaymentReceipt receipt = service.processPayment(1500.0, "MOMO", false);
        assertEquals(5.0, receipt.getFee(), 0.001);
        assertEquals("FAILED", receipt.getStatus());
    }

    @Test
    @DisplayName("TC-PM-05: MOMO giao dịch nhỏ (<= 1000)")
    public void testMomoSmallAmount() {
        PaymentService service = new PaymentService();
        PaymentReceipt receipt = service.processPayment(500.0, "MOMO", false);
        assertEquals(2.0, receipt.getFee(), 0.001);
    }

    @Test
    @DisplayName("TC-PM-06: BANK_TRANSFER miễn phí giao dịch")
    public void testBankTransferFreeOfCharge() {
        PaymentService service = new PaymentService();
        PaymentReceipt receipt = service.processPayment(2000.0, "BANK_TRANSFER", false);
        assertEquals(0.0, receipt.getFee(), 0.001);
        assertEquals(2000.0, receipt.getTotalAmount(), 0.001);
    }

    @Test
    @DisplayName("TC-PM-07: COD vượt hạn mức (> 5000) ném ngoại lệ (Node 11)")
    public void testCodOverLimitThrowsException() {
        PaymentService service = new PaymentService();
        assertThrows(IllegalArgumentException.class, () -> {
            service.processPayment(6000.0, "COD", false);
        });
    }

    @Test
    @DisplayName("TC-PM-08: COD hợp lệ (<= 5000) tính phí thu hộ 10.0 (Node 12)")
    public void testCodValidAmount() {
        PaymentService service = new PaymentService();
        PaymentReceipt receipt = service.processPayment(3000.0, "COD", false);
        assertEquals(10.0, receipt.getFee(), 0.001);
        assertEquals(3010.0, receipt.getTotalAmount(), 0.001);
    }

    @Test
    @DisplayName("TC-PM-09: Phương thức thanh toán không hỗ trợ hoặc null ném ngoại lệ (Node 13)")
    public void testUnsupportedOrNullPaymentMethodThrowsException() {
        PaymentService service = new PaymentService();
        assertThrows(IllegalArgumentException.class, () -> {
            service.processPayment(500.0, "CRYPTO", false);
        });
        assertThrows(IllegalArgumentException.class, () -> {
            service.processPayment(500.0, null, false);
        });
    }
}
