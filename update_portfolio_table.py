#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script cập nhật danh mục đầu tư trong bảng PORTFOLIO theo thiết kế hình 1:
- Cập nhật số liệu chuẩn xác cho BTC (Bitcoin) và thêm đầy đủ ETH, SOL, XRP, TRON.
- Các con số Holdings, Price, Value, 24h PnL được phân bổ hợp lý, tổng giá trị đúng bằng $14,983,724.72.
- Thiết kế chuẩn token icon, chain badge, tabular numerals sáng rõ và % tăng trưởng xanh mướt.
"""

from bs4 import BeautifulSoup

HTML_FILE = "index.html"

# Danh sách 5 đồng coin với số liệu phân bổ chuẩn xác (Tổng = $14,983,724.72)
COIN_DATA = [
    {
        "symbol": "BTC",
        "name": "Bitcoin",
        "price": "$80,370",
        "price_change": "+0.21%",
        "price_is_up": True,
        "holdings": "111.86",
        "value": "$8.99M",
        "full_value": "$8,990,234.83",
        "pnl": "+0.21%",
        "pnl_is_up": True,
    },
    {
        "symbol": "ETH",
        "name": "Ethereum",
        "price": "$2,648.50",
        "price_change": "+1.85%",
        "price_is_up": True,
        "holdings": "1,414.36",
        "value": "$3.75M",
        "full_value": "$3,745,931.18",
        "pnl": "+1.85%",
        "pnl_is_up": True,
    },
    {
        "symbol": "SOL",
        "name": "Solana",
        "price": "$182.40",
        "price_change": "+3.42%",
        "price_is_up": True,
        "holdings": "8,214.76",
        "value": "$1.50M",
        "full_value": "$1,498,372.47",
        "pnl": "+3.42%",
        "pnl_is_up": True,
    },
    {
        "symbol": "XRP",
        "name": "XRP",
        "price": "$0.5390",
        "price_change": "-0.65%",
        "price_is_up": False,
        "holdings": "833.97K",
        "value": "$449.51K",
        "full_value": "$449,511.74",
        "pnl": "-0.65%",
        "pnl_is_up": False,
    },
    {
        "symbol": "TRX",
        "name": "Tron",
        "price": "$0.1652",
        "price_change": "+0.92%",
        "price_is_up": True,
        "holdings": "1.81M",
        "value": "$299.67K",
        "full_value": "$299,674.50",
        "pnl": "+0.92%",
        "pnl_is_up": True,
    },
]


def update_portfolio():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    tab_portfolio = soup.find("button", id="btn-tab-portfolio")
    header = tab_portfolio.parent.parent
    body = header.find_next_sibling()
    default_view = body.find("div", id="portfolio-view-default") or body.find("div", class_=lambda c: c and "contain-[layout_paint]" in str(c))

    rows = default_view.find_all("div", role="row")[1:]
    print(f"Tìm thấy {len(rows)} hàng coin trong danh mục mặc định.")

    for idx, r in enumerate(rows):
        if idx >= len(COIN_DATA):
            break
        data = COIN_DATA[idx]
        cells = r.find_all("div", role="cell")

        # Cell #3: Price
        cell3 = cells[3]
        cell3.clear()
        price_span = soup.new_tag("span", **{
            "class": "inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums text-inherit font-light"
        })
        price_span.string = data["price"]
        cell3.append(price_span)

        # Cell #4: 24h Price Change
        cell4 = cells[4]
        cell4.clear()
        btn4 = soup.new_tag("button", **{"class": "cursor-pointer", "type": "button"})
        color4 = "text-[var(--app-status-open-text)]" if data["price_is_up"] else "text-[var(--app-danger-text)]"
        span4 = soup.new_tag("span", **{
            "class": f"inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums font-light {color4}"
        })
        span4.string = data["price_change"]
        btn4.append(span4)
        cell4.append(btn4)

        # Cell #5: Holdings (Thiết kế chuẩn như hình 1)
        cell5 = cells[5]
        cell5.clear()
        span5_wrapper = soup.new_tag("span", **{
            "class": "flex min-w-0 cursor-pointer items-baseline justify-end gap-1.5"
        })
        # Lượng coin sáng rõ
        span5_val = soup.new_tag("span", **{
            "class": "inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums text-inherit font-light text-white"
        })
        span5_val.string = data["holdings"]
        # Ký hiệu coin màu xám dịu
        span5_sym = soup.new_tag("span", **{
            "class": "truncate text-(--data-panel-text-muted) font-extralight text-slate-400"
        })
        span5_sym.string = data["symbol"]
        span5_wrapper.append(span5_val)
        span5_wrapper.append(span5_sym)
        cell5.append(span5_wrapper)

        # Cell #6: Value (Giá trị USD sáng rõ)
        cell6 = cells[6]
        cell6.clear()
        span6_val = soup.new_tag("span", **{
            "class": "inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums text-inherit font-light text-white",
            "title": data["full_value"]
        })
        span6_val.string = data["value"]
        cell6.append(span6_val)

        # Cell #7: PnL / Share (+% xanh mướt)
        cell7 = cells[7]
        cell7.clear()
        btn7 = soup.new_tag("button", **{"class": "cursor-pointer", "type": "button"})
        color7 = "text-[var(--app-status-open-text)]" if data["pnl_is_up"] else "text-[var(--app-danger-text)]"
        span7_val = soup.new_tag("span", **{
            "class": f"inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums font-light {color7}"
        })
        span7_val.string = data["pnl"]
        btn7.append(span7_val)
        cell7.append(btn7)

        print(f"  ✓ {data['symbol']:4}: {data['price']:10} | {data['holdings']} {data['symbol']:4} | {data['value']:10} ({data['full_value']})")

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"💾 Đã cập nhật thành công {HTML_FILE}!")


if __name__ == "__main__":
    update_portfolio()
