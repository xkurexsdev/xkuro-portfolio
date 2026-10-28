# xKuro Portfolio Tracker ⚡

Trang theo dõi danh mục tài sản tiền mã hóa Satoshi Nakamoto, được tùy biến và tái định vị thương hiệu tự động bằng Python & BeautifulSoup.

## 🚀 Live Demo
🌐 **Website:** [https://xkurexsdev.github.io/xkuro-portfolio/](https://xkurexsdev.github.io/xkuro-portfolio/)

---

## 🛠️ Công Nghệ Sử Dụng
- **HTML5 & CSS3** (SingleFile snapshot từ Arkham Intel)
- **Python 3 & BeautifulSoup 4 (BS4)**: Tự động hóa xử lý DOM, chuẩn hóa thương hiệu và làm sạch mã theo dõi.

---

## ⚙️ Tính Năng Tự Động Hóa (`edit_html.py`)
Script [edit_html.py](file:///Users/xuankuandev/Documents/agent-clonevs/edit_html.py) cung cấp quy trình chỉnh sửa toàn diện:
1. **Rebranding:** Tự động thay thế `arkm` / `arkham` thành tên thương hiệu mới (`xKuro`), cập nhật logo navbar và xóa watermark biểu đồ.
2. **Metadata & Title:** Cập nhật `<title>`, `og:title`, `twitter:title` đồng bộ.
3. **Chuyển hướng liên kết:** Cập nhật toàn bộ link đăng ký / đăng nhập trỏ về trang authentication của bạn.
4. **Loại bỏ Trackers:** Tự động quét và xóa sạch Google Analytics / GTM, Facebook Pixel, Cloudflare Insights và các beacon pixel ẩn.

### Cách sử dụng script
```bash
# Cài đặt thư viện:
pip install beautifulsoup4 lxml

# Chạy với thông số mặc định:
python3 edit_html.py

# Hoặc tùy biến thông số qua CLI:
python3 edit_html.py \
  --input output.html \
  --output index.html \
  --brand "xKuro" \
  --title "Satoshi Nakamoto ｜ xKuro Wallet" \
  --link "https://xkuro.io/login" \
  --domain "xkuro.io"
```

---

## 📄 Bản Quyền
Dự án được xây dựng cho mục đích học tập và tùy biến giao diện cá nhân.
