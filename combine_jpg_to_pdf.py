import os
import img2pdf
from PIL import Image
from tqdm import tqdm

def compress_and_resize_image(input_path, output_path, max_width, max_height, quality):
    with Image.open(input_path) as img:
        width, height = img.size
        aspect_ratio = width / height
        
        if width > height:
            if width > max_width:
                width = max_width
                height = int(max_width / aspect_ratio)
        else:
            if height > max_height:
                height = max_height
                width = int(max_height * aspect_ratio)
        
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        img.save(output_path, "JPEG", quality=quality)

def main():
    folder_path = input("請輸入資料夾路徑：")
    if not os.path.exists(folder_path):
        print("資料夾不存在。")
        return

    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    folder_name = os.path.basename(os.path.normpath(folder_path))
    output_pdf_path = os.path.join(output_folder, f"{folder_name}.pdf")

    try:
        quality = int(input("請輸入壓縮比（1-100，預設為70）：") or 70)
    except ValueError:
        print("輸入無效，使用預設壓縮比70。")
        quality = 70

    images = sorted([f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')])
    
    compressed_images = []
    temp_folder = os.path.join(output_folder, "temp")
    os.makedirs(temp_folder, exist_ok=True)

    print("壓縮並調整大小中...")
    for img_name in tqdm(images, desc="處理圖片"):
        input_path = os.path.join(folder_path, img_name)
        output_path = os.path.join(temp_folder, img_name)
        compress_and_resize_image(input_path, output_path, 1920, 1920, quality)
        compressed_images.append(output_path)

    print("合併圖片成PDF中...")
    with open(output_pdf_path, "wb") as f:
        f.write(img2pdf.convert(compressed_images))

    print(f"PDF檔案已儲存至：{output_pdf_path}")

    for img_path in compressed_images:
        os.remove(img_path)
    os.rmdir(temp_folder)

if __name__ == "__main__":
    main()
