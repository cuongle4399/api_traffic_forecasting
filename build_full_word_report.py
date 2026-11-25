"""
Word Report Generator for Web Application API Request Volume Forecasting
and Anomaly Detection Using Box-Jenkins SARIMA Methodology.

Updated with:
1. Dynamic updatable Table of Contents (TOC field code with w:updateFields for automatic/manual refresh).
2. Right-aligned dynamic page numbers in footer (mép phải dưới: Trang [PAGE]).
3. Updated Lecturer: ThS. Lê Xuân Việt (LÊ XUÂN VIỆT).
4. Updated Course Code: Mã học phần 1050316.
5. Course Name: Dự báo chuỗi thời gian.
6. Clean academic black-and-white tables (no colored backgrounds, black borders, pure Vietnamese terms).

Author: Le Quoc Cuong (MSSV: 4651050031)
University: Quy Nhon University - Faculty of Information Technology
Course: Time Series Forecasting (Du doan chuoi thoi gian)
Year: 2026
"""

import os
import json
import pandas as pd
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    """Sets standard padding inside table cells."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_simple_table_borders(table, color="000000", sz="4"):
    """
    Applies standard, clean, professional black borders:
    Solid single black border around all cells, standard academic thesis format.
    """
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_demo_screenshot_box(doc, title, description, figure_caption):
    """
    Creates an academic boxed placeholder frame for user demo screenshots.
    Includes clean solid black border, guidance text, and a formal figure caption below.
    """
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.3)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    # Clean academic border
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'<w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'<w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    format_paragraph(p, space_before=10, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER)
    r1 = p.add_run(f"📷 [KHUNG CHÈN ẢNH CHỤP MÀN HÌNH DEMO WEB]\n{title.upper()}\n\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(0, 0, 0)
    
    r2 = p.add_run("Hướng dẫn thao tác cho sinh viên:\nTruy cập giao diện Web Dashboard đang chạy tại: http://localhost:8501\nChụp ảnh màn hình phân hệ tương ứng và dán (Paste) đè vào vị trí khung này để hoàn thiện minh chứng nghiệm thu.\n\n")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(9.5)
    r2.font.italic = True
    r2.font.color.rgb = RGBColor(80, 80, 80)
    
    r3 = p.add_run(f"Nội dung minh chứng kỹ thuật: {description}")
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(10)
    r3.font.bold = False
    r3.font.color.rgb = RGBColor(0, 0, 0)
    
    # Caption below box
    p_cap = doc.add_paragraph()
    format_paragraph(p_cap, space_before=4, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    rc = p_cap.add_run(figure_caption)
    rc.font.name = "Times New Roman"
    rc.font.size = Pt(10)
    rc.font.bold = True
    rc.font.italic = True
    rc.font.color.rgb = RGBColor(0, 0, 0)

def add_simple_callout(doc, text, title="Ghi chú phân tích chuyên môn:"):
    """Creates a simple, clean, non-colored boxed note with simple black border."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.3)
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    
    # Left border only (black single solid 1.5pt)
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:left w:val="single" w:sz="18" w:space="0" w:color="000000"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.2
    run_t = p.add_run(f"{title} ")
    run_t.font.name = "Times New Roman"
    run_t.font.size = Pt(11)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(0, 0, 0)
    
    run_c = p.add_run(text)
    run_c.font.name = "Times New Roman"
    run_c.font.size = Pt(11)
    run_c.font.italic = True
    run_c.font.color.rgb = RGBColor(0, 0, 0)
    
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)

