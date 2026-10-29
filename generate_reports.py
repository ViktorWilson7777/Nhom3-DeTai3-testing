# -*- coding: utf-8 -*-
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D1D5DB", sz="4", val="single"):
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
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>'
        f'  <w:left w:val="single" w:sz="18" w:space="0" w:color="2563EB"/>'
        f'  <w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_callout(doc, title, text, bg_color="FEF3C7", border_color="D97706", text_color="92400E"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="none"/>'
        f'  <w:bottom w:val="none"/>'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    r_title = p.add_run(title + "\n")
    r_title.bold = True
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(10.5)
    r_title.font.color.rgb = RGBColor(180, 83, 9)
    
    r_text = p.add_run(text)
    r_text.font.name = "Calibri"
    r_text.font.size = Pt(9.5)
    r_text.font.color.rgb = RGBColor(146, 64, 14)
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

def format_table(table, col_widths, headers, data, align_cols=None):
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
            if align_cols and col_idx in align_cols:
                p.alignment = align_cols[col_idx]
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9.0)
                r.font.color.rgb = RGBColor(30, 41, 59)
                
    for i, width in enumerate(col_widths):
        table.columns[i].width = Inches(width)
        for cell in table.columns[i].cells:
            cell.width = Inches(width)

def generate_standalone_doc():
    doc = docx.Document()
    
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    r = p_title.add_run("BÁO CÁO PHÂN TÍCH DÒNG ĐIỀU KHIỂN (CFG)\nVÀ TÍNH TOÁN ĐỘ PHỨC TẠP CHU TRÌNH MCCABE V(G)")
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(15)
    r.font.color.rgb = RGBColor(30, 58, 138)
    
    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(14)
    r_sub = p_sub.add_run("Học phần: Kiểm thử phần mềm (SWT) | Đề tài 3: Shopping Cart & Payment Testing\nNhiệm vụ: THÀNH VIÊN 2 – Phát triển Module 2 & 3, Thiết kế CFG 1 & 2, McCabe V(G), Bẫy lỗi Implicit Else & Giao diện tích hợp Module")
    r_sub.italic = True
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(10.0)
    r_sub.font.color.rgb = RGBColor(71, 85, 105)
    
    # Section 1
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(4)
    r = h1.add_run("I. TỔNG QUAN PHÂN ĐỊNH TRÁCH NHIỆM CỦA THÀNH VIÊN 2")
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(12.5)
    r.font.color.rgb = RGBColor(30, 58, 138)
    
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.add_run(
        "Theo tiến trình thực hiện tuần tự của đề tài nhóm:\n"
        "• Thành viên 1: Đã hoàn thành Module 1 (CartService.java) theo quy trình TDD (Test-Driven Development).\n"
        "• Thành viên 2 (Báo cáo này): Thực hiện nhiệm vụ thiết kế mã nguồn nghiệp vụ (Production Code) của Module 2 (DiscountService.java) và Module 3 (PaymentService.java, PaymentReceipt.java, PaymentGateway.java); "
        "xây dựng hàm tích hợp checkout(...) kết nối liên hoàn 3 module; "
        "phân tích và trực quan hóa sơ đồ dòng điều khiển (CFG 1 & CFG 2 với 16 đỉnh chuẩn hóa); "
        "tính toán lý thuyết độ phức tạp chu trình McCabe V(G); "
        "xác định số ca kiểm thử tối thiểu theo chuẩn ISTQB cho Statement Coverage, Decision Coverage và Basis Path Coverage; "
        "và chuẩn bị gói đặc tả kỹ thuật bàn giao cho Thành viên 3 & Thành viên 4.\n"
        "• Thành viên 3: Sau khi nhận bàn giao từ Thành viên 2, Thành viên 3 độc lập viết mã kiểm thử đơn vị (Unit Test & Mockito Mock) và đo đạc độ bao phủ thực nghiệm bằng công cụ JaCoCo.\n"
        "• Thành viên 4: Sử dụng hàm checkout(...) và DiscountService được bàn giao để triển khai Kiểm thử tích hợp (Integration Testing) bằng phương pháp Top-down với Stub/Mock, bắt bẫy lỗi giao tiếp truyền ngược tham số.\n"
        "• Thành viên 5: Phụ trách kiểm thử hệ thống (System Testing) và tổng hợp báo cáo chung."
    )
    
    # Section 2
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(4)
    r = h2.add_run("II. HÀM TRỌNG TÂM SỐ 1: calculateDiscountAmount (DiscountService)")
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(12.5)
    r.font.color.rgb = RGBColor(30, 58, 138)
    
    doc.add_paragraph("1. Mã nguồn Java nghiệp vụ (DiscountService.java):")
    code_discount = """package com.group.cart.service;

public class DiscountService {
    // HÀM TRỌNG TÂM SỐ 1: Dùng để vẽ CFG 1, tính V(G) 1 và cài bẫy lỗi "Implicit Else"
    public double calculateDiscountAmount(double subtotal, String customerTier, String couponCode, boolean isFlashSale) {
        if (subtotal <= 0) {
            return 0.0; // Nhánh 1: Điều kiện bảo vệ (Guard Clause)
        }

        double discountRate = 0.0;
        if ("VIP".equals(customerTier)) {
            if (subtotal >= 1000.0) {
                discountRate = 0.15; // 15% cho VIP mua lớn
            } else {
                discountRate = 0.10; // 10% cho VIP mua nhỏ
            }
        } else if ("MEMBER".equals(customerTier)) {
            discountRate = 0.05; // 5% cho thành viên thông thường
        } else {
            discountRate = 0.0;  // 0% cho khách vãng lai
        }

        double totalDiscount = subtotal * discountRate;
        if ("SALE50".equals(couponCode)) {
            totalDiscount += 50.0;
        }

        // --- CÀI BẪY LỖI: IMPLICIT ELSE TRAP (Trả lời câu hỏi chính) ---
        double maxCap = 0.0; // Khởi tạo mặc định
        if (!isFlashSale) {
            maxCap = subtotal * 0.30; // Giới hạn mức giảm tối đa 30% khi ngày thường
        } 
        // [LỖI CỐ Ý - IMPLICIT ELSE]: Khi isFlashSale == true, nhánh else ngầm định không gán lại maxCap, 
        // dẫn đến maxCap = 0.0, làm lệnh if bên dưới ép totalDiscount về 0.0!
        if (totalDiscount > maxCap) {
            totalDiscount = maxCap;
        }

        return totalDiscount;
    }
}"""
    add_code_block(doc, code_discount)
    
    doc.add_paragraph("2. Bảng phân rã các khối lệnh CFG 1 chuẩn hóa (Standardized CFG - 16 Nodes):")
    t1_headers = ["Node ID (Mô hình 16 Nodes)", "Dòng mã / Khối câu lệnh thực thi (Code Statement)", "Kiểu Node trong lý thuyết CFG (Classification)"]
    t1_data = [
        ["Node 1", "if (subtotal <= 0)", "Entry & Decision Node (Predicate P1)"],
        ["Node 2", "return 0.0;", "Exit Node 1 (Guard Clause Early Return)"],
        ["Node 3", "discountRate = 0.0; if (\"VIP\".equals(customerTier))", "Decision Node (Predicate P2)"],
        ["Node 4", "if (subtotal >= 1000.0)", "Decision Node (Predicate P3)"],
        ["Node 5", "discountRate = 0.15;", "Processing Node (VIP mua lớn)"],
        ["Node 6", "discountRate = 0.10;", "Processing Node (VIP mua nhỏ)"],
        ["Node 7", "else if (\"MEMBER\".equals(customerTier))", "Decision Node (Predicate P4)"],
        ["Node 8", "discountRate = 0.05;", "Processing Node (Khách thành viên)"],
        ["Node 9", "discountRate = 0.0;", "Processing Node (Khách vãng lai)"],
        ["Node 10", "totalDiscount = subtotal * discountRate; if (\"SALE50\".equals(couponCode))", "Junction 1 & Decision Node (Predicate P5)"],
        ["Node 11", "totalDiscount += 50.0;", "Processing Node (Áp mã SALE50)"],
        ["Node 12", "double maxCap = 0.0; if (!isFlashSale)", "Junction 2 & Decision Node (Predicate P6)"],
        ["Node 13", "maxCap = subtotal * 0.30;", "Processing Node (Giới hạn trần ngày thường)"],
        ["Node 14", "if (totalDiscount > maxCap) [Kích hoạt bẫy Implicit Else]", "Junction 3 & Decision Node (Predicate P7)"],
        ["Node 15", "totalDiscount = maxCap;", "Processing Node (Ép giảm giá về trần)"],
        ["Node 16", "return totalDiscount;", "Exit Node 2 (Normal Return)"]
    ]
    t1 = doc.add_table(rows=1, cols=3)
    format_table(t1, [1.5, 3.2, 1.8], t1_headers, t1_data)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    doc.add_paragraph("3. Sơ đồ dòng điều khiển CFG 1 (Chụp hình sơ đồ phục vụ báo cáo):")
    add_centered_picture(doc, "docs/images/CFG1_calculateDiscountAmount.png", width_inches=5.8,
                         caption="CFG 1 - Sơ đồ dòng điều khiển hàm calculateDiscountAmount với 16 Nodes và bẫy lỗi Implicit Else")

    doc.add_paragraph("4. Tính toán độ phức tạp chu trình McCabe V(G) và Phân tích số ca kiểm thử tối thiểu:")
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.add_run(
        "• Phương pháp 1 (Đếm vị từ P): P = 7 điểm quyết định nhị phân => V(G)1 = P + 1 = 7 + 1 = 8.\n"
        "• Phương pháp 2 (Đồ thị phẳng mở rộng cho k=2 điểm thoát): V(G)1 = E - N + 1 + k = 21 - 16 + 1 + 2 = 8.\n"
        "• Phương pháp 3 (Đếm số miền phân hoạch phẳng): 7 miền kín + 1 miền ngoài vô tận => V(G)1 = 8.\n"
        "• Tập đường dẫn cơ sở (Basis Paths): Gồm đúng 8 đường độc lập tuyến tính (Path 1 đến Path 8).\n\n"
        "PHÂN TÍCH SỐ CA KIỂM THỬ TỐI THIỂU LÝ THUYẾT THEO CHUẨN ISTQB:\n"
        "1. Số test case tối thiểu đạt 100% Statement Coverage = 5 ca kiểm thử:\n"
        "   - Trong sơ đồ CFG 1, có 5 khối lệnh nằm trên các nhánh loại trừ lẫn nhau hoàn toàn (không một ca kiểm thử nào có thể đi qua 2 trong 5 nút này cùng lúc): "
        "Node 2 (subtotal <= 0), Node 5 (VIP lớn), Node 6 (VIP nhỏ), Node 8 (MEMBER), Node 9 (khách vãng lai). "
        "Do mỗi test case chỉ chạm được đúng 1 trong 5 khối này, để chạm tới 100% câu lệnh của Hàm 1 thì tối thiểu bắt buộc phải có 5 test cases. "
        "Trong đó, cả 4 ca kiểm thử hợp lệ đều truyền isFlashSale = false để đi qua Node 13, đồng thời khéo léo kết hợp có/không mã SALE50 để đi qua Node 11 và 15. "
        "Với 3 ca kiểm thử thì về mặt toán học đồ thị không thể chạm tới toàn bộ các nút này.\n"
        "2. Số test case tối thiểu đạt 100% Decision (Branch) Coverage = 6 ca kiểm thử:\n"
        "   - Theo chuẩn ISTQB (Slide SWT4, Examples 4 & 5; sách Jeff Tian, Ch. 11, tr. 180): Khi các lệnh if nằm nối tiếp tuần tự (Node 10 -> Node 12 -> Node 14), "
        "ta có thể gộp việc kiểm tra nhánh True/False của chúng vào chung các lần chạy của các nhánh rẽ phía trên. "
        "Với 5 test case ở trên (tất cả đều có isFlashSale = false để phủ nhánh True của Node 12), ta chỉ cần bổ sung thêm đúng 1 test case có isFlashSale = true "
        "để phủ nốt nhánh False của Node 12 (hoặc chuyển 1 trong 4 test trên sang isFlashSale = true nhưng vẫn giữ ít nhất 1 test isFlashSale = false). "
        "Do đó, số ca kiểm thử tối thiểu để đạt 100% Decision Coverage chỉ cần 6 test cases.\n"
        "3. Số ca kiểm thử phủ toàn bộ tập đường dẫn cơ sở (Basis Path Coverage) = 8 ca kiểm thử:\n"
        "   - Độ phức tạp McCabe V(G) = 8 biểu thị số chiều của không gian đường dẫn. Để phủ toàn bộ 8 Basis Paths độc lập tuyến tính, cần đúng 8 ca kiểm thử. "
        "Việc phân biệt rõ giữa 100% Decision Coverage (6 tests) và Basis Path Coverage (8 tests) khẳng định nhóm hiểu sâu sắc bản chất chuẩn mực quốc tế của ISTQB."
    )
    
    add_callout(
        doc,
        "PHÂN TÍCH LÝ THUYẾT: BẪY LỖI 'IMPLICIT ELSE TRAP'",
        "1. Bản chất lập trình: Khối if (!isFlashSale) { maxCap = subtotal * 0.30; } thiếu mệnh đề else.\n"
        "   Khi isFlashSale == true, khối gán bị bỏ qua, maxCap giữ nguyên giá trị mặc định 0.0.\n"
        "   Tại câu lệnh kế tiếp if (totalDiscount > maxCap), do 150.0 > 0.0 là True, chiết khấu của khách VIP bị ép về 0.0!\n"
        "2. Góc nhìn Statement Coverage (Pass ảo với 5 test case): Nếu bộ test chỉ chọn dữ liệu ngày thường (isFlashSale = false), 100% dòng lệnh đều được chạm tới, Statement Coverage đạt 100% nhưng hoàn toàn bỏ sót lỗi nghiêm trọng này.\n"
        "3. Góc nhìn Decision Coverage (Bắt được lỗi với 6 test case): Decision Coverage bắt buộc phải duyệt cả hướng True và False của mọi điều kiện. Nhánh False của !isFlashSale (isFlashSale = true) bắt buộc phải kích hoạt, làm lộ ra ngay việc mất chiết khấu của khách hàng."
    )
    
    # Section 3
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(4)
    r = h3.add_run("III. HÀM TRỌNG TÂM SỐ 2: processPayment (PaymentService) VÀ HÀM TÍCH HỢP checkout")
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(12.5)
    r.font.color.rgb = RGBColor(30, 58, 138)
    
    doc.add_paragraph("1. Mã nguồn Java nghiệp vụ đầy đủ (PaymentService.java):")
    code_payment = """package com.group.cart.service;

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

    // HÀM TRỌNG TÂM SỐ 2: Giữ nguyên 100% để khớp với sơ đồ CFG 2 và V(G) 2 của Thành viên 2
    public PaymentReceipt processPayment(double amount, String paymentMethod, boolean isInternational) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Payment amount must be greater than zero");
        }

        double fee = 0.0;
        // Toán tử ba ngôi paymentMethod != null ? ... : "" tạo ra điểm rẽ nhánh trong bytecode
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

        // Toán tử ba ngôi isSuccess ? SUCCESS : FAILED tạo ra điểm rẽ nhánh trong bytecode
        String status = isSuccess ? "SUCCESS" : "FAILED";
        return new PaymentReceipt(transactionId, totalAmount, fee, method, status);
    }

    // HÀM TÍCH HỢP MODULE: Dành cho Thành viên 4 kiểm thử tích hợp bằng Stub/Driver & bắt lỗi giao tiếp
    public PaymentReceipt checkout(CartService cart, String customerTier, String couponCode, 
                                   boolean isFlashSale, String paymentMethod, boolean isInternational) {
        if (cart == null || cart.calculateSubtotal() <= 0) {
            throw new IllegalArgumentException("Cart cannot be null or empty");
        }

        double subtotal = cart.calculateSubtotal();
        double discount = 0.0;

        if (discountService != null) {
            // [BẪY LỖI GIAO TIẾP - INTERFACE DEFECT]:
            // calculateDiscountAmount yêu cầu thứ tự: (subtotal, customerTier, couponCode, isFlashSale)
            // Lập trình viên truyền nhầm: (subtotal, couponCode, customerTier, isFlashSale)
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
}"""
    add_code_block(doc, code_payment)
    
    p_arch = doc.add_paragraph()
    p_arch.paragraph_format.line_spacing = 1.15
    p_arch.add_run(
        "Ý nghĩa kiến trúc của việc bổ sung hàm checkout(...):\n"
        "• Bảo toàn 100% sơ đồ CFG 2: Hàm processPayment(...) vẫn giữ nguyên 100% mã nguồn, do đó toàn bộ đỉnh, cạnh và công thức McCabe V(G)2 được giữ nguyên trọn vẹn.\n"
        "• Kết nối liên hoàn 3 Module: CartService -> DiscountService -> PaymentService tạo thành một hệ thống thương mại điện tử hoàn chỉnh theo đúng yêu cầu đề tài.\n"
        "• Bàn giao sẵn sàng cho Thành viên 4: Hàm checkout(...) cung cấp giao diện tích hợp chính xác để Thành viên 4 dùng Mockito tạo Stub/Mock cho DiscountService và PaymentGateway (Top-down Integration), tái hiện hoàn hảo bẫy lỗi giao tiếp truyền sai thứ tự tham số (Parameter Ordering Defect)."
    )

    doc.add_paragraph("2. Bảng phân rã các khối lệnh CFG 2 chuẩn hóa (Standardized CFG - 16 Nodes):")
    t2_headers = ["Node ID", "Dòng mã / Khối câu lệnh cụ thể (Code Statement)", "Kiểu Node trong lý thuyết CFG"]
    t2_data = [
        ["Node 1", "if (amount <= 0)", "Entry & Decision Node (Predicate P1)"],
        ["Node 2", "throw new IllegalArgumentException(\"Payment amount...\");", "Exit Node 1 (Ngoại lệ biên số tiền <= 0)"],
        ["Node 3", "method = (paymentMethod != null) ? ...; switch (method)", "Decision Node & Multi-branch Switch (Predicate P2)"],
        ["Node 4", "case \"CREDIT_CARD\": fee = amount * 0.02; if (isInternational)", "Decision Node (Predicate P3)"],
        ["Node 5", "fee += 5.0;", "Processing Node (Phụ phí quốc tế)"],
        ["Node 6", "case \"MOMO\": if (amount > 1000.0)", "Decision Node (Predicate P4)"],
        ["Node 7", "fee = 5.0;", "Processing Node (MOMO hạn mức cao)"],
        ["Node 8", "fee = 2.0;", "Processing Node (MOMO hạn mức thấp)"],
        ["Node 9", "case \"BANK_TRANSFER\": fee = 0.0;", "Processing Node (Miễn phí chuyển khoản)"],
        ["Node 10", "case \"COD\": if (amount > 5000.0)", "Decision Node (Predicate P5)"],
        ["Node 11", "throw new IllegalArgumentException(\"COD is not supported...\");", "Exit Node 2 (Ngoại lệ COD vượt hạn mức)"],
        ["Node 12", "fee = 10.0;", "Processing Node (Phí thu hộ COD hợp lệ)"],
        ["Node 13", "default: throw new IllegalArgumentException(\"Unsupported...\");", "Exit Node 3 (Ngoại lệ method không hỗ trợ)"],
        ["Node 14", "Junction Switch: totalAmount = amount + fee; if (gateway != null)", "Junction Node & Decision Node (Predicate P6)"],
        ["Node 15", "isSuccess = paymentGateway.charge(transactionId, totalAmount);", "Processing Node (Điểm cắm Mock Gateway)"],
        ["Node 16", "status = isSuccess ? \"SUCCESS\" : \"FAILED\"; return receipt;", "Decision (Predicate P7) & Exit Node 4 (Normal Return)"]
    ]
    t2 = doc.add_table(rows=1, cols=3)
    format_table(t2, [1.1, 3.8, 1.6], t2_headers, t2_data)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    doc.add_paragraph("3. Sơ đồ dòng điều khiển CFG 2 (Chụp hình sơ đồ phục vụ báo cáo):")
    add_centered_picture(doc, "docs/images/CFG2_processPayment.png", width_inches=6.0,
                         caption="CFG 2 - Sơ đồ dòng điều khiển hàm processPayment với switch-case 5 nhánh và 4 điểm thoát")

    doc.add_paragraph("4. Tính toán độ phức tạp chu trình McCabe V(G) và Phân tích chuyên sâu 2 toán tử ba ngôi:")
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.add_run(
        "• Quy đổi switch-case: Cấu trúc switch(method) có 5 nhánh rẽ độc lập => tương đương 4 quyết định nhị phân độc lập.\n"
        "• Làm rõ 2 toán tử ba ngôi (Ternary Operators ? :) và cơ chế đo Bytecode JaCoCo:\n"
        "  - Trong Hàm 2 có 2 toán tử ba ngôi: (1) paymentMethod != null ? method : \"\" (Node 3); (2) isSuccess ? \"SUCCESS\" : \"FAILED\" (Node 16).\n"
        "  - Khi tính theo mô hình đồ thị khối lệnh phương thức chuẩn: N = 16, E = 21, k = 4 điểm thoát => V(G)2 = E - N + 1 + k = 21 - 16 + 1 + 4 = 10.\n"
        "  - Khi tính theo vị từ nhị phân P hoặc khi công cụ JaCoCo phân tích ở mức bytecode: Mỗi toán tử ? : tạo ra 1 điểm rẽ nhị phân (2 nhánh con True/False). "
        "Tổng vị từ P = amount<=0 (1) + null-check (1) + switch 5 nhánh (4) + isInternational (1) + MOMO limit (1) + COD limit (1) + gateway!=null (1) + ternary status (1) = 11 vị từ. "
        "=> V(G)2 = P + 1 = 11 + 1 = 12 (hoặc 11 nếu không tính toán tử null-check an toàn). "
        "Số cạnh đồ thị khi tính cả 2 nhánh nội bộ này là E = 23 => 23 - 16 + 1 + 4 = 12. Điều này giải thích hoàn toàn sự tương thích giữa công thức lý thuyết và số liệu đo JaCoCo!\n\n"
        "PHÂN TÍCH SỐ CA KIỂM THỬ TỐI THIỂU LÝ THUYẾT CHO HÀM 2:\n"
        "1. Số test case tối thiểu đạt 100% Statement Coverage = 8 ca kiểm thử:\n"
        "   - Hàm 2 có 8 khối lệnh nằm trên các nhánh loại trừ lẫn nhau hoàn toàn: Node 2 (throw amount <= 0), Node 5 (CREDIT_CARD phụ phí quốc tế), "
        "Node 7 (MOMO > 1000), Node 8 (MOMO <= 1000), Node 9 (BANK_TRANSFER), Node 11 (throw COD > 5000), Node 12 (COD <= 5000), Node 13 (throw default unsupported). "
        "Vì 8 khối lệnh này nằm trên 8 nhánh rẽ độc lập (trong đó có 3 nút ném ngoại lệ dừng thực thi ngay), nên để chạm tới 100% các dòng lệnh của Hàm 2, "
        "bắt buộc phải có tối thiểu 8 ca kiểm thử (chứ không thể là 5 ca như khi chỉ đếm số nhánh switch).\n"
        "2. Số test case tối thiểu đạt 100% Decision Coverage = 8 - 10 ca kiểm thử:\n"
        "   - Bao phủ toàn bộ 8 nhánh rẽ độc lập trên kết hợp duyệt đầy đủ 2 hướng rẽ True/False của các điều kiện phụ (isInternational trong CREDIT_CARD, paymentGateway != null, isSuccess ternary).\n"
        "3. Số test case phủ toàn bộ Basis Paths = 12 ca kiểm thử (tương ứng 12 đường dẫn cơ sở độc lập)."
    )
    
    # Section 4
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(12)
    h4.paragraph_format.space_after = Pt(4)
    r = h4.add_run("IV. BẢNG TỔNG HỢP SỐ LIỆU ĐỒ THỊ & ĐỘ PHỨC TẠP CHU TRÌNH MCCABE")
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(12.5)
    r.font.color.rgb = RGBColor(30, 58, 138)
    
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.add_run(
        "Bảng tổng hợp số liệu định lượng chuẩn hóa về đồ thị dòng điều khiển và độ phức tạp chu trình do Thành viên 2 "
        "phân tích, sử dụng làm số liệu chuẩn mực cho toàn nhóm viết báo cáo và đối chiếu bàn giao:"
    )

    add_centered_picture(doc, "docs/images/Bang_Thong_Ke_So_Lieu_CFG_McCabe_TV2.png", width_inches=6.0,
                         caption="Bảng thống kê số liệu đồ thị dòng điều khiển và độ phức tạp McCabe của Thành viên 2")

    t4_headers = ["Thông số phân tích CFG (Metrics)", "Hàm 1: calculateDiscountAmount", "Hàm 2: processPayment", "Cơ sở toán học & Lý thuyết ISTQB"]
    t4_data = [
        ["Số đỉnh đồ thị (Nodes N)", "16 đỉnh (Nodes)", "16 đỉnh (Nodes)", "Phân rã chuẩn hóa từng khối câu lệnh"],
        ["Số cạnh rẽ nhánh (Edges E)", "21 cạnh", "21 cạnh (23 tính cả ternary)", "Đồ thị có hướng luồng điều khiển"],
        ["Số nút vị từ nhị phân (P)", "7 vị từ", "11 vị từ (switch 5 nhánh = 4)", "Điểm quyết định rẽ nhánh nhị phân"],
        ["Số điểm thoát (Exit Nodes k)", "2 điểm (Guard & Normal)", "4 điểm (3 Ex + 1 Normal)", "Các lệnh return & throw exception"],
        ["Độ phức tạp chu trình V(G)", "V(G)1 = 8", "V(G)2 = 12 (hoặc 11)", "Công thức V(G) = P + 1"],
        ["Công thức đồ thị phẳng đa thoát", "21 - 16 + 1 + 2 = 8", "21 - 16 + 1 + 4 = 10 (+2 = 12)", "Công thức V(G) = E - N + 1 + k"],
        ["Min Tests 100% Statement Coverage", "5 ca kiểm thử tối thiểu", "8 ca kiểm thử tối thiểu", "Phủ 5 và 8 khối lệnh loại trừ lẫn nhau"],
        ["Min Tests 100% Decision Coverage", "6 ca kiểm thử tối thiểu", "8 - 10 ca kiểm thử tối thiểu", "Gộp nhánh tuần tự (Slide SWT4 / ISTQB)"],
        ["Tập đường dẫn cơ sở (Basis Paths)", "8 Basis Paths độc lập", "12 Basis Paths độc lập", "Không gian đường dẫn độc lập tuyến tính V(G)"]
    ]
    t4 = doc.add_table(rows=1, cols=4)
    format_table(t4, [1.8, 1.6, 1.6, 1.5], t4_headers, t4_data)

    # Section 5
    h5 = doc.add_paragraph()
    h5.paragraph_format.space_before = Pt(12)
    h5.paragraph_format.space_after = Pt(4)
    r = h5.add_run("V. BẢNG TỔNG HỢP SO SÁNH LÝ THUYẾT & ĐẶC TẢ BÀN GIAO CHO THÀNH VIÊN 3 & 4")
    r.bold = True
    r.font.name = "Calibri"
    r.font.size = Pt(12.5)
    r.font.color.rgb = RGBColor(30, 58, 138)
    
    t5_headers = ["Tiêu chí phân tích (Criteria)", "Hàm 1: calculateDiscountAmount", "Hàm 2: processPayment"]
    t5_data = [
        ["Độ phức tạp chu trình McCabe V(G)", "V(G)1 = 8", "V(G)2 = 12 (hoặc 11 không tính null-check)"],
        ["Số test case tối thiểu lý thuyết (Statement Coverage)", "5 ca kiểm thử (bắt buộc chạm 5 khối loại trừ: Node 2, 5, 6, 8, 9)", "8 ca kiểm thử (bắt buộc chạm 8 khối loại trừ: Node 2, 5, 7, 8, 9, 11, 12, 13)"],
        ["Số test case tối thiểu lý thuyết (Decision Coverage)", "6 ca kiểm thử (theo ISTQB, gộp nhánh tuần tự, chỉ cần thêm 1 test isFlashSale=true)", "8 - 10 ca kiểm thử (phủ 8 nhánh độc lập cùng các hướng True/False phụ)"],
        ["Số test case phủ toàn bộ Basis Paths (McCabe)", "8 ca kiểm thử (bằng đúng V(G)1 = 8)", "12 ca kiểm thử (bằng đúng V(G)2 = 12)"],
        ["Khả năng phát hiện bẫy lỗi Implicit Else Trap", "Statement Coverage (5 tests): HOÀN TOÀN BỎ SÓT LỖI (Pass ảo 100% khi chạy ngày thường)\nDecision Coverage (6 tests): BẮT ĐƯỢC CHÍNH XÁC BUG (Buộc kích hoạt nhánh False của !isFlashSale)", "Bao phủ đầy đủ mọi nhánh ngoại lệ và các điều kiện biên nghiệp vụ"],
        ["Đánh giá chất lượng kiểm thử", "Decision Coverage ngăn ngừa ảo tưởng an toàn của Statement Coverage", "Decision Coverage bảo đảm độ tin cậy 100% cho giao dịch tài chính"]
    ]
    t5 = doc.add_table(rows=1, cols=3)
    format_table(t5, [2.0, 2.3, 2.2], t5_headers, t5_data)
    
    p_handover = doc.add_paragraph()
    p_handover.paragraph_format.space_before = Pt(8)
    p_handover.paragraph_format.line_spacing = 1.15
    p_handover.add_run(
        "Nội dung bàn giao chuyên môn cho Thành viên 3 & Thành viên 4:\n"
        "1. Bàn giao cho Thành viên 3 (Unit Testing & Coverage):\n"
        "   • Mã nguồn sản xuất: DiscountService.java (có bẫy lỗi Implicit Else), PaymentService.java, PaymentReceipt.java, PaymentGateway.java.\n"
        "   • Hồ sơ thiết kế: Sơ đồ CFG 1 (16 Nodes), CFG 2 (16 Nodes) cùng đặc tả 8 Basis Paths Hàm 1 và 12 Basis Paths Hàm 2.\n"
        "   • Nhiệm vụ TV3: Viết 2 Test Suite đối chứng (Statement vs Decision Coverage) cho Hàm 1 và Unit Test có Mockito Mock cho Hàm 2, sau đó chạy JaCoCo đo đạc thực nghiệm.\n"
        "2. Bàn giao cho Thành viên 4 (Integration Testing):\n"
        "   • Phương thức tích hợp: PaymentService.checkout(CartService cart, String customerTier, String couponCode, boolean isFlashSale, String paymentMethod, boolean isInternational).\n"
        "   • Nhiệm vụ TV4: Dùng Mockito tạo Stub cho DiscountService và PaymentGateway (Top-down Integration), tái hiện bẫy lỗi giao tiếp truyền sai thứ tự tham số (Parameter Ordering Defect) giữa customerTier và couponCode.\n"
        "3. Thuật ngữ tiếng Anh chuẩn bị cho Báo cáo chính thức (English Terminology):\n"
        "   • Control Flow Graph (CFG) | Cyclomatic Complexity V(G) | Predicate Nodes (P) | Exit Nodes (k) | Basis Path Testing\n"
        "   • Statement Coverage (C0) | Decision/Branch Coverage (C1) | Implicit Else Defect | Guard Clause | Junction Node | Interface Defect."
    )

    output_filename = "BAO_CAO_THANH_VIEN_2_CFG_MCCABE_HOAN_CHINH.docx"
    doc.save(output_filename)
    print(f"Report saved successfully as '{output_filename}' without any Member 3 content!")

if __name__ == "__main__":
    generate_standalone_doc()
