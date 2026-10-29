# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ensure output directory exists
os.makedirs("docs/images", exist_ok=True)

# Remove old JaCoCo image if exists
if os.path.exists("docs/images/JaCoCo_So_Lieu_Thuc_Nghiem_TV2.png"):
    os.remove("docs/images/JaCoCo_So_Lieu_Thuc_Nghiem_TV2.png")

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8

def draw_node(ax, x, y, w, h, text, bg_color, border_color, text_color='#1E293B', fontsize=8.5, bold=False):
    box = patches.FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.08,rounding_size=0.15",
        facecolor=bg_color,
        edgecolor=border_color,
        linewidth=1.5,
        zorder=3
    )
    ax.add_patch(box)
    weight = 'bold' if bold else 'normal'
    ax.text(x, y, text, ha='center', va='center', color=text_color, fontsize=fontsize, weight=weight, zorder=4)

def draw_arrow(ax, x1, y1, x2, y2, label=None, label_pos=0.5, label_offset=(0, 0), color='#475569', label_color='#0F172A', rad=0.0):
    connectionstyle = f"arc3,rad={rad}" if rad != 0 else "arc3,rad=0"
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(
            arrowstyle="->,head_width=0.35,head_length=0.45",
            color=color,
            lw=1.6,
            shrinkA=2, shrinkB=2,
            connectionstyle=connectionstyle
        ),
        zorder=2
    )
    if label:
        lx = x1 + (x2 - x1) * label_pos + label_offset[0]
        ly = y1 + (y2 - y1) * label_pos + label_offset[1]
        ax.text(lx, ly, label, ha='center', va='center', color=label_color, fontsize=7.5, weight='bold',
                bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none", alpha=0.9), zorder=5)

def generate_cfg1():
    fig, ax = plt.subplots(figsize=(10, 15), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 17)
    ax.axis('off')

    # Header Box
    header = patches.FancyBboxPatch((0.5, 15.7), 9.0, 1.0, boxstyle="round,pad=0.1",
                                    facecolor="#1E3A8A", edgecolor="#1E3A8A", linewidth=1)
    ax.add_patch(header)
    ax.text(5.0, 16.35, "CFG 1: SƠ ĐỒ DÒNG ĐIỀU KHIỂN - HÀM calculateDiscountAmount()",
            ha='center', va='center', color='white', fontsize=11, weight='bold')
    ax.text(5.0, 15.95, "Số đỉnh N = 16 | Số cạnh E = 21 | Số vị từ P = 7 | McCabe V(G)1 = 8 | 8 Đường dẫn cơ sở",
            ha='center', va='center', color='#BFDBFE', fontsize=8.5)

    # Nodes
    draw_node(ax, 5.0, 14.8, 4.2, 0.65, "Node 1: Entry - if (subtotal <= 0)", "#DBEAFE", "#2563EB", bold=True)
    draw_node(ax, 8.5, 14.8, 2.2, 0.65, "Node 2: return 0.0\n(Exit 1: Guard)", "#FEE2E2", "#DC2626", bold=True)
    draw_node(ax, 5.0, 13.5, 4.2, 0.65, "Node 3: if (\"VIP\".equals(customerTier))", "#DBEAFE", "#2563EB")
    
    draw_node(ax, 2.7, 12.2, 3.2, 0.6, "Node 4: if (subtotal >= 1000)", "#DBEAFE", "#2563EB")
    draw_node(ax, 7.3, 12.2, 3.2, 0.6, "Node 7: if (\"MEMBER\".equals(customerTier))", "#DBEAFE", "#2563EB")

    draw_node(ax, 1.6, 11.0, 2.2, 0.55, "Node 5: rate = 0.15", "#DCFCE7", "#16A34A")
    draw_node(ax, 3.8, 11.0, 2.2, 0.55, "Node 6: rate = 0.10", "#DCFCE7", "#16A34A")
    draw_node(ax, 6.2, 11.0, 2.2, 0.55, "Node 8: rate = 0.05", "#DCFCE7", "#16A34A")
    draw_node(ax, 8.4, 11.0, 2.2, 0.55, "Node 9: rate = 0.00", "#DCFCE7", "#16A34A")

    draw_node(ax, 5.0, 9.6, 5.2, 0.7, "Node 10: Junction 1 - totalDiscount = subtotal * rate\nif (\"SALE50\".equals(couponCode))", "#FEF3C7", "#D97706", bold=True)
    draw_node(ax, 2.2, 8.3, 3.2, 0.6, "Node 11: totalDiscount += 50.0", "#DCFCE7", "#16A34A")

    draw_node(ax, 5.0, 7.0, 5.0, 0.7, "Node 12: Junction 2 - double maxCap = 0.0\nif (!isFlashSale)", "#FEF3C7", "#D97706", bold=True)
    draw_node(ax, 2.2, 5.7, 3.2, 0.6, "Node 13: maxCap = subtotal * 0.30", "#DCFCE7", "#16A34A")

    draw_node(ax, 5.0, 4.4, 5.5, 0.7, "Node 14: Junction 3 [BẪY LỖI IMPLICIT ELSE]\nif (totalDiscount > maxCap)", "#FDE68A", "#B45309", bold=True)
    draw_node(ax, 2.2, 3.1, 3.2, 0.6, "Node 15: totalDiscount = maxCap", "#DCFCE7", "#16A34A")

    draw_node(ax, 5.0, 1.6, 4.5, 0.7, "Node 16: return totalDiscount\n(Exit 2: Normal Return)", "#D1FAE5", "#059669", bold=True)

    # Arrows
    draw_arrow(ax, 7.1, 14.8, 7.4, 14.8, label="True", color="#DC2626")
    draw_arrow(ax, 5.0, 14.47, 5.0, 13.83, label="False")

    draw_arrow(ax, 4.0, 13.18, 3.2, 12.5, label="True", label_pos=0.4, label_offset=(-0.3, 0.1))
    draw_arrow(ax, 6.0, 13.18, 6.8, 12.5, label="False", label_pos=0.4, label_offset=(0.3, 0.1))

    draw_arrow(ax, 2.2, 11.9, 1.8, 11.28, label="True", label_pos=0.4)
    draw_arrow(ax, 3.2, 11.9, 3.6, 11.28, label="False", label_pos=0.4)

    draw_arrow(ax, 6.8, 11.9, 6.4, 11.28, label="True", label_pos=0.4)
    draw_arrow(ax, 7.8, 11.9, 8.2, 11.28, label="False", label_pos=0.4)

    # Converge to Node 10
    draw_arrow(ax, 1.6, 10.72, 3.5, 9.95)
    draw_arrow(ax, 3.8, 10.72, 4.5, 9.95)
    draw_arrow(ax, 6.2, 10.72, 5.5, 9.95)
    draw_arrow(ax, 8.4, 10.72, 6.5, 9.95)

    # Coupon: Node 10 -> Node 11 / Node 12
    draw_arrow(ax, 3.5, 9.25, 2.5, 8.6, label="True", label_pos=0.4, label_offset=(-0.3, 0))
    draw_arrow(ax, 6.5, 9.25, 6.5, 7.35, label="False", rad=-0.3, color="#2563EB", label_pos=0.5, label_offset=(0.4, 0))
    draw_arrow(ax, 2.5, 8.0, 3.8, 7.35)

    # FlashSale: Node 12 -> Node 13 / Node 14 (Implicit Else Trap)
    draw_arrow(ax, 3.5, 6.65, 2.5, 6.0, label="True (!FlashSale)", label_pos=0.4, label_offset=(-0.6, 0))
    draw_arrow(ax, 6.5, 6.65, 6.5, 4.75, label="False (isFlashSale - IMPLICIT ELSE)", rad=-0.4, color="#DC2626", label_pos=0.5, label_offset=(1.5, 0))
    draw_arrow(ax, 2.5, 5.4, 3.8, 4.75)

    # Exceed MaxCap: Node 14 -> Node 15 / Node 16
    draw_arrow(ax, 3.5, 4.05, 2.5, 3.4, label="True (> maxCap)", label_pos=0.4, label_offset=(-0.6, 0))
    draw_arrow(ax, 6.5, 4.05, 6.5, 1.95, label="False", rad=-0.35, color="#2563EB", label_pos=0.5, label_offset=(0.4, 0))
    draw_arrow(ax, 2.5, 2.8, 4.0, 1.95)

    # Callout Box for Implicit Else
    callout = patches.FancyBboxPatch((0.5, 0.2), 9.0, 0.85, boxstyle="round,pad=0.08",
                                     facecolor="#FEF3C7", edgecolor="#D97706", linewidth=1.2)
    ax.add_patch(callout)
    ax.text(5.0, 0.65, "[!] BẪY LỖI IMPLICIT ELSE: Khi isFlashSale == true, nhánh False bỏ qua Node 13, maxCap = 0.0.",
            ha='center', va='center', color='#92400E', fontsize=8.2, weight='bold')
    ax.text(5.0, 0.38, "Statement Coverage bỏ sót vì chỉ chạy ngày thường. Decision Coverage bắt buộc kích hoạt nhánh ngầm định!",
            ha='center', va='center', color='#78350F', fontsize=7.8)

    plt.tight_layout()
    output_path = "docs/images/CFG1_calculateDiscountAmount.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"CFG 1 saved successfully as '{output_path}'")

def generate_cfg2():
    fig, ax = plt.subplots(figsize=(12, 14), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # Header Box
    header = patches.FancyBboxPatch((0.5, 14.8), 11.0, 0.95, boxstyle="round,pad=0.1",
                                    facecolor="#1E3A8A", edgecolor="#1E3A8A", linewidth=1)
    ax.add_patch(header)
    ax.text(6.0, 15.45, "CFG 2: SƠ ĐỒ DÒNG ĐIỀU KHIỂN - HÀM processPayment()",
            ha='center', va='center', color='white', fontsize=11.5, weight='bold')
    ax.text(6.0, 15.05, "Số đỉnh N = 16 | Số cạnh E = 21 | Số vị từ P = 11 | McCabe V(G)2 = 12 | 12 Đường dẫn cơ sở",
            ha='center', va='center', color='#BFDBFE', fontsize=8.5)

    # Entry and Guard Exit
    draw_node(ax, 5.0, 13.9, 4.2, 0.6, "Node 1: Entry - if (amount <= 0)", "#DBEAFE", "#2563EB", bold=True)
    draw_node(ax, 9.8, 13.9, 3.2, 0.6, "Node 2: throw Exception\n(Exit 1: Invalid Amount)", "#FEE2E2", "#DC2626", bold=True)
    draw_arrow(ax, 7.1, 13.9, 8.2, 13.9, label="True", color="#DC2626")

    # Switch
    draw_node(ax, 5.0, 12.6, 5.0, 0.6, "Node 3: method = ... ; switch (method)", "#DBEAFE", "#2563EB", bold=True)
    draw_arrow(ax, 5.0, 13.6, 5.0, 12.9, label="False")

    # 5 Branches of Switch
    # Branch 1: CREDIT_CARD
    draw_node(ax, 1.4, 11.0, 2.2, 0.6, "Node 4: CREDIT_CARD\nif (isInternational)", "#DBEAFE", "#2563EB")
    draw_node(ax, 1.4, 9.5, 2.0, 0.55, "Node 5: fee += 5.0", "#DCFCE7", "#16A34A")
    draw_arrow(ax, 3.5, 12.3, 1.8, 11.3, label="CREDIT_CARD", label_pos=0.6, label_offset=(-0.4, 0))
    draw_arrow(ax, 1.4, 10.7, 1.4, 9.78, label="True")

    # Branch 2: MOMO
    draw_node(ax, 3.9, 11.0, 2.2, 0.6, "Node 6: MOMO\nif (amount > 1000)", "#DBEAFE", "#2563EB")
    draw_node(ax, 3.0, 9.5, 1.6, 0.55, "Node 7:\nfee = 5.0", "#DCFCE7", "#16A34A")
    draw_node(ax, 4.8, 9.5, 1.6, 0.55, "Node 8:\nfee = 2.0", "#DCFCE7", "#16A34A")
    draw_arrow(ax, 4.2, 12.3, 3.9, 11.3, label="MOMO")
    draw_arrow(ax, 3.4, 10.7, 3.0, 9.78, label="True")
    draw_arrow(ax, 4.4, 10.7, 4.8, 9.78, label="False")

    # Branch 3: BANK_TRANSFER
    draw_node(ax, 6.5, 11.0, 2.2, 0.6, "Node 9:\nBANK_TRANSFER\nfee = 0.0", "#DCFCE7", "#16A34A")
    draw_arrow(ax, 5.6, 12.3, 6.5, 11.3, label="BANK_TRANSFER")

    # Branch 4: COD
    draw_node(ax, 9.0, 11.0, 2.2, 0.6, "Node 10: COD\nif (amount > 5000)", "#DBEAFE", "#2563EB")
    draw_node(ax, 8.2, 9.5, 2.0, 0.55, "Node 11: throw Ex\n(Exit 2: COD limit)", "#FEE2E2", "#DC2626", bold=True)
    draw_node(ax, 10.2, 9.5, 1.6, 0.55, "Node 12:\nfee = 10.0", "#DCFCE7", "#16A34A")
    draw_arrow(ax, 6.8, 12.3, 8.8, 11.3, label="COD")
    draw_arrow(ax, 8.6, 10.7, 8.2, 9.78, label="True", color="#DC2626")
    draw_arrow(ax, 9.4, 10.7, 10.0, 9.78, label="False")

    # Branch 5: default
    draw_node(ax, 11.0, 11.0, 1.6, 0.6, "Node 13:\ndefault\n(Exit 3)", "#FEE2E2", "#DC2626", bold=True)
    draw_arrow(ax, 7.5, 12.5, 10.6, 11.3, label="default", color="#DC2626")

    # Junction Switch: Node 14
    draw_node(ax, 5.0, 7.8, 6.0, 0.7, "Node 14: Junction Switch - totalAmount = amount + fee\nif (paymentGateway != null)", "#FEF3C7", "#D97706", bold=True)
    
    # Connect cases to Node 14
    draw_arrow(ax, 1.4, 9.22, 3.5, 8.15)
    draw_arrow(ax, 2.2, 10.7, 3.0, 8.15, rad=0.2, label="False")
    draw_arrow(ax, 3.0, 9.22, 4.2, 8.15)
    draw_arrow(ax, 4.8, 9.22, 4.8, 8.15)
    draw_arrow(ax, 6.5, 10.7, 5.8, 8.15)
    draw_arrow(ax, 10.2, 9.22, 6.8, 8.15)

    # Mock gateway: Node 15
    draw_node(ax, 2.5, 6.3, 3.5, 0.6, "Node 15: isSuccess = gateway.charge(...)", "#EDE9FE", "#7C3AED")
    draw_arrow(ax, 4.0, 7.45, 3.0, 6.6, label="True", label_pos=0.4)

    # Node 16: Return Receipt
    draw_node(ax, 5.0, 4.8, 6.0, 0.7, "Node 16: status = isSuccess ? SUCCESS : FAILED\nreturn new PaymentReceipt(...) (Exit 4: Normal)", "#D1FAE5", "#059669", bold=True)
    draw_arrow(ax, 2.5, 6.0, 4.0, 5.15)
    draw_arrow(ax, 6.5, 7.45, 6.5, 5.15, label="False (Standalone)", rad=-0.3, label_pos=0.5, label_offset=(0.8, 0))

    # Notes Box
    notes = patches.FancyBboxPatch((0.5, 2.2), 11.0, 1.8, boxstyle="round,pad=0.08",
                                  facecolor="#F8FAFC", edgecolor="#CBD5E1", linewidth=1.2)
    ax.add_patch(notes)
    ax.text(6.0, 3.65, "TỔNG HỢP CÁC ĐIỂM QUYẾT ĐỊNH VÀ ĐIỂM THOÁT TRONG CFG 2:",
            ha='center', va='center', color='#1E3A8A', fontsize=9.0, weight='bold')
    ax.text(6.0, 3.25, "1. Số điểm vị từ P = 11: amount<=0 (1) + null-check (1) + switch 5 nhánh (4) + isInternational (1) + MOMO>1000 (1) + COD>5000 (1) + gateway!=null (1) + status ternary (1)",
            ha='center', va='center', color='#334155', fontsize=8.0)
    ax.text(6.0, 2.85, "2. Số điểm thoát k = 4: Exit 1 (Node 2: Số tiền <= 0), Exit 2 (Node 11: COD > 5000), Exit 3 (Node 13: Unsupported), Exit 4 (Node 16: Normal Return).",
            ha='center', va='center', color='#334155', fontsize=8.0)
    ax.text(6.0, 2.45, "3. Công thức McCabe: V(G)2 = P + 1 = 11 + 1 = 12 | Đồ thị phẳng k điểm thoát: V(G)2 = E - N + 1 + k = 21 - 16 + 1 + 4 = 10 (chưa cộng 2 nhánh ternary).",
            ha='center', va='center', color='#334155', fontsize=8.0)

    plt.tight_layout()
    output_path = "docs/images/CFG2_processPayment.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"CFG 2 saved successfully as '{output_path}'")

def generate_metrics_summary_table_image():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Title Card
    card = patches.FancyBboxPatch((0.5, 0.4), 10.0, 7.2, boxstyle="round,pad=0.15",
                                 facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.5)
    ax.add_patch(card)

    header = patches.FancyBboxPatch((0.7, 6.5), 9.6, 0.9, boxstyle="round,pad=0.08",
                                    facecolor="#1E3A8A", edgecolor="#1E3A8A")
    ax.add_patch(header)
    ax.text(5.5, 7.05, "BẢNG TỔNG HỢP SỐ LIỆU ĐỒ THỊ DÒNG ĐIỀU KHIỂN & ĐỘ PHỨC TẠP CHU TRÌNH MCCABE",
            ha='center', va='center', color='white', fontsize=10.5, weight='bold')
    ax.text(5.5, 6.70, "Phạm vi phân tích thiết kế của THÀNH VIÊN 2 (Phục vụ báo cáo chuyên môn)",
            ha='center', va='center', color='#93C5FD', fontsize=8.5)

    # Method 1 Card
    m1_box = patches.FancyBboxPatch((0.8, 3.6), 4.6, 2.6, boxstyle="round,pad=0.1",
                                    facecolor="#F0FDF4", edgecolor="#86EFAC", linewidth=1.2)
    ax.add_patch(m1_box)
    ax.text(3.1, 5.9, "HÀM 1: calculateDiscountAmount()", ha='center', va='center', color='#166534', fontsize=9.5, weight='bold')
    
    m1_text = (
        "• Số đỉnh đồ thị (Nodes N): 16 đỉnh chuẩn hóa\n"
        "• Số cạnh rẽ nhánh (Edges E): 21 cạnh\n"
        "• Số nút vị từ rẽ nhánh (P): 7 vị từ nhị phân\n"
        "• Số điểm thoát (Exit Nodes k): 2 điểm (Guard & Normal)\n"
        "• Độ phức tạp chu trình McCabe V(G)1: 8\n"
        "• Min Tests Statement Coverage: 5 ca (5 khối loại trừ)\n"
        "• Min Tests Decision: 6 ca | Basis Paths V(G): 8 đường"
    )
    ax.text(1.0, 4.65, m1_text, ha='left', va='center', color='#14532D', fontsize=8.0, linespacing=1.35)

    # Method 2 Card
    m2_box = patches.FancyBboxPatch((5.6, 3.6), 4.6, 2.6, boxstyle="round,pad=0.1",
                                    facecolor="#EFF6FF", edgecolor="#93C5FD", linewidth=1.2)
    ax.add_patch(m2_box)
    ax.text(7.9, 5.9, "HÀM 2: processPayment()", ha='center', va='center', color='#1E40AF', fontsize=9.5, weight='bold')
    
    m2_text = (
        "• Số đỉnh đồ thị (Nodes N): 16 đỉnh chuẩn hóa\n"
        "• Số cạnh rẽ nhánh (Edges E): 21 cạnh\n"
        "• Số nút vị từ (P): 11 vị từ (switch 5 nhánh + 2 ternary)\n"
        "• Số điểm thoát (Exit Nodes k): 4 điểm (3 Ex + 1 Normal)\n"
        "• Độ phức tạp chu trình McCabe V(G)2: 12 (hoặc 11)\n"
        "• Min Tests Statement Coverage: 8 ca (8 khối loại trừ)\n"
        "• Min Tests Decision: 8-10 ca | Basis Paths V(G): 12 đường"
    )
    ax.text(5.8, 4.65, m2_text, ha='left', va='center', color='#1E3A8A', fontsize=8.0, linespacing=1.35)

    # Summary Table Banner
    banner = patches.FancyBboxPatch((0.8, 0.7), 9.4, 2.6, boxstyle="round,pad=0.1",
                                    facecolor="#F8FAFC", edgecolor="#E2E8F0", linewidth=1.2)
    ax.add_patch(banner)
    ax.text(5.5, 3.05, "ĐỐI CHIẾU THÔNG SỐ TOÁN HỌC ĐỒ THỊ TRONG PHẠM VI THÀNH VIÊN 2",
            ha='center', va='center', color='#0F172A', fontsize=9.0, weight='bold')

    headers = ["Thông số phân tích CFG", "Hàm 1 (DiscountService)", "Hàm 2 (PaymentService)", "Cơ sở lý thuyết / Công thức"]
    rows = [
        ["Độ phức tạp chu trình V(G)", "P = 7 => V(G)1 = 8", "P = 11 => V(G)2 = 12", "V(G) = P + 1 (hoặc E - N + 1 + k)"],
        ["Min Tests Statement Coverage", "5 ca kiểm thử tối thiểu", "8 ca kiểm thử tối thiểu", "Khối rẽ nhánh loại trừ lẫn nhau"],
        ["Min Tests Decision Coverage", "6 ca kiểm thử tối thiểu", "8 - 10 ca kiểm thử tối thiểu", "Gộp nhánh tuần tự (Slide SWT4 / ISTQB)"],
        ["Tập đường dẫn cơ sở (Basis Paths)", "8 Basis Paths độc lập", "12 Basis Paths độc lập", "Số đường độc lập tuyến tính bằng V(G)"]
    ]

    col_x = [1.0, 3.8, 6.6, 9.0]
    y_pos = 2.6
    for i, h in enumerate(headers):
        ax.text(col_x[i], y_pos, h, ha='left', va='center', color='#334155', fontsize=8.0, weight='bold')

    y_pos -= 0.35
    for r in rows:
        for i, val in enumerate(r):
            color = '#1E3A8A' if ('V(G)' in val or 'Coverage' in val) else '#475569'
            ax.text(col_x[i], y_pos, val, ha='left', va='center', color=color, fontsize=7.6)
        y_pos -= 0.30

    plt.tight_layout()
    output_path = "docs/images/Bang_Thong_Ke_So_Lieu_CFG_McCabe_TV2.png"
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Metrics summary table image saved as '{output_path}'")

if __name__ == "__main__":
    generate_cfg1()
    generate_cfg2()
    generate_metrics_summary_table_image()
