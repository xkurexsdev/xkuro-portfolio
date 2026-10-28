#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tinh chỉnh giao diện chuẩn 100% phong cách Arkham Intelligence:
1. Bảng TRANSFERS:
   - Điều chỉnh grid-template-columns với kích thước các cột rộng rãi, chuyên nghiệp, chống triệt để lỗi đè chữ (overlap).
   - Dòng rút trộm Top 1:
     + Time: 5 mins ago
     + Action: Outflow (mũi tên đỏ ↗)
     + From: Patrick Xuan Kuan
     + To: Nhãn tối bo góc [Drainer] kèm địa chỉ Bitcoin `bc1q9x...7m2a` (xóa hoàn toàn Fake_Phishing).
     + Value: 1,096,000
     + Token: BTC
     + USD: -$88,114,592,670 (#ef4444 in đậm).
   - Giữ các cột tách biệt rõ ràng, min-width an toàn, cuộn ngang mượt mà.
2. Khu vực TOP COUNTERPARTIES:
   - Đồng bộ tiêu đề bảng sang tiếng Anh chuẩn Arkham:
     `#`, `COUNTERPARTY`, `% OUTFLOW`, `VOLUME`.
   - Vị trí Top 1:
     + Counterparty: Tag [Drainer] bc1q9x...7m2a
     + % Outflow: 100.0% kèm thanh tiến trình đỏ rực
     + Volume: $88.11B (font-mono in đậm).
   - Bố cục flex tách biệt rõ ràng giữa nhãn địa chỉ và khối lượng/tỷ trọng (gap: 12px), tuyệt đối không chồng chéo.
"""

from bs4 import BeautifulSoup

HTML_FILE = "index.html"


def refine_arkham_interface():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # =========================================================================
    # 1. BẢNG TRANSFERS: Tối ưu grid columns & cập nhật dòng giao dịch Top 1
    # =========================================================================
    transfers_btn = soup.find(lambda t: t.name == "button" and "TRANSFERS" == t.get_text().strip())
    if transfers_btn:
        transfers_body = transfers_btn.parent.parent.find_next_sibling()
        
        # 1.1 Đảm bảo xóa class blur
        for el in transfers_body.find_all(class_=lambda c: c and "blur" in str(c)):
            if "backdrop" not in str(el.get("class", [])):
                el["class"] = [c for c in el.get("class", []) if "blur" not in c]

        # 1.2 Tối ưu grid layout của Transfers: Cột TO và USD rộng rãi, không bị đè
        grid = transfers_body.find("div", class_=lambda c: c and "grid-rows-" in str(c))
        if grid:
            grid["style"] = "grid-template-columns: 0.5rem 2.25rem minmax(4.5rem, max-content) minmax(7rem, 1.2fr) minmax(12rem, 1.8fr) minmax(6rem, 1fr) minmax(4.5rem, 0.8fr) minmax(8.5rem, 1.2fr) 0.5rem; min-width: 740px; width: max-content;"
            scroll_wrapper = grid.parent
            if scroll_wrapper:
                scroll_wrapper["style"] = "overflow-x: auto !important; -webkit-overflow-scrolling: touch !important;"

        # 1.3 Cập nhật dòng Top 1 trong tbody
        tbody_transfers = transfers_body.find("div", class_=lambda c: c and "auto-rows-max" in str(c))
        if tbody_transfers:
            # Xóa các dòng rút trộm cũ nếu có
            for old_row in tbody_transfers.find_all("div", role="row"):
                txt = old_row.get_text()
                if "Drainer" in txt or "Fake_Phishing" in txt or "88,114,592,670" in txt or "14,983,724.72" in txt:
                    old_row.decompose()

            # Lấy avatar Patrick Xuan Kuan
            avatar_src = ""
            for img in soup.find_all("img"):
                if "patrick-xuan-kuan" in img.get("alt", "") and img.get("src", "").startswith("data:"):
                    avatar_src = img["src"]
                    break

            drain_row_html = f"""
            <div class="group/row relative grid transition-colors bg-red-950/25 hover:bg-red-900/35 text-xs duration-0 border-l-2 border-red-500" role="row" style="grid-column:1/-1;grid-template-columns:subgrid">
                <!-- Cell 0: Left spacer -->
                <div class="flex h-full min-w-0 items-center justify-start text-left px-0 py-0" role="cell" style="min-height:2.75rem"></div>

                <!-- Cell 1: Action (Outflow màu đỏ kèm icon mũi tên hướng ra ngoài) -->
                <div class="flex h-full min-w-0 items-center px-3 justify-start text-left pl-0.75 pr-1 py-1.25 shrink-0" role="cell" style="min-height:2.75rem">
                    <div class="flex items-center gap-1.5" title="Outflow">
                        <span class="inline-flex items-center justify-center size-5 rounded bg-red-500/20 text-red-400 border border-red-500/30">
                            <svg class="size-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 19.5l15-15m0 0H8.25m11.25 0v11.25"></path>
                            </svg>
                        </span>
                        <span class="text-[11px] font-semibold text-red-400 uppercase tracking-wider hidden sm:inline font-mono">Outflow</span>
                    </div>
                </div>

                <!-- Cell 2: Time (5 mins ago) -->
                <div class="flex h-full min-w-0 items-center justify-start text-left px-1 py-1.25 shrink-0" role="cell" style="min-height:2.75rem">
                    <span class="inline-flex min-w-0">
                        <span class="truncate text-xs font-semibold text-red-300 font-mono">5 mins ago</span>
                    </span>
                </div>

                <!-- Cell 3: From (Patrick Xuan Kuan) -->
                <div class="flex h-full min-w-0 items-center justify-start text-left px-1.5 py-1.25 overflow-hidden" role="cell" style="min-height:2.75rem">
                    <span class="relative flex items-center whitespace-nowrap max-w-full min-w-0 text-xs">
                        <span class="flex min-w-0 flex-1 items-center overflow-hidden gap-1.5">
                            <span class="size-4 shrink-0 overflow-hidden rounded-full ring-1 ring-slate-600">
                                <img alt="Patrick Xuan Kuan" class="size-full object-cover" src="{avatar_src}">
                            </span>
                            <span class="leading-[21px] font-medium text-white font-arkham-sans truncate">Patrick Xuan Kuan</span>
                        </span>
                    </span>
                </div>

                <!-- Cell 4: To (Địa chỉ Bitcoin chuẩn on-chain, nhãn Drainer màu đỏ nhạt, nền xám đen bo góc) -->
                <div class="flex h-full min-w-0 items-center justify-start text-left px-1.5 py-1.25 overflow-hidden" role="cell" style="min-height:2.75rem">
                    <span class="relative flex items-center whitespace-nowrap max-w-full min-w-0 text-xs">
                        <div class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded bg-[#161a23] border border-red-500/30 text-xs max-w-full">
                            <span class="px-1.5 py-0.2 rounded text-[10px] font-mono font-bold bg-red-500/20 text-red-400 border border-red-500/30 shrink-0">Drainer</span>
                            <span class="font-mono text-xs text-amber-200/90 font-medium truncate">bc1q9x...7m2a</span>
                        </div>
                    </span>
                </div>

                <!-- Cell 5: Value / Amount (1,096,000 BTC) -->
                <div class="flex h-full min-w-0 items-center justify-end text-right px-1.5 py-1.25 font-mono overflow-hidden" role="cell" style="min-height:2.75rem">
                    <div class="flex min-w-0 justify-end text-right">
                        <span class="inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums text-red-400 font-semibold truncate text-xs">
                            1,096,000
                        </span>
                    </div>
                </div>

                <!-- Cell 6: Token (BTC) -->
                <div class="flex h-full min-w-0 items-center justify-start text-left px-1.5 py-1.25 shrink-0 overflow-hidden" role="cell" style="min-height:2.75rem">
                    <span class="inline-flex items-center gap-1.5 font-mono text-xs text-white">
                        <span class="inline-flex shrink-0 items-center justify-center overflow-hidden rounded-full" style="width: 16px; height: 16px;">
                            <svg width="16" height="16" viewBox="0 0 32 32">
                                <circle cx="16" cy="16" fill="#F7931A" r="16"></circle>
                                <path d="M23.189 14.02c.314-2.096-1.283-3.223-3.465-3.975l.708-2.84-1.728-.43-.69 2.765c-.454-.114-.92-.22-1.385-.326l.695-2.783-1.728-.431-.708 2.839c-.376-.086-.745-.17-1.104-.26l.002-.008-2.384-.595-.46 1.846s1.283.294 1.256.312c.7.175.826.638.805 1.006l-.806 3.235c.048.012.11.03.18.057l-.183-.045-1.13 4.532c-.086.212-.303.531-.793.41.018.025-1.256-.314-1.256-.314l-.858 1.978 2.25.561c.418.105.828.215 1.231.318l-.715 2.872 1.727.43.708-2.84c.472.127.93.245 1.378.357l-.706 2.828 1.728.431.715-2.866c2.948.558 5.164.333 6.097-2.333.752-2.146-.037-3.385-1.588-4.192 1.13-.26 1.98-1.003 2.207-2.538zm-3.95 5.537c-.535 2.146-4.148.986-5.318.695l.949-3.805c1.17.292 4.929.872 4.369 3.11zm.536-5.567c-.487 1.953-3.495.96-4.47.718l.86-3.45c.975.242 4.117.694 3.61 2.732z" fill="#fff"></path>
                            </svg>
                        </span>
                        <span class="font-medium">BTC</span>
                    </span>
                </div>

                <!-- Cell 7: USD Value (-$88,114,592,670 màu đỏ in đậm #ef4444) -->
                <div class="flex h-full min-w-0 items-center px-3 justify-end text-right pl-1 pr-0.75 py-1.25 font-mono overflow-hidden" role="cell" style="min-height:2.75rem">
                    <div class="flex min-w-0 justify-end text-right">
                        <span class="inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums font-bold text-[#ef4444] truncate text-xs tracking-tight">
                            -$88,114,592,670
                        </span>
                    </div>
                </div>

                <!-- Cell 8: Right spacer -->
                <div class="flex h-full min-w-0 items-center justify-start text-left px-0 py-0" role="cell" style="min-height:2.75rem"></div>
            </div>
            """
            new_row_soup = BeautifulSoup(drain_row_html, "html.parser").find("div", role="row")
            tbody_transfers.insert(0, new_row_soup)
            print("  ✓ Đã cập nhật dòng rút trộm Transfers: bc1q9x...7m2a (Drainer) | 1,096,000 BTC | -$88,114,592,670.")

    # =========================================================================
    # 2. KHU VỰC TOP COUNTERPARTIES: Tiêu đề tiếng Anh & layout flex chống đè chữ
    # =========================================================================
    counterparties_btn = soup.find(lambda t: t.name == "button" and "TOP COUNTERPARTIES" in t.get_text())
    if counterparties_btn:
        tab_bar = counterparties_btn.parent
        header = tab_bar.parent
        body = header.find_next_sibling()
        body.clear()

        # Tạo bảng hoàn chỉnh với flexbox chuẩn, khoảng cách 12px, header tiếng Anh
        counterparties_html = """
        <div class="flex min-h-0 flex-1 flex-col overflow-hidden bg-(--data-panel-body-bg) p-3 font-arkham-sans">
            <!-- Filter Bar: All / Deposits / Withdrawals (Active) -->
            <div class="flex items-center justify-between border-b border-white/10 pb-2.5 mb-2.5">
                <div class="inline-flex items-center rounded-lg bg-slate-900/90 p-0.5 border border-white/10 text-xs font-mono">
                    <button class="px-2.5 py-1 rounded text-slate-400 hover:text-white transition-colors cursor-pointer" type="button">ALL</button>
                    <button class="px-2.5 py-1 rounded text-slate-400 hover:text-white transition-colors cursor-pointer" type="button">DEPOSITS</button>
                    <button class="px-2.5 py-1 rounded bg-red-500/20 text-red-400 border border-red-500/30 font-semibold transition-colors flex items-center gap-1.5 cursor-default" type="button">
                        <span class="size-1.5 rounded-full bg-red-500 animate-pulse"></span>
                        WITHDRAWALS
                    </button>
                </div>
                <span class="text-[11px] font-mono text-slate-400 hidden sm:inline uppercase tracking-wider">24H OUTFLOW ANALYSIS</span>
            </div>

            <!-- Bảng Counterparties chuẩn tiêu đề tiếng Anh: #, COUNTERPARTY, % OUTFLOW, VOLUME -->
            <div class="flex-1 min-h-0 overflow-y-auto scrollbar-thin">
                <table class="w-full text-left border-collapse text-xs font-mono">
                    <thead class="text-[11px] uppercase tracking-wider text-slate-400 border-b border-white/10 sticky top-0 bg-[#0f141d] z-10">
                        <tr>
                            <th class="py-2.5 px-2 text-center w-8">#</th>
                            <th class="py-2.5 px-3">COUNTERPARTY</th>
                            <th class="py-2.5 px-3 text-right">% OUTFLOW</th>
                            <th class="py-2.5 px-3 text-right">VOLUME</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-white/[0.04]">
                        <!-- TOP 1: DRAINER (Layout flex chống đè chữ, tách biệt rõ ràng) -->
                        <tr class="bg-red-950/25 hover:bg-red-950/35 transition-colors border-l-2 border-red-500">
                            <td class="py-3 px-2 text-center font-bold text-red-400">1</td>
                            <td class="py-3 px-3">
                                <div class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded bg-[#161a23] border border-red-500/30 text-xs">
                                    <span class="px-1.5 py-0.2 rounded text-[10px] font-mono font-bold bg-red-500/20 text-red-400 border border-red-500/30 shrink-0">Drainer</span>
                                    <span class="font-mono text-xs text-amber-200/90 font-medium">bc1q9x...7m2a</span>
                                </div>
                            </td>
                            <td class="py-3 px-3 text-right">
                                <div class="inline-flex flex-col items-end gap-1 w-28 sm:w-36">
                                    <span class="font-bold text-red-400 text-xs">100.0%</span>
                                    <div class="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                                        <div class="h-full bg-red-500 rounded-full shadow-[0_0_8px_rgba(239,68,68,0.7)]" style="width: 100%;"></div>
                                    </div>
                                </div>
                            </td>
                            <td class="py-3 px-3 text-right font-bold text-red-400 text-sm tracking-tight">
                                $88.11B
                            </td>
                        </tr>

                        <!-- Rank 2: Binance Cold Storage -->
                        <tr class="hover:bg-white/[0.02] transition-colors text-slate-500">
                            <td class="py-2.5 px-2 text-center">2</td>
                            <td class="py-2.5 px-3">
                                <div class="flex items-center gap-2">
                                    <span class="text-slate-400 font-sans">Binance: Cold Storage</span>
                                    <span class="text-[11px] text-slate-500 font-mono">bc1qxy...48kd</span>
                                </div>
                            </td>
                            <td class="py-2.5 px-3 text-right">
                                <div class="inline-flex flex-col items-end gap-1 w-28 sm:w-36">
                                    <span class="text-slate-500 text-xs">0.00%</span>
                                    <div class="w-full h-1 bg-slate-800 rounded-full"></div>
                                </div>
                            </td>
                            <td class="py-2.5 px-3 text-right text-slate-500 font-mono">$0.00</td>
                        </tr>

                        <!-- Rank 3: Coinbase Prime Custody -->
                        <tr class="hover:bg-white/[0.02] transition-colors text-slate-500">
                            <td class="py-2.5 px-2 text-center">3</td>
                            <td class="py-2.5 px-3">
                                <div class="flex items-center gap-2">
                                    <span class="text-slate-400 font-sans">Coinbase: Prime Custody</span>
                                    <span class="text-[11px] text-slate-500 font-mono">bc1q7w...921a</span>
                                </div>
                            </td>
                            <td class="py-2.5 px-3 text-right">
                                <div class="inline-flex flex-col items-end gap-1 w-28 sm:w-36">
                                    <span class="text-slate-500 text-xs">0.00%</span>
                                    <div class="w-full h-1 bg-slate-800 rounded-full"></div>
                                </div>
                            </td>
                            <td class="py-2.5 px-3 text-right text-slate-500 font-mono">$0.00</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Thanh cảnh báo chân bảng chuẩn tiếng Anh -->
            <div class="mt-2.5 pt-2 border-t border-white/5 flex items-center justify-between text-[11px] font-mono text-red-400 bg-red-950/15 px-2.5 py-1.5 rounded border border-red-500/20">
                <span class="flex items-center gap-1.5">
                    <span class="size-1.5 rounded-full bg-red-500 animate-ping"></span>
                    Security Alert: 100% of 24h outflow was drained to exploiter address
                </span>
                <span class="text-slate-500 hidden sm:inline">xKuro On-Chain Forensic</span>
            </div>
        </div>
        """
        body.append(BeautifulSoup(counterparties_html, "html.parser"))
        print("  ✓ Đã cập nhật bảng TOP COUNTERPARTIES chuẩn tiếng Anh (#, COUNTERPARTY, % OUTFLOW, VOLUME).")

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"💾 Đã lưu thay đổi hoàn tất vào {HTML_FILE}!")


if __name__ == "__main__":
    refine_arkham_interface()