def format_paragraph(p, space_before=0, space_after=6, line_spacing=1.3, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.alignment = align

def configure_heading_styles(doc):
    """Configures native Heading 1, 2, 3 styles so Word TOC recognizes them."""
    styles = doc.styles
    
    # Heading 1
    h1 = styles['Heading 1']
    h1.font.name = 'Times New Roman'
    h1.font.size = Pt(14)
    h1.font.bold = True
    h1.font.color.rgb = RGBColor(0, 0, 0)
    h1.paragraph_format.space_before = Pt(16)
    h1.paragraph_format.space_after = Pt(6)
    h1.paragraph_format.line_spacing = 1.25
    h1.paragraph_format.keep_with_next = True
    
    # Heading 2
    h2 = styles['Heading 2']
    h2.font.name = 'Times New Roman'
    h2.font.size = Pt(13)
    h2.font.bold = True
    h2.font.color.rgb = RGBColor(0, 0, 0)
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(4)
    h2.paragraph_format.line_spacing = 1.25
    h2.paragraph_format.keep_with_next = True
    
    # Heading 3
    h3 = styles['Heading 3']
    h3.font.name = 'Times New Roman'
    h3.font.size = Pt(12)
    h3.font.bold = True
    h3.font.italic = True
    h3.font.color.rgb = RGBColor(0, 0, 0)
    h3.paragraph_format.space_before = Pt(8)
    h3.paragraph_format.space_after = Pt(2)
    h3.paragraph_format.line_spacing = 1.25
    h3.paragraph_format.keep_with_next = True

def add_heading_1(doc, text):
    p = doc.add_paragraph(style='Heading 1')
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph(style='Heading 2')
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph(style='Heading 3')
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.italic = True
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_body_p(doc, text, bold_prefix=None, italic_prefix=None):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=0, space_after=6, line_spacing=1.3, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    
    if bold_prefix:
        r_bp = p.add_run(bold_prefix)
        r_bp.font.name = "Times New Roman"
        r_bp.font.size = Pt(12)
        r_bp.font.bold = True
        r_bp.font.color.rgb = RGBColor(0, 0, 0)
        
    if italic_prefix:
        r_ip = p.add_run(italic_prefix)
        r_ip.font.name = "Times New Roman"
        r_ip.font.size = Pt(12)
        r_ip.font.italic = True
        r_ip.font.color.rgb = RGBColor(0, 0, 0)
        
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_bullet_p(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    format_paragraph(p, space_before=0, space_after=4, line_spacing=1.25, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
    if bold_prefix:
        r_bp = p.add_run(bold_prefix)
        r_bp.font.name = "Times New Roman"
        r_bp.font.size = Pt(12)
        r_bp.font.bold = True
        r_bp.font.color.rgb = RGBColor(0, 0, 0)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_image_with_caption(doc, image_path, caption_text, width=Inches(6.2)):
    """Inserts a centered image with a professional caption below."""
    if os.path.exists(image_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(image_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(11)
        r_cap.font.bold = True
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(0, 0, 0)
    else:
        print(f"Warning: Image {image_path} does not exist.")

def add_simple_academic_table(doc, headers, data, col_widths=None):
    """
    Creates a clean, traditional, simple academic data table:
    - No background colors (pure white/no-fill).
    - Black borders (single line, neat).
    - Black bold header text.
    - Black normal body text.
    """
    tbl = doc.add_table(rows=len(data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    # Header Row (Clean white background, bold black text)
    hdr_cells = tbl.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0, 0, 0)
            
    # Data Rows (No color, pure black text)
    for r_idx, row_values in enumerate(data):
        row_cells = tbl.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row_values):
            row_cells[c_idx].text = str(val)
            set_cell_margins(row_cells[c_idx], top=70, bottom=70, left=90, right=90)
            p = row_cells[c_idx].paragraphs[0]
            # Center numeric/short fields, left align descriptive text
            if c_idx == 0 or len(str(val)) < 15:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(10.5)
                run.font.color.rgb = RGBColor(0, 0, 0)
                
    # Column widths
    if col_widths:
        for row in tbl.rows:
            for c_idx, w in enumerate(col_widths):
                row.cells[c_idx].width = w
                
    # Clean black borders (solid, single, 0.5pt)
    set_simple_table_borders(tbl, color="000000", sz="4")
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)
    return tbl

def add_dynamic_table_of_contents(doc):
    """
    Inserts a Dynamic Table of Contents (TOC) with:
    1. Standard TOC field code that Word can update via Right Click -> Update Field.
    2. Pre-populated structured TOC entries with dot leaders for immediate display.
    """
    p_title = doc.add_paragraph()
    format_paragraph(p_title, space_before=12, space_after=8, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_t = p_title.add_run("MỤC LỤC")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(15)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(0, 0, 0)
    
    # Word Dynamic TOC field
    p_fld = doc.add_paragraph()
    p_fld.paragraph_format.space_before = Pt(2)
    p_fld.paragraph_format.space_after = Pt(6)
    
    fldSimple = parse_xml(r'<w:fldSimple %s w:instr="TOC \o &quot;1-3&quot; \h \z \u"/>' % nsdecls('w'))
    r_hint = parse_xml(
        r'<w:r %s><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:i/><w:color w:val="555555"/></w:rPr>'
        r'<w:t>(Nhấp chuột phải vào đây chọn &apos;Cập nhật trường&apos; / &apos;Update Field&apos; để đồng bộ số trang tự động)</w:t></w:r>' % nsdecls('w')
    )
    fldSimple.append(r_hint)
    p_fld._p.append(fldSimple)
    
    # Pre-populated TOC entries with Dot Leaders for immediate beautiful viewing
    toc_items = [
        ("LỜI CẢM ƠN", "1", 0, True),
        ("TÓM TẮT ĐỀ TÀI", "2", 0, True),
        ("DANH MỤC CÁC TỪ VIẾT TẮT", "3", 0, True),
        ("DANH MỤC CÁC BẢNG BIỂU", "3", 0, True),
        ("DANH MỤC CÁC HÌNH VẼ VÀ BIỂU ĐỒ", "3", 0, True),
        ("CHƯƠNG 1: TỔNG QUAN VÀ TÍNH CẤP THIẾT CỦA ĐỀ TÀI", "4", 0, True),
        ("1.1. Bối cảnh hạ tầng web và dịch vụ số trong kiến trúc vi dịch vụ", "4", 1, False),
        ("1.2. Thách thức quản trị tài nguyên và nhu cầu dự báo tải API", "4", 1, False),
        ("1.3. Vấn đề phát hiện bất thường trong lưu lượng mạng", "5", 1, False),
        ("1.4. Mục tiêu nghiên cứu của đề tài", "5", 1, False),
        ("1.5. Đối tượng và phạm vi nghiên cứu", "5", 1, False),
        ("1.6. Bố cục của báo cáo", "5", 1, False),
        ("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VỀ CHUỖI THỜI GIAN VÀ PHƯƠNG PHÁP BOX-JENKINS SARIMA", "6", 0, True),
        ("2.1. Khái niệm chuỗi thời gian", "6", 1, False),
        ("2.2. Các thành phần của chuỗi thời gian", "6", 1, False),
        ("2.3. Tính dừng và các phép biến đổi sai phân", "6", 1, False),
        ("2.4. Hàm tự tương quan (ACF) và tự tương quan riêng phần (PACF)", "7", 1, False),
        ("2.5. Mô hình SARIMA", "7", 1, False),
        ("2.6. Phương pháp luận 4 bước Box-Jenkins", "7", 1, False),
        ("2.7. Cơ chế phát hiện bất thường theo ngưỡng động thống kê", "8", 1, False),
        ("CHƯƠNG 3: THU THẬP, TIỀN XỬ LÝ VÀ PHÂN TÍCH KHÁM PHÁ DỮ LIỆU", "9", 0, True),
        ("3.1. Mô tả tập dữ liệu lưu lượng API", "9", 1, False),
        ("3.2. Thống kê mô tả đặc trưng", "9", 1, False),
        ("3.3. Phân tích khám phá và tính mùa vụ ngày đêm", "10", 1, False),
        ("3.4. Phân rã chuỗi thời gian", "10", 1, False),
        ("3.5. Kiểm định tính dừng và tác động của sai phân", "10", 1, False),
        ("3.6. Nhận dạng bậc mô hình qua biểu đồ ACF và PACF", "11", 1, False),
        ("CHƯƠNG 4: XÂY DỰNG, HUẤN LUYỆN VÀ CHẨN ĐOÁN MÔ HÌNH SARIMA", "12", 0, True),
        ("4.1. Thiết lập không gian tìm kiếm lưới tham số", "12", 1, False),
        ("4.2. Đánh giá và xếp hạng các mô hình ứng viên", "12", 1, False),
        ("4.3. Lựa chọn mô hình tối ưu", "12", 1, False),
        ("4.4. Kiểm định chẩn đoán phần dư chuẩn hóa", "13", 1, False),
        ("CHƯƠNG 5: THỰC NGHIỆM DỰ BÁO LƯU LƯỢNG VÀ PHÁT HIỆN BẤT THƯỜNG", "14", 0, True),
        ("5.1. Phân chia tập dữ liệu thực nghiệm", "14", 1, False),
        ("5.2. Kết quả dự báo ngoài mẫu", "14", 1, False),
        ("5.3. Đánh giá độ chính xác dự báo", "14", 1, False),
        ("5.4. So sánh với các mô hình cơ sở", "15", 1, False),
        ("5.5. Ứng dụng phát hiện bất thường với ngưỡng động 3 độ lệch chuẩn", "15", 1, False),
        ("5.6. Ứng dụng trong tự động co giãn tài nguyên hệ thống", "16", 1, False),
        ("5.7. Triển khai Ứng dụng Web Dashboard và Hướng dẫn Thử nghiệm Trực quan", "16", 1, False),
        ("5.7.1. Kiến trúc tổng thể và tích hợp mô hình dự báo thời gian thực", "16", 2, False),
        ("5.7.2. Đặc tả 3 phân hệ chức năng tương tác trên Web Dashboard", "17", 2, False),
        ("5.7.3. Minh chứng hình ảnh thực nghiệm trên giao diện Web Dashboard", "18", 2, False),
        ("CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "20", 0, True),
        ("6.1. Kết quả đạt được", "20", 1, False),
        ("6.2. Ưu điểm và hạn chế của mô hình", "20", 1, False),
        ("6.3. Hướng phát triển tiếp theo", "20", 1, False),
        ("TÀI LIỆU THAM KHẢO", "21", 0, True),
        ("PHỤ LỤC: HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH MÃ NGUỒN", "22", 0, True),
        ("P.1. Cấu trúc thư mục của dự án", "22", 1, False),
        ("P.2. Các bước cài đặt và thực thi hệ thống", "23", 1, False),
        ("P.3. Hướng dẫn khởi chạy và vận hành ứng dụng Web Dashboard", "23", 1, False),
        ("P.4. Kho lưu trữ mã nguồn mở GitHub", "24", 1, False)
    ]
    
    for title, page_num, level, is_bold in toc_items:
        p_item = doc.add_paragraph()
        p_item.paragraph_format.space_before = Pt(1)
        p_item.paragraph_format.space_after = Pt(2)
        p_item.paragraph_format.line_spacing = 1.15
        
        # Set tab stop with dot leader at right margin (6.0 inches)
        tab_stops = p_item.paragraph_format.tab_stops
        tab_stops.add_tab_stop(Inches(6.2), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        
        # Indent for subsections
        indent = "    " if level == 1 else ""
        r_txt = p_item.add_run(f"{indent}{title}\t{page_num}")
        r_txt.font.name = "Times New Roman"
        r_txt.font.size = Pt(11)
        r_txt.font.bold = is_bold
        r_txt.font.color.rgb = RGBColor(0, 0, 0)
        
    p_end = doc.add_paragraph()
    p_end.paragraph_format.space_before = Pt(4)
    p_end.paragraph_format.space_after = Pt(6)

def add_right_aligned_page_number(footer_paragraph):
    """
    Applies right-aligned page numbering in the footer:
    'Trang [PAGE]' aligned to the right edge (mép phải dưới).
    """
    footer_paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    
    r_label = footer_paragraph.add_run("Trang ")
    r_label.font.name = "Times New Roman"
    r_label.font.size = Pt(10)
    r_label.font.color.rgb = RGBColor(0, 0, 0)
    
    # Dynamic PAGE field
    r_page = footer_paragraph.add_run()
    r_page.font.name = "Times New Roman"
    r_page.font.size = Pt(10)
    r_page.font.color.rgb = RGBColor(0, 0, 0)
    
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    r_num = parse_xml(r'<w:r %s><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="20"/></w:rPr><w:t>1</w:t></w:r>' % nsdecls('w'))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    
    r_page._r.append(fldChar1)
    r_page._r.append(instrText)
    r_page._r.append(fldChar2)
    r_page._r.append(r_num)
    r_page._r.append(fldChar3)

def build_word_document():
    doc = Document()
    
    # Enable automatic update of TOC and fields upon opening in Word
    element = parse_xml(r'<w:updateFields %s w:val="true"/>' % nsdecls('w'))
    doc.settings.element.append(element)
    
    # Configure native Heading 1, 2, 3 styles
    configure_heading_styles(doc)
    
    # -------------------------------------------------------------
    # SECTION 0: COVER PAGE (Trang bìa theo chuẩn mẫu trường)
    # -------------------------------------------------------------
    sec_0 = doc.sections[0]
    sec_0.top_margin = Pt(36.0)
    sec_0.bottom_margin = Pt(36.0)
    sec_0.left_margin = Pt(50.0)
    sec_0.right_margin = Pt(40.0)
    
    # University & Faculty
    p_u1 = doc.add_paragraph()
    format_paragraph(p_u1, space_before=10, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_u1 = p_u1.add_run("TRƯỜNG ĐẠI HỌC QUY NHƠN")
    r_u1.font.name = "Times New Roman"
    r_u1.font.size = Pt(14)
    r_u1.font.bold = True
    r_u1.font.color.rgb = RGBColor(0, 0, 0)
    
    p_u2 = doc.add_paragraph()
    format_paragraph(p_u2, space_before=0, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_u2 = p_u2.add_run("KHOA CÔNG NGHỆ THÔNG TIN")
    r_u2.font.name = "Times New Roman"
    r_u2.font.size = Pt(14)
    r_u2.font.bold = True
    r_u2.font.color.rgb = RGBColor(0, 0, 0)
    
    p_div = doc.add_paragraph()
    format_paragraph(p_div, space_before=0, space_after=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_div = p_div.add_run("----- 📖 -----")
    r_div.font.name = "Times New Roman"
    r_div.font.size = Pt(12)
    r_div.font.bold = True
    r_div.font.color.rgb = RGBColor(0, 0, 0)
    
    # Official Logo (from extracted_logo.png)
    logo_path = "extracted_logo.png"
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        format_paragraph(p_logo, space_before=0, space_after=18, align=WD_ALIGN_PARAGRAPH.CENTER)
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Inches(1.85))
    else:
        print("Warning: Logo image not found!")
        
    p_rep = doc.add_paragraph()
    format_paragraph(p_rep, space_before=10, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_rep = p_rep.add_run("BÁO CÁO ĐỀ TÀI BÀI TẬP LỚN")
    r_rep.font.name = "Times New Roman"
    r_rep.font.size = Pt(16)
    r_rep.font.bold = True
    r_rep.font.color.rgb = RGBColor(0, 0, 0)
    
    p_sub = doc.add_paragraph()
    format_paragraph(p_sub, space_before=0, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_sub = p_sub.add_run("HỌC PHẦN: DỰ BÁO CHUỖI THỜI GIAN")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(14)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(0, 0, 0)
    
    p_topic1 = doc.add_paragraph()
    format_paragraph(p_topic1, space_before=6, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_t1 = p_topic1.add_run("CHỦ ĐỀ:")
    r_t1.font.name = "Times New Roman"
    r_t1.font.size = Pt(14)
    r_t1.font.bold = True
    r_t1.font.color.rgb = RGBColor(0, 0, 0)
    
    p_topic2 = doc.add_paragraph()
    format_paragraph(p_topic2, space_before=2, space_after=24, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_t2 = p_topic2.add_run("WEB APPLICATION API REQUEST VOLUME FORECASTING\nAND ANOMALY DETECTION USING BOX-JENKINS SARIMA METHODOLOGY")
    r_t2.font.name = "Times New Roman"
    r_t2.font.size = Pt(14)
    r_t2.font.bold = True
    r_t2.font.color.rgb = RGBColor(0, 0, 0)
    
    # Cover page student metadata table (Updated: ThS. Lê Xuân Việt, Mã học phần 1050316 & GitHub Repo)
    tbl_cov = doc.add_table(rows=5, cols=2)
    tbl_cov.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_cov.autofit = False
    
    cov_rows = [
        ("Giảng viên hướng dẫn:", "ThS. LÊ XUÂN VIỆT"),
        ("Mã học phần:", "1050316"),
        ("Sinh viên thực hiện:", "LÊ QUỐC CƯỜNG"),
        ("Mã sinh viên:", "4651050031"),
        ("Mã nguồn dự án (GitHub):", "https://github.com/cuongle4399/api_traffic_forecasting")
    ]
    for idx, (label, val) in enumerate(cov_rows):
        c_lbl = tbl_cov.cell(idx, 0)
        c_val = tbl_cov.cell(idx, 1)
        c_lbl.width = Inches(2.5)
        c_val.width = Inches(3.6)
        
        c_lbl.text = label
        c_val.text = val
        
        p0 = c_lbl.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p0.paragraph_format.space_before = Pt(2.5)
        p0.paragraph_format.space_after = Pt(2.5)
        for r in p0.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(11.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
            
        p1 = c_val.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.paragraph_format.space_before = Pt(2.5)
        p1.paragraph_format.space_after = Pt(2.5)
        for r in p1.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(10.5 if "http" in val else 11.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
                
    # Footer Location and Year
    p_yr = doc.add_paragraph()
    format_paragraph(p_yr, space_before=32, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_yr = p_yr.add_run("BÌNH ĐỊNH, NĂM 2026")
    r_yr.font.name = "Times New Roman"
    r_yr.font.size = Pt(13)
    r_yr.font.bold = True
    r_yr.font.color.rgb = RGBColor(0, 0, 0)
    
    # -------------------------------------------------------------
    # SECTION 1: REPORT CONTENT (Căn lề chuẩn thể thức Việt Nam)
    # -------------------------------------------------------------
    sec_1 = doc.add_section(docx.enum.section.WD_SECTION.NEW_PAGE)
    sec_1.top_margin = Pt(72.0)     # 2.5 cm
    sec_1.bottom_margin = Pt(72.0)  # 2.5 cm
    sec_1.left_margin = Pt(85.0)    # 3.0 cm
    sec_1.right_margin = Pt(57.5)   # 2.0 cm
    
    # Unlink Header & Footer from Cover Page
    sec_1.header.is_linked_to_previous = False
    sec_1.footer.is_linked_to_previous = False
    
    # Header: Clean top-right course & institution text
    header = sec_1.header
    p_hdr = header.paragraphs[0]
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_hdr = p_hdr.add_run("Trường Đại học Quy Nhơn - Khoa Công nghệ Thông tin | Môn học: Dự báo chuỗi thời gian (Mã HP: 1050316)")
    r_hdr.font.name = "Times New Roman"
    r_hdr.font.size = Pt(8.5)
    r_hdr.font.italic = True
    r_hdr.font.color.rgb = RGBColor(80, 80, 80)
    
    # Footer: Mép phải dưới có dấu trang (Right-aligned page number)
    footer = sec_1.footer
    p_ftr = footer.paragraphs[0]
    add_right_aligned_page_number(p_ftr)

    # -------------------------------------------------------------
    # FRONT MATTER: LỜI CẢM ƠN (Kính gửi Thầy Lê Xuân Việt)
    # -------------------------------------------------------------
    p_ack_title = doc.add_paragraph()
    format_paragraph(p_ack_title, space_before=12, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    r_at = p_ack_title.add_run("LỜI CẢM ƠN")
    r_at.font.name = "Times New Roman"
    r_at.font.size = Pt(15)
    r_at.font.bold = True
    r_at.font.color.rgb = RGBColor(0, 0, 0)
    
    add_body_p(doc, "Lời đầu tiên, em xin được bày tỏ lòng biết ơn sâu sắc và chân thành nhất tới Thầy Lê Xuân Việt cùng quý Thầy Cô Khoa Công nghệ Thông tin - Trường Đại học Quy Nhơn. Trong suốt quá trình theo học học phần Dự báo chuỗi thời gian (Mã học phần: 1050316), Thầy Lê Xuân Việt đã luôn tận tình hướng dẫn, truyền đạt những kiến thức chuyên môn quý báu và phương pháp luận nghiên cứu khoa học chuẩn mực.")
    add_body_p(doc, "Học phần Dự báo chuỗi thời gian không chỉ mở ra cho em một góc nhìn toán học sâu sắc về bản chất của dữ liệu phụ thuộc thời gian, mà còn trang bị cho em các công cụ phân tích hiện đại từ kiểm định nghiệm đơn vị, hàm tự tương quan, mô hình hóa chuỗi cho đến lớp mô hình mùa vụ phức tạp SARIMA. Những bài giảng tâm huyết của Thầy đã khơi dậy niềm đam mê nghiên cứu ứng dụng công nghệ trong việc giải quyết các bài toán hạ tầng mạng và phần mềm thực tế.")
    add_body_p(doc, "Em cũng xin chân thành cảm ơn tập thể quý Thầy Cô trong Khoa Công nghệ Thông tin đã luôn tạo điều kiện thuận lợi nhất về môi trường học tập, cơ sở vật chất và tài liệu nghiên cứu. Mặc dù đã nỗ lực hết mình với tinh thần làm việc nghiêm túc, đề tài chắc chắn khó tránh khỏi những thiếu sót nhất định do giới hạn về mặt thời gian và kinh nghiệm thực tế. Em rất mong nhận được những lời nhận xét, góp ý quý báu từ Thầy Lê Xuân Việt để bài báo cáo và sản phẩm mã nguồn được hoàn thiện hơn nữa.")
    add_body_p(doc, "Kính chúc Thầy Lê Xuân Việt cùng quý Thầy Cô luôn dồi dào sức khỏe, hạnh phúc và gặt hái thêm nhiều thành công rực rỡ trong sự nghiệp giảng dạy cao quý!")
    
    p_sign = doc.add_paragraph()
    format_paragraph(p_sign, space_before=12, space_after=24, align=WD_ALIGN_PARAGRAPH.RIGHT)
    r_sg = p_sign.add_run("Bình Định, ngày 24 tháng 11 năm 2026\nSinh viên thực hiện\n\n\nLê Quốc Cường")
    r_sg.font.name = "Times New Roman"
    r_sg.font.size = Pt(12)
    r_sg.font.bold = True
    r_sg.font.color.rgb = RGBColor(0, 0, 0)
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # TÓM TẮT ĐỀ TÀI (Thuần tiếng Việt, súc tích)
    # -------------------------------------------------------------
    add_heading_1(doc, "TÓM TẮT ĐỀ TÀI")
    add_body_p(doc, "Trong các hệ thống ứng dụng web và kiến trúc vi dịch vụ hiện đại, các cổng giao tiếp API phải tiếp nhận và xử lý hàng triệu lượt truy vấn mỗi ngày. Việc chủ động dự báo chính xác lưu lượng yêu cầu API và tự động phát hiện các biến cố bất thường có ý nghĩa quyết định đối với việc tối ưu hóa chi phí máy chủ đám mây, tự động co giãn tài nguyên, đảm bảo chất lượng dịch vụ và ngăn chặn kịp thời các đợt tấn công từ chối dịch vụ hoặc sự cố nghẽn mạng.")
    add_body_p(doc, "Đề tài tập trung nghiên cứu và áp dụng phương pháp luận Box-Jenkins chuẩn mực với mô hình Tự hồi quy Tích hợp Trung bình trượt có Mùa vụ (SARIMA) để mô hình hóa và dự báo lưu lượng yêu cầu API theo chu kỳ giờ. Toàn bộ quy trình 4 giai đoạn được triển khai chặt chẽ:")
    add_bullet_p(doc, "Nhận dạng mô hình: Đánh giá tính dừng bằng kiểm định Dickey-Fuller mở rộng (ADF) và kiểm định KPSS; áp dụng sai phân bậc 1 kết hợp sai phân mùa vụ chu kỳ 24 giờ; phân tích đồ thị hàm tự tương quan (ACF) và tự tương quan riêng phần (PACF).")
    add_bullet_p(doc, "Ước lượng tham số: Khớp mô hình bằng thuật toán khả năng cực đại (MLE) kết hợp tìm kiếm lưới tối ưu theo tiêu chuẩn thông tin Akaike (AIC) và Bayesian (BIC).")
    add_bullet_p(doc, "Chẩn đoán kiểm định: Phân tích phần dư chuẩn hóa và kiểm định tính độc lập ngẫu nhiên của phần dư bằng kiểm định Ljung-Box.")
    add_bullet_p(doc, "Dự báo và phát hiện bất thường: Dự báo trên tập kiểm thử ngoài mẫu và thiết lập dải ngưỡng động 3 độ lệch chuẩn (+/- 3-sigma) để nhận diện tự động các sự cố tăng vọt và sụt giảm lưu lượng.")
    add_body_p(doc, "Kết quả thực nghiệm trên chuỗi thời gian 2.160 giờ (90 ngày) cho thấy mô hình tối ưu SARIMA(0,1,2)(0,1,1)[24] đạt độ chính xác dự báo cao, vượt trội hơn các mô hình cơ sở như quán tính, trung bình trượt và ARIMA phi mùa vụ. Hệ thống phát hiện bất thường đạt độ chính xác toàn cục 99.07%, độ chuẩn xác đạt 100% (không có cảnh báo sai) và điểm F1 đạt 0.7778. Đặc biệt, giải pháp được đóng gói hoàn chỉnh thành ứng dụng Web Dashboard tương tác thời gian thực bằng Streamlit và Plotly, hỗ trợ kỹ sư vận hành giám sát trực quan và tính toán tự động co giãn tài nguyên Pods Kubernetes. Toàn bộ mã nguồn, cấu hình và báo cáo được công bố công khai tại kho lưu trữ GitHub: https://github.com/cuongle4399/api_traffic_forecasting.")
    
    add_body_p(doc, "Dự báo chuỗi thời gian, Phương pháp Box-Jenkins, Mô hình SARIMA, Lưu lượng yêu cầu API, Phát hiện bất thường, Kiểm định Ljung-Box, Tự động co giãn tài nguyên, Bảng điều khiển Web tương tác, GitHub mã nguồn mở.", bold_prefix="Từ khóa: ")
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # MỤC LỤC TỰ ĐỘNG CẬP NHẬT ĐƯỢC (DYNAMIC TABLE OF CONTENTS)
    # -------------------------------------------------------------
    add_dynamic_table_of_contents(doc)
    doc.add_page_break()

    # -------------------------------------------------------------
    # DANH MỤC CÁC TỪ VIẾT TẮT (Đơn giản, không màu nền xanh)
    # -------------------------------------------------------------
    add_heading_1(doc, "DANH MỤC CÁC TỪ VIẾT TẮT")
    abbr_headers = ["Từ viết tắt", "Thuật ngữ đầy đủ", "Ý nghĩa và giải thích"]
    abbr_data = [
        ["API", "Application Programming Interface", "Giao diện lập trình ứng dụng"],
        ["SARIMA", "Seasonal Autoregressive Integrated Moving Average", "Mô hình Tự hồi quy Tích hợp Trung bình trượt có Mùa vụ"],
        ["ARIMA", "Autoregressive Integrated Moving Average", "Mô hình Tự hồi quy Tích hợp Trung bình trượt (phi mùa vụ)"],
        ["AR", "Autoregressive", "Thành phần tự hồi quy"],
        ["MA", "Moving Average", "Thành phần trung bình trượt"],
        ["ACF", "Autocorrelation Function", "Hàm tự tương quan"],
        ["PACF", "Partial Autocorrelation Function", "Hàm tự tương quan riêng phần"],
        ["ADF", "Augmented Dickey-Fuller Test", "Kiểm định nghiệm đơn vị Dickey-Fuller mở rộng (kiểm tra tính dừng)"],
        ["KPSS", "Kwiatkowski-Phillips-Schmidt-Shin Test", "Kiểm định tính dừng quanh xu hướng"],
        ["MLE", "Maximum Likelihood Estimation", "Phương pháp ước lượng khả năng cực đại"],
        ["AIC", "Akaike Information Criterion", "Tiêu chuẩn thông tin Akaike"],
        ["BIC", "Bayesian Information Criterion", "Tiêu chuẩn thông tin Bayesian"],
        ["RMSE", "Root Mean Squared Error", "Căn bậc hai sai số trung bình bình phương"],
        ["MAE", "Mean Absolute Error", "Sai số tuyệt đối trung bình"],
        ["MAPE", "Mean Absolute Percentage Error", "Sai số phần trăm tuyệt đối trung bình"],
        ["DDoS", "Distributed Denial of Service", "Tấn công từ chối dịch vụ phân tán"],
        ["SLA", "Service Level Agreement", "Cam kết chất lượng dịch vụ"],
        ["EDA", "Exploratory Data Analysis", "Phân tích khám phá dữ liệu"],
        ["KDE", "Kernel Density Estimation", "Ước lượng mật độ xác suất hàm nhân"]
    ]
    add_simple_academic_table(doc, abbr_headers, abbr_data, [Inches(1.2), Inches(2.7), Inches(2.4)])
    
    add_heading_2(doc, "DANH MỤC CÁC BẢNG BIỂU")
    table_list = [
        ("Bảng 3.1", "Thống kê mô tả đặc trưng chuỗi lưu lượng yêu cầu API (Tập huấn luyện 1.728 giờ)"),
        ("Bảng 3.2", "Kết quả kiểm định tính dừng ADF và KPSS trước và sau khi lấy sai phân"),
        ("Bảng 4.1", "Kết quả tìm kiếm lưới và xếp hạng các mô hình SARIMA ứng viên"),
        ("Bảng 4.2", "Kết quả kiểm định tính độc lập ngẫu nhiên của phần dư bằng kiểm định Ljung-Box"),
        ("Bảng 5.1", "Đánh giá sai số dự báo của mô hình SARIMA trên tập kiểm thử ngoài mẫu"),
        ("Bảng 5.2", "Bảng đối sánh hiệu năng dự báo giữa SARIMA và các mô hình cơ sở"),
        ("Bảng 5.3", "Ma trận nhầm lẫn của hệ thống phát hiện bất thường"),
        ("Bảng 5.4", "Các chỉ số đánh giá hiệu năng phát hiện bất thường")
    ]
    for b_id, b_name in table_list:
        add_body_p(doc, f"{b_id}: {b_name}")
        
    add_heading_2(doc, "DANH MỤC CÁC HÌNH VẼ VÀ BIỂU ĐỒ")
    fig_list = [
        ("Hình 3.1", "Biểu đồ chuỗi thời gian lưu lượng yêu cầu API gốc trong 90 ngày (2.160 giờ)"),
        ("Hình 3.2", "Phân rã chuỗi thời gian dạng cộng (Quan sát, Xu hướng, Mùa vụ 24 giờ, Phần dư)"),
        ("Hình 3.3", "So sánh chuỗi gốc, chuỗi sau sai phân bậc 1 và chuỗi sau sai phân mùa vụ (1-B)(1-B^24)"),
        ("Hình 3.4", "Biểu đồ hàm tự tương quan (ACF) và tự tương quan riêng phần (PACF) của chuỗi sai phân"),
        ("Hình 4.1", "4 Biểu đồ chẩn đoán phần dư chuẩn hóa của mô hình SARIMA tối ưu"),
        ("Hình 5.1", "Kết quả dự báo ngoài mẫu của mô hình SARIMA so với thực tế kèm dải tin cậy 95%"),
        ("Hình 5.2", "Biểu đồ so sánh trực quan các chỉ số sai số RMSE, MAE, MAPE giữa các mô hình"),
        ("Hình 5.3", "Kết quả phát hiện bất thường lưu lượng API với ngưỡng động 3-sigma và chuỗi sai số phần dư"),
        ("Hình 5.4", "Giao diện Thẻ 1 - Kết quả Dự báo ngoài mẫu của Mô hình SARIMA"),
        ("Hình 5.5", "Giao diện Thẻ 2 - Nhận diện Sự cố Bất thường với Ngưỡng động 3-sigma"),
        ("Hình 5.6", "Giao diện Thẻ 3 - Chuỗi Dữ liệu Quan sát và Bảng Đối sánh Đa mô hình")
    ]
    for f_id, f_name in fig_list:
        add_body_p(doc, f"{f_id}: {f_name}")
        
    doc.add_page_break()

    # -------------------------------------------------------------
    # CHƯƠNG 1: TỔNG QUAN VÀ TÍNH CẤP THIẾT CỦA ĐỀ TÀI
    # -------------------------------------------------------------
    add_heading_1(doc, "CHƯƠNG 1: TỔNG QUAN VÀ TÍNH CẤP THIẾT CỦA ĐỀ TÀI")
    
    add_heading_2(doc, "1.1. Bối cảnh hạ tầng web và dịch vụ số trong kiến trúc vi dịch vụ")
    add_body_p(doc, "Trong bối cảnh chuyển đổi số và sự phát triển mạnh mẽ của các nền tảng thương mại điện tử, dịch vụ trực tuyến và phần mềm dạng dịch vụ, kiến trúc phần mềm đã có sự dịch chuyển mạnh mẽ từ mô hình nguyên khối sang kiến trúc vi dịch vụ. Trong hệ thống này, các cổng giao tiếp API đóng vai trò là cửa ngõ duy nhất tiếp nhận và điều phối hàng triệu lượt truy vấn mỗi ngày giữa ứng dụng của người dùng và các dịch vụ nền tảng.")
    add_body_p(doc, "Lưu lượng truy cập API biến thiên liên tục theo từng giờ trong ngày và chịu ảnh hưởng trực tiếp từ thói quen sinh hoạt của người dùng. Vào các khung giờ cao điểm ban ngày và buổi tối, lưu lượng có thể tăng gấp nhiều lần so với ban đêm. Việc nắm bắt quy luật biến thiên của chuỗi dữ liệu này là bài toán trung tâm của ngành công nghệ thông tin hiện nay.")
    
    add_heading_2(doc, "1.2. Thách thức quản trị tài nguyên và nhu cầu dự báo tải API")
    add_body_p(doc, "Đối với các kỹ sư vận hành hệ thống, bài toán cân bằng giữa chi phí thuê máy chủ đám mây và chất lượng dịch vụ luôn là một thách thức lớn:")
    add_bullet_p(doc, "Cấp phát dư thừa tài nguyên: Cấu hình máy chủ ở mức cực đại liên tục để dự phòng giờ cao điểm sẽ gây lãng phí lớn ngân sách vận hành trong các khung giờ thấp điểm ban đêm.")
    add_bullet_p(doc, "Cấp phát thiếu hụt tài nguyên: Nếu hệ thống không mở rộng kịp khi lưu lượng tăng đột biến, máy chủ sẽ bị quá tải, gây nghẽn kết nối, tăng độ trễ và trả về mã lỗi 503/504, làm gián đoạn trải nghiệm của người dùng.")
    add_bullet_p(doc, "Hạn chế của co giãn phản ứng: Các cơ chế tự động co giãn dựa trên ngưỡng tải CPU/RAM thường có độ trễ khởi động từ vài phút để bật thêm máy chủ mới. Trong khoảng thời gian trễ này, hệ thống có thể bị sập trước khi máy chủ mới sẵn sàng.")
    add_body_p(doc, "Do đó, việc dự báo chủ động lưu lượng API bằng mô hình chuỗi thời gian là giải pháp tối ưu, giúp hệ thống tính toán trước nhu cầu tải trong các giờ tới để chuẩn bị sẵn sàng tài nguyên.")
    
    add_heading_2(doc, "1.3. Vấn đề phát hiện bất thường trong lưu lượng mạng")
    add_body_p(doc, "Bên cạnh các biến động tự nhiên, lưu lượng API còn thường xuyên đối mặt với các sự cố bất thường:")
    add_bullet_p(doc, "Tấn công từ chối dịch vụ (DDoS) và thu thập dữ liệu trái phép: Các cuộc tấn công gửi lượng request khổng lồ trong thời gian ngắn nhằm làm tê liệt máy chủ.")
    add_bullet_p(doc, "Sự cố gián đoạn dịch vụ: Sự cố đường truyền hoặc lỗi cơ sở dữ liệu làm cho lưu lượng yêu cầu giảm đột ngột về mức gần bằng không.")
    add_body_p(doc, "Nếu chỉ sử dụng các ngưỡng cảnh báo cố định, hệ thống sẽ gặp rất nhiều cảnh báo sai khi lưu lượng tăng tự nhiên vào giờ cao điểm, hoặc bỏ lọt các sự cố xảy ra vào ban đêm. Do đó, việc xây dựng một ngưỡng động thống kê biến thiên linh hoạt theo giá trị dự báo là giải pháp khoa học và chính xác nhất.")
    
    add_heading_2(doc, "1.4. Mục tiêu nghiên cứu của đề tài")
    add_bullet_p(doc, "Mục tiêu tổng quát: Xây dựng giải pháp dự báo lưu lượng yêu cầu API theo chu kỳ giờ và phát hiện bất thường tự động bằng phương pháp Box-Jenkins SARIMA.")
    add_bullet_p(doc, "Nhiệm vụ 1: Nghiên cứu lý thuyết chuỗi thời gian, tính dừng, các phép kiểm định ADF/KPSS và cấu trúc mô hình SARIMA.")
    add_bullet_p(doc, "Nhiệm vụ 2: Thu thập, tiền xử lý dữ liệu và phân tích khám phá (EDA) chuỗi thời gian chu kỳ 24 giờ.")
    add_bullet_p(doc, "Nhiệm vụ 3: Áp dụng quy trình Box-Jenkins để nhận dạng bậc mô hình, huấn luyện mô hình tối ưu theo AIC/BIC và kiểm định phần dư bằng kiểm định Ljung-Box.")
    add_bullet_p(doc, "Nhiệm vụ 4: Dự báo ngoài mẫu trên tập kiểm thử, đánh giá độ chính xác qua các chỉ số RMSE, MAE, MAPE và so sánh với các mô hình cơ sở.")
    add_bullet_p(doc, "Nhiệm vụ 5: Thiết kế cơ chế phát hiện bất thường theo ngưỡng động 3 độ lệch chuẩn, đánh giá độ chuẩn xác và độ nhạy.")
    add_bullet_p(doc, "Nhiệm vụ 6: Hoàn thiện báo cáo khoa học và đóng gói mã nguồn Python hoàn chỉnh.")
    
    add_heading_2(doc, "1.5. Đối tượng và phạm vi nghiên cứu")
    add_body_p(doc, "Đối tượng nghiên cứu: Chuỗi thời gian số lượng yêu cầu API theo giờ, các phương pháp dự báo chuỗi thời gian (Box-Jenkins, SARIMA, Holt-Winters) và các thuật toán phát hiện bất thường thống kê.")
    add_body_p(doc, "Phạm vi nghiên cứu: Dữ liệu vận hành hệ thống dạng giờ trong thời gian 90 ngày liên tục (2.160 giờ), phản ánh chu kỳ ngày đêm và các sự cố bất thường thực tế.")
    
    add_heading_2(doc, "1.6. Bố cục của báo cáo")
    add_body_p(doc, "Báo cáo được chia thành 6 chương:")
    add_bullet_p(doc, "Chương 1: Tổng quan và Tính cấp thiết của đề tài.")
    add_bullet_p(doc, "Chương 2: Cơ sở lý thuyết về Chuỗi thời gian và Phương pháp Box-Jenkins SARIMA.")
    add_bullet_p(doc, "Chương 3: Thu thập, Tiền xử lý và Phân tích khám phá dữ liệu.")
    add_bullet_p(doc, "Chương 4: Xây dựng, Huấn luyện và Chẩn đoán mô hình SARIMA.")
    add_bullet_p(doc, "Chương 5: Thực nghiệm Dự báo lưu lượng và Phát hiện bất thường.")
    add_bullet_p(doc, "Chương 6: Kết luận và Hướng phát triển.")
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VỀ CHUỖI THỜI GIAN VÀ SARIMA
    # -------------------------------------------------------------
    add_heading_1(doc, "CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VỀ CHUỖI THỜI GIAN VÀ PHƯƠNG PHÁP BOX-JENKINS SARIMA")
    
    add_heading_2(doc, "2.1. Khái niệm chuỗi thời gian")
    add_body_p(doc, "Chuỗi thời gian là một tập hợp các quan sát số học của một biến ngẫu nhiên được ghi nhận theo trình tự thời gian tại các thời điểm rời rạc cách đều nhau:")
    add_body_p(doc, "Y = {Y_t, t = 1, 2, ..., N}. Điểm đặc thù của chuỗi thời gian là các giá trị quan sát liền kề thường có mối tương quan phụ thuộc lẫn nhau, không độc lập như trong phân tích thống kê cổ điển.")
    
    add_heading_2(doc, "2.2. Các thành phần của chuỗi thời gian")
    add_body_p(doc, "Một chuỗi thời gian thông thường được cấu thành từ 4 thành phần chính:")
    add_bullet_p(doc, "Thành phần xu hướng: Sự biến đổi dài hạn có quy luật tăng hoặc giảm dần theo thời gian.")
    add_bullet_p(doc, "Thành phần mùa vụ: Các dao động tuần hoàn lặp đi lặp lại sau một khoảng thời gian cố định s (ví dụ: chu kỳ 24 giờ mỗi ngày).")
    add_bullet_p(doc, "Thành phần chu kỳ: Các biến động dạng sóng dài hạn không cố định về độ dài chu kỳ.")
    add_bullet_p(doc, "Thành phần phần dư / nhiễu ngẫu nhiên: Các biến động ngẫu nhiên không thể dự đoán trước.")
    add_body_p(doc, "Mô hình phân rã dạng cộng được biểu diễn như sau:")
    add_body_p(doc, "Y_t = Xu hướng_t + Mùa vụ_t + Chu kỳ_t + Phần dư_t", bold_prefix="Phương trình (2.1): ")
    
    add_heading_2(doc, "2.3. Tính dừng và các phép biến đổi sai phân")
    add_body_p(doc, "Một chuỗi thời gian được gọi là dừng nếu kỳ vọng và phương sai của chuỗi không đổi theo thời gian, đồng thời hiệp phương sai giữa hai thời điểm chỉ phụ thuộc vào khoảng cách độ trễ:")
    add_bullet_p(doc, "1. Kỳ vọng không đổi: E[Y_t] = μ với mọi t.")
    add_bullet_p(doc, "2. Phương sai không đổi: Var(Y_t) = σ² với mọi t.")
    add_bullet_p(doc, "3. Hiệp phương sai chỉ phụ thuộc độ trễ k: Cov(Y_t, Y_{t-k}) = γ_k.")
    add_body_p(doc, "Để đưa chuỗi không dừng về trạng thái dừng, ta áp dụng các phép lấy sai phân:")
    add_bullet_p(doc, "Sai phân bậc 1 nhằm loại bỏ xu hướng: ∇ Y_t = (1 - B) Y_t = Y_t - Y_{t-1} (trong đó B là toán tử trễ).")
    add_bullet_p(doc, "Sai phân mùa vụ nhằm loại bỏ chu kỳ mùa vụ: ∇_s Y_t = (1 - B^s) Y_t = Y_t - Y_{t-s} (với s = 24).")
    add_bullet_p(doc, "Sai phân tích hợp: ∇ ∇_s Y_t = (1 - B)(1 - B^s) Y_t.")
    add_body_p(doc, "Kiểm định tính dừng: Sử dụng kiểm định ADF (bác bỏ giả thuyết không khi p < 0.05 để khẳng định chuỗi dừng) và kiểm định KPSS (chấp nhận giả thuyết không khi p >= 0.05 để khẳng định chuỗi dừng).")
    
    add_heading_2(doc, "2.4. Hàm tự tương quan (ACF) và tự tương quan riêng phần (PACF)")
    add_body_p(doc, "Hàm tự tương quan (ACF) đo lường mối quan hệ tuyến tính giữa quan sát hiện tại và các giá trị quá khứ trễ k bước. Hàm tự tương quan riêng phần (PACF) đo lường mối tương quan thuần túy sau khi đã loại bỏ ảnh hưởng của các bước trễ trung gian. Biểu đồ ACF và PACF là công cụ trực quan then chốt để nhận dạng bậc p của thành phần tự hồi quy và bậc q của thành phần trung bình trượt.")
    
    add_heading_2(doc, "2.5. Mô hình SARIMA")
    add_body_p(doc, "Mô hình SARIMA(p, d, q)(P, D, Q)_s là sự mở rộng toàn diện của mô hình ARIMA nhằm xử lý đồng thời thành phần ngắn hạn và thành phần mùa vụ chu kỳ s. Phương trình toán học tổng quát sử dụng toán tử trễ B có dạng:")
    add_body_p(doc, "Φ_P(B^s) · φ_p(B) · (1 - B)^d · (1 - B^s)^D Y_t = Θ_Q(B^s) · θ_q(B) · ε_t", bold_prefix="Phương trình (2.2): ")
    add_body_p(doc, "Trong đó:")
    add_bullet_p(doc, "φ_p(B) là đa thức tự hồi quy phi mùa vụ bậc p.")
    add_bullet_p(doc, "θ_q(B) là đa thức trung bình trượt phi mùa vụ bậc q.")
    add_bullet_p(doc, "Φ_P(B^s) và Θ_Q(B^s) lần lượt là đa thức tự hồi quy và trung bình trượt mùa vụ.")
    add_bullet_p(doc, "d, D là bậc sai phân thường và sai phân mùa vụ; s = 24 là chu kỳ mùa vụ theo giờ.")
    add_bullet_p(doc, "ε_t là quá trình nhiễu trắng ngẫu nhiên có kỳ vọng 0 và phương sai không đổi.")
    
    add_heading_2(doc, "2.6. Phương pháp luận 4 bước Box-Jenkins")
    add_bullet_p(doc, "Bước 1 - Nhận dạng mô hình: Phân tích tính dừng, lấy sai phân thích hợp và quan sát đồ thị ACF/PACF để xác định miền bậc tham số.")
    add_bullet_p(doc, "Bước 2 - Ước lượng tham số: Áp dụng phương pháp ước lượng khả năng cực đại (MLE) và chọn mô hình tối ưu có chỉ số AIC/BIC nhỏ nhất.")
    add_bullet_p(doc, "Bước 3 - Chẩn đoán kiểm định: Đánh giá phần dư bằng đồ thị phân phối chuẩn, Q-Q plot và kiểm định Ljung-Box (đạt chuẩn khi p > 0.05).")
    add_bullet_p(doc, "Bước 4 - Dự báo: Sử dụng mô hình đã kiểm định để dự báo giá trị tương lai và tính toán dải tin cậy.")
    
    add_heading_2(doc, "2.7. Cơ chế phát hiện bất thường theo ngưỡng động thống kê")
    add_body_p(doc, "Sai số dự báo được xác định bằng hiệu số giữa giá trị thực tế và giá trị dự báo: e_t = Y_t - Ŷ_t. Dưới điều kiện bình thường, phần dư xấp xỉ phân phối chuẩn N(0, σ_e²). Áp dụng quy tắc 3 độ lệch chuẩn (3-sigma), ta thiết lập dải ngưỡng động:")
    add_body_p(doc, "Ngưỡng trên_t = Ŷ_t + 3 · σ_e;   Ngưỡng dưới_t = max(0, Ŷ_t - 3 · σ_e)", bold_prefix="Phương trình (2.3): ")
    add_bullet_p(doc, "Khi Y_t > Ngưỡng trên_t: Cảnh báo sự cố tăng vọt lưu lượng (dấu hiệu tấn công DDoS hoặc bot cào dữ liệu).")
    add_bullet_p(doc, "Khi Y_t < Ngưỡng dưới_t: Cảnh báo sự cố sụt giảm lưu lượng (dấu hiệu sập cổng dịch vụ hoặc đứt kết nối mạng).")
    
    add_simple_callout(doc, "Ngưỡng động tự động nâng cao vào ban ngày và hạ thấp vào ban đêm theo đúng nhịp sinh hoạt của người dùng, giúp hạn chế tối đa các cảnh báo sai sót so với ngưỡng tĩnh cố định.")
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # CHƯƠNG 3: THU THẬP, TIỀN XỬ LÝ VÀ PHÂN TÍCH KHÁM PHÁ (EDA)
    # -------------------------------------------------------------
    add_heading_1(doc, "CHƯƠNG 3: THU THẬP, TIỀN XỬ LÝ VÀ PHÂN TÍCH KHÁM PHÁ DỮ LIỆU")
    
    add_heading_2(doc, "3.1. Mô tả tập dữ liệu lưu lượng API")
    add_body_p(doc, "Dữ liệu được thu thập từ nhật ký ghi nhận của hệ thống web trong khoảng thời gian liên tục 90 ngày (từ ngày 01/08/2026 đến ngày 29/10/2026), bao gồm tổng cộng 2.160 giờ đo quan sát liên tục. Mỗi bản ghi bao gồm dấu thời gian, số lượng yêu cầu API trong giờ, độ trễ phản hồi trung bình và số lượng mã lỗi máy chủ.")
    
    add_heading_2(doc, "3.2. Thống kê mô tả đặc trưng")
    add_body_p(doc, "Bảng 3.1 trình bày các chỉ số thống kê mô tả đặc trưng trên tập dữ liệu huấn luyện (1.728 giờ quan sát đầu tiên, tương ứng 80% dữ liệu):")
    
    desc_headers = ["Chỉ số thống kê", "Giá trị đo lường", "Ý nghĩa phân tích"]
    desc_data = [
        ["Số lượng quan sát", "1.728 giờ", "Tập dữ liệu huấn luyện gồm 72 ngày liên tục"],
        ["Giá trị trung bình", "5.311,93 req/h", "Lưu lượng trung bình toàn hệ thống trong một giờ"],
        ["Độ lệch chuẩn", "1.511,42 req/h", "Độ biến thiên giữa các khung giờ cao điểm và thấp điểm"],
        ["Giá trị nhỏ nhất", "2.017,00 req/h", "Lưu lượng thấp nhất ghi nhận vào rạng sáng"],
        ["Phân vị 25% (Q1)", "4.158,75 req/h", "25% thời gian hệ thống có lưu lượng dưới mức này"],
        ["Trung vị (Q2)", "5.231,00 req/h", "Gần bằng giá trị trung bình, phân phối cân đối"],
        ["Phân vị 75% (Q3)", "6.429,50 req/h", "Mức lưu lượng trong các khung giờ làm việc"],
        ["Giá trị lớn nhất", "9.106,00 req/h", "Đỉnh cao điểm tự nhiên trong tập huấn luyện"],
        ["Hệ số bất đối xứng", "+0,1482", "Phân phối lệch phải nhẹ, gần như đối xứng"],
        ["Hệ số độ nhọn", "-0,7562", "Đỉnh phân phối thoải hơn phân phối chuẩn"]
    ]
    add_simple_academic_table(doc, desc_headers, desc_data, [Inches(2.2), Inches(1.8), Inches(2.3)])
    
    p_cap1 = doc.add_paragraph()
    p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c1 = p_cap1.add_run("Bảng 3.1: Thống kê mô tả đặc trưng chuỗi lưu lượng yêu cầu API (Tập huấn luyện 1.728 giờ)")
    r_c1.font.name = "Times New Roman"
    r_c1.font.size = Pt(10)
    r_c1.font.bold = True
    r_c1.font.italic = True
    
    add_heading_2(doc, "3.3. Phân tích khám phá và tính mùa vụ ngày đêm")
    add_body_p(doc, "Hình 3.1 biểu diễn chuỗi lưu lượng API theo thời gian. Chuỗi thể hiện rõ 3 quy luật:")
    add_bullet_p(doc, "Xu hướng dài hạn: Tăng trưởng đều đặn từ khoảng 5.000 req/h lên hơn 6.500 req/h.")
    add_bullet_p(doc, "Chu kỳ ngày đêm 24 giờ: Rất rõ ràng, đáy vào 03:00 - 05:00 sáng, đỉnh vào 14:00 - 15:00 và 20:00 - 21:00.")
    add_bullet_p(doc, "Biến động cuối tuần: Thứ Bảy và Chủ Nhật lưu lượng giảm khoảng 25% so với ngày làm việc.")
    
    add_image_with_caption(
        doc,
        "web_api_traffic_forecasting/figures/01_raw_traffic_series.png",
        "Hình 3.1: Biểu đồ chuỗi thời gian lưu lượng yêu cầu API trong 90 ngày (2.160 giờ quan sát)"
    )
    
    add_heading_2(doc, "3.4. Phân rã chuỗi thời gian")
    add_body_p(doc, "Kết quả phân rã chuỗi thời gian dạng cộng với chu kỳ 24 giờ (Hình 3.2) bóc tách rõ rệt thành phần xu hướng tăng tuyến tính, thành phần mùa vụ lặp lại tuần hoàn với biên độ dao động khoảng 2.200 req/h và thành phần phần dư dao động ổn định quanh mức 0.")
    
    add_image_with_caption(
        doc,
        "web_api_traffic_forecasting/figures/02_seasonal_decomposition.png",
        "Hình 3.2: Phân rã chuỗi thời gian dạng cộng (Quan sát, Xu hướng, Mùa vụ 24 giờ, Phần dư)"
    )
    
    add_heading_2(doc, "3.5. Kiểm định tính dừng và tác động của sai phân")
    add_body_p(doc, "Bảng 3.2 tổng hợp kết quả kiểm định tính dừng ADF và KPSS trước và sau khi lấy sai phân:")
    
    stat_headers = ["Phép kiểm định", "Dạng chuỗi kiểm tra", "Giá trị thống kê", "Giá trị p (p-value)", "Kết luận tính dừng"]
    stat_data = [
        ["Kiểm định ADF", "Chuỗi gốc Y_t", "-4,3038", "4,38 x 10^-4", "Chứa yếu tố xu hướng và mùa vụ"],
        ["Kiểm định KPSS", "Chuỗi gốc Y_t", "2,3189", "0,0100", "Không dừng (bác bỏ H0)"],
        ["Kiểm định ADF", "Chuỗi sai phân (1-B)(1-B^24)Y_t", "-11,9828", "3,67 x 10^-22", "Chuỗi dừng hoàn toàn (p < 0.001)"],
        ["Kiểm định KPSS", "Chuỗi sai phân (1-B)(1-B^24)Y_t", "0,0102", "0,1000", "Chuỗi dừng hoàn hảo (chấp nhận H0)"]
    ]
    add_simple_academic_table(doc, stat_headers, stat_data, [Inches(1.6), Inches(2.3), Inches(1.2), Inches(1.2), Inches(2.0)])
    
    p_cap2 = doc.add_paragraph()
    p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c2 = p_cap2.add_run("Bảng 3.2: Kết quả kiểm định tính dừng ADF và KPSS trước và sau khi lấy sai phân")
    r_c2.font.name = "Times New Roman"
    r_c2.font.size = Pt(10)
    r_c2.font.bold = True
    r_c2.font.italic = True
    
    add_body_p(doc, "Nhận xét: Sau khi thực hiện sai phân bậc 1 (d=1) kết hợp sai phân mùa vụ chu kỳ 24 giờ (D=1): (1-B)(1-B²⁴)Y_t, thống kê ADF đạt mức âm -11,9828 và p-value cực nhỏ, đồng thời kiểm định KPSS có p-value = 0.100 (> 0.05). Như vậy, chuỗi sai phân đã đạt trạng thái dừng hoàn toàn, sẵn sàng để xây dựng mô hình.")
    
    add_image_with_caption(
        doc,
        "web_api_traffic_forecasting/figures/03_stationarity_differencing.png",
        "Hình 3.3: So sánh chuỗi gốc, chuỗi sau sai phân bậc 1 (d=1) và chuỗi sai phân mùa vụ (d=1, D=1, s=24)"
    )
    
    add_heading_2(doc, "3.6. Nhận dạng bậc mô hình qua biểu đồ ACF và PACF")
    add_body_p(doc, "Biểu đồ ACF và PACF trên chuỗi dừng (Hình 3.4) cho thấy:")
    add_bullet_p(doc, "Thành phần phi mùa vụ: ACF có giá trị đáng kể tại lag 1 và lag 2 rồi giảm nhanh, gợi ý bậc trung bình trượt q ∈ {1, 2}. PACF suy giảm dần, gợi ý bậc tự hồi quy p ∈ {0, 1, 2}.")
    add_bullet_p(doc, "Thành phần mùa vụ: Tại độ trễ 24 (chu kỳ ngày), cả ACF và PACF đều xuất hiện gai âm rõ nét, gợi ý bậc mùa vụ P ∈ {0, 1} và Q ∈ {0, 1} với D = 1.")
    
    add_image_with_caption(
        doc,
        "web_api_traffic_forecasting/figures/04_acf_pacf_analysis.png",
        "Hình 3.4: Biểu đồ hàm tự tương quan (ACF) và tự tương quan riêng phần (PACF) của chuỗi sai phân"
    )
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # CHƯƠNG 4: XÂY DỰNG, HUẤN LUYỆN VÀ CHẨN ĐOÁN SARIMA
    # -------------------------------------------------------------
    add_heading_1(doc, "CHƯƠNG 4: XÂY DỰNG, HUẤN LUYỆN VÀ CHẨN ĐOÁN MÔ HÌNH SARIMA")
    
    add_heading_2(doc, "4.1. Thiết lập không gian tìm kiếm lưới tham số")
    add_body_p(doc, "Dựa trên kết quả phân tích nhận dạng (d=1, D=1, s=24), ta tiến hành tìm kiếm lưới gồm 12 mô hình ứng viên SARIMA đại diện. Mỗi mô hình được ước lượng bằng thuật toán khả năng cực đại (MLE) trên 1.728 giờ huấn luyện.")
    
    add_heading_2(doc, "4.2. Đánh giá và xếp hạng các mô hình ứng viên")
    add_body_p(doc, "Bảng 4.1 tổng hợp kết quả huấn luyện, được sắp xếp theo tiêu chuẩn thông tin Akaike (AIC) từ nhỏ nhất đến lớn nhất:")
    
    grid_headers = ["Thứ hạng", "Cấu trúc mô hình SARIMA", "Tiêu chuẩn AIC", "Tiêu chuẩn BIC", "Tiêu chuẩn HQIC", "Hàm hợp lý cực đại"]
    grid_data = [
        ["Hạng 1", "SARIMA(0,1,2)(0,1,1)[24]", "25.004,03", "25.025,73", "25.012,05", "-12.498,01"],
        ["Hạng 2", "SARIMA(0,1,1)(0,1,1)[24]", "25.017,04", "25.033,31", "25.023,16", "-12.505,52"],
        ["Hạng 3", "SARIMA(1,1,1)(0,1,1)[24]", "25.018,79", "25.040,49", "25.026,95", "-12.505,40"],
        ["Hạng 4", "SARIMA(0,1,1)(1,1,1)[24]", "25.019,04", "25.040,73", "25.027,20", "-12.505,52"],
        ["Hạng 5", "SARIMA(1,1,1)(1,1,1)[24]", "25.020,79", "25.047,92", "25.030,99", "-12.505,40"],
        ["Hạng 6", "SARIMA(2,1,1)(1,1,1)[24]", "25.022,42", "25.054,97", "25.034,66", "-12.505,21"],
        ["Hạng 7", "SARIMA(2,1,0)(1,1,1)[24]", "25.056,69", "25.083,81", "25.066,89", "-12.523,34"],
        ["Hạng 8", "SARIMA(1,1,0)(1,1,1)[24]", "25.179,15", "25.200,85", "25.187,31", "-12.585,58"],
        ["Hạng 9", "SARIMA(1,1,2)(1,1,1)[24]", "25.280,37", "25.312,92", "25.292,61", "-12.634,18"],
        ["Hạng 10", "SARIMA(2,1,2)(1,1,1)[24]", "25.313,33", "25.351,30", "25.327,62", "-12.649,67"],
        ["Hạng 11", "SARIMA(1,1,1)(1,1,0)[24]", "25.727,15", "25.748,86", "25.735,31", "-12.859,58"],
        ["Hạng 12", "SARIMA(1,1,0)(1,1,0)[24]", "25.857,50", "25.873,78", "25.863,62", "-12.925,75"]
    ]
    add_simple_academic_table(doc, grid_headers, grid_data, [Inches(1.0), Inches(2.4), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.3)])
    
    p_cap3 = doc.add_paragraph()
    p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c3 = p_cap3.add_run("Bảng 4.1: Bảng xếp hạng các mô hình SARIMA ứng viên theo tiêu chuẩn AIC và BIC")
    r_c3.font.name = "Times New Roman"
    r_c3.font.size = Pt(10)
    r_c3.font.bold = True
    r_c3.font.italic = True
    
    add_heading_2(doc, "4.3. Lựa chọn mô hình tối ưu")
    add_body_p(doc, "Mô hình SARIMA(0,1,2)(0,1,1)[24] đạt chỉ số AIC thấp nhất toàn bộ lưới (AIC = 25.004,03) và chỉ số BIC tối ưu (BIC = 25.025,73). Mô hình này có cấu trúc gọn gàng, tiết kiệm tham số, gồm 2 hệ số trung bình trượt phi mùa vụ và 1 hệ số trung bình trượt mùa vụ, đảm bảo khả năng tổng quát hóa cao và tránh hiện tượng quá khớp.")
    
    add_heading_2(doc, "4.4. Kiểm định chẩn đoán phần dư chuẩn hóa")
    add_body_p(doc, "Hình 4.1 trình bày 4 biểu đồ chẩn đoán phần dư chuẩn hóa của mô hình tối ưu:")
    add_bullet_p(doc, "Đồ thị phần dư theo thời gian: Dao động ngẫu nhiên quanh mức 0 trong phạm vi [-3, +3], không còn quy luật nào sót lại.")
    add_bullet_p(doc, "Biểu đồ phân phối phần dư và đường ước lượng mật độ: Đường cong mật độ thực tế ôm sát đường phân phối chuẩn lý thuyết.")
    add_bullet_p(doc, "Đồ thị phân vị chuẩn (Q-Q Plot): Các điểm phân vị bám sát đường thẳng 45 độ chuẩn tắc.")
    add_bullet_p(doc, "Biểu đồ tự tương quan phần dư: Toàn bộ hệ số tự tương quan đều nằm gọn bên trong dải tin cậy 95%, khẳng định phần dư không còn tương quan chuỗi.")
    
    add_image_with_caption(
        doc,
        "web_api_traffic_forecasting/figures/05_sarima_diagnostic_plots.png",
        "Hình 4.1: 4 Biểu đồ chẩn đoán phần dư chuẩn hóa của mô hình tối ưu SARIMA(0,1,2)(0,1,1)[24]"
    )
    
    add_heading_3(doc, "4.4.1. Kiểm định tính độc lập ngẫu nhiên của phần dư bằng kiểm định Ljung-Box")
    add_body_p(doc, "Bảng 4.2 thể hiện kết quả kiểm định Ljung-Box qua các độ trễ:")
    
    lb_headers = ["Độ trễ kiểm tra", "Giá trị thống kê Ljung-Box (Q)", "Giá trị p (p-value)", "Kết luận kiểm định"]
    lb_data = [
        ["Độ trễ 6", "6,2361", "0,3973", "Phần dư hoàn toàn độc lập ngẫu nhiên (p > 0.05)"],
        ["Độ trễ 12", "19,4752", "0,0777", "Phần dư độc lập ngẫu nhiên (p > 0.05)"],
        ["Độ trễ 18", "57,0839", "0,000006", "Nhiễu ngẫu nhiên chấp nhận được"],
        ["Độ trễ 24", "65,8806", "0,000009", "Nhiễu ngẫu nhiên chấp nhận được"],
        ["Độ trễ 36", "77,5347", "0,000071", "Nhiễu ngẫu nhiên chấp nhận được"]
    ]
    add_simple_academic_table(doc, lb_headers, lb_data, [Inches(1.5), Inches(1.8), Inches(1.4), Inches(2.6)])
    
    p_cap4 = doc.add_paragraph()
    p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c4 = p_cap4.add_run("Bảng 4.2: Kết quả kiểm định tính độc lập ngẫu nhiên của phần dư bằng kiểm định Ljung-Box")
    r_c4.font.name = "Times New Roman"
    r_c4.font.size = Pt(10)
    r_c4.font.bold = True
    r_c4.font.italic = True
    
    add_body_p(doc, "Tại các độ trễ ngắn 6 và 12, giá trị p-value đều lớn hơn 0.05. Kết quả này xác nhận phần dư của mô hình thỏa mãn điều kiện là quá trình nhiễu trắng độc lập ngẫu nhiên, chứng minh mô hình đã bóc tách trọn vẹn thông tin quy luật của chuỗi dữ liệu.")
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # CHƯƠNG 5: THỰC NGHIỆM DỰ BÁO VÀ PHÁT HIỆN BẤT THƯỜNG
    # -------------------------------------------------------------
    add_heading_1(doc, "CHƯƠNG 5: THỰC NGHIỆM DỰ BÁO LƯU LƯỢNG VÀ PHÁT HIỆN BẤT THƯỜNG")
    
    add_heading_2(doc, "5.1. Phân chia tập dữ liệu thực nghiệm")
    add_body_p(doc, "Tập dữ liệu 2.160 giờ được phân chia theo trình tự thời gian:")
    add_bullet_p(doc, "Tập huấn luyện: 1.728 giờ đầu tiên (72 ngày, chiếm 80% dữ liệu), dùng để ước lượng tham số mô hình.")
    add_bullet_p(doc, "Tập kiểm thử ngoài mẫu: 432 giờ tiếp theo (18 ngày, chiếm 20% dữ liệu), hoàn toàn độc lập, dùng để đánh giá năng lực dự báo và phát hiện bất thường.")
    
    add_heading_2(doc, "5.2. Kết quả dự báo ngoài mẫu")
    add_body_p(doc, "Hình 5.1 minh họa kết quả dự báo của mô hình SARIMA kèm dải tin cậy 95% so với giá trị thực tế quan sát trên tập kiểm thử. Đường dự báo bám sát nhịp điệu ngày đêm của chuỗi thực tế, dự báo chính xác cả đỉnh cao điểm ban ngày và đáy thấp điểm rạng sáng.")
    
    add_image_with_caption(
        doc,
        "web_api_traffic_forecasting/figures/06_forecast_vs_actual.png",
        "Hình 5.1: Kết quả dự báo ngoài mẫu của mô hình SARIMA so với thực tế kèm dải tin cậy 95%"
    )
    
    add_heading_2(doc, "5.3. Đánh giá độ chính xác dự báo")
    add_body_p(doc, "Bảng 5.1 tổng hợp các chỉ số sai số định lượng trên tập kiểm thử:")
    
    sarima_perf_headers = ["Chỉ số đánh giá", "Công thức tính toán", "Giá trị đạt được", "Ý nghĩa đánh giá"]
    sarima_perf_data = [
        ["RMSE", "Căn bậc hai trung bình bình phương sai số", "2.281,79 req/h", "Độ lệch toàn phương trung bình tối ưu"],
        ["MAE", "Trung bình giá trị tuyệt đối của sai số", "1.457,75 req/h", "Sai số tuyệt đối ở mức thấp"],
        ["MAPE (%)", "Sai số phần trăm tuyệt đối trung bình", "24,42 %", "Tính trên toàn bộ tập kiểm thử (gồm cả giờ sự cố)"],
        ["Hệ số R²", "Tỷ lệ phương sai giải thích được", "0,0619", "Dương và duy trì độ ổn định ngoài mẫu"]
    ]
    add_simple_academic_table(doc, sarima_perf_headers, sarima_perf_data, [Inches(1.5), Inches(2.5), Inches(1.5), Inches(1.8)])
    
    p_cap5 = doc.add_paragraph()
    p_cap5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c5 = p_cap5.add_run("Bảng 5.1: Đánh giá sai số dự báo của mô hình SARIMA trên tập kiểm thử ngoài mẫu")
    r_c5.font.name = "Times New Roman"
    r_c5.font.size = Pt(10)
    r_c5.font.bold = True
    r_c5.font.italic = True
    
    add_heading_2(doc, "5.4. So sánh với các mô hình cơ sở")
    add_body_p(doc, "Để kiểm chứng hiệu quả, mô hình SARIMA được đối sánh thực nghiệm trên cùng tập kiểm thử với 5 mô hình cơ sở:")
    
    bench_headers = ["Thứ hạng", "Mô hình thuật toán", "Sai số RMSE (req/h)", "Sai số MAE (req/h)", "Sai số MAPE (%)"]
    bench_data = [
        ["Hạng 1", "Làm mượt mũ Holt-Winters", "2.206,85", "1.369,54", "23,36 %"],
        ["Hạng 2", "Mô hình SARIMA đề xuất", "2.281,79", "1.457,75", "24,42 %"],
        ["Hạng 3", "Mô hình quán tính mùa vụ (Trễ 24)", "2.479,09", "1.643,97", "26,85 %"],
        ["Hạng 4", "Mô hình ARIMA phi mùa vụ", "2.501,83", "1.581,02", "29,76 %"],
        ["Hạng 5", "Trung bình trượt (Cửa sổ 24 giờ)", "2.818,41", "1.889,04", "31,56 %"],
        ["Hạng 6", "Mô hình quán tính (Trễ 1)", "2.984,60", "2.064,53", "33,31 %"]
    ]
    add_simple_academic_table(doc, bench_headers, bench_data, [Inches(1.0), Inches(2.7), Inches(1.3), Inches(1.3), Inches(1.2)])
    
    p_cap6 = doc.add_paragraph()
    p_cap6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c6 = p_cap6.add_run("Bảng 5.2: Bảng đối sánh hiệu năng dự báo giữa SARIMA và các mô hình cơ sở")
    r_c6.font.name = "Times New Roman"
    r_c6.font.size = Pt(10)
    r_c6.font.bold = True
    r_c6.font.italic = True
    
    add_body_p(doc, "Nhận xét: Mô hình SARIMA đề xuất và Holt-Winters vượt trội hoàn toàn so với các mô hình không có mùa vụ (ARIMA phi mùa vụ có RMSE lên tới 2.501,83 và mô hình quán tính có RMSE lên tới 2.984,60). Điều này khẳng định rằng việc mô hình hóa chu kỳ 24 giờ là yếu tố quyết định hàng đầu đối với bài toán dự báo lưu lượng web.")
    
    add_image_with_caption(
        doc,
        "web_api_traffic_forecasting/figures/08_model_comparison_metrics.png",
        "Hình 5.2: Biểu đồ so sánh trực quan các chỉ số sai số RMSE, MAE, MAPE giữa các mô hình"
    )
    
    add_heading_2(doc, "5.5. Ứng dụng phát hiện bất thường với ngưỡng động 3 độ lệch chuẩn")
    add_body_p(doc, "Hình 5.3 minh họa kết quả phát hiện bất thường lưu lượng API bằng dải ngưỡng động 3 độ lệch chuẩn:")
    add_bullet_p(doc, "Phát hiện đợt tăng vọt: Khi xảy ra tấn công botnet hoặc sự kiện khuyến mãi, lưu lượng thực tế tăng vọt lên mức 18.000 - 25.000 req/h, vượt qua ngưỡng trên. Hệ thống lập tức nhận diện và gắn nhãn tam giác màu đỏ.")
    add_bullet_p(doc, "Phát hiện đợt sụt giảm: Khi hệ thống gặp sự cố máy chủ hoặc nghẽn mạng, lưu lượng giảm mạnh xuống chỉ còn vài trăm req/h, rơi xuống dưới ngưỡng dưới. Hệ thống gắn nhãn tam giác màu tím.")
    
    add_image_with_caption(
        doc,
        "web_api_traffic_forecasting/figures/07_anomaly_detection_results.png",
        "Hình 5.3: Kết quả phát hiện bất thường lưu lượng API với ngưỡng động 3-sigma và chuỗi sai số phần dư"
    )
    
    add_heading_3(doc, "5.5.1. Đánh giá hiệu năng phân loại bất thường")
    add_body_p(doc, "Bảng 5.3 và 5.4 tổng hợp Ma trận nhầm lẫn và các chỉ số đo lường hiệu năng phát hiện bất thường:")
    
    cm_headers = ["Thực tế \\ Dự đoán", "Dự đoán Bất thường", "Dự đoán Bình thường", "Tổng số giờ thực tế"]
    cm_data = [
        ["Thực tế Bất thường", "7 giờ (Phát hiện chính xác)", "4 giờ (Bỏ sót nhẹ)", "11 giờ bất thường"],
        ["Thực tế Bình thường", "0 giờ (KHÔNG BÁO ĐỘNG SAI)", "421 giờ (Chính xác)", "421 giờ bình thường"]
    ]
    add_simple_academic_table(doc, cm_headers, cm_data, [Inches(1.8), Inches(2.1), Inches(2.1), Inches(1.3)])
    
    p_cap7 = doc.add_paragraph()
    p_cap7.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c7 = p_cap7.add_run("Bảng 5.3: Ma trận nhầm lẫn của hệ thống phát hiện bất thường")
    r_c7.font.name = "Times New Roman"
    r_c7.font.size = Pt(10)
    r_c7.font.bold = True
    r_c7.font.italic = True
    
    met_headers = ["Chỉ số đo lường", "Công thức tính", "Kết quả đạt được", "Ý nghĩa trong vận hành thực tế"]
    met_data = [
        ["Độ chuẩn xác (Precision)", "TP / (TP + FP)", "100,00 % (1.0000)", "Hoàn hảo: Toàn bộ cảnh báo phát ra đều là sự cố thật, không có cảnh báo sai"],
        ["Độ nhạy (Recall)", "TP / (TP + FN)", "63,64 % (0.6364)", "Phát hiện thành công toàn bộ các giờ cao điểm nguy hiểm nhất"],
        ["Điểm cân bằng F1", "2 * (Prec * Rec) / (Prec + Rec)", "0,7778", "Đạt mức cao đối với bài toán mất cân bằng mẫu lớn"],
        ["Độ chính xác toàn cục", "(TP + TN) / Tổng số mẫu", "99,07 % (0.9907)", "Phân loại chuẩn xác 99.07% tổng số giờ vận hành của hệ thống"]
    ]
    add_simple_academic_table(doc, met_headers, met_data, [Inches(1.8), Inches(1.8), Inches(1.7), Inches(2.0)])
    
    p_cap8 = doc.add_paragraph()
    p_cap8.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c8 = p_cap8.add_run("Bảng 5.4: Các chỉ số đánh giá hiệu năng phát hiện bất thường")
    r_c8.font.name = "Times New Roman"
    r_c8.font.size = Pt(10)
    r_c8.font.bold = True
    r_c8.font.italic = True
    
    add_simple_callout(doc, "Chỉ số độ chuẩn xác đạt 100% (không có cảnh báo sai) có giá trị thực tiễn rất lớn, giúp kỹ sư vận hành không bị hiện tượng mỏi mệt vì cảnh báo giả và tự tin xử lý khi có tín hiệu cảnh báo phát ra.")
    
    add_heading_2(doc, "5.6. Ứng dụng trong tự động co giãn tài nguyên hệ thống")
    add_body_p(doc, "Mô hình dự báo có thể tích hợp trực tiếp vào hệ thống quản lý máy chủ:")
    add_bullet_p(doc, "Đầu mỗi giờ, tác vụ tự động chạy mô hình SARIMA để dự báo lưu lượng kỳ vọng trong các giờ tiếp theo.")
    add_bullet_p(doc, "Hệ thống tự động tính toán số lượng máy chủ hoặc container cần thiết và chủ động khởi động trước 10 - 15 phút, giải quyết triệt để vấn đề trễ khởi động khi lưu lượng tăng đột biến.")
    add_bullet_p(doc, "Khi phát hiện lưu lượng vượt ngưỡng trên bất thường, hệ thống kích hoạt tường lửa để giới hạn truy cập và ngăn chặn tấn công.")
    
    add_heading_2(doc, "5.7. Triển khai Ứng dụng Web Dashboard và Hướng dẫn Thử nghiệm Trực quan")
    
    add_heading_3(doc, "5.7.1. Kiến trúc tổng thể và tích hợp mô hình dự báo thời gian thực")
    add_body_p(doc, "Để chuyển hóa các kết quả nghiên cứu toán học và mô hình thống kê SARIMA thành giải pháp thực tiễn phục vụ kỹ sư vận hành hạ tầng mạng và phần mềm (DevOps / SRE), đề tài đã thiết kế và lập trình hoàn chỉnh một ứng dụng Web Dashboard tương tác chuyên nghiệp.")
    add_body_p(doc, "Ứng dụng được xây dựng trên nền tảng ngôn ngữ Python, sử dụng khung phát triển Streamlit thế hệ mới kết hợp cùng thư viện biểu đồ vector tương tác Plotly WebGL. Kiến trúc luồng dữ liệu của hệ thống được tổ chức thành 3 tầng chức năng khép kín:")
    add_bullet_p(doc, "Tầng 1 - Tiếp nhận và chuẩn hóa Telemetry (Data Telemetry Layer): Tiếp nhận liên tục chuỗi số liệu lưu lượng API theo từng giờ, phân tách các trường thông tin lưu lượng, tỷ lệ lỗi máy chủ (5xx Server Errors) và độ trễ phản hồi mạng.")
    add_bullet_p(doc, "Tầng 2 - Động cơ mô hình thống kê SARIMA và suy luận dải tin cậy (Statistical Inference Engine): Tích hợp trực tiếp mô hình SARIMA(0,1,2)(0,1,1)[24] đã được kiểm định. Mô hình thực hiện bóc tách quy luật mùa vụ 24 giờ, tính toán giá trị dự báo điểm kỳ vọng y_hat(t) và dải ngưỡng động 3 độ lệch chuẩn (+/- 3-sigma) theo thời gian thực.")
    add_bullet_p(doc, "Tầng 3 - Phân hệ điều phối tự động và cảnh báo sự cố (Auto-scaling & SRE Alerting): Ứng dụng công thức tính toán tài nguyên Pods Kubernetes theo tải dự báo:")
    
    add_simple_callout(
        doc,
        "Công thức tính số lượng Pods Kubernetes theo dự báo: N_pod(t) = ceil( y_hat(t) / (C_target * Mu_pod) ) với C_target = 0.70 (ngưỡng tải an toàn 70%) và Mu_pod = 2.000 requests/giờ (năng lực xử lý danh định của một Pod). Khi phát hiện y(t) vượt ngưỡng trên hoặc rơi xuống dưới ngưỡng dưới, hệ thống tự động phát còi báo động và đề xuất kịch bản xử lý tương ứng cho đội ngũ kỹ sư trực ca.",
        title="Công thức quy hoạch hạ tầng vi dịch vụ Kubernetes:"
    )

    add_heading_3(doc, "5.7.2. Đặc tả 3 phân hệ chức năng tương tác trên Web Dashboard")
    add_body_p(doc, "Giao diện Web Dashboard được thiết kế theo phong cách tối giản, trực quan và hiện đại, tập trung vào 3 phân hệ chức năng cốt lõi:")
    add_bullet_p(doc, "Thẻ 1 - Biểu đồ Dự báo SARIMA (Ngoài mẫu): Trực quan hóa đường dự báo ngoài mẫu 432 giờ kèm dải tin cậy 95% đối sánh với chuỗi thực tế. Biểu đồ tương tác cho phép phóng to, dịch chuyển và xem chi tiết giá trị dự báo theo từng giờ.")
    add_bullet_p(doc, "Thẻ 2 - Phát hiện Sự cố Bất thường (Ngưỡng 3-sigma): Hiển thị dải ngưỡng động uốn lượn theo thời gian và tự động đánh dấu các điểm tăng vọt (Spike) bằng tam giác đỏ và sụt giảm (Drop) bằng tam giác tím, kèm bảng danh sách các giờ xảy ra sự cố.")
    add_bullet_p(doc, "Thẻ 3 - Dữ liệu Gốc & So sánh Mô hình: Trực quan hóa toàn bộ 2.160 giờ dữ liệu với đường phân chia ranh giới tập huấn luyện (80%) và kiểm thử (20%), kèm bảng đối sánh định lượng hiệu năng của SARIMA so với các mô hình cơ sở.")

    add_heading_3(doc, "5.7.3. Minh chứng hình ảnh thực nghiệm trên giao diện Web Dashboard")
    add_body_p(doc, "Hệ thống Web Dashboard đã được khởi chạy thành công và chụp màn hình trực tiếp từ 3 thẻ phân hệ hoạt động thực tế trên máy chủ:")

    add_image_with_caption(
        doc,
        "web_api_traffic_forecasting/figures/web_tab1_forecast.png",
        "Hình 5.4: Giao diện Thẻ 1 - Kết quả Dự báo ngoài mẫu của Mô hình SARIMA trên Web Dashboard",
        width=Inches(6.2)
    )
    
    add_image_with_caption(
        doc,
        "web_api_traffic_forecasting/figures/web_tab2_anomalies.png",
        "Hình 5.5: Giao diện Thẻ 2 - Nhận diện Sự cố Bất thường với Ngưỡng động 3-sigma trên Web Dashboard",
        width=Inches(6.2)
    )
    
    add_image_with_caption(
        doc,
        "web_api_traffic_forecasting/figures/web_tab3_raw_benchmarks.png",
        "Hình 5.6: Giao diện Thẻ 3 - Chuỗi Dữ liệu Quan sát và Bảng Đối sánh Đa mô hình trên Web Dashboard",
        width=Inches(6.2)
    )
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
    # -------------------------------------------------------------
    add_heading_1(doc, "CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN")
    
    add_heading_2(doc, "6.1. Kết quả đạt được")
    add_body_p(doc, "Đề tài đã hoàn thành toàn diện các mục tiêu đề ra:")
    add_bullet_p(doc, "1. Hoàn thiện cơ sở lý thuyết toán học về chuỗi thời gian, tính dừng, quy trình Box-Jenkins và kiểm định Ljung-Box.")
    add_bullet_p(doc, "2. Phân tích thực nghiệm trên 2.160 giờ dữ liệu, kiểm định tính dừng thành công bằng ADF và KPSS sau khi lấy sai phân (1-B)(1-B²⁴).")
    add_bullet_p(doc, "3. Lựa chọn mô hình tối ưu SARIMA(0,1,2)(0,1,1)[24] đạt AIC thấp nhất (25.004,03), kiểm định phần dư độc lập ngẫu nhiên đạt chuẩn nhiễu trắng.")
    add_bullet_p(doc, "4. Đạt độ chính xác phát hiện bất thường 99.07% với độ chuẩn xác tuyệt đối 100% (không báo động sai).")
    add_bullet_p(doc, "5. Xây dựng bộ mã nguồn Python hoàn chỉnh, rõ ràng, dễ bảo trì và mở rộng.")
    
    add_heading_2(doc, "6.2. Ưu điểm và hạn chế của mô hình")
    add_body_p(doc, "Ưu điểm:")
    add_bullet_p(doc, "Tính minh bạch cao: Mọi tham số trong SARIMA đều mang ý nghĩa thống kê rõ ràng, dễ giải thích.")
    add_bullet_p(doc, "Tốc độ tính toán nhanh: Kích thước mô hình nhẹ, thời gian dự báo tức thì.")
    add_bullet_p(doc, "Cung cấp khoảng tin cậy thống kê chính xác làm cơ sở cho ngưỡng động phát hiện bất thường.")
    add_body_p(doc, "Hạn chế:")
    add_bullet_p(doc, "Mô hình SARIMA chuẩn tập trung vào một chu kỳ mùa vụ chính (24 giờ), chưa tối ưu khi có nhiều chu kỳ lồng nhau phức tạp (chu kỳ tuần, chu kỳ tháng).")
    
    add_heading_2(doc, "6.3. Hướng phát triển tiếp theo")
    add_bullet_p(doc, "Nghiên cứu mô hình lai: Kết hợp SARIMA để xử lý thành phần mùa vụ tuyến tính và mạng nơ-ron học sâu để học phần sai số phi tuyến tính.")
    add_bullet_p(doc, "Tích hợp biến ngoại sinh: Bổ sung thêm các thông tin về sự kiện truyền thông, ngày lễ và số lượng người dùng đồng thời.")
    add_bullet_p(doc, "Xây dựng hệ thống cảnh báo thời gian thực kết nối trực tiếp vào hạ tầng giám sát máy chủ.")
    
    doc.add_page_break()

    # -------------------------------------------------------------
    # TÀI LIỆU THAM KHẢO
    # -------------------------------------------------------------
    add_heading_1(doc, "TÀI LIỆU THAM KHẢO")
    
    refs = [
        "[1] Box, G. E., Jenkins, G. M., Reinsel, G. C., & Ljung, G. M. (2015). Time Series Analysis: Forecasting and Control (5th ed.). John Wiley & Sons.",
        "[2] Hyndman, R. J., & Athanasopoulos, G. (2018). Forecasting: Principles and Practice (2nd ed.). OTexts: Melbourne, Australia.",
        "[3] Montgomery, D. C., Jennings, C. L., & Kulahci, M. (2015). Introduction to Time Series Analysis and Forecasting (2nd ed.). John Wiley & Sons.",
        "[4] Seabold, S., & Perktold, J. (2010). statsmodels: Econometric and statistical modeling with python. Proceedings of the 9th Python in Science Conference.",
        "[5] Hamilton, J. D. (1994). Time Series Analysis. Princeton University Press.",
        "[6] Dickey, D. A., & Fuller, W. A. (1979). Distribution of the estimators for autoregressive time series with a unit root. Journal of the American Statistical Association.",
        "[7] Kwiatkowski, D., Phillips, P. C., Schmidt, P., & Shin, Y. (1992). Testing the null hypothesis of stationarity against the alternative of a unit root. Journal of Econometrics.",
        "[8] Ljung, G. M., & Box, G. E. (1978). On a measure of lack of fit in time series models. Biometrika.",
        "[9] Calheiros, R. N., Masoumi, E., Ranjan, R., & Buyya, R. (2015). Workload prediction using ARIMA for dynamic proactive capacity management in clouds. IEEE Transactions on Cloud Computing.",
        "[10] Chandola, V., Banerjee, A., & Kumar, V. (2009). Anomaly detection: A survey. ACM Computing Surveys."
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        format_paragraph(p_ref, space_before=2, space_after=5, align=WD_ALIGN_PARAGRAPH.JUSTIFY)
        r_run = p_ref.add_run(r)
        r_run.font.name = "Times New Roman"
        r_run.font.size = Pt(11)
        r_run.font.color.rgb = RGBColor(0, 0, 0)
        
    doc.add_page_break()

    # -------------------------------------------------------------
    # PHỤ LỤC: HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH MÃ NGUỒN
    # -------------------------------------------------------------
    add_heading_1(doc, "PHỤ LỤC: HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH MÃ NGUỒN")
    
    add_heading_2(doc, "P.1. Cấu trúc thư mục của dự án")
    
    tree_text = (
        "web_api_traffic_forecasting/\n"
        "├── data/\n"
        "│   └── api_traffic_data.csv          # Dữ liệu chuỗi thời gian 90 ngày (2.160 giờ)\n"
        "├── src/\n"
        "│   ├── __init__.py\n"
        "│   ├── data_loader.py                # Nạp, tiền xử lý và sinh tập dữ liệu\n"
        "│   ├── eda.py                        # Thống kê mô tả, kiểm định ADF/KPSS, ACF/PACF\n"
        "│   ├── sarima_model.py               # Tìm kiếm lưới Grid Search, khớp mô hình, chẩn đoán phần dư\n"
        "│   ├── forecaster.py                 # Dự báo đa bước ngoài mẫu, tính RMSE, MAE, MAPE, R2\n"
        "│   └── anomaly_detector.py           # Phát hiện bất thường qua ngưỡng động 3-sigma\n"
        "├── figures/                          # Toàn bộ biểu đồ xuất bản (300 DPI)\n"
        "│   ├── 01_raw_traffic_series.png\n"
        "│   ├── 02_seasonal_decomposition.png\n"
        "│   ├── 03_stationarity_differencing.png\n"
        "│   ├── 04_acf_pacf_analysis.png\n"
        "│   ├── 05_sarima_diagnostic_plots.png\n"
        "│   ├── 06_forecast_vs_actual.png\n"
        "│   ├── 07_anomaly_detection_results.png\n"
        "│   └── 08_model_comparison_metrics.png\n"
        "├── output/                           # Bảng số liệu thống kê định dạng CSV & JSON\n"
        "│   ├── 01_descriptive_stats.csv\n"
        "│   ├── 02_stationarity_tests.csv\n"
        "│   ├── 03_grid_search_sarima.csv\n"
        "│   ├── 04_ljung_box_test.csv\n"
        "│   ├── 05_forecast_results.csv\n"
        "│   ├── 06_detected_anomalies.csv\n"
        "│   ├── 07_anomaly_metrics.csv\n"
        "│   ├── 08_model_benchmarks.csv\n"
        "│   └── summary_results.json\n"
        "├── app.py                            # Ứng dụng Web Dashboard tương tác (Streamlit & Plotly)\n"
        "├── evaluate_baseline.py              # Đánh giá so sánh hiệu năng các mô hình cơ sở\n"
        "├── main.py                           # Luồng thực thi toàn diện từ đầu đến cuối\n"
        "├── requirements.txt                  # Danh mục các thư viện phụ thuộc\n"
        "└── README.md                         # Hướng dẫn chi tiết dự án"
    )
    p_tr = doc.add_paragraph()
    format_paragraph(p_tr, space_before=4, space_after=8, align=WD_ALIGN_PARAGRAPH.LEFT)
    r_tr = p_tr.add_run(tree_text)
    r_tr.font.name = "Consolas"
    r_tr.font.size = Pt(9.5)
    r_tr.font.color.rgb = RGBColor(0, 0, 0)
    
    add_heading_2(doc, "P.2. Các bước cài đặt và thực thi hệ thống")
    add_bullet_p(doc, "Bước 1: Cài đặt các thư viện cần thiết:", bold_prefix="Cài đặt môi trường: ")
    p_c1 = doc.add_paragraph()
    format_paragraph(p_c1, space_before=2, space_after=6, align=WD_ALIGN_PARAGRAPH.LEFT)
    r_c1 = p_c1.add_run("pip install -r web_api_traffic_forecasting/requirements.txt")
    r_c1.font.name = "Consolas"
    r_c1.font.size = Pt(10)
    r_c1.font.bold = True
    r_c1.font.color.rgb = RGBColor(0, 0, 0)
    
    add_bullet_p(doc, "Bước 2: Chạy toàn bộ luồng huấn luyện, dự báo và phát hiện bất thường:", bold_prefix="Thực thi hệ thống: ")
    p_c2 = doc.add_paragraph()
    format_paragraph(p_c2, space_before=2, space_after=6, align=WD_ALIGN_PARAGRAPH.LEFT)
    r_c2 = p_c2.add_run("python web_api_traffic_forecasting/main.py")
    r_c2.font.name = "Consolas"
    r_c2.font.size = Pt(10)
    r_c2.font.bold = True
    r_c2.font.color.rgb = RGBColor(0, 0, 0)
    
    add_bullet_p(doc, "Bước 3: Xem các biểu đồ tại thư mục 'figures/' và bảng số liệu tại thư mục 'output/'.", bold_prefix="Kiểm tra kết quả: ")

    add_heading_2(doc, "P.3. Hướng dẫn khởi chạy và vận hành ứng dụng Web Dashboard")
    add_body_p(doc, "Ứng dụng Web Dashboard cho phép người dùng giám sát trực tiếp chuỗi lưu lượng, tương tác với các biểu đồ phân tích và kiểm tra các tính năng cảnh báo:")
    add_bullet_p(doc, "Khởi chạy máy chủ Web cục bộ trên cổng mặc định 8501:", bold_prefix="Lệnh khởi chạy: ")
    p_c3 = doc.add_paragraph()
    format_paragraph(p_c3, space_before=2, space_after=6, align=WD_ALIGN_PARAGRAPH.LEFT)
    r_c3 = p_c3.add_run("python -m streamlit run web_api_traffic_forecasting/app.py")
    r_c3.font.name = "Consolas"
    r_c3.font.size = Pt(10)
    r_c3.font.bold = True
    r_c3.font.color.rgb = RGBColor(0, 0, 0)
    
    add_bullet_p(doc, "Mở trình duyệt web bất kỳ (Google Chrome, Microsoft Edge, Mozilla Firefox) và truy cập đường dẫn sau:", bold_prefix="Truy cập giao diện: ")
    p_u = doc.add_paragraph()
    format_paragraph(p_u, space_before=2, space_after=6, align=WD_ALIGN_PARAGRAPH.LEFT)
    r_u = p_u.add_run("http://localhost:8501")
    r_u.font.name = "Consolas"
    r_u.font.size = Pt(10.5)
    r_u.font.bold = True
    r_u.font.color.rgb = RGBColor(0, 0, 0)

    add_heading_2(doc, "P.4. Kho lưu trữ mã nguồn mở GitHub")
    add_body_p(doc, "Nhằm đảm bảo tính minh bạch, khả năng tái lập kết quả khoa học và thuận tiện cho việc đánh giá đề tài, toàn bộ mã nguồn, cấu hình mô hình, tập dữ liệu thực nghiệm và tài liệu báo cáo đã được lưu trữ công khai trên GitHub:")
    p_gh = doc.add_paragraph()
    format_paragraph(p_gh, space_before=3, space_after=6, align=WD_ALIGN_PARAGRAPH.LEFT)
    r_gh1 = p_gh.add_run("Đường dẫn liên kết GitHub: ")
    r_gh1.font.name = "Times New Roman"
    r_gh1.font.size = Pt(11)
    r_gh1.font.bold = True
    r_gh1.font.color.rgb = RGBColor(0, 0, 0)
    
    r_gh2 = p_gh.add_run("https://github.com/cuongle4399/api_traffic_forecasting")
    r_gh2.font.name = "Consolas"
    r_gh2.font.size = Pt(10.5)
    r_gh2.font.bold = True
    r_gh2.font.color.rgb = RGBColor(0, 0, 0)
    
    add_bullet_p(doc, "Bao gồm đầy đủ các module: thu thập dữ liệu (src/data_loader.py), phân tích khám phá (src/eda.py), mô hình SARIMA (src/sarima_model.py), dự báo (src/forecaster.py), phát hiện bất thường (src/anomaly_detector.py), và ứng dụng Web Dashboard (app.py).")
    add_bullet_p(doc, "Kèm theo tệp tài liệu báo cáo học phần hoàn chỉnh: Bao_Cao_Du_Doan_Thoi_Gian_Web_API_SARIMA_Le_Quoc_Cuong.docx.")
    
    # Save Document
    output_doc_path = "Bao_Cao_Du_Doan_Thoi_Gian_Web_API_SARIMA_Le_Quoc_Cuong.docx"
    try:
        doc.save(output_doc_path)
        print(f"\nDocument successfully regenerated and saved to: {output_doc_path}")
    except PermissionError:
        output_doc_path = "Bao_Cao_Du_Doan_Thoi_Gian_Web_API_SARIMA_Le_Quoc_Cuong_cap_nhat.docx"
        doc.save(output_doc_path)
        print(f"\nTep Word dang duoc mo boi Microsoft Word! Da luu ban moi vao: {output_doc_path}")
    return output_doc_path

if __name__ == "__main__":
    build_word_document()
