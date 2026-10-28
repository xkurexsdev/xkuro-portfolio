#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script mô phỏng chính xác giao diện ví bị hacker rút sạch toàn bộ tài sản (drain wallet):
1. Đổi chỉ số biến động cạnh $0.00 thành -100.00% với màu đỏ #ef4444.
2. Vẽ đường biểu đồ Balances History rơi thẳng đứng 90 độ xuống sát đáy $0 (cliff drop).
3. Thay thế danh mục Portfolio bằng thông báo rỗng: <div class="text-center py-8 text-zinc-500">No assets found in wallet</div>.
4. Thêm giao dịch rút tiền Drainer: Inferno lên đầu bảng TRANSFERS:
   - 10 mins ago | Outflow (đỏ) | Patrick Xuan Kuan -> Drainer: Inferno (0x7a25...c4e9 Fake_Phishing) | -$14,983,724.72 (#ef4444).
"""

import re
import io
import base64
from bs4 import BeautifulSoup, NavigableString
from PIL import Image, ImageDraw

HTML_FILE = "index.html"


def simulate_drained_wallet():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # =========================================================================
    # 1. CHỈ SỐ % BIẾN ĐỘNG: Đổi +0.00% thành -100.00% màu đỏ cảnh báo #ef4444
    # =========================================================================
    balance_span = soup.find("span", class_=lambda c: c and "lg:text-2xl" in str(c))
    if balance_span:
        parent_box = balance_span.parent
        # Tìm span chứa % trong parent_box
        pct_span = None
        for s in parent_box.find_all("span"):
            if "%" in s.get_text():
                pct_span = s
                break
        if pct_span:
            pct_span.string = "-100.00%"
            pct_span["style"] = "color: #ef4444 !important; font-weight: 600;"
            print("✓ 1. Đã đổi chỉ số biến động thành -100.00% màu đỏ (#ef4444).")
        else:
            print("! Không tìm thấy span % trong parent_box")

    # =========================================================================
    # 2. BIỂU ĐỒ BALANCES HISTORY: Vẽ vách đá dựng đứng 90 độ lao xuống đáy $0
    # =========================================================================
    chart_div = soup.find("div", class_=lambda c: c and "tv-lightweight-charts" in str(c))
    if chart_div:
        canvases = chart_div.find_all("canvas")
        # Canvas 2 là canvas chính vẽ line biểu đồ
        if len(canvases) > 2:
            canvas_2 = canvases[2]
            style_str = canvas_2.get("style", "")
            match = re.search(r"url\((data:image/png;base64,[^)]+)\)", style_str)
            if match:
                raw_b64 = match.group(1).split(",")[1]
                img_data = base64.b64decode(raw_b64)
                img = Image.open(io.BytesIO(img_data)).convert("RGBA")
                
                # Tìm điểm cao nhất cuối cùng bên phải
                # Đã scan được: X=1124, Y=94
                x_drop = 1124
                y_top = 94
                y_bottom = 445  # Trục đáy sát $0
                
                draw = ImageDraw.Draw(img)
                line_color = (109, 165, 255, 255)  # Giữ nguyên màu xanh neon của đường vẽ
                
                # Vẽ vách đá dựng đứng đâm thẳng 90 độ xuống đáy
                draw.line([(x_drop, y_top), (x_drop, y_bottom)], fill=line_color, width=4)
                # Kéo dài đường nằm bệt sát đáy sang phải (flatline ở $0)
                draw.line([(x_drop, y_bottom), (x_drop + 36, y_bottom)], fill=line_color, width=4)
                
                # Lưu lại ảnh Base64
                out_buffer = io.BytesIO()
                img.save(out_buffer, format="PNG")
                new_b64 = base64.b64encode(out_buffer.getvalue()).decode("utf-8")
                new_data_url = f"data:image/png;base64,{new_b64}"
                
                # Thay thế vào style của canvas 2
                canvas_2["style"] = style_str.replace(match.group(1), new_data_url)
                print("✓ 2. Đã cập nhật biểu đồ Balances History với vách đá 90 độ cắm thẳng xuống $0.")
            else:
                print("! Không tìm thấy data URL trong Canvas 2")
        else:
            print("! Không tìm thấy đủ canvas trong chart_div")

    # =========================================================================
    # 3. DANH MỤC PORTFOLIO (BẢNG BÊN TRÁI): Thay thế bằng thông báo rỗng
    # =========================================================================
    portfolio_view = soup.find("div", id="portfolio-view-default")
    if portfolio_view:
        # Tìm tbody chứa các hàng coin
        grid = portfolio_view.find("div", class_=lambda c: c and "grid-rows-" in str(c))
        if grid:
            children = [c for c in grid.children if getattr(c, "name", None)]
            if len(children) >= 2:
                tbody = children[1]
                tbody.clear()
                
                # Tạo thẻ thông báo trạng thái rỗng chuẩn yêu cầu
                empty_tag = soup.new_tag("div", **{
                    "class": "text-center py-8 text-zinc-500 font-sans flex flex-col items-center justify-center w-full",
                    "style": "grid-column: 1 / -1; min-height: 12rem;"
                })
                empty_tag.append(BeautifulSoup("""
                    <div class="flex flex-col items-center justify-center gap-2">
                        <svg class="size-8 text-zinc-600 opacity-60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path>
                        </svg>
                        <div class="text-zinc-500 font-medium">No assets found in wallet</div>
                    </div>
                """, "html.parser"))
                tbody.append(empty_tag)
                print("✓ 3. Đã thay thế bảng danh mục Portfolio bằng thông báo: 'No assets found in wallet'.")

    # =========================================================================
    # 4. BẢNG GIAO DỊCH TRANSFERS: Thêm giao dịch rút sạch tiền lên đầu bảng
    # =========================================================================
    transfers_btn = soup.find(lambda t: t.name == "button" and "TRANSFERS" == t.get_text().strip())
    if transfers_btn:
        transfers_body = transfers_btn.parent.parent.find_next_sibling()
        # Tìm tbody của Transfers
        tbody_transfers = transfers_body.find("div", class_=lambda c: c and "auto-rows-max" in str(c))
        if tbody_transfers:
            # Lấy avatar Patrick Xuan Kuan từ thẻ img bất kỳ
            avatar_src = ""
            for img in soup.find_all("img"):
                if "patrick-xuan-kuan" in img.get("alt", "") and img.get("src", "").startswith("data:"):
                    avatar_src = img["src"]
                    break

            new_drain_row_html = f"""
            <div class="group/row relative grid transition-colors bg-red-950/20 hover:bg-red-900/30 text-xs duration-0 border-l-2 border-red-500 animate-pulse" role="row" style="grid-column:1/-1;grid-template-columns:subgrid">
                <!-- Cell 0: Left spacer -->
                <div class="flex h-full min-w-0 items-center justify-start text-left px-0 py-0" role="cell" style="min-height:2.75rem"></div>

                <!-- Cell 1: Action (Outflow màu đỏ kèm icon mũi tên hướng ra ngoài) -->
                <div class="flex h-full min-w-0 items-center px-3 justify-start text-left pl-0.75 pr-1 py-1.25" role="cell" style="min-height:2.75rem">
                    <div class="flex items-center gap-1.5" title="Outflow">
                        <span class="inline-flex items-center justify-center size-5 rounded bg-red-500/20 text-red-400 border border-red-500/30">
                            <svg class="size-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 19.5l15-15m0 0H8.25m11.25 0v11.25"></path>
                            </svg>
                        </span>
                        <span class="text-[11px] font-semibold text-red-400 uppercase tracking-wider hidden sm:inline">Outflow</span>
                    </div>
                </div>

                <!-- Cell 2: Time (10 mins ago) -->
                <div class="flex h-full min-w-0 items-center justify-start text-left px-1 py-1.25" role="cell" style="min-height:2.75rem">
                    <span class="inline-flex min-w-0">
                        <span class="truncate text-xs font-medium text-red-300">10 mins ago</span>
                    </span>
                </div>

                <!-- Cell 3: From (Patrick Xuan Kuan) -->
                <div class="flex h-full min-w-0 items-center justify-start text-left px-1.5 py-1.25" role="cell" style="min-height:2.75rem">
                    <span class="relative flex items-center whitespace-nowrap max-w-full min-w-0 text-xs">
                        <span class="flex min-w-0 flex-1 items-center overflow-hidden gap-1.5">
                            <span class="size-4 shrink-0 overflow-hidden rounded-full ring-1 ring-slate-600">
                                <img alt="Patrick Xuan Kuan" class="size-full object-cover" src="{avatar_src}">
                            </span>
                            <span class="leading-[21px] font-medium text-white font-arkham-sans truncate">Patrick Xuan Kuan</span>
                        </span>
                    </span>
                </div>

                <!-- Cell 4: To (0x7a25...c4e9 Fake_Phishing / Drainer: Inferno) -->
                <div class="flex h-full min-w-0 items-center justify-start text-left px-1.5 py-1.25" role="cell" style="min-height:2.75rem">
                    <span class="relative flex items-center whitespace-nowrap max-w-full min-w-0 text-xs">
                        <span class="flex min-w-0 flex-1 items-center overflow-hidden gap-1.5">
                            <span class="size-4 shrink-0 overflow-hidden rounded-full bg-red-950 border border-red-500/50 flex items-center justify-center text-[10px] text-red-400 font-bold">☠</span>
                            <span class="px-1.5 py-0.5 rounded text-[10px] font-mono font-bold bg-red-500/20 text-red-400 border border-red-500/30">Drainer: Inferno</span>
                            <span class="font-mono text-xs text-red-300/90 truncate">0x7a25...c4e9 (Fake_Phishing)</span>
                        </span>
                    </span>
                </div>

                <!-- Cell 5: Value / Amount -->
                <div class="flex h-full min-w-0 items-center justify-end text-right px-1 py-1.25 font-mono" role="cell" style="min-height:2.75rem">
                    <div class="flex min-w-0 justify-end text-right">
                        <span class="inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums text-red-400 font-semibold truncate text-xs">
                            ALL
                        </span>
                    </div>
                </div>

                <!-- Cell 6: Token -->
                <div class="flex h-full min-w-0 items-center justify-start text-left px-1 py-1.25" role="cell" style="min-height:2.75rem">
                    <span class="inline-flex items-center gap-1 font-mono text-xs text-red-400 font-medium">
                        <span class="px-1.5 py-0.5 rounded bg-red-950/40 border border-red-500/30 text-[10px]">MULTI</span>
                    </span>
                </div>

                <!-- Cell 7: USD Value (-$14,983,724.72 màu đỏ #ef4444) -->
                <div class="flex h-full min-w-0 items-center px-3 justify-end text-right pl-1 pr-0.75 py-1.25 font-mono" role="cell" style="min-height:2.75rem">
                    <div class="flex min-w-0 justify-end text-right">
                        <span class="inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums font-bold text-[#ef4444] truncate text-xs tracking-tight">
                            -$14,983,724.72
                        </span>
                    </div>
                </div>

                <!-- Cell 8: Right spacer -->
                <div class="flex h-full min-w-0 items-center justify-start text-left px-0 py-0" role="cell" style="min-height:2.75rem"></div>
            </div>
            """
            new_row_soup = BeautifulSoup(new_drain_row_html, "html.parser").find("div", role="row")
            tbody_transfers.insert(0, new_row_soup)
            print("✓ 4. Đã thêm giao dịch rút tiền Drainer: Inferno (-$14,983,724.72) lên đầu bảng TRANSFERS.")

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"💾 Đã lưu thay đổi vào {HTML_FILE} thành công!")


if __name__ == "__main__":
    simulate_drained_wallet()
