"""
Tạo icon cho FFmpeg Auto Setup
Chạy 1 lần để tạo assets/icon.ico
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Tạo các kích thước icon
    sizes = [16, 32, 48, 64, 128, 256]
    images = []

    for size in sizes:
        # Tạo image với background gradient-like
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Vẽ hình tròn nền
        padding = size // 10
        draw.ellipse(
            [padding, padding, size - padding, size - padding],
            fill='#89b4fa'  # Catppuccin blue
        )

        # Vẽ chữ "FF" ở giữa
        try:
            font_size = size // 3
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        text = "FF"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (size - text_width) // 2
        y = (size - text_height) // 2 - size // 10

        draw.text((x, y), text, fill='#1e1e2e', font=font)

        images.append(img)

    # Lưu icon
    output_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Lưu với nhiều kích thước
    images[0].save(
        output_path,
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=images[1:]
    )

    print(f"Icon created: {output_path}")
    return output_path


if __name__ == "__main__":
    create_icon()
