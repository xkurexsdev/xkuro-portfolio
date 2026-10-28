#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script cập nhật thông tin cá nhân và số dư trên file index.html:
1. Đổi 'Satoshi Nakamoto' thành 'Patrick Xuan Kuan' (ở tiêu đề, heading H1, meta, schema, transaction table).
2. Đổi số dư tổng $88,114,592,670.78 thành $14,983,724.72.
3. Đổi số lượng coin và giá trị trong bảng danh mục:
   - 1.096M BTC -> 186.43 BTC
   - $88.11B -> $14.98M
4. Đổi ảnh đại diện avatar thành chuỗi Base64 từ file avatar.png.
"""

import os
import re
import base64
from bs4 import BeautifulSoup, NavigableString

HTML_FILE = "index.html"
AVATAR_FILE = "avatar.png"

NEW_NAME = "Patrick Xuan Kuan"
NEW_TOTAL_BALANCE = "$14,983,724.72"
NEW_BTC_HOLDINGS = "186.43"
NEW_BTC_VALUE = "$14.98M"


def update_index_html():
    if not os.path.exists(HTML_FILE):
        raise FileNotFoundError(f"Không tìm thấy file {HTML_FILE}")
    if not os.path.exists(AVATAR_FILE):
        raise FileNotFoundError(f"Không tìm thấy file {AVATAR_FILE}")

    # 1. Mã hóa avatar.png thành Base64
    with open(AVATAR_FILE, "rb") as f:
        avatar_data = f.read()
    avatar_b64 = base64.b64encode(avatar_data).decode("utf-8")
    avatar_data_url = f"data:image/png;base64,{avatar_b64}"
    print(f"✓ Đã chuyển đổi {AVATAR_FILE} thành chuỗi Base64 ({len(avatar_data_url)} ký tự).")

    # 2. Đọc file index.html
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # 3. Đổi tên hiển thị: 'Satoshi Nakamoto' -> 'Patrick Xuan Kuan'
    name_count = 0
    # Text nodes
    for text_node in soup.find_all(string=re.compile(r"Satoshi Nakamoto")):
        parent = text_node.parent
        if parent and parent.name not in ["script", "style"]:
            new_text = text_node.replace("Satoshi Nakamoto", NEW_NAME)
            text_node.replace_with(NavigableString(new_text))
            name_count += 1

    # Meta tags (og:title, twitter:title, description, etc.)
    for meta in soup.find_all("meta"):
        content = meta.get("content", "")
        if "Satoshi Nakamoto" in content:
            meta["content"] = content.replace("Satoshi Nakamoto", NEW_NAME)
            name_count += 1

    # Thẻ <title>
    if soup.title and "Satoshi Nakamoto" in str(soup.title.string):
        soup.title.string = soup.title.string.replace("Satoshi Nakamoto", NEW_NAME)
        name_count += 1

    # Thẻ JSON-LD schema
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        if script.string and "Satoshi Nakamoto" in script.string:
            script.string = script.string.replace("Satoshi Nakamoto", NEW_NAME).replace(
                "satoshi-nakamoto", "patrick-xuan-kuan"
            )
            name_count += 1

    print(f"✓ Đã đổi tên 'Satoshi Nakamoto' thành '{NEW_NAME}' tại {name_count} vị trí.")

    # 4. Đổi số dư tổng: $88,114,592,670.78 -> $14,983,724.72
    balance_updated = False
    for s in soup.find_all(string=re.compile(r"88,114,592,670\.78")):
        s.replace_with(NavigableString(NEW_TOTAL_BALANCE))
        balance_updated = True
    print(f"✓ Đã cập nhật số dư tổng thành: {NEW_TOTAL_BALANCE} ({'Thành công' if balance_updated else 'Không tìm thấy'})")

    # 5. Đổi số lượng coin & giá trị trong danh mục: 1.096M -> 186.43, $88.11B -> $14.98M
    holdings_updated = False
    for s in soup.find_all(string=re.compile(r"1\.096M")):
        s.replace_with(NavigableString(NEW_BTC_HOLDINGS))
        holdings_updated = True

    value_updated = False
    for s in soup.find_all(string=re.compile(r"88\.11B")):
        s.replace_with(NavigableString(NEW_BTC_VALUE))
        value_updated = True

    print(f"✓ Đã cập nhật số lượng BTC trong danh mục: {NEW_BTC_HOLDINGS} BTC ({'Thành công' if holdings_updated else 'Không tìm thấy'})")
    print(f"✓ Đã cập nhật giá trị BTC trong danh mục: {NEW_BTC_VALUE} ({'Thành công' if value_updated else 'Không tìm thấy'})")

    # 6. Đổi ảnh đại diện avatar sang Base64
    avatar_updated_count = 0
    # Profile avatar chính
    profile_imgs = soup.find_all("img", alt=re.compile(r"profile image for|satoshi", re.I))
    for img in profile_imgs:
        img["src"] = avatar_data_url
        if "alt" in img.attrs:
            img["alt"] = (
                img["alt"]
                .replace("Satoshi Nakamoto", NEW_NAME)
                .replace("satoshi-nakamoto", "patrick-xuan-kuan")
            )
        avatar_updated_count += 1

    # Cập nhật cả biến CSS --sf-img-11 nếu có để mọi avatar nhỏ trong bảng giao dịch đồng bộ theo ảnh mới
    for style_tag in soup.find_all("style"):
        if style_tag.string and "--sf-img-11" in style_tag.string:
            style_tag.string = re.sub(
                r"--sf-img-11:\s*url\([^)]+\)",
                f'--sf-img-11: url("{avatar_data_url}")',
                style_tag.string,
            )

    print(f"✓ Đã thay thế ảnh đại diện thành chuỗi Base64 ({avatar_updated_count} thẻ <img> và biến CSS đồng bộ).")

    # 7. Lưu lại file index.html
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(str(soup))

    file_size_kb = os.path.getsize(HTML_FILE) / 1024
    print(f"💾 Đã lưu thành công file {HTML_FILE} ({file_size_kb:.1f} KB).")


if __name__ == "__main__":
    update_index_html()
