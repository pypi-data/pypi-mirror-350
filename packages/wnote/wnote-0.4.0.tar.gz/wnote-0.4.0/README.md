# WNote - Terminal Note Taking Application

WNote là ứng dụng ghi chú CLI chạy hoàn toàn trên terminal với giao diện đẹp mắt và dễ sử dụng.

![WNote Screenshot](https://via.placeholder.com/800x450.png?text=WNote+Terminal+Application)

## Tính năng

- ✏️ Tạo, chỉnh sửa, xem và xóa ghi chú
- 🏷️ Gắn thẻ (tag) cho ghi chú
- 🎨 Tùy chỉnh màu sắc cho từng thẻ
- 🔍 Lọc ghi chú theo thẻ
- 📝 Soạn thảo ghi chú với trình soạn thảo yêu thích của bạn (vim, nano, etc.)
- 📎 Đính kèm file hoặc thư mục vào ghi chú
- 🖥️ Mở file/thư mục đính kèm trực tiếp từ ghi chú
- 📊 Thống kê và phân tích ghi chú
- 🔐 Mã hóa ghi chú quan trọng
- 📅 Lịch và nhắc nhở cho ghi chú
- 📤 Xuất ghi chú sang nhiều định dạng (Markdown, PDF, HTML)

## Cài đặt

### Yêu cầu

- Python 3.7+
- pip

### Cài đặt từ PyPI

```bash
pip install wnote
```

## Sử dụng

### Các lệnh cơ bản

- Tạo ghi chú mới:
```bash
wnote add "Tiêu đề ghi chú" -t "tag1,tag2"
```

- Tạo ghi chú với file đính kèm:
```bash
wnote add "Tiêu đề ghi chú" -f "/đường/dẫn/đến/file"
```

- Đính kèm file vào ghi chú hiện có:
```bash
wnote attach 1 "/đường/dẫn/đến/file"
```

- Xem tất cả ghi chú:
```bash
wnote show
```

- Xem ghi chú theo ID:
```bash
wnote show 1
```

- Xem ghi chú theo ID và tự động mở tất cả file đính kèm:
```bash
wnote show 1 -o
```

- Xem ghi chú theo thẻ:
```bash
wnote show -t "work"
```

- Chỉnh sửa nội dung ghi chú:
```bash
wnote edit 1
```

- Cập nhật tiêu đề hoặc thẻ:
```bash
wnote update 1 -t "new title" --tags "tag1,tag2,tag3"
```

- Xóa ghi chú:
```bash
wnote delete 1
```

- Xem tất cả thẻ:
```bash
wnote tags
```

- Đặt màu cho thẻ:
```bash
wnote color work blue
```

- Xem cấu hình:
```bash
wnote config
```

### Các tính năng mới

- Xuất ghi chú sang Markdown:
```bash
wnote export 1 --format markdown
```

- Mã hóa ghi chú:
```bash
wnote encrypt 1
```

- Thống kê ghi chú:
```bash
wnote stats
```

- Tùy chỉnh chủ đề màu:
```bash
wnote theme dark
```

## Đường dẫn cấu hình

- Cơ sở dữ liệu: `~/.config/wnote/notes.db`
- Tệp cấu hình: `~/.config/wnote/config.json`
- Thư mục đính kèm: `~/.config/wnote/attachments`

## Các màu có sẵn

- red, green, blue, yellow, magenta, cyan, white, black
- bright_red, bright_green, bright_blue, bright_yellow, bright_magenta, bright_cyan, bright_white

## Giấy phép

Phân phối dưới giấy phép MIT. Xem `LICENSE` để biết thêm chi tiết. 