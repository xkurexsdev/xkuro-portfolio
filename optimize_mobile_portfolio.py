#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tối ưu hóa hoàn toàn giao diện bảng PORTFOLIO trên iPhone và sửa triệt để lỗi khoảng cách trống:
1. Di chuyển 5 hàng coin (BTC, ETH, SOL, XRP, TRX) từ Child 0 (contents) vào Child 1 (tbody grid):
   - Loại bỏ hoàn toàn khoảng cách trống khổng lồ (200px) do hàng coin bị đặt nhầm vào hàng tiêu đề CSS Grid.
2. Tối ưu cột CHAINS (Cell 2):
   - Giữ lại badge icon chain 16px x 16px sắc nét chuẩn Arkham.
   - Ẩn text tên chain trên màn hình nhỏ (chỉ hiện trên desktop: `hidden md:inline`), giúp giải phóng 70px chiều ngang.
3. Chống đè chữ (overlapping) trên iPhone:
   - Thêm `translate="no"` và class `notranslate` để Safari Translate không dịch "$" thành "đô la" hay "triệu đô la".
   - Thêm CSS `min-width: 520px` cho grid trên mobile kèm `-webkit-overflow-scrolling: touch` để cuộn ngang mượt mà.
4. Điều chỉnh chiều cao linh hoạt trên mobile:
   - Thay `h-[32em]` bằng `h-auto` để panel ôm sát 5 hàng coin, không còn khoảng trống đen ở dưới.
"""

from bs4 import BeautifulSoup

HTML_FILE = "index.html"


def optimize_portfolio():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    tab_portfolio = soup.find("button", id="btn-tab-portfolio")
    if not tab_portfolio:
        print("Không tìm thấy tab portfolio!")
        return

    header = tab_portfolio.parent.parent
    body = header.find_next_sibling()
    default_view = body.find("div", id="portfolio-view-default") or body.find("div", class_=lambda c: c and "contain-[layout_paint]" in str(c))
    
    # Đặt ID rõ ràng cho default view và thêm translate="no"
    default_view["id"] = "portfolio-view-default"
    default_view["translate"] = "no"
    default_view_classes = default_view.get("class", [])
    if "notranslate" not in default_view_classes:
        default_view["class"] = default_view_classes + ["notranslate"]

    # Bỏ h-[32em] trên mobile để không bị khoảng trống đen khổng lồ
    h32_div = default_view.find("div", class_=lambda c: c and "h-[32em]" in str(c))
    if h32_div:
        h32_div["class"] = [c for c in h32_div.get("class", []) if c != "h-[32em]"] + ["h-auto"]
        print("  ✓ Đã bỏ h-[32em] trên mobile, chuyển thành h-auto ôm sát dữ liệu.")

    # Tìm grid và 2 children (Child 0: contents/header, Child 1: tbody)
    grid = default_view.find("div", class_=lambda c: c and "grid-rows-" in str(c))
    children = [c for c in grid.children if getattr(c, "name", None)]
    if len(children) < 2:
        print("Cấu trúc grid không đủ 2 children!")
        return

    contents = children[0]
    tbody = children[1]

    # Đặt class định danh cho grid và scroll wrapper
    scroll_wrapper = grid.parent
    scroll_wrapper["class"] = [c for c in scroll_wrapper.get("class", [])] + ["portfolio-scroll-wrapper"]
    scroll_wrapper["style"] = "overflow-x: auto !important; -webkit-overflow-scrolling: touch !important;"

    grid["class"] = [c for c in grid.get("class", [])] + ["portfolio-table-grid"]
    grid["style"] = "grid-template-columns: 0.3125rem minmax(6.5rem, 1.4fr) minmax(2.5rem, 0.6fr) minmax(4.5rem, 0.9fr) minmax(3.5rem, 0.7fr) minmax(5.5rem, 1fr) minmax(4.5rem, 0.8fr) minmax(4.5rem, 0.8fr) 0.3125rem; min-width: 100%;"

    # Lấy các hàng data từ contents
    all_rows = contents.find_all("div", role="row")
    if len(all_rows) > 1:
        data_rows = all_rows[1:]
        print(f"Di chuyển {len(data_rows)} hàng coin từ Child 0 (contents) vào Child 1 (tbody)...")
        for r in data_rows:
            # Tối ưu Cell 2 (Chains)
            cells = r.find_all("div", role="cell")
            if len(cells) >= 3:
                cell2 = cells[2]
                text_span = cell2.find("span", class_=lambda c: c and "text-slate-400" in str(c))
                if text_span:
                    text_span["class"] = [c for c in text_span.get("class", []) if c != "truncate"] + ["hidden", "md:inline", "truncate"]
                
                # Đảm bảo các cell không bị đè chữ
                for cell in cells:
                    cell_style = cell.get("style", "")
                    if "overflow: hidden" not in cell_style:
                        cell["style"] = (cell_style + "; overflow: hidden;").strip("; ")

            # Trích xuất và đưa vào tbody
            r_extracted = r.extract()
            tbody.append(r_extracted)
        print("  ✓ Đã di chuyển toàn bộ hàng coin vào tbody thành công!")

    # Cập nhật style CSS chuyên biệt vào thẻ <style>
    style_tag = soup.find("style")
    if style_tag:
        mobile_fix_css = """
/* Tối ưu hóa bảng danh mục trên thiết bị di động (iPhone / Safari) */
@media (max-width: 640px) {
    .portfolio-scroll-wrapper {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        overscroll-behavior-x: contain;
    }
    .portfolio-table-grid {
        min-width: 520px !important;
        width: max-content !important;
    }
}
.portfolio-scroll-wrapper::-webkit-scrollbar {
    height: 4px;
}
.portfolio-scroll-wrapper::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 9999px;
}
"""
        if "portfolio-table-grid" not in style_tag.string:
            style_tag.string += "\n" + mobile_fix_css
            print("  ✓ Đã bổ sung CSS tối ưu iPhone cho .portfolio-table-grid vào <style>.")

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"💾 Đã lưu tối ưu hóa vào {HTML_FILE} thành công!")


if __name__ == "__main__":
    optimize_portfolio()
