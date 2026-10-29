# -*- coding: utf-8 -*-
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import shutil

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'  <w:left w:val="single" w:sz="16" w:space="0" w:color="1D4ED8"/>'
        f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
    f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_centered_picture(doc, img_path, width_inches=6.0, caption=""):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.add_run().add_picture(img_path, width=Inches(width_inches))
        
        if caption:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(8)
            r = p_cap.add_run(f"Hình: {caption}")
            r.italic = True
            r.font.name = "Calibri"
            r.font.size = Pt(9.0)
            r.font.color.rgb = RGBColor(100, 116, 139)

def format_table(table, col_widths, headers, data):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table)
    
    hdr_cells = table.rows[0].cells
    for i, header_text in enumerate(headers):
        hdr_cells[i].text = header_text
        set_cell_background(hdr_cells[i], "1E3A8A")
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    for row_idx, row_data in enumerate(data):
        row_cells = table.add_row().cells
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = cell_value
            set_cell_background(row_cells[col_idx], bg)
            set_cell_margins(row_cells[col_idx], top=70, bottom=70, left=90, right=90)
            p = row_cells[col_idx].paragraphs[0]
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9.0)
                r.font.color.rgb = RGBColor(30, 41, 59)
                
    for i, width in enumerate(col_widths):
        table.columns[i].width = Inches(width)
        for cell in table.columns[i].cells:
            cell.width = Inches(width)

