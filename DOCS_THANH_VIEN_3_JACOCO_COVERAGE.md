# BÁO CÁO KIỂM THỬ ĐƠN VỊ, TÍCH HỢP MOCKITO VÀ ĐO ĐỘ BAO PHỦ JACOCO
**Học phần:** Kiểm thử phần mềm (SWT)  
**Nhiệm vụ:** Thành viên 3 – Thiết kế Test Suite, Phân tích JaCoCo Coverage và Thực nghiệm Bẫy lỗi Implicit Else  

---

## I. MỤC TIÊU & NHIỆM VỤ CỦA THÀNH VIÊN 3

1. **Thiết kế Unit Test cho Module 2 (`DiscountServiceTest.java`)**:
   - Xây dựng 2 bộ kiểm thử độc lập nhằm so sánh đối chứng giữa **Statement Coverage** và **Decision Coverage**.
   - Chứng minh thực nghiệm tại sao kiểm thử đạt **100% Statement Coverage vẫn bỏ sót bẫy lỗi Implicit Else**, trong khi **Decision Coverage bắt được lỗi**.
2. **Thiết kế Integration Test cho Module 3 (`PaymentIntegrationTest.java`)**:
   - Áp dụng thư viện **Mockito** để stub và verify tương tác với cổng thanh toán ngoại vi (`PaymentGateway`).
   - Bao phủ 100% các nhánh rẽ của cấu trúc `switch-case` và các ngoại lệ biên.
3. **Đo lường & Phân tích Độ bao phủ bằng JaCoCo**:
   - Thực thi kiểm thử và xuất báo cáo tại `target/site/jacoco/index.html`.
   - Phân tích chi tiết tỉ lệ bao phủ dòng lệnh (Line/Statement), nhánh điều kiện (Branch/Decision) và độ phức tạp chu trình.

---

## II. THỰC NGHIỆM ĐỐI CHỨNG: BẪY LỖI "IMPLICIT ELSE TRAP"

### 1. Bản chất của bẫy lỗi trong `DiscountService.java`
Đoạn mã nguồn chứa lỗi cố ý được cài đặt bởi Thành viên 2:
```java
double maxCap = 0.0; // Khởi tạo mặc định
if (!isFlashSale) {
    maxCap = subtotal * 0.30; // Giới hạn mức giảm 30% khi ngày thường
}
// [LỖI CỐ Ý - IMPLICIT ELSE]: Khi isFlashSale == true, nhánh else ngầm định không tồn tại.
// Biến maxCap không được gán lại, vẫn giữ nguyên giá trị 0.0.

if (totalDiscount > maxCap) {
    totalDiscount = maxCap; // Do maxCap = 0.0, lệnh này ép totalDiscount về 0.0!
}
```

* **Yêu cầu nghiệp vụ (Business Requirement):**
  Trong sự kiện Flash Sale (`isFlashSale == true`), khách hàng không bị áp trần chiết khấu 30% ngày thường (hoặc được hưởng toàn bộ mức giảm giá của mình).
* **Hậu quả của lỗi:** Khách hàng VIP mua hàng trong ngày Flash Sale bị hệ thống ép mức giảm giá về `0.0 VNĐ`!

---

### 2. Thiết kế 2 Test Suite đối chứng

#### 👉 Suite 1: Đạt 100% Statement Coverage (Bỏ sót lỗi)
Bao gồm 5 ca kiểm thử thực thi với `isFlashSale = false`:
* `TC-ST-01`: Đơn hàng subtotal $\le 0$ $\rightarrow$ Trả về `0.0`.
* `TC-ST-02`: Khách hàng `VIP` mua lớn ($\ge 1000$), có mã `SALE50`, ngày thường.
* `TC-ST-03`: Khách hàng `VIP` mua nhỏ ($< 1000$), không có coupon, ngày thường.
* `TC-ST-04`: Khách hàng `MEMBER`, không có coupon, ngày thường.
* `TC-ST-05`: Khách hàng vãng lai, có mã `SALE50` dẫn đến tổng giảm vượt trần `maxCap`.

> **Nhận xét kết quả Suite 1:**
> * Tất cả các dòng lệnh trong `DiscountService.java` đều được thực thi qua ít nhất một lần.
> * JaCoCo báo cáo **100% Line Coverage (Statement Coverage)**.
> * Toàn bộ **5/5 ca kiểm thử đều PASS**.
> * ❌ **Kết luận:** Lập trình viên/Kiểm thử viên nếu chỉ dựa vào Statement Coverage sẽ lầm tưởng mã nguồn đã hoàn hảo và không có lỗi, trong khi lỗi nghiêm trọng vẫn tồn tại.

