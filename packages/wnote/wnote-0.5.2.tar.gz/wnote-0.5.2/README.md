# WNote - Terminal Note Taking Application

WNote is a beautiful and user-friendly CLI note-taking application that runs entirely in the terminal.

![WNote Screenshot](https://via.placeholder.com/800x450.png?text=WNote+Terminal+Application)

## Features

- ✏️ Create, edit, view, and delete notes
- 🏷️ Tag notes for better organization
- 🎨 Customize colors for each tag
- 🔍 Filter notes by tags and search content
- 📝 Edit notes with your favorite editor (vim, nano, etc.)
- 📎 Attach files or directories to notes
- 🖥️ Open attachments directly from notes
- 📊 Statistics and note analysis
- ⏰ Reminders for notes
- 📤 Export notes to multiple formats (Markdown, HTML, Text)

## Recent Updates (v0.5.2)

🔧 **Critical Bug Fixes:**
- **Fixed attachment inheritance bug**: New notes with reused IDs no longer inherit attachments from deleted notes
- **Fixed timezone issue**: All timestamps now use local system time instead of UTC
- **Improved data integrity**: Enabled SQLite foreign key constraints for proper cascade deletion
- **Enhanced attachment management**: Better error handling and explicit cleanup of attachment files

🚀 **Improvements:**
- Better datetime parsing with support for both standard and ISO formats
- More robust attachment deletion process
- Enhanced database connection reliability

## Installation

### Requirements

- Python 3.7+
- pip

### Install from PyPI

```bash
pip install wnote
```

### Install from Source

```bash
git clone https://github.com/yourusername/wnote.git
cd wnote
pip install -e .
```

## Usage

### Basic Commands

- Create a new note:
```bash
wnote add "Note Title" -t "tag1,tag2"
```

- Create a note with attachment:
```bash
wnote add "Note Title" -f "/path/to/file"
```

- Attach file to existing note:
```bash
wnote attach 1 "/path/to/file"
```

- Remove attachment from note:
```bash
wnote deattach 1 --attachment-id 1
```

- View all notes:
```bash
wnote show
```

- View note by ID:
```bash
wnote show 1
```

- View note and open attachments:
```bash
wnote show 1 -o
```

- View notes by tag:
```bash
wnote show -t "work"
```

- Search notes:
```bash
wnote search "keyword"
```

- Edit note content:
```bash
wnote edit 1
```

- Update title or tags:
```bash
wnote update 1 -t "new title" --tags "tag1,tag2,tag3"
```

- Delete note:
```bash
wnote delete 1
```

- Delete tag:
```bash
wnote delete tag_name --tag
```

- View all tags:
```bash
wnote tags
```

- Set tag color:
```bash
wnote color work blue
```

- View configuration:
```bash
wnote config
```

### Advanced Features

- Export note to Markdown:
```bash
wnote export 1 --format markdown
```

- Export note to HTML:
```bash
wnote export 1 --format html --output note.html
```

- View statistics:
```bash
wnote stats
```

- Add reminder to note:
```bash
wnote reminder 1 "2025-12-31 14:30" "Project deadline"
```

- View reminders:
```bash
wnote reminders
```

## Configuration Paths

- Database: `~/.config/wnote/notes.db`
- Config file: `~/.config/wnote/config.json`
- Attachments directory: `~/.config/wnote/attachments`

## Available Colors

- Standard: red, green, blue, yellow, magenta, cyan, white, black
- Bright: bright_red, bright_green, bright_blue, bright_yellow, bright_magenta, bright_cyan, bright_white

## Development

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wnote.git
cd wnote
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Building Package

```bash
python -m build
```

### Publishing to PyPI

1. Update version in `pyproject.toml` and `setup.py`
2. Build package:
```bash
python -m build
```
3. Upload to PyPI:
```bash
python -m twine upload dist/*
```

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

# WNote - Ứng dụng Ghi chú Terminal

WNote là ứng dụng ghi chú CLI chạy hoàn toàn trên terminal với giao diện đẹp mắt và dễ sử dụng.

## Tính năng

- ✏️ Tạo, chỉnh sửa, xem và xóa ghi chú
- 🏷️ Gắn thẻ (tag) cho ghi chú
- 🎨 Tùy chỉnh màu sắc cho từng thẻ
- 🔍 Lọc ghi chú theo thẻ và tìm kiếm nội dung
- 📝 Soạn thảo ghi chú với trình soạn thảo yêu thích của bạn (vim, nano, etc.)
- 📎 Đính kèm file hoặc thư mục vào ghi chú
- 🖥️ Mở file/thư mục đính kèm trực tiếp từ ghi chú
- 📊 Thống kê và phân tích ghi chú
- ⏰ Nhắc nhở cho ghi chú
- 📤 Xuất ghi chú sang nhiều định dạng (Markdown, HTML, Text)

## Cài đặt

### Yêu cầu

- Python 3.7+
- pip

### Cài đặt từ PyPI

```bash
pip install wnote
```

### Cài đặt từ Source

```bash
git clone https://github.com/yourusername/wnote.git
cd wnote
pip install -e .
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

- Bỏ file đính kèm khỏi ghi chú:
```bash
wnote deattach 1 --attachment-id 1
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

- Tìm kiếm ghi chú:
```bash
wnote search "từ khóa"
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

- Xóa thẻ:
```bash
wnote delete tag_name --tag
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

### Các tính năng nâng cao

- Xuất ghi chú sang Markdown:
```bash
wnote export 1 --format markdown
```

- Xuất ghi chú sang HTML:
```bash
wnote export 1 --format html --output note.html
```

- Thống kê ghi chú:
```bash
wnote stats
```

- Thêm nhắc nhở cho ghi chú:
```bash
wnote reminder 1 "2025-12-31 14:30" "Deadline cho dự án"
```

- Xem các nhắc nhở:
```bash
wnote reminders
```

## Đường dẫn cấu hình

- Cơ sở dữ liệu: `~/.config/wnote/notes.db`
- Tệp cấu hình: `~/.config/wnote/config.json`
- Thư mục đính kèm: `~/.config/wnote/attachments`

## Các màu có sẵn

- Chuẩn: red, green, blue, yellow, magenta, cyan, white, black
- Sáng: bright_red, bright_green, bright_blue, bright_yellow, bright_magenta, bright_cyan, bright_white

## Phát triển

### Thiết lập môi trường phát triển

1. Clone repository:
```bash
git clone https://github.com/yourusername/wnote.git
cd wnote
```

2. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# hoặc
venv\Scripts\activate  # Windows
```

3. Cài đặt các gói phát triển:
```bash
pip install -e ".[dev]"
```

### Chạy kiểm thử

```bash
pytest
```

### Đóng gói

```bash
python -m build
```

### Đăng lên PyPI

1. Cập nhật phiên bản trong `pyproject.toml` và `setup.py`
2. Đóng gói:
```bash
python -m build
```
3. Đăng lên PyPI:
```bash
python -m twine upload dist/*
```

## Giấy phép

Phân phối dưới giấy phép MIT. Xem `LICENSE` để biết thêm chi tiết. 