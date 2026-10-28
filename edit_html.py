#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script chỉnh sửa file HTML cloned (Arkham) sử dụng BeautifulSoup:
1. Thay toàn bộ chữ 'arkm' (và 'arkham') thành tên thương hiệu mới.
2. Đổi thẻ <title> (kèm các thẻ meta og:title, twitter:title).
3. Đổi tất cả các link <a> trỏ về trang login/signup thành link đích của bạn.
4. Xóa bỏ các script theo dõi (Google Analytics, Cloudflare Insights, Facebook Pixel).
5. Xóa watermark Arkham mờ ở background biểu đồ (tùy chọn).
6. Thay thế chữ logo vector trên thanh điều hướng thành tên thương hiệu mới (tùy chọn).
7. Lưu kết quả ra file mới: index.html.
"""

import os
import re
import sys
import argparse
from bs4 import BeautifulSoup, Comment, NavigableString

# ==============================================================================
# CẤU HÌNH MẶC ĐỊNH (BẠN CÓ THỂ ĐỔI TRỰC TIẾP TẠI ĐÂY HOẶC TRUYỀN QUA THAM SỐ CLI)
# ==============================================================================
DEFAULT_INPUT_FILE = "output.html"
DEFAULT_OUTPUT_FILE = "index.html"

# Tên thương hiệu mới (ví dụ: xKuro, MyBrand, ...)
NEW_BRAND = "xKuro"

# Tiêu đề mới cho trang web
NEW_TITLE = "Satoshi Nakamoto ｜ xKuro Wallet"

# Link đăng nhập / đăng ký mới của bạn
NEW_AUTH_LINK = "https://xkuro.io/login"

# Tên miền mới thay thế cho arkm.com trong các link nội bộ
NEW_DOMAIN = "xkuro.io"

# Thay thế luôn chữ 'arkham'/'Arkham'/'ARKHAM' (Khuyên dùng để giao diện đồng bộ hoàn toàn)
REPLACE_ARKHAM = True

# Đổi SVG chữ 'ARKHAM' trên header navbar thành tên thương hiệu dạng chữ
REPLACE_LOGO_TEXT = True

# Xóa watermark 'ARKHAM' mờ xuất hiện ở các khung biểu đồ
REMOVE_WATERMARK = True


def smart_case_replace(text: str, search_word: str, replacement: str) -> str:
    """
    Thay thế từ giữ nguyên định dạng chữ hoa/chữ thường:
    - arkm -> xkuro
    - Arkm -> Xkuro
    - ARKM -> XKURO
    """
    if not text:
        return text

    def replacer(match):
        matched = match.group(0)
        if matched.isupper():
            return replacement.upper()
        if len(matched) > 1 and matched[0].isupper() and matched[1:].islower():
            return replacement.capitalize()
        if matched.islower():
            return replacement.lower()
        return replacement

    pattern = re.compile(re.escape(search_word), re.IGNORECASE)
    return pattern.sub(replacer, text)


def remove_tracking_scripts(soup: BeautifulSoup) -> dict:
    """
    Tìm và xóa tất cả các script theo dõi:
    - Google Analytics / Google Tag Manager
    - Cloudflare Insights / Beacons
    - Facebook Pixel (Meta Pixel)
    - Tracking noscript & meta tags
    """
    stats = {
        "google_analytics": 0,
        "cloudflare_insights": 0,
        "facebook_pixel": 0,
        "noscript_beacons": 0,
        "meta_verification": 0,
    }

    # Các mẫu URL của script tracker
    tracker_src_rules = [
        ("google_analytics", [
            r"google-analytics\.com",
            r"googletagmanager\.com",
            r"analytics\.js",
            r"gtag/js",
            r"ga\.js",
        ]),
        ("cloudflare_insights", [
            r"cloudflareinsights\.com",
            r"beacon\.min\.js",
            r"challenges\.cloudflare\.com",
            r"static\.cloudflareinsights\.com",
        ]),
        ("facebook_pixel", [
            r"connect\.facebook\.net",
            r"fbevents\.js",
        ]),
    ]

    # Các mẫu nội dung trong inline script tracker
    tracker_inline_rules = [
        ("google_analytics", [
            r"gtag\(",
            r"GoogleAnalyticsObject",
            r"ga\((\"|')create",
            r"ga\((\"|')send",
            r"dataLayer\.push",
            r"dataLayer\s*=\s*\[",
        ]),
        ("cloudflare_insights", [
            r"cloudflareinsights",
            r"__cfBeacon",
            r"cf-beacon",
        ]),
        ("facebook_pixel", [
            r"fbq\(",
            r"_fbq",
            r"fbq\.push",
        ]),
    ]

    # 1. Quét các thẻ <script>
    scripts_to_remove = []
    for script in soup.find_all("script"):
        src = script.get("src", "").strip()
        content = script.string or script.get_text() or ""
        matched_category = None

        if src:
            for cat, patterns in tracker_src_rules:
                if any(re.search(p, src, re.IGNORECASE) for p in patterns):
                    matched_category = cat
                    break

        if not matched_category and content:
            for cat, patterns in tracker_inline_rules:
                if any(re.search(p, content, re.IGNORECASE) for p in patterns):
                    matched_category = cat
                    break

        if matched_category:
            scripts_to_remove.append((script, matched_category))

    for script, cat in scripts_to_remove:
        stats[cat] += 1
        script.decompose()

    # 2. Quét các thẻ <noscript> chứa pixel ảnh theo dõi
    for ns in soup.find_all("noscript"):
        ns_str = str(ns)
        if any(tracker in ns_str for tracker in ["facebook.com/tr", "googletagmanager.com/ns.html"]):
            stats["noscript_beacons"] += 1
            ns.decompose()

    # 3. Xóa các meta theo dõi (như google-site-verification)
    for meta in soup.find_all("meta", attrs={"name": re.compile(r"google-site-verification", re.I)}):
        stats["meta_verification"] += 1
        meta.decompose()

    return stats


def update_title_and_meta(soup: BeautifulSoup, new_title: str) -> int:
    """
    Cập nhật thẻ <title> và các thẻ OpenGraph / Twitter meta title tương ứng.
    """
    updated_count = 0

    title_tag = soup.find("title")
    if title_tag:
        title_tag.string = new_title
        updated_count += 1
    else:
        if soup.head:
            new_tag = soup.new_tag("title")
            new_tag.string = new_title
            soup.head.insert(0, new_tag)
            updated_count += 1

    for meta in soup.find_all("meta"):
        prop = meta.get("property", "") or meta.get("name", "")
        if prop in ["og:title", "twitter:title"]:
            meta["content"] = new_title
            updated_count += 1

    return updated_count


def update_auth_links(soup: BeautifulSoup, new_auth_link: str) -> list:
    """
    Tìm và đổi tất cả các thẻ <a> trỏ về login / signup / register thành new_auth_link.
    """
    changed_links = []
    auth_keywords = ["/login", "/register", "/signup", "/signin"]
    auth_text_keywords = ["log in", "login", "sign up", "signup", "register", "sign in", "đăng nhập", "đăng ký"]

    for a in soup.find_all("a"):
        href = a.get("href", "")
        text = a.get_text(strip=True).lower()
        href_lower = href.lower()

        is_auth = False
        if any(kw in href_lower for kw in auth_keywords):
            is_auth = True
        elif any(kw in text for kw in auth_text_keywords):
            is_auth = True

        if is_auth:
            old_href = href
            a["href"] = new_auth_link
            changed_links.append((a.get_text(strip=True) or "[link]", old_href))

    return changed_links


def replace_brand_occurrences(
    soup: BeautifulSoup,
    new_brand: str,
    new_domain: str,
    replace_arkham: bool = True,
    replace_logo_text: bool = True,
    remove_watermark: bool = True,
) -> dict:
    """
    Thay thế chữ 'arkm' (và 'arkham') thành tên thương hiệu mới:
    - Trong các đoạn text (NavigableString)
    - Trong các liên kết (href)
    - Trong metadata (content, title, alt, aria-label, placeholder)
    - Trong JSON-LD schema
    - Cập nhật logo navbar và watermark biểu đồ
    Lưu ý: Không thay đổi class CSS để đảm bảo giao diện hiển thị chuẩn 100%.
    """
    stats = {
        "text_nodes": 0,
        "href_attrs": 0,
        "meta_attrs": 0,
        "aria_labels": 0,
        "other_attrs": 0,
        "json_ld": 0,
        "watermarks_removed": 0,
        "logo_updated": 0,
    }

    words_to_replace = ["arkm"]
    if replace_arkham:
        words_to_replace.append("arkham")

    # 1. Cập nhật Logo Text trên Navbar nếu có
    if replace_logo_text:
        logo_svg = soup.find("svg", attrs={"aria-label": re.compile(r"ARKHAM|arkm", re.I)})
        if logo_svg:
            brand_label = soup.new_tag(
                "span",
                **{
                    "class": "hidden md:inline-block font-sans font-bold tracking-wider text-white text-base ml-1 select-none",
                    "aria-label": new_brand,
                },
            )
            brand_label.string = new_brand.upper()
            logo_svg.replace_with(brand_label)
            stats["logo_updated"] += 1

    # 2. Xóa Watermark nền nếu được yêu cầu
    if remove_watermark:
        watermarks = soup.find_all(class_=re.compile(r"arkham-watermark"))
        for wm in watermarks:
            wm.decompose()
            stats["watermarks_removed"] += 1

    # 3. Thay thế trong Text Nodes (bỏ qua thẻ <script> và <style>)
    for text_node in soup.find_all(string=True):
        parent = text_node.parent
        if not parent or parent.name in ["script", "style", "title"]:
            continue
        if isinstance(text_node, Comment):
            continue

        original_text = str(text_node)
        new_text = original_text

        for word in words_to_replace:
            new_text = smart_case_replace(new_text, word, new_brand)

        if new_text != original_text:
            text_node.replace_with(NavigableString(new_text))
            stats["text_nodes"] += 1

    # 4. Thay thế trong thuộc tính href của <a> và <link>
    for tag in soup.find_all(["a", "link"]):
        href = tag.get("href")
        if href and isinstance(href, str):
            orig_href = href
            if "arkm.com" in href:
                href = href.replace("arkm.com", new_domain)
            if "mailto:" in href and "arkm" in href.lower():
                href = smart_case_replace(href, "arkm", new_brand.lower())
            for word in words_to_replace:
                href = smart_case_replace(href, word, new_brand.lower())
            if href != orig_href:
                tag["href"] = href
                stats["href_attrs"] += 1

    # 5. Thay thế trong <meta content="...">
    for meta in soup.find_all("meta"):
        content = meta.get("content")
        if content and isinstance(content, str):
            orig_content = content
            for word in words_to_replace:
                content = smart_case_replace(content, word, new_brand)
            if "arkm.com" in content:
                content = content.replace("arkm.com", new_domain)
            if content != orig_content:
                meta["content"] = content
                stats["meta_attrs"] += 1

    # 6. Thay thế trong aria-label, alt, title, placeholder
    for tag in soup.find_all(attrs={"aria-label": True}):
        orig = tag["aria-label"]
        for word in words_to_replace:
            tag["aria-label"] = smart_case_replace(tag["aria-label"], word, new_brand)
        if tag["aria-label"] != orig:
            stats["aria_labels"] += 1

    for attr_name in ["alt", "placeholder"]:
        for tag in soup.find_all(attrs={attr_name: True}):
            orig = tag[attr_name]
            for word in words_to_replace:
                tag[attr_name] = smart_case_replace(tag[attr_name], word, new_brand)
            if tag[attr_name] != orig:
                stats["other_attrs"] += 1

    for tag in soup.find_all(attrs={"title": True}):
        if tag.name != "title":
            orig = tag["title"]
            for word in words_to_replace:
                tag["title"] = smart_case_replace(tag["title"], word, new_brand)
            if tag["title"] != orig:
                stats["other_attrs"] += 1

    # 7. Thay thế trong JSON-LD schema (<script type="application/ld+json">)
    for s in soup.find_all("script", attrs={"type": "application/ld+json"}):
        if s.string:
            orig = s.string
            s_content = orig
            for word in words_to_replace:
                s_content = smart_case_replace(s_content, word, new_brand)
            s_content = s_content.replace("arkm.com", new_domain)
            if s_content != orig:
                s.string = s_content
                stats["json_ld"] += 1

    return stats


def process_html_file(
    input_file: str,
    output_file: str,
    new_brand: str,
    new_title: str,
    new_auth_link: str,
    replace_arkham: bool = True,
    new_domain: str = "xkuro.io",
    replace_logo_text: bool = True,
    remove_watermark: bool = True,
):
    print("=" * 64)
    print("🚀 BẮT ĐẦU CHỈNH SỬA FILE HTML VỚI BEAUTIFULSOUP")
    print("=" * 64)
    print(f"📂 File nguồn     : {input_file}")
    print(f"💾 File đích      : {output_file}")
    print(f"🏷️  Thương hiệu mới: {new_brand}")
    print(f"📄 Tiêu đề mới    : {new_title}")
    print(f"🔗 Link Login/Reg : {new_auth_link}")
    print(f"🌐 Domain nội bộ  : {new_domain}")
    print(f"🔄 Đổi 'arkham'   : {'Bật' if replace_arkham else 'Tắt'}")
    print(f"✨ Thay logo chữ  : {'Bật' if replace_logo_text else 'Tắt'}")
    print(f"🧹 Xóa watermark  : {'Bật' if remove_watermark else 'Tắt'}")
    print("-" * 64)

    # 1. Đọc file HTML nguồn
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Không tìm thấy file nguồn: {input_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Dùng lxml nếu có, fallback html.parser
    try:
        soup = BeautifulSoup(html_content, "lxml")
    except Exception:
        soup = BeautifulSoup(html_content, "html.parser")

    # 2. Xóa các script theo dõi
    print("\n[1/4] 🛡️  Đang quét và xóa các script theo dõi...")
    tracker_stats = remove_tracking_scripts(soup)
    total_trackers = sum(tracker_stats.values())
    print(f"  ✓ Đã xóa {total_trackers} phần tử theo dõi:")
    print(f"    - Google Analytics / GTM  : {tracker_stats['google_analytics']}")
    print(f"    - Cloudflare Insights     : {tracker_stats['cloudflare_insights']}")
    print(f"    - Facebook Pixel          : {tracker_stats['facebook_pixel']}")
    print(f"    - NoScript Tracking Pixel : {tracker_stats['noscript_beacons']}")
    print(f"    - Meta Site Verification  : {tracker_stats['meta_verification']}")

    # 3. Đổi thẻ <title>
    print("\n[2/4] 🏷️  Đang cập nhật <title> và thẻ OpenGraph meta...")
    updated_titles = update_title_and_meta(soup, new_title)
    print(f"  ✓ Đã cập nhật {updated_titles} thẻ (title, og:title, twitter:title).")

    # 4. Đổi link <a> login / signup
    print("\n[3/4] 🔗 Đang cập nhật tất cả link Login / Sign up...")
    auth_links = update_auth_links(soup, new_auth_link)
    print(f"  ✓ Đã chuyển hướng {len(auth_links)} liên kết xác thực sang: {new_auth_link}")
    for text, old_href in auth_links:
        print(f"    • [{text}]: {old_href[:65]}...")

    # 5. Thay thế thương hiệu 'arkm' (và 'arkham')
    print(f"\n[4/4] 🔤 Đang thay thế 'arkm' (và 'arkham') thành '{new_brand}'...")
    brand_stats = replace_brand_occurrences(
        soup=soup,
        new_brand=new_brand,
        new_domain=new_domain,
        replace_arkham=replace_arkham,
        replace_logo_text=replace_logo_text,
        remove_watermark=remove_watermark,
    )
    print(f"  ✓ Kết quả thay thế thương hiệu:")
    print(f"    - Đoạn văn bản (text nodes) : {brand_stats['text_nodes']}")
    print(f"    - Liên kết (href)          : {brand_stats['href_attrs']}")
    print(f"    - Thẻ metadata             : {brand_stats['meta_attrs']}")
    print(f"    - Thuộc tính aria-label    : {brand_stats['aria_labels']}")
    print(f"    - Thuộc tính alt/title     : {brand_stats['other_attrs']}")
    print(f"    - JSON-LD Structured Data  : {brand_stats['json_ld']}")
    if remove_watermark:
        print(f"    - Watermark đã xóa         : {brand_stats['watermarks_removed']}")
    if replace_logo_text:
        print(f"    - Logo Navbar cập nhật     : {brand_stats['logo_updated']}")

    # 6. Ghi kết quả ra file mới
    print(f"\n💾 Đang ghi kết quả ra file: {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(str(soup))

    file_size_kb = os.path.getsize(output_file) / 1024
    print("=" * 64)
    print(f"✅ HOÀN TẤT THÀNH CÔNG! File đã được tạo: {output_file} ({file_size_kb:.1f} KB)")
    print("=" * 64)


def main():
    parser = argparse.ArgumentParser(description="Chỉnh sửa file HTML clone với BeautifulSoup")
    parser.add_argument("-i", "--input", default=DEFAULT_INPUT_FILE, help="Đường dẫn file HTML nguồn (mặc định: output.html)")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT_FILE, help="Đường dẫn file HTML đích (mặc định: index.html)")
    parser.add_argument("-b", "--brand", default=NEW_BRAND, help=f"Tên thương hiệu mới (mặc định: {NEW_BRAND})")
    parser.add_argument("-t", "--title", default=NEW_TITLE, help=f"Tiêu đề trang mới (mặc định: {NEW_TITLE})")
    parser.add_argument("-l", "--link", default=NEW_AUTH_LINK, help=f"Link login/signup mới (mặc định: {NEW_AUTH_LINK})")
    parser.add_argument("-d", "--domain", default=NEW_DOMAIN, help=f"Tên miền mới thay cho arkm.com (mặc định: {NEW_DOMAIN})")
    parser.add_argument("--no-arkham", action="store_true", help="Chỉ thay chữ 'arkm', không thay chữ 'arkham'")
    parser.add_argument("--keep-watermark", action="store_true", help="Không xóa watermark 'ARKHAM' ở nền biểu đồ")
    parser.add_argument("--keep-logo-svg", action="store_true", help="Không thay đổi chữ logo 'ARKHAM' trên navbar")

    args = parser.parse_args()

    # Kiểm tra file input, nếu chưa có thì tìm file trong Downloads
    input_file = args.input
    if not os.path.exists(input_file):
        downloads_path = os.path.expanduser("~/Downloads/Satoshi Nakamoto ｜ Arkham (28_10_2026 23：52：17).html")
        if os.path.exists(downloads_path):
            print(f"ℹ️ Không tìm thấy {input_file}, tự động sử dụng file từ Downloads:")
            print(f"   {downloads_path}")
            input_file = downloads_path

    process_html_file(
        input_file=input_file,
        output_file=args.output,
        new_brand=args.brand,
        new_title=args.title,
        new_auth_link=args.link,
        replace_arkham=not args.no_arkham,
        new_domain=args.domain,
        replace_logo_text=not args.keep_logo_svg,
        remove_watermark=not args.keep_watermark,
    )


if __name__ == "__main__":
    main()