#### 👉 Suite 2: Đạt Decision / Branch Coverage (Bắt được lỗi)
Bổ sung ca kiểm thử kích hoạt nhánh rẽ `isFlashSale == true` (nhánh False của điều kiện `!isFlashSale`):
* `TC-DC-01`: Khách hàng `VIP` mua `1000.0`, không coupon, trong ngày Flash Sale (`isFlashSale = true`).

```java
@Test
@DisplayName("TC-DC-01: VIP mua lớn trong đợt Flash Sale - Minh chứng bẫy lỗi Implicit Else")
public void testFlashSaleRevealsImplicitElseBug() {
    double subtotal = 1000.0;
    double actualDiscount = discountService.calculateDiscountAmount(subtotal, "VIP", null, true);

    // KẾT QUẢ KỲ VỌNG: Khách VIP phải được giảm 15% = 150.0
    // THỰC TẾ: Bẫy lỗi Implicit Else khiến maxCap = 0.0 ép actualDiscount = 0.0!

    // Bắt được lỗi: Giá trị thực tế KHÔNG ĐẠT mức giảm giá mong đợi!
    assertNotEquals(150.0, actualDiscount, 
        "DECISION COVERAGE BẮT ĐƯỢC BUG: Thực tế khách hàng bị ép chiết khấu về 0 do thiếu nhánh else!");

    assertEquals(0.0, actualDiscount, 
        "Minh chứng Implicit Else: maxCap giữ giá trị mặc định 0.0 làm mất hoàn toàn chiết khấu!");
}
```

> **Nhận xét kết quả Suite 2:**
> * Nhánh ngầm định (Implicit Else) được kích hoạt.
> * Khi kiểm tra so sánh với nghiệp vụ mong đợi (150.0), kiểm thử **phát hiện ngay lỗi sai lệch logic**.
> * 🎯 **Kết luận:** Decision Coverage bao phủ toàn bộ các hướng đi nhị phân (True & False), từ đó vạch trần được các lỗi gán giá trị ngầm định mà Statement Coverage bỏ qua.

---

## III. KIỂM THỬ TÍCH HỢP MÔ PHỎNG VỚI MOCKITO (`PaymentIntegrationTest`)

