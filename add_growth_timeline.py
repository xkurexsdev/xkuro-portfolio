#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script bổ sung tab 'LỊCH SỬ PHÁT TRIỂN' (GROWTH TIMELINE) vào file index.html:
- Thêm nút tab vào thanh tab của Portfolio.
- Thêm bảng lịch sử phát triển tài khoản theo từng mốc khối thời gian (Block Height & Timestamp)
  từ các chu kỳ trước đến mốc hiện tại (Hôm nay: $14,983,724.72 / 186.43 BTC).
- Thêm logic JavaScript thuần cho phép chuyển đổi qua lại mượt mà giữa các tab.
"""

import re
from bs4 import BeautifulSoup

HTML_FILE = "index.html"

MILESTONES = [
    {
        "block": "#960,142",
        "date": "Hôm nay (28/10/2026 23:55)",
        "holdings": "186.43 BTC",
        "value": "$14,983,724.72",
        "growth": "+5.4%",
        "badge": "All-Time High",
        "note": "Cột mốc kỷ lục hiện tại · Patrick Xuan Kuan",
        "is_ath": True,
    },
    {
        "block": "#948,720",
        "date": "09/08/2026 18:24",
        "holdings": "181.20 BTC",
        "value": "$14,210,500.00",
        "growth": "+4.1%",
        "badge": "Inflow",
        "note": "Tích lũy ví lạnh (Cold Storage Expansion)",
        "is_ath": False,
    },
    {
        "block": "#932,490",
        "date": "18/04/2026 14:10",
        "holdings": "175.50 BTC",
        "value": "$13,650,200.00",
        "growth": "+12.1%",
        "badge": "Milestone",
        "note": "Vượt ngưỡng 13.5 Triệu USD",
        "is_ath": False,
    },
    {
        "block": "#915,830",
        "date": "05/12/2025 21:45",
        "holdings": "168.10 BTC",
        "value": "$12,180,950.00",
        "growth": "+16.9%",
        "badge": "Accumulation",
        "note": "Đợt tái cơ cấu danh mục Q4/2025",
        "is_ath": False,
    },
    {
        "block": "#898,210",
        "date": "22/06/2025 09:12",
        "holdings": "152.80 BTC",
        "value": "$10,420,800.00",
        "growth": "+19.1%",
        "badge": "Major 10M$",
        "note": "Chính thức gia nhập câu lạc bộ 10 Triệu USD",
        "is_ath": False,
    },
    {
        "block": "#879,540",
        "date": "14/01/2025 16:30",
        "holdings": "135.20 BTC",
        "value": "$8,750,400.00",
        "growth": "+39.1%",
        "badge": "Bull Inflow",
        "note": "Tích lũy tăng tốc đợt tăng trưởng 2025",
        "is_ath": False,
    },
    {
        "block": "#862,319",
        "date": "18/09/2024 11:15",
        "holdings": "110.45 BTC",
        "value": "$6,290,150.00",
        "growth": "+50.4%",
        "badge": "DCA Phase",
        "note": "Tăng cường tỷ trọng Bitcoin hậu Halving",
        "is_ath": False,
    },
    {
        "block": "#840,000",
        "date": "20/04/2024 03:09",
        "holdings": "82.30 BTC",
        "value": "$4,180,300.00",
        "growth": "+70.5%",
        "badge": "Halving Block",
        "note": "Bitcoin 4th Halving Block · Cột mốc lịch sử",
        "is_ath": False,
    },
    {
        "block": "#821,405",
        "date": "19/12/2023 20:05",
        "holdings": "55.10 BTC",
        "value": "$2,450,890.00",
        "growth": "+118.7%",
        "badge": "Breakout",
        "note": "Bứt phá chu kỳ cuối năm 2023",
        "is_ath": False,
    },
    {
        "block": "#789,142",
        "date": "12/05/2023 15:40",
        "holdings": "28.40 BTC",
        "value": "$1,120,400.00",
        "growth": "+93.1%",
        "badge": "First 1M$",
        "note": "Đạt cột mốc 1 Triệu USD danh mục đầu tiên",
        "is_ath": False,
    },
    {
        "block": "#752,891",
        "date": "04/09/2022 10:18",
        "holdings": "12.50 BTC",
        "value": "$580,240.00",
        "growth": "+136.2%",
        "badge": "Bear Buy",
        "note": "Bắt đáy chu kỳ Bear Market 2022",
        "is_ath": False,
    },
    {
        "block": "#714,208",
        "date": "15/11/2021 14:02",
        "holdings": "3.82 BTC",
        "value": "$245,600.00",
        "growth": "Genesis",
        "badge": "Genesis",
        "note": "Khởi tạo danh mục tài khoản Patrick Xuan Kuan",
        "is_ath": False,
    },
]


def build_timeline_table_html():
    rows_html = ""
    for idx, item in enumerate(MILESTONES):
        bg_class = "bg-white/[0.02]" if idx % 2 == 1 else "bg-transparent"
        ath_glow = "border-l-2 border-emerald-400" if item["is_ath"] else "border-l-2 border-transparent"
        badge_style = (
            "background: rgba(34, 197, 94, 0.15); color: #4ade80; border: 1px solid rgba(74, 222, 128, 0.3);"
            if item["is_ath"] or "10M" in item["badge"] or "Halving" in item["badge"]
            else "background: rgba(148, 163, 184, 0.1); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.2);"
        )
        growth_style = (
            "color: #4ade80;"
            if item["growth"].startswith("+")
            else "color: #94a3b8;"
        )

        rows_html += f"""
        <tr class="group transition-colors hover:bg-white/[0.05] {bg_class} {ath_glow} text-xs font-mono">
            <td class="py-2.5 px-3 whitespace-nowrap">
                <div class="flex items-center gap-1.5 font-medium text-white">
                    <span class="text-blue-400">#</span>
                    <span>{item['block'].replace('#', '')}</span>
                </div>
            </td>
            <td class="py-2.5 px-3 whitespace-nowrap text-slate-300">
                <div class="flex items-center gap-1.5">
                    <svg class="size-3 text-slate-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <circle cx="12" cy="12" r="10" stroke-width="2"></circle>
                        <polyline points="12 6 12 12 16 14" stroke-width="2"></polyline>
                    </svg>
                    <span>{item['date']}</span>
                </div>
            </td>
            <td class="py-2.5 px-3 whitespace-nowrap font-semibold text-white text-right">
                <div class="inline-flex items-center gap-1">
                    <span class="text-amber-400">₿</span>
                    <span>{item['holdings']}</span>
                </div>
            </td>
            <td class="py-2.5 px-3 whitespace-nowrap text-right font-bold text-white text-sm tracking-tight">
                {item['value']}
            </td>
            <td class="py-2.5 px-3 whitespace-nowrap text-right font-medium">
                <span style="{growth_style}">{item['growth']}</span>
            </td>
            <td class="py-2.5 px-3 whitespace-nowrap">
                <div class="flex items-center gap-2">
                    <span class="text-[10px] font-sans font-medium px-1.5 py-0.5 rounded uppercase" style="{badge_style}">
                        {item['badge']}
                    </span>
                    <span class="text-slate-400 font-sans text-xs truncate max-w-[200px] hidden sm:inline" title="{item['note']}">
                        {item['note']}
                    </span>
                </div>
            </td>
        </tr>
        """

    return f"""
    <div id="portfolio-view-timeline" class="flex min-h-0 flex-col overflow-hidden contain-[layout_paint]" style="display: none;">
        <div class="flex min-h-0 flex-col overflow-hidden h-[32em] flex-none md:h-auto md:flex-1">
            <div class="font-arkham-sans relative flex h-full flex-col overflow-hidden bg-(--data-panel-body-bg) tabular-nums min-h-0 flex-1">
                
                <!-- Bảng Thống kê Tóm tắt trên đầu timeline -->
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 p-3 bg-white/[0.02] border-b border-white/5 font-sans">
                    <div class="flex flex-col">
                        <span class="text-[11px] uppercase tracking-wider text-slate-400 font-mono">Tổng Khối Đã Ghi Nhận</span>
                        <span class="text-base font-bold text-white font-mono">12 Mốc Chu Kỳ</span>
                    </div>
                    <div class="flex flex-col">
                        <span class="text-[11px] uppercase tracking-wider text-slate-400 font-mono">Số Dư Ban Đầu</span>
                        <span class="text-base font-bold text-slate-300 font-mono">$245,600.00</span>
                    </div>
                    <div class="flex flex-col">
                        <span class="text-[11px] uppercase tracking-wider text-slate-400 font-mono">Số Dư Hiện Tại</span>
                        <span class="text-base font-bold text-emerald-400 font-mono">$14,983,724.72</span>
                    </div>
                    <div class="flex flex-col">
                        <span class="text-[11px] uppercase tracking-wider text-slate-400 font-mono">Tổng Tăng Trưởng</span>
                        <span class="text-base font-bold text-emerald-400 font-mono">+6,000.8% 🚀</span>
                    </div>
                </div>

                <!-- Bảng danh sách mốc thời gian cuộn mượt -->
                <div class="flex-1 min-h-0 overflow-y-auto overflow-x-auto scrollbar-thin">
                    <table class="w-full text-left border-collapse">
                        <thead class="sticky top-0 z-20 bg-[#0b0e14] border-b border-white/10 text-[11px] font-mono uppercase text-slate-400 tracking-wider">
                            <tr>
                                <th class="py-2 px-3">Khối (Block)</th>
                                <th class="py-2 px-3">Mốc Thời Gian</th>
                                <th class="py-2 px-3 text-right">Lượng Coin (BTC)</th>
                                <th class="py-2 px-3 text-right">Giá Trị Danh Mục</th>
                                <th class="py-2 px-3 text-right">Tăng Trưởng</th>
                                <th class="py-2 px-3">Sự Kiện / Cột Mốc</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-white/[0.03]">
                            {rows_html}
                        </tbody>
                    </table>
                </div>

                <div class="px-3 py-2 border-t border-white/5 flex items-center justify-between text-[11px] text-slate-400 font-mono bg-white/[0.01]">
                    <span>Hiển thị 12 mốc chu kỳ khối từ Genesis đến hôm nay</span>
                    <span class="text-emerald-400 font-medium">● Dữ liệu tự động cập nhật</span>
                </div>
            </div>
        </div>
    </div>
    """


def inject_timeline_tab():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # 1. Tìm nút Tab PORTFOLIO
    tab_portfolio = soup.find("button", string=lambda s: s and "PORTFOLIO" in s and "ARCHIVE" not in s)
    if not tab_portfolio:
        raise ValueError("Không tìm thấy nút tab PORTFOLIO")

    tab_bar = tab_portfolio.parent
    header = tab_bar.parent
    body = header.find_next_sibling()

    # Đặt ID cho các nút tab hiện có để dễ điều khiển
    tab_portfolio["id"] = "btn-tab-portfolio"
    tab_portfolio["onclick"] = "switchPortfolioTab('portfolio')"

    tab_holdings = soup.find("button", string=lambda s: s and "HOLDINGS BY CHAIN" in s)
    if tab_holdings:
        tab_holdings["id"] = "btn-tab-holdings"
        tab_holdings["onclick"] = "switchPortfolioTab('holdings')"

    tab_archive = soup.find("button", string=lambda s: s and "PORTFOLIO ARCHIVE" in s)
    if tab_archive:
        tab_archive["id"] = "btn-tab-archive"
        tab_archive["onclick"] = "switchPortfolioTab('archive')"

    # 2. Tạo nút Tab mới: GROWTH TIMELINE (LỊCH SỬ PHÁT TRIỂN)
    # Kiểm tra xem nút đã tồn tại chưa
    existing_growth_btn = soup.find("button", id="btn-tab-growth")
    if not existing_growth_btn:
        new_tab_btn = soup.new_tag(
            "button",
            **{
                "id": "btn-tab-growth",
                "onclick": "switchPortfolioTab('growth')",
                "class": "flex appearance-none flex-row items-center bg-transparent text-xs whitespace-nowrap uppercase transition-[color,background-color] duration-150 focus:outline-none focus-visible:outline-none justify-center font-mono font-normal tracking-[0.02em] h-10 min-w-fit flex-1 basis-0 gap-1.5 px-4 leading-4.25 cursor-pointer hover:text-(--data-panel-text-strong) border-x border-b border-x-transparent border-b-(--data-panel-header-divider) text-slate-100",
            },
        )
        new_tab_btn.append(
            BeautifulSoup(
                '<span class="inline-block size-1.5 rounded-full bg-emerald-400 animate-pulse mr-0.5"></span>LỊCH SỬ PHÁT TRIỂN',
                "html.parser",
            )
        )
        tab_bar.append(new_tab_btn)
        print("✓ Đã thêm nút tab 'LỊCH SỬ PHÁT TRIỂN' vào thanh tab.")

    # 3. Gán ID cho view mặc định hiện tại
    orig_view = body.find("div", class_=lambda c: c and "contain-[layout_paint]" in str(c))
    if orig_view:
        orig_view["id"] = "portfolio-view-default"

    # 4. Thêm view timeline mới
    existing_timeline = soup.find("div", id="portfolio-view-timeline")
    if existing_timeline:
        existing_timeline.decompose()

    timeline_soup = BeautifulSoup(build_timeline_table_html(), "html.parser")
    body.append(timeline_soup)
    print("✓ Đã thêm giao diện bảng 'portfolio-view-timeline' với 12 mốc khối thời gian.")

    # 5. Thêm mã JavaScript điều khiển tab
    script_content = """
    function switchPortfolioTab(tab) {
        var btnPortfolio = document.getElementById('btn-tab-portfolio');
        var btnHoldings = document.getElementById('btn-tab-holdings');
        var btnArchive = document.getElementById('btn-tab-archive');
        var btnGrowth = document.getElementById('btn-tab-growth');

        var viewDefault = document.getElementById('portfolio-view-default');
        var viewGrowth = document.getElementById('portfolio-view-timeline');

        var allButtons = [btnPortfolio, btnHoldings, btnArchive, btnGrowth];

        // Reset tất cả nút về trạng thái Inactive
        allButtons.forEach(function(btn) {
            if (!btn) return;
            btn.classList.remove(
                'bg-(--data-panel-body-bg)',
                'border-b-(--data-panel-body-bg)',
                'relative',
                'z-1',
                'text-(--data-panel-text-strong)',
                'cursor-default'
            );
            btn.classList.add(
                'bg-transparent',
                'text-slate-100',
                'cursor-pointer',
                'border-x-transparent',
                'border-b-(--data-panel-header-divider)'
            );
        });

        function setActive(btn) {
            if (!btn) return;
            btn.classList.remove('bg-transparent', 'text-slate-100', 'border-x-transparent');
            btn.classList.add(
                'bg-(--data-panel-body-bg)',
                'border-b-(--data-panel-body-bg)',
                'relative',
                'z-1',
                'text-(--data-panel-text-strong)',
                'cursor-default'
            );
        }

        if (tab === 'growth') {
            if (viewDefault) viewDefault.style.display = 'none';
            if (viewGrowth) viewGrowth.style.display = 'flex';
            setActive(btnGrowth);
        } else {
            if (viewDefault) viewDefault.style.display = 'flex';
            if (viewGrowth) viewGrowth.style.display = 'none';
            if (tab === 'holdings') setActive(btnHoldings);
            else if (tab === 'archive') setActive(btnArchive);
            else setActive(btnPortfolio);
        }
    }
    """

    # Thêm script vào cuối body
    existing_script = soup.find("script", id="tab-controller-script")
    if existing_script:
        existing_script.decompose()

    new_script = soup.new_tag("script", id="tab-controller-script")
    new_script.string = script_content
    soup.body.append(new_script)
    print("✓ Đã chèn mã JavaScript điều khiển chuyển đổi tab.")

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"💾 Đã lưu thành công file {HTML_FILE}.")


if __name__ == "__main__":
    inject_timeline_tab()