def main():
    shutil.copyfile("PHẦN 2 RBL SWT_backup.docx", "PHẦN 2 RBL SWT.docx")
    doc = docx.Document("PHẦN 2 RBL SWT.docx")
    
    # Append completed section
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(18)
    p_div.paragraph_format.space_after = Pt(6)
    r = p_div.add_run("========================================================================\n"
                      "HOÀN THIỆN ĐẦY ĐỦ CÔNG VIỆC CỦA THÀNH VIÊN 2 (SƠ ĐỒ & BẢNG SỐ LIỆU ĐỒ THỊ)\n"
                      "========================================================================")
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(30, 58, 138)

    # 1. Bổ sung chuẩn hóa CFG 1 & Ảnh sơ đồ
    h_cfg1 = doc.add_paragraph()
    h_cfg1.paragraph_format.space_before = Pt(10)
    h_cfg1.paragraph_format.space_after = Pt(4)
    r = h_cfg1.add_run("2.1 Chuẩn hóa Mô hình 16 Nodes cho Hàm 1 & Sơ đồ CFG 1:")
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(30, 58, 138)

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.add_run(
        "• Mô hình chuẩn hóa CFG 16 Nodes cho Hàm 1:\n"
        "  - Node 1: Entry if (subtotal <= 0) | Node 2: return 0.0 (Exit 1: Guard)\n"
        "  - Node 3: if (VIP) | Node 4: if (subtotal >= 1000) | Node 5 & 6: discountRate = 0.15 / 0.10\n"
        "  - Node 7: else if (MEMBER) | Node 8 & 9: discountRate = 0.05 / 0.0\n"
        "  - Node 10: Junction 1 + if (SALE50) | Node 11: totalDiscount += 50.0\n"
        "  - Node 12: Junction 2 + if (!isFlashSale) | Node 13: maxCap = subtotal * 0.30\n"
        "  - Node 14: Junction 3 (Implicit Else) + if (totalDiscount > maxCap) | Node 15: totalDiscount = maxCap\n"
        "  - Node 16: return totalDiscount (Exit 2: Normal)\n"
        "• Độ phức tạp chu trình McCabe: V(G)1 = P + 1 = 7 + 1 = 8. (Basis Paths = 8).\n"
        "• Số ca test tối thiểu: Statement Coverage = 5 ca (5 khối loại trừ) | Decision Coverage = 6 ca (gộp nhánh tuần tự theo ISTQB) | Basis Path = 8 ca."
    )

    add_centered_picture(doc, "docs/images/CFG1_calculateDiscountAmount.png", width_inches=5.8,
                         caption="CFG 1 - Sơ đồ dòng điều khiển hàm calculateDiscountAmount()")

    # 2. Hoàn thiện Module 3: PaymentService
    h_mod3 = doc.add_paragraph()
    h_mod3.paragraph_format.space_before = Pt(14)
    h_mod3.paragraph_format.space_after = Pt(4)
    r = h_mod3.add_run("3. Hoàn thiện Module 3: PaymentService.java, Hàm tích hợp checkout, Sơ đồ CFG 2 và V(G)2")
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(11.5)
    r.font.color.rgb = RGBColor(30, 58, 138)

    doc.add_paragraph("Mã nguồn Java Module 3 (PaymentService.java) có đầy đủ hàm checkout kết nối 3 module:")
    code_payment = """package com.group.cart.service;

import com.group.cart.model.PaymentReceipt;
import java.util.UUID;

public class PaymentService {
    private PaymentGateway paymentGateway;
    private DiscountService discountService; // Bổ sung để tích hợp với Module 2

    public PaymentService() {}

    public PaymentService(PaymentGateway paymentGateway) {
        this.paymentGateway = paymentGateway;
    }

    public PaymentService(DiscountService discountService, PaymentGateway paymentGateway) {
        this.discountService = discountService;
        this.paymentGateway = paymentGateway;
    }

    public PaymentReceipt processPayment(double amount, String paymentMethod, boolean isInternational) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Payment amount must be greater than zero");
        }

        double fee = 0.0;
        String method = (paymentMethod != null) ? paymentMethod.toUpperCase() : "";

        switch (method) {
            case "CREDIT_CARD":
                fee = amount * 0.02;
                if (isInternational) {
                    fee += 5.0;
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
                fee = 0.0;
                break;
            case "COD":
                if (amount > 5000.0) {
                    throw new IllegalArgumentException("COD is not supported for amounts over 5000");
                }
                fee = 10.0;
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

    // HÀM TÍCH HỢP MODULE (Dành cho Thành viên 4 kiểm thử tích hợp bằng Stub/Driver & bắt lỗi giao tiếp)
    public PaymentReceipt checkout(CartService cart, String customerTier, String couponCode, 
                                   boolean isFlashSale, String paymentMethod, boolean isInternational) {
        if (cart == null || cart.calculateSubtotal() <= 0) {
            throw new IllegalArgumentException("Cart cannot be null or empty");
        }

        double subtotal = cart.calculateSubtotal();
        double discount = 0.0;

        if (discountService != null) {
            discount = discountService.calculateDiscountAmount(subtotal, customerTier, couponCode, isFlashSale);
        }

        double finalAmountToPay = subtotal - discount;
        return processPayment(finalAmountToPay, paymentMethod, isInternational);
    }
}"""
    add_code_block(doc, code_payment)

    doc.add_paragraph("Bảng phân rã các khối lệnh CFG 2 chuẩn hóa (16 Nodes):")
    t_cfg2_hdr = ["Node ID", "Khối lệnh trong processPayment", "Kiểu Node"]
    t_cfg2_data = [
        ["Node 1", "if (amount <= 0)", "Entry & Decision (P1)"],
        ["Node 2", "throw new IllegalArgumentException(\"Payment amount...\");", "Exit 1 (Ngoại lệ biên)"],
        ["Node 3", "method = (paymentMethod != null) ? ...; switch (method)", "Decision & Switch (P2)"],
        ["Node 4", "case \"CREDIT_CARD\": fee = amount * 0.02; if (isInternational)", "Decision (P3)"],
        ["Node 5", "fee += 5.0;", "Processing"],
        ["Node 6", "case \"MOMO\": if (amount > 1000.0)", "Decision (P4)"],
        ["Node 7", "fee = 5.0;", "Processing"],
        ["Node 8", "fee = 2.0;", "Processing"],
        ["Node 9", "case \"BANK_TRANSFER\": fee = 0.0;", "Processing"],
        ["Node 10", "case \"COD\": if (amount > 5000.0)", "Decision (P5)"],
        ["Node 11", "throw new IllegalArgumentException(\"COD is not supported...\");", "Exit 2 (Ngoại lệ COD)"],
        ["Node 12", "fee = 10.0;", "Processing"],
        ["Node 13", "default: throw new IllegalArgumentException(\"Unsupported...\");", "Exit 3 (Ngoại lệ default)"],
        ["Node 14", "Junction Switch: totalAmount = amount + fee; if (gateway != null)", "Junction & Decision (P6)"],
        ["Node 15", "isSuccess = paymentGateway.charge(transactionId, totalAmount);", "Processing (Điểm cắm Mock Gateway)"],
        ["Node 16", "status = isSuccess ? \"SUCCESS\" : \"FAILED\"; return receipt;", "Decision (P7) & Exit 4 (Normal)"]
    ]
    t_cfg2 = doc.add_table(rows=1, cols=3)
    format_table(t_cfg2, [1.1, 4.0, 1.4], t_cfg2_hdr, t_cfg2_data)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    doc.add_paragraph("Sơ đồ dòng điều khiển CFG 2:")
    add_centered_picture(doc, "docs/images/CFG2_processPayment.png", width_inches=6.0,
                         caption="CFG 2 - Sơ đồ dòng điều khiển hàm processPayment()")

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    p.add_run(
        "• Độ phức tạp chu trình McCabe V(G)2:\n"
        "  - Lệnh switch(method) có 5 nhánh => tương đương 4 quyết định nhị phân.\n"
        "  - 2 toán tử ba ngôi (paymentMethod != null ? ... và isSuccess ? ...) tạo thêm 2 điểm rẽ nhánh trong bytecode JaCoCo.\n"
        "  - Tổng số vị từ P = 11 => V(G)2 = P + 1 = 11 + 1 = 12 (hoặc 11 nếu không tính null-check).\n"
        "  - Theo công thức mở rộng đa thoát: V(G)2 = E - N + 1 + k = 21 - 16 + 1 + 4 = 10 (cộng thêm 2 nhánh ternary = 12).\n"
        "  - Tập đường dẫn cơ sở: 12 Basis Paths."
    )

    # 3. Bảng tổng hợp số liệu đồ thị & McCabe
    h_exp = doc.add_paragraph()
    h_exp.paragraph_format.space_before = Pt(14)
    h_exp.paragraph_format.space_after = Pt(4)
    r = h_exp.add_run("4. Bảng tổng hợp số liệu đồ thị dòng điều khiển & Độ phức tạp McCabe")
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(11.5)
    r.font.color.rgb = RGBColor(30, 58, 138)

    add_centered_picture(doc, "docs/images/Bang_Thong_Ke_So_Lieu_CFG_McCabe_TV2.png", width_inches=6.0,
                         caption="Bảng thống kê số liệu đồ thị CFG và độ phức tạp McCabe của Thành viên 2")

    t_exp_hdr = ["Thông số phân tích CFG", "Hàm 1: calculateDiscountAmount", "Hàm 2: processPayment", "Cơ sở toán học & ISTQB"]
    t_exp_data = [
        ["Số đỉnh đồ thị (Nodes N)", "16 đỉnh", "16 đỉnh", "Phân rã chuẩn hóa từng khối câu lệnh"],
        ["Số cạnh rẽ nhánh (Edges E)", "21 cạnh", "21 cạnh (23 tính cả ternary)", "Đồ thị có hướng"],
        ["Số nút vị từ nhị phân (P)", "7 vị từ", "11 vị từ (switch 5 nhánh = 4)", "Điểm quyết định nhị phân"],
        ["Số điểm thoát (Exit Nodes k)", "2 điểm (Guard & Normal)", "4 điểm (3 Ex + 1 Normal)", "Các lệnh return & throw"],
        ["Độ phức tạp chu trình V(G)", "V(G)1 = 8", "V(G)2 = 12 (hoặc 11)", "Công thức V(G) = P + 1"],
        ["Min Tests 100% Statement Coverage", "5 ca kiểm thử", "8 ca kiểm thử", "Khối rẽ nhánh loại trừ lẫn nhau"],
        ["Min Tests 100% Decision Coverage", "6 ca kiểm thử", "8 - 10 ca kiểm thử", "Gộp nhánh tuần tự (Slide SWT4 / ISTQB)"],
        ["Số đường dẫn cơ sở (Basis Paths)", "8 Basis Paths độc lập", "12 Basis Paths độc lập", "Đặc tả bàn giao cho Thành viên 3 & 4"]
    ]
    t_exp = doc.add_table(rows=1, cols=4)
    format_table(t_exp, [1.8, 1.6, 1.6, 1.5], t_exp_hdr, t_exp_data)

    # 4. Bảng so sánh toàn diện lý thuyết
    h_cmp = doc.add_paragraph()
    h_cmp.paragraph_format.space_before = Pt(14)
    h_cmp.paragraph_format.space_after = Pt(4)
    r = h_cmp.add_run("5. Bảng tổng hợp so sánh lý thuyết giữa Statement Coverage và Decision Coverage")
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(11.5)
    r.font.color.rgb = RGBColor(30, 58, 138)

    t_cmp_hdr = ["Tiêu chí phân tích", "Hàm 1: calculateDiscountAmount", "Hàm 2: processPayment"]
    t_cmp_data = [
        ["Độ phức tạp chu trình V(G)", "V(G)1 = 8", "V(G)2 = 12"],
        ["Số test case tối thiểu lý thuyết (Statement)", "5 ca kiểm thử (5 khối loại trừ: Node 2, 5, 6, 8, 9)", "8 ca kiểm thử (8 khối loại trừ: Node 2, 5, 7, 8, 9, 11, 12, 13)"],
        ["Số test case tối thiểu lý thuyết (Decision)", "6 ca kiểm thử (gộp nhánh tuần tự theo ISTQB, thêm isFlashSale=true)", "8 - 10 ca kiểm thử (phủ 8 nhánh rẽ và các điều kiện phụ)"],
        ["Số test case phủ toàn bộ Basis Paths", "8 ca kiểm thử (bằng đúng V(G)1)", "12 ca kiểm thử (bằng đúng V(G)2)"],
        ["Khả năng phát hiện bẫy lỗi Implicit Else Trap", "Statement Coverage (5 tests): HOÀN TOÀN BỎ SÓT (Pass ảo 100%)\nDecision Coverage (6 tests): BẮT ĐƯỢC CHÍNH XÁC BUG (kích hoạt !isFlashSale False)", "Bao phủ đầy đủ các nhánh ngoại lệ và điều kiện biên"]
    ]
    t_cmp = doc.add_table(rows=1, cols=3)
    format_table(t_cmp, [2.0, 2.3, 2.2], t_cmp_hdr, t_cmp_data)

    # Handover note
    p_end = doc.add_paragraph()
    p_end.paragraph_format.space_before = Pt(12)
    p_end.paragraph_format.line_spacing = 1.15
    r_end = p_end.add_run(
        "👉 Bàn giao cho Thành viên 3 & 4: Sau khi Thành viên 2 hoàn thành toàn bộ mã nguồn Module 2 & 3, "
        "hàm tích hợp checkout(...), sơ đồ CFG 1 & 2 (16 Nodes) và tập đường dẫn cơ sở lý thuyết (8 Basis Paths Hàm 1, 12 Basis Paths Hàm 2), "
        "tài liệu này được bàn giao để Thành viên 3 triển khai Unit Test / đo độ bao phủ JaCoCo và Thành viên 4 triển khai Integration Test bắt lỗi giao tiếp!"
    )
    r_end.bold = True
    r_end.font.color.rgb = RGBColor(21, 128, 61)

    doc.save("PHẦN 2 RBL SWT.docx")
    print("Updated PHAN 2 RBL SWT.docx successfully!")

if __name__ == "__main__":
    main()