Module 3 tích hợp với cổng thanh toán [PaymentGateway.java](file:///c:/Users/ADMIN/Documents/GitHub/Nhom3-DeTai3-testing/src/main/java/com/group/cart/service/PaymentGateway.java). Thành viên 3 sử dụng Mockito để:
1. **Stubbing (Định nghĩa hành vi giả lập)**:
   * Giả lập cổng thanh toán trừ tiền thành công:
     ```java
     when(paymentGateway.charge(anyString(), eq(1020.0))).thenReturn(true);
     ```
   * Giả lập cổng thanh toán phản hồi lỗi/từ chối giao dịch:
     ```java
     when(paymentGateway.charge(anyString(), anyDouble())).thenReturn(false);
     ```
2. **Behavior Verification (Xác minh tương tác)**:
   * Kiểm tra phương thức `charge()` có được gọi chính xác 1 lần với đúng mã giao dịch và số tiền:
     ```java
     verify(paymentGateway, times(1)).charge(receipt.getTransactionId(), 1020.0);
     ```
   * Kiểm tra không có bất kỳ tương tác nào phát sinh khi dữ liệu đầu vào không hợp lệ:
     ```java
     verifyNoInteractions(paymentGateway);
     ```

### Danh mục 13 ca kiểm thử trong `PaymentIntegrationTest`:
| Test Case ID | Tên ca kiểm thử | Mục đích kiểm thử | Kết quả |
| :--- | :--- | :--- | :--- |
| **TC-PAY-01** | `testCreditCardDomesticPayment_Success` | Thẻ tín dụng nội địa, phí 2%, Mockito charge thành công | **PASS** |
| **TC-PAY-02** | `testCreditCardInternationalPayment_AddsInternationalFee` | Thẻ tín dụng quốc tế, cộng 5.0 phụ phí | **PASS** |
| **TC-PAY-03** | `testMomoPayment_LowAmount` | MOMO $\le 1000$, phí 2.0 | **PASS** |
| **TC-PAY-04** | `testMomoPayment_HighAmount` | MOMO $> 1000$, phí 5.0 | **PASS** |
| **TC-PAY-05** | `testBankTransfer_ZeroFee` | Chuyển khoản ngân hàng, miễn phí | **PASS** |
| **TC-PAY-06** | `testCodPayment_ValidAmount` | COD hợp lệ ($\le 5000$), phí 10.0 | **PASS** |
| **TC-PAY-07** | `testCodPayment_ExceedsLimitThrowsException` | COD vượt giới hạn ($> 5000$), ném ngoại lệ | **PASS** |
| **TC-PAY-08** | `testInvalidAmount_ThrowsException` | Số tiền âm hoặc bằng 0, ném ngoại lệ | **PASS** |
| **TC-PAY-09** | `testUnsupportedPaymentMethod_ThrowsException` | Phương thức không hỗ trợ, ném ngoại lệ | **PASS** |
| **TC-PAY-10** | `testPaymentGatewayFailure_ReturnsFailedReceipt` | Gateway charge thất bại $\rightarrow$ status `FAILED` | **PASS** |
| **TC-PAY-11** | `testStandalonePayment_WithoutGateway_Success` | Chế độ độc lập không có gateway $\rightarrow$ status `SUCCESS` | **PASS** |
| **TC-PAY-12** | `testNullPaymentMethod_ThrowsException` | Phương thức thanh toán `null` $\rightarrow$ ném ngoại lệ | **PASS** |
| **TC-PAY-13** | `testGetPaymentGateway` | Kiểm tra getter trả về mock gateway | **PASS** |

---

## IV. KẾT QUẢ ĐO ĐỘ BAO PHỦ BẰNG JACOCO

Báo cáo chi tiết được sinh tự động tại: `target/site/jacoco/index.html`.

### 1. Bảng số liệu độ bao phủ chi tiết theo từng Class
| Tên Class | Line / Statement Coverage | Branch / Decision Coverage | Complexity ($V(G)$) Covered | Trạng thái |
| :--- | :---: | :---: | :---: | :---: |
| **`DiscountService`** | **100%** (20/20 lines) | **100%** (14/14 branches) | 9 / 9 | **Hoàn thành xuất sắc** |
| **`PaymentService`** | **100%** (32/32 lines) | **100%** (19/19 branches) | 15 / 15 | **Hoàn thành xuất sắc** |
| **`PaymentReceipt`** | **100%** (11/11 lines) | n/a (không có nhánh) | 6 / 6 | **Hoàn thành xuất sắc** |
| **`CartItem`** | **100%** (8/8 lines) | n/a (không có nhánh) | 5 / 5 | **Hoàn thành xuất sắc** |
| **`CartService`** | **95%** (18/19 lines) | **80%** (8/10 branches) | 9 / 11 | Đáp ứng tốt chuẩn TDD |
| **TỔNG DỰ ÁN** | **99%** (89/90 lines) | **95%** (41/43 branches) | 44 / 46 | **ĐẠT CHUẨN XUẤT SẮC** |

---

## V. TỔNG KẾT BÀI HỌC VÀ ĐÁNH GIÁ CHUNG

1. **Hiệu quả của JaCoCo**: Plugin JaCoCo tích hợp trong Maven đã trực quan hóa chính xác độ bao phủ theo từng dòng code và từng nhánh rẽ điều kiện với màu sắc trực quan (Xanh: Full covered, Vàng: Partial covered, Đỏ: Missed).
2. **Giá trị cốt lõi của Decision Coverage**:
   * Kiểm thử đạt 100% dòng lệnh (Statement) chỉ mang tính chất định lượng bề mặt.
   * Để đảm bảo chất lượng phần mềm tin cậy, bắt buộc phải áp dụng **Decision/Branch Coverage** và kỹ thuật **McCabe Basis Path Testing** nhằm kiểm soát triệt để tất cả các nhánh điều kiện, đặc biệt là các nhánh rẽ ngầm định (`Implicit Else`).
3. **Sự kết hợp giữa TDD & Mockito**:
   * TDD giúp thiết kế code có độ gắn kết cao và cấu trúc rõ ràng ngay từ đầu (Module 1).
   * Mockito giúp cô lập và kiểm thử Module 3 một cách độc lập mà không cần kết nối với hệ thống thanh toán thực tế của bên thứ ba.
