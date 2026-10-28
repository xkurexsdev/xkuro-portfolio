#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script đặt tất cả con số trong bảng danh mục PORTFOLIO và các số dư về 0:
- Giá token (Price): $0.00
- Biến động giá 24h (%): 0.00% (màu xám trung tính text-slate-400)
- Lượng nắm giữ (Holdings): 0.00 BTC / ETH / SOL / XRP / TRX
- Giá trị danh mục (Value): $0.00
- Lãi/lỗ 24h (PnL): 0.00% (màu xám trung tính text-slate-400)
- Đồng bộ số dư hiện tại trong tab Timeline về $0.00 để toàn bộ trang nhất quán tuyệt đối.
"""

from bs4 import BeautifulSoup, NavigableString

HTML_FILE = "index.html"

TOKENS = ["BTC", "ETH", "SOL", "XRP", "TRX"]


def set_all_numbers_to_zero():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    view = soup.find("div", id="portfolio-view-default")
    if not view:
        print("Không tìm thấy portfolio-view-default!")
        return

    rows = view.find_all("div", role="row")[1:]
    print(f"Cập nhật {len(rows)} hàng coin về số 0...")

    for idx, r in enumerate(rows):
        cells = r.find_all("div", role="cell")
        if len(cells) < 8:
            continue

        sym = TOKENS[idx] if idx < len(TOKENS) else "TOKEN"

        # 1. Cell 3: Price -> $0.00
        cell3 = cells[3]
        cell3.clear()
        price_span = soup.new_tag("span", **{
            "class": "inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums text-inherit font-light notranslate",
            "translate": "no"
        })
        price_span.string = "$0.00"
        cell3.append(price_span)

        # 2. Cell 4: 24h Price Change -> 0.00%
        cell4 = cells[4]
        cell4.clear()
        btn4 = soup.new_tag("button", **{"class": "cursor-pointer", "type": "button"})
        span4 = soup.new_tag("span", **{
            "class": "inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums font-light text-slate-400 notranslate",
            "translate": "no"
        })
        span4.string = "0.00%"
        btn4.append(span4)
        cell4.append(btn4)

        # 3. Cell 5: Holdings -> 0.00 {SYM}
        cell5 = cells[5]
        cell5.clear()
        span5_wrapper = soup.new_tag("span", **{
            "class": "flex min-w-0 cursor-pointer items-baseline justify-end gap-1.5"
        })
        span5_val = soup.new_tag("span", **{
            "class": "inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums text-inherit font-light text-white notranslate",
            "translate": "no"
        })
        span5_val.string = "0.00"
        span5_sym = soup.new_tag("span", **{
            "class": "truncate text-(--data-panel-text-muted) font-extralight text-slate-400"
        })
        span5_sym.string = sym
        span5_wrapper.append(span5_val)
        span5_wrapper.append(span5_sym)
        cell5.append(span5_wrapper)

        # 4. Cell 6: Value -> $0.00
        cell6 = cells[6]
        cell6.clear()
        span6_val = soup.new_tag("span", **{
            "class": "inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums text-inherit font-light text-white notranslate",
            "title": "$0.00",
            "translate": "no"
        })
        span6_val.string = "$0.00"
        cell6.append(span6_val)

        # 5. Cell 7: 24h PnL -> 0.00%
        cell7 = cells[7]
        cell7.clear()
        btn7 = soup.new_tag("button", **{"class": "cursor-pointer", "type": "button"})
        span7_val = soup.new_tag("span", **{
            "class": "inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums font-light text-slate-400 notranslate",
            "translate": "no"
        })
        span7_val.string = "0.00%"
        btn7.append(span7_val)
        cell7.append(btn7)

        print(f"  ✓ {sym:4}: Price=$0.00 | Change=0.00% | Holdings=0.00 {sym:4} | Value=$0.00 | PnL=0.00%")

    # 6. Đồng bộ số dư hiện tại trong timeline header
    timeline_view = soup.find("div", id="portfolio-view-timeline")
    if timeline_view:
        for span in timeline_view.find_all("span"):
            if "$14,983,724.72" in span.get_text():
                span.string = "$0.00"
                print("  ✓ Đã cập nhật số dư hiện tại trong tab Timeline thành $0.00")
            elif "+6,000.8%" in span.get_text():
                span.string = "0.00%"
                print("  ✓ Đã cập nhật tổng tăng trưởng trong tab Timeline thành 0.00%")

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"💾 Đã lưu toàn bộ số liệu về 0 vào {HTML_FILE} thành công!")


if __name__ == "__main__":
    set_all_numbers_to_zero()
