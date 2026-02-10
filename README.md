# FFmpeg Auto Setup

Công cụ cài đặt FFmpeg tự động cho Windows - Dành cho người dùng phổ thông, không cần kiến thức kỹ thuật.

![Windows](https://img.shields.io/badge/Windows-10%2F11-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## Tại sao cần FFmpeg?

**FFmpeg** là công cụ xử lý video/audio mạnh mẽ nhất, được sử dụng bởi:
- **yt-dlp** - Tải video từ YouTube, TikTok,...
- **OBS Studio** - Live stream, ghi màn hình
- **HandBrake** - Chuyển đổi định dạng video
- **Davinci Resolve, Premiere** - Phần mềm edit video chuyên nghiệp
- Và hàng trăm ứng dụng khác...

**Vấn đề thường gặp:**
- Cài đặt FFmpeg thủ công rất phức tạp (tải file, giải nén, thêm PATH)
- Di chuyển/đổi tên folder → mất PATH → lỗi "system cannot find file"
- Người dùng phổ thông không biết PATH là gì

**Giải pháp:** FFmpeg Auto Setup - Cài đặt 1-click, tự động hoàn toàn!

---

## Tính năng

- **1-Click Install** - Chỉ cần nhấn nút, mọi thứ tự động
- **Tự động tải** - Nếu không có file zip, tự động tải từ internet
- **Offline Support** - Đặt file `ffmpeg.zip` cùng thư mục để cài offline
- **Tự động cấu hình PATH** - Không cần chỉnh sửa thủ công
- **Giao diện đẹp** - Dark theme, dễ sử dụng
- **Portable EXE** - Build thành file `.exe` độc lập, không cần Python

---

## Cách sử dụng

### Cách 1: Dùng file EXE (Khuyến nghị)

1. Tải file `FFmpegSetup.exe` từ [Releases](../../releases)
2. (Tùy chọn) Đặt file `ffmpeg.zip` cùng thư mục để cài offline
3. Double-click `FFmpegSetup.exe`
4. Nhấn nút **"Cài đặt FFmpeg"**
5. Đợi hoàn tất, mở CMD mới và gõ `ffmpeg -version`

### Cách 2: Dùng Batch Script (Không cần Python)

```batch
Setup_FFmpeg_NoRequirePython.bat
```
- Script này sử dụng PowerShell (có sẵn trên Windows) để tải và giải nén
- Không cần cài đặt Python

### Cách 3: Dùng Python Script

```batch
Cai_dat_FFmpeg.bat
```
hoặc
```bash
python setup_ffmpeg.py
```

---

## Sau khi cài đặt

### Hướng dẫn sử dụng
- Mở **CMD/PowerShell MỚI** để sử dụng lệnh `ffmpeg`
- **KHÔNG cần** khởi động lại máy
- **KHÔNG cần** Log out

### Kiểm tra cài đặt
```bash
ffmpeg -version
```

### LƯU Ý QUAN TRỌNG

> **TUYỆT ĐỐI KHÔNG:**
> - Đổi tên thư mục `C:\Tools\ffmpeg`
> - Di chuyển thư mục này sang vị trí khác
> - Xóa thư mục này
>
> Nếu vi phạm, FFmpeg sẽ ngừng hoạt động do PATH bị mất!

---

## Cấu trúc thư mục cài đặt

```
C:\Tools\ffmpeg\
└── ffmpeg-master-latest-win64-gpl\
    └── bin\
        ├── ffmpeg.exe      ← Công cụ chính
        ├── ffprobe.exe     ← Phân tích media
        └── ffplay.exe      ← Trình phát media
```

---

## Dành cho Developer

### Yêu cầu hệ thống

- Windows 10/11 (64-bit)
- Python 3.10+ (nếu chạy từ source)

### Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Chạy từ source

```bash
python src/main.py
```

### Build file EXE

```batch
build.bat
```

hoặc thủ công:

```bash
pyinstaller --onefile --windowed --name=FFmpegSetup --clean ^
    --icon=assets/icon.ico ^
    --add-data "src/core;core" ^
    --add-data "src/ui;ui" ^
    --add-data "assets;assets" ^
    src/main.py
```

File output: `dist/FFmpegSetup.exe`

### Cấu trúc project

```
AutoFixFFMpeg/
├── src/
│   ├── main.py              # Entry point
│   ├── core/
│   │   └── installer.py     # Logic cài đặt (tải, giải nén, PATH)
│   └── ui/
│       └── main_window.py   # Giao diện PyQt6
├── assets/
│   ├── icon.ico             # Icon ứng dụng
│   └── icon.jpg             # Icon gốc
├── docs/
│   └── PRD.md               # Product Requirements Document
├── build.bat                # Script build EXE
├── setup_ffmpeg.py          # Script CLI (cần Python)
├── Cai_dat_FFmpeg.bat       # Wrapper cho setup_ffmpeg.py
├── Setup_FFmpeg_NoRequirePython.bat  # Script không cần Python
├── requirements.txt         # Dependencies
├── ffmpeg.zip               # (Tùy chọn) File FFmpeg offline
└── README.md                # File này
```

### Dependencies

| Package | Version | Mô tả |
|---------|---------|-------|
| PyQt6 | >=6.5.0 | Framework GUI |
| pyinstaller | >=6.0.0 | Build EXE |

### Tech Stack

- **GUI Framework:** PyQt6
- **Build Tool:** PyInstaller
- **Nguồn FFmpeg:** [BtbN/FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds)

---

## Xử lý sự cố

### Lỗi "ffmpeg is not recognized"

**Nguyên nhân:** CMD/PowerShell cũ chưa nhận PATH mới

**Giải pháp:** Đóng và mở lại CMD/PowerShell

### Lỗi "system cannot find file"

**Nguyên nhân:** Thư mục FFmpeg đã bị đổi tên hoặc xóa

**Giải pháp:** Chạy lại FFmpeg Auto Setup để cài đặt lại

### Lỗi tải file từ internet

**Nguyên nhân:** Mạng chậm hoặc bị firewall chặn

**Giải pháp:**
1. Tải thủ công từ: https://github.com/BtbN/FFmpeg-Builds/releases
2. Đặt file `.zip` cùng thư mục với FFmpegSetup.exe
3. Chạy lại chương trình

### Muốn cài đặt vào thư mục khác

Hiện tại chương trình cài đặt cố định vào `C:\Tools\ffmpeg`. Nếu muốn thay đổi:

1. Mở file `src/core/installer.py`
2. Sửa dòng: `FFMPEG_INSTALL_DIR = r"C:\Tools\ffmpeg"`
3. Build lại EXE

---

## Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

---

## License

MIT License - Xem file [LICENSE](LICENSE) để biết thêm chi tiết.

---

## Tác giả

**Diện Tech**
- Hotline: 0973323090
- Facebook: [Nguyễn Duy Diện](https://www.facebook.com/nguyenduydien)

Được tạo với love cho cộng đồng Việt Nam.

---

## Liên kết hữu ích

- [FFmpeg Official](https://ffmpeg.org/)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [BtbN/FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds) - Nguồn tải FFmpeg
