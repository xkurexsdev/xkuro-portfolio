#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script sửa dứt điểm kích thước biểu tượng các đồng coin (BTC, ETH, SOL, XRP, TRX):
- Chỉ tác động chính xác vào `svg.parent` (thẻ span bọc trực tiếp icon), KHÔNG chạm vào thẻ cha ngoài cùng chứa text.
- Đặt kích thước cố định tường minh (explicit inline styles & attributes) cho tất cả icon:
  + Icon Token (Cell #1): 18px x 18px (span và svg đều khóa chặt 18px)
  + Icon Chain (Cell #2): 16px x 16px (span và svg đều khóa chặt 16px)
  + Icon Chain trong tab Holdings by Chain: 20px x 20px
- Bổ sung CSS class hỗ trợ vào thẻ <style> để đảm bảo không bao giờ bị vỡ layout trên bất kỳ thiết bị/trình duyệt nào.
"""

from bs4 import BeautifulSoup

HTML_FILE = "index.html"


def fix_coin_icons():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # 1. Thêm CSS chuyên biệt vào thẻ <style>
    style_tag = soup.find("style")
    if style_tag:
        icon_css = """
/* Fix kích thước coin icons chống phình to */
.coin-icon-wrapper-18 {
    width: 18px !important;
    height: 18px !important;
    min-width: 18px !important;
    min-height: 18px !important;
    max-width: 18px !important;
    max-height: 18px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
    overflow: hidden !important;
    border-radius: 9999px !important;
}
.coin-icon-svg-18 {
    width: 18px !important;
    height: 18px !important;
    min-width: 18px !important;
    min-height: 18px !important;
    max-width: 18px !important;
    max-height: 18px !important;
    display: block !important;
    flex-shrink: 0 !important;
}
.coin-icon-wrapper-16 {
    width: 16px !important;
    height: 16px !important;
    min-width: 16px !important;
    min-height: 16px !important;
    max-width: 16px !important;
    max-height: 16px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
    overflow: hidden !important;
    border-radius: 9999px !important;
}
.coin-icon-svg-16 {
    width: 16px !important;
    height: 16px !important;
    min-width: 16px !important;
    min-height: 16px !important;
    max-width: 16px !important;
    max-height: 16px !important;
    display: block !important;
    flex-shrink: 0 !important;
}
.coin-icon-wrapper-20 {
    width: 20px !important;
    height: 20px !important;
    min-width: 20px !important;
    min-height: 20px !important;
    max-width: 20px !important;
    max-height: 20px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0 !important;
    overflow: hidden !important;
    border-radius: 9999px !important;
}
.coin-icon-svg-20 {
    width: 20px !important;
    height: 20px !important;
    min-width: 20px !important;
    min-height: 20px !important;
    max-width: 20px !important;
    max-height: 20px !important;
    display: block !important;
    flex-shrink: 0 !important;
}
"""
        if "coin-icon-wrapper-18" not in style_tag.string:
            style_tag.string += "\n" + icon_css

    # 2. Xử lý bảng PORTFOLIO chính (default_view)
    tab_portfolio = soup.find("button", id="btn-tab-portfolio")
    if tab_portfolio:
        header = tab_portfolio.parent.parent
        body = header.find_next_sibling()
        default_view = body.find("div", id="portfolio-view-default") or body.find("div", class_=lambda c: c and "contain-[layout_paint]" in str(c))
        if default_view:
            rows = default_view.find_all("div", role="row")[1:]
            print(f"Bắt đầu chuẩn hóa kích thước icon cho {len(rows)} hàng coin trong tab PORTFOLIO...")

            for idx, r in enumerate(rows):
                cells = r.find_all("div", role="cell")
                if len(cells) < 3:
                    continue

                # 2.1 Sửa Token Icon ở Cell #1 (18px x 18px)
                cell1 = cells[1]
                svg1 = cell1.find("svg")
                if svg1:
                    span1 = svg1.parent  # Chỉ lấy đúng span bọc trực tiếp SVG
                    span1["class"] = ["inline-flex", "shrink-0", "items-center", "justify-center", "overflow-hidden", "rounded-full", "coin-icon-wrapper-18"]
                    span1["style"] = "width: 18px !important; height: 18px !important; min-width: 18px !important; max-width: 18px !important; min-height: 18px !important; max-height: 18px !important; display: inline-flex !important; align-items: center !important; justify-content: center !important; flex-shrink: 0 !important; overflow: hidden !important; border-radius: 9999px !important;"
                    
                    svg1["width"] = "18"
                    svg1["height"] = "18"
                    svg1["class"] = ["coin-icon-svg-18"]
                    svg1["style"] = "width: 18px !important; height: 18px !important; min-width: 18px !important; min-height: 18px !important; max-width: 18px !important; max-height: 18px !important; display: block !important; flex-shrink: 0 !important;"

                # 2.2 Sửa Chain Icon ở Cell #2 (16px x 16px)
                cell2 = cells[2]
                svg2 = cell2.find("svg")
                if svg2:
                    span2 = svg2.parent  # Chỉ lấy đúng span bọc trực tiếp SVG
                    span2["class"] = ["inline-flex", "shrink-0", "items-center", "justify-center", "overflow-hidden", "rounded-full", "coin-icon-wrapper-16"]
                    span2["style"] = "width: 16px !important; height: 16px !important; min-width: 16px !important; max-width: 16px !important; min-height: 16px !important; max-height: 16px !important; display: inline-flex !important; align-items: center !important; justify-content: center !important; flex-shrink: 0 !important; overflow: hidden !important; border-radius: 9999px !important;"
                    
                    svg2["width"] = "16"
                    svg2["height"] = "16"
                    svg2["class"] = ["coin-icon-svg-16"]
                    svg2["style"] = "width: 16px !important; height: 16px !important; min-width: 16px !important; min-height: 16px !important; max-width: 16px !important; max-height: 16px !important; display: block !important; flex-shrink: 0 !important;"

                token_name = cells[1].get_text(separator=" ", strip=True)
                print(f"  ✓ Đã chuẩn hóa icon cho: {token_name}")

    # 3. Xử lý bảng Holdings by Chain (portfolio-view-holdings)
    holdings_view = soup.find("div", id="portfolio-view-holdings")
    if holdings_view:
        for svg in holdings_view.find_all("svg"):
            span = svg.parent
            span["class"] = ["inline-flex", "shrink-0", "rounded-full", "overflow-hidden", "coin-icon-wrapper-20"]
            span["style"] = "width: 20px !important; height: 20px !important; min-width: 20px !important; max-width: 20px !important; min-height: 20px !important; max-height: 20px !important; display: inline-flex !important; align-items: center !important; justify-content: center !important; flex-shrink: 0 !important; overflow: hidden !important; border-radius: 9999px !important;"
            
            svg["width"] = "20"
            svg["height"] = "20"
            svg["class"] = ["coin-icon-svg-20"]
            svg["style"] = "width: 20px !important; height: 20px !important; min-width: 20px !important; min-height: 20px !important; max-width: 20px !important; max-height: 20px !important; display: block !important; flex-shrink: 0 !important;"
        print("  ✓ Đã chuẩn hóa icon cho tab Holdings by Chain (20px)")

    # 4. Ghi lại kết quả
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"💾 Đã lưu thay đổi vào {HTML_FILE} thành công!")


if __name__ == "__main__":
    fix_coin_icons()
