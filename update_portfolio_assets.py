#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script cập nhật danh mục tài sản theo yêu cầu người dùng:
1. Đổi số dư tổng trên đỉnh về $0.00 (+0.00%).
2. Thêm 4 danh mục tài sản: Ethereum, XRP, Tron, Solana cùng với Bitcoin trong tab PORTFOLIO.
   - Thông tin thị trường (Price, 24h change, Chains) hiển thị chuẩn.
   - Số lượng (Holdings) và Giá trị (Value) của tất cả coin (kể cả BTC) đều về 0.00 ($0.00).
3. Bổ sung giao diện chi tiết cho tab HOLDINGS BY CHAIN với số dư của từng chain cũng về $0.00.
4. Cập nhật script chuyển đổi mượt mà giữa các tab.
"""

from bs4 import BeautifulSoup
import re

HTML_FILE = "index.html"

# Định nghĩa 5 tài sản tiền mã hóa
ASSETS_DATA = [
    {
        "symbol": "BTC",
        "name": "Bitcoin",
        "chain_name": "Bitcoin",
        "price": "$80,370",
        "change": "+0.21%",
        "is_positive": True,
        "holdings": "0.00",
        "value": "$0.00",
        "portfolio_pct": "0.00%",
        "icon_type": "btc",
    },
    {
        "symbol": "ETH",
        "name": "Ethereum",
        "chain_name": "Ethereum",
        "price": "$2,648.50",
        "change": "+1.85%",
        "is_positive": True,
        "holdings": "0.00",
        "value": "$0.00",
        "portfolio_pct": "0.00%",
        "icon_type": "eth",
    },
    {
        "symbol": "SOL",
        "name": "Solana",
        "chain_name": "Solana",
        "price": "$182.40",
        "change": "+3.42%",
        "is_positive": True,
        "holdings": "0.00",
        "value": "$0.00",
        "portfolio_pct": "0.00%",
        "icon_type": "sol",
    },
    {
        "symbol": "XRP",
        "name": "XRP",
        "chain_name": "XRP Ledger",
        "price": "$0.5390",
        "change": "-0.65%",
        "is_positive": False,
        "holdings": "0.00",
        "value": "$0.00",
        "portfolio_pct": "0.00%",
        "icon_type": "xrp",
    },
    {
        "symbol": "TRX",
        "name": "Tron",
        "chain_name": "Tron",
        "price": "$0.1652",
        "change": "+0.92%",
        "is_positive": True,
        "holdings": "0.00",
        "value": "$0.00",
        "portfolio_pct": "0.00%",
        "icon_type": "trx",
    },
]


def get_asset_icon_html(icon_type: str) -> str:
    if icon_type == "btc":
        return """<svg class="size-full" viewBox="0 0 32 32"><circle cx="16" cy="16" r="16" fill="#F7931A"/><path d="M23.189 14.02c.314-2.096-1.283-3.223-3.465-3.975l.708-2.84-1.728-.43-.69 2.765c-.454-.114-.92-.22-1.385-.326l.695-2.783-1.728-.431-.708 2.839c-.376-.086-.745-.17-1.104-.26l.002-.008-2.384-.595-.46 1.846s1.283.294 1.256.312c.7.175.826.638.805 1.006l-.806 3.235c.048.012.11.03.18.057l-.183-.045-1.13 4.532c-.086.212-.303.531-.793.41.018.025-1.256-.314-1.256-.314l-.858 1.978 2.25.561c.418.105.828.215 1.231.318l-.715 2.872 1.727.43.708-2.84c.472.127.93.245 1.378.357l-.706 2.828 1.728.431.715-2.866c2.948.558 5.164.333 6.097-2.333.752-2.146-.037-3.385-1.588-4.192 1.13-.26 1.98-1.003 2.207-2.538zm-3.95 5.537c-.535 2.146-4.148.986-5.318.695l.949-3.805c1.17.292 4.929.872 4.369 3.11zm.536-5.567c-.487 1.953-3.495.96-4.47.718l.86-3.45c.975.242 4.117.694 3.61 2.732z" fill="#fff"/></svg>"""
    elif icon_type == "eth":
        return """<svg class="size-full" viewBox="0 0 32 32"><circle cx="16" cy="16" r="16" fill="#627EEA"/><path d="M16.498 4v8.87l7.497 3.35L16.498 4z" fill="#fff" fill-opacity=".6"/><path d="M16.498 4L9 16.22l7.498-3.35V4z" fill="#fff"/><path d="M16.498 21.968v6.027L24 17.616l-7.502 4.352z" fill="#fff" fill-opacity=".6"/><path d="M16.498 27.995v-6.028L9 17.616l7.498 10.38z" fill="#fff"/><path d="M16.498 20.573l7.497-4.353-7.497-3.348v7.7z" fill="#fff" fill-opacity=".2"/><path d="M9 16.22l7.498 4.353v-7.7L9 16.22z" fill="#fff" fill-opacity=".6"/></svg>"""
    elif icon_type == "sol":
        return """<svg class="size-full" viewBox="0 0 32 32"><circle cx="16" cy="16" r="16" fill="#14151a"/><path d="M9.5 20.5a.6.6 0 01.42-.18h12.58a.6.6 0 01.42 1.02l-2.4 2.4a.6.6 0 01-.42.18H7.52a.6.6 0 01-.42-1.02l2.4-2.4z" fill="#00FFA3"/><path d="M9.5 8.5a.6.6 0 01.42-.18h12.58a.6.6 0 01.42 1.02l-2.4 2.4a.6.6 0 01-.42.18H7.52a.6.6 0 01-.42-1.02l2.4-2.4z" fill="#00FFA3"/><path d="M22.5 14.5a.6.6 0 00-.42-.18H9.5a.6.6 0 00-.42 1.02l2.4 2.4a.6.6 0 00.42.18h12.58a.6.6 0 00.42-1.02l-2.4-2.4z" fill="#DC1FFF"/></svg>"""
    elif icon_type == "xrp":
        return """<svg class="size-full" viewBox="0 0 32 32"><circle cx="16" cy="16" r="16" fill="#23292F"/><path d="M23.5 9h2.3l-5.7 5.7c-1.2 1.2-3.1 1.2-4.3 0L10.2 9h2.3l4.5 4.5c.6.6 1.5.6 2.1 0L23.5 9zM8.5 23H6.2l5.7-5.7c1.2-1.2 3.1-1.2 4.3 0l5.6 5.7h-2.3l-4.5-4.5c-.6-.6-1.5-.6-2.1 0L8.5 23z" fill="#fff"/></svg>"""
    elif icon_type == "trx":
        return """<svg class="size-full" viewBox="0 0 32 32"><circle cx="16" cy="16" r="16" fill="#EC0928"/><path d="M24 10.5l-15.5-3 6.8 17.5 8.7-14.5zm-2.8 1.4l-5.6 9.3-4.3-11.1 9.9 1.8z" fill="#fff"/></svg>"""
    return ""


def build_portfolio_row_html(asset: dict, is_even: bool) -> str:
    bg_class = "bg-[var(--app-row-bg-alt)]" if is_even else "bg-transparent"
    change_color = "text-[var(--app-status-open-text)]" if asset["is_positive"] else "text-red-400"
    icon_svg = get_asset_icon_html(asset["icon_type"])

    return f"""
    <div class="group/row relative grid transition-colors cursor-pointer hover:bg-(--app-row-bg-hover) {bg_class} text-xs border-b border-white/[0.02]" role="row" style="grid-column:1/-1;grid-template-columns:subgrid" tabindex="0">
        <div class="flex h-full min-w-0 items-center justify-start text-left px-0 py-0" role="cell" style="min-height:2.625rem"></div>
        <div class="flex h-full min-w-0 items-center justify-start text-left px-1.5 py-1.25" role="cell" style="min-height:2.625rem">
            <a class="group flex min-w-0" href="https://xkuro.io/explorer/token/{asset['name'].lower()}">
                <span class="inline-flex items-center min-w-0 gap-1.5">
                    <span class="inline-flex shrink-0 items-center justify-center overflow-hidden rounded-full text-(--app-text-muted) h-[1.25em] w-[1.25em] min-w-[1.25em]">
                        {icon_svg}
                    </span>
                    <span class="flex min-w-0 items-baseline gap-1">
                        <span class="shrink-0 font-light text-(--data-panel-text-strong) group-hover:underline">{asset['symbol']}</span>
                        <span class="truncate font-extralight text-slate-100">{asset['name']}</span>
                    </span>
                </span>
            </a>
        </div>
        <div class="flex h-full min-w-0 items-center justify-start text-left px-1.5 py-1.25" role="cell" style="min-height:2.625rem">
            <span class="inline-flex items-center gap-1.5">
                <span class="inline-flex shrink-0 items-center justify-center overflow-hidden rounded-full h-[1em] w-[1em] min-w-[1em]">
                    {icon_svg}
                </span>
                <span class="text-slate-400 font-mono text-[11px] truncate">{asset['chain_name']}</span>
            </span>
        </div>
        <div class="flex h-full min-w-0 items-center justify-end text-right px-1.5 py-1.25 font-mono font-light tracking-[-0.02em]" role="cell" style="min-height:2.625rem">
            <span class="inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums text-inherit">{asset['price']}</span>
        </div>
        <div class="flex h-full min-w-0 items-center justify-end text-right px-1.5 py-1.25 font-mono font-light tracking-[-0.02em]" role="cell" style="min-height:2.625rem">
            <button class="cursor-pointer" type="button">
                <span class="inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums {change_color}">{asset['change']}</span>
            </button>
        </div>
        <div class="flex h-full min-w-0 items-center justify-end text-right px-1.5 py-1.25 font-mono font-light tracking-[-0.02em]" role="cell" style="min-height:2.625rem">
            <span class="flex min-w-0 cursor-pointer items-baseline justify-end gap-1">
                <span class="inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums text-slate-400 font-medium">{asset['holdings']}</span>
                <span class="truncate text-(--data-panel-text-muted)">{asset['symbol']}</span>
            </span>
        </div>
        <div class="flex h-full min-w-0 items-center justify-end text-right px-1.5 py-1.25 font-mono font-light tracking-[-0.02em]" role="cell" style="min-height:2.625rem">
            <span class="inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums text-slate-400 font-medium">{asset['value']}</span>
        </div>
        <div class="flex h-full min-w-0 items-center justify-end text-right px-1.5 py-1.25 font-mono font-light tracking-[-0.02em]" role="cell" style="min-height:2.625rem">
            <span class="inline-flex max-w-full items-baseline whitespace-nowrap tabular-nums text-slate-500">{asset['portfolio_pct']}</span>
        </div>
        <div class="flex h-full min-w-0 items-center justify-start text-left px-0 py-0" role="cell" style="min-height:2.625rem"></div>
    </div>
    """


def build_holdings_by_chain_view_html() -> str:
    chains = [
        {"chain": "Bitcoin Network", "symbol": "BTC", "icon": "btc", "tokens": "1 Token", "balance": "$0.00", "holdings": "0.00 BTC"},
        {"chain": "Ethereum Network", "symbol": "ETH", "icon": "eth", "tokens": "1 Token", "balance": "$0.00", "holdings": "0.00 ETH"},
        {"chain": "Solana Network", "symbol": "SOL", "icon": "sol", "tokens": "1 Token", "balance": "$0.00", "holdings": "0.00 SOL"},
        {"chain": "XRP Ledger", "symbol": "XRP", "icon": "xrp", "tokens": "1 Token", "balance": "$0.00", "holdings": "0.00 XRP"},
        {"chain": "Tron Network", "symbol": "TRX", "icon": "trx", "tokens": "1 Token", "balance": "$0.00", "holdings": "0.00 TRX"},
    ]

    rows_html = ""
    for idx, c in enumerate(chains):
        bg = "bg-white/[0.02]" if idx % 2 == 1 else "bg-transparent"
        icon_svg = get_asset_icon_html(c["icon"])
        rows_html += f"""
        <tr class="group transition-colors hover:bg-white/[0.05] {bg} text-xs font-mono border-b border-white/[0.03]">
            <td class="py-3 px-3">
                <div class="flex items-center gap-2">
                    <span class="inline-flex shrink-0 size-5 rounded-full overflow-hidden">{icon_svg}</span>
                    <span class="font-medium text-white font-sans">{c['chain']}</span>
                </div>
            </td>
            <td class="py-3 px-3 text-slate-400 font-sans">{c['tokens']}</td>
            <td class="py-3 px-3 text-right font-semibold text-slate-300">{c['holdings']}</td>
            <td class="py-3 px-3 text-right font-bold text-white text-sm">{c['balance']}</td>
            <td class="py-3 px-3 text-right text-slate-500">0.00%</td>
        </tr>
        """

    return f"""
    <div id="portfolio-view-holdings" class="flex min-h-0 flex-col overflow-hidden contain-[layout_paint]" style="display: none;">
        <div class="flex min-h-0 flex-col overflow-hidden h-[32em] flex-none md:h-auto md:flex-1">
            <div class="font-arkham-sans relative flex h-full flex-col overflow-hidden bg-(--data-panel-body-bg) tabular-nums min-h-0 flex-1">
                
                <div class="p-3 bg-white/[0.02] border-b border-white/5 flex items-center justify-between font-mono text-xs">
                    <span class="text-slate-400">TỔNG SỐ CHAIN THEO DÕI: <strong class="text-white">5 MẠNG LƯỚI</strong></span>
                    <span class="text-slate-400">TỔNG GIÁ TRỊ: <strong class="text-white">$0.00</strong></span>
                </div>

                <div class="flex-1 min-h-0 overflow-y-auto scrollbar-thin">
                    <table class="w-full text-left border-collapse">
                        <thead class="sticky top-0 z-20 bg-[#0b0e14] border-b border-white/10 text-[11px] font-mono uppercase text-slate-400 tracking-wider">
                            <tr>
                                <th class="py-2.5 px-3">Mạng Lưới (Chain)</th>
                                <th class="py-2.5 px-3">Tokens</th>
                                <th class="py-2.5 px-3 text-right">Số Lượng</th>
                                <th class="py-2.5 px-3 text-right">Giá Trị USD</th>
                                <th class="py-2.5 px-3 text-right">Tỷ Trọng</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_html}
                        </tbody>
                    </table>
                </div>

                <div class="px-3 py-2 border-t border-white/5 flex items-center justify-between text-[11px] text-slate-400 font-mono bg-white/[0.01]">
                    <span>Tất cả số dư chain đều đã đồng bộ về 0.00</span>
                    <span class="text-slate-500">xKuro Multi-Chain Explorer</span>
                </div>
            </div>
        </div>
    </div>
    """


def update_portfolio_assets():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # 1. Đổi số dư tổng trên đỉnh về $0.00
    top_balance = soup.find(string=re.compile(r"14,983,724|88,114,592"))
    if top_balance:
        top_balance.replace_with("$0.00")
        print("✓ Đã đổi số dư tổng trên đỉnh về: $0.00")
    else:
        # Tìm thẻ h1 hoặc profile header có số tiền
        spans = soup.find_all("span", class_=lambda c: c and "lg:text-2xl" in str(c))
        for sp in spans:
            sp.string = "$0.00"
            print("✓ Đã cập nhật số dư tổng qua class lg:text-2xl về $0.00")

    # Đổi biến động cạnh số dư: +0.21% -> +0.00%
    change_btn = soup.find(string=re.compile(r"\+0\.21%"))
    if change_btn and change_btn.parent:
        change_btn.replace_with("+0.00%")
        print("✓ Đã đổi biến động tổng về +0.00%")

    # 2. Cập nhật bảng PORTFOLIO (thêm Bitcoin, Ethereum, Solana, XRP, Tron)
    default_view = soup.find("div", id="portfolio-view-default")
    if not default_view:
        raise ValueError("Không tìm thấy div portfolio-view-default")

    # Xóa các dòng asset cũ (chỉ giữ lại dòng tiêu đề role='row' đầu tiên)
    rows = default_view.find_all("div", role="row")
    header_row = rows[0]  # ASSET, CHAINS, PRICE, HOLDINGS, VALUE
    for old_row in rows[1:]:
        old_row.decompose()

    # Thêm 5 dòng asset mới vào sau header_row
    parent_grid = header_row.parent
    for idx, asset in enumerate(ASSETS_DATA):
        row_html = build_portfolio_row_html(asset, idx % 2 == 1)
        row_soup = BeautifulSoup(row_html, "html.parser")
        parent_grid.append(row_soup)

    print(f"✓ Đã thêm 5 tài sản (Bitcoin, Ethereum, Solana, XRP, Tron) vào bảng PORTFOLIO với số dư về 0.")

    # 3. Thêm hoặc cập nhật tab HOLDINGS BY CHAIN view
    existing_holdings_view = soup.find("div", id="portfolio-view-holdings")
    if existing_holdings_view:
        existing_holdings_view.decompose()

    header = soup.find("button", id="btn-tab-portfolio").parent.parent
    body = header.find_next_sibling()
    holdings_view_soup = BeautifulSoup(build_holdings_by_chain_view_html(), "html.parser")
    body.append(holdings_view_soup)
    print("✓ Đã thêm giao diện chi tiết cho tab HOLDINGS BY CHAIN với 5 chain về $0.00.")

    # 4. Cập nhật JavaScript chuyển đổi tab (hỗ trợ cả PORTFOLIO, HOLDINGS BY CHAIN, ARCHIVE, GROWTH TIMELINE)
    updated_script = """
    function switchPortfolioTab(tab) {
        var btnPortfolio = document.getElementById('btn-tab-portfolio');
        var btnHoldings = document.getElementById('btn-tab-holdings');
        var btnArchive = document.getElementById('btn-tab-archive');
        var btnGrowth = document.getElementById('btn-tab-growth');

        var viewDefault = document.getElementById('portfolio-view-default');
        var viewHoldings = document.getElementById('portfolio-view-holdings');
        var viewGrowth = document.getElementById('portfolio-view-timeline');

        var allButtons = [btnPortfolio, btnHoldings, btnArchive, btnGrowth];

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

        // Hide all views first
        if (viewDefault) viewDefault.style.display = 'none';
        if (viewHoldings) viewHoldings.style.display = 'none';
        if (viewGrowth) viewGrowth.style.display = 'none';

        if (tab === 'growth') {
            if (viewGrowth) viewGrowth.style.display = 'flex';
            setActive(btnGrowth);
        } else if (tab === 'holdings') {
            if (viewHoldings) viewHoldings.style.display = 'flex';
            setActive(btnHoldings);
        } else {
            if (viewDefault) viewDefault.style.display = 'flex';
            if (tab === 'archive') setActive(btnArchive);
            else setActive(btnPortfolio);
        }
    }
    """

    script_tag = soup.find("script", id="tab-controller-script")
    if script_tag:
        script_tag.string = updated_script
        print("✓ Đã cập nhật mã JavaScript điều khiển tab hoàn hảo.")

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"💾 Đã lưu thành công file {HTML_FILE}.")


if __name__ == "__main__":
    update_portfolio_assets()
