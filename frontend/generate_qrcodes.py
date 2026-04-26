import qrcode
from PIL import Image
import os

# 输出目录
output_dir = os.path.dirname(os.path.abspath(__file__))

# 网站体验二维码
website_url = "https://luvoy.cn"
qr_website = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr_website.add_data(website_url)
qr_website.make(fit=True)
img_website = qr_website.make_image(fill_color="black", back_color="white")
website_path = os.path.join(output_dir, "qr_website.png")
img_website.save(website_path)
print(f"网站二维码已生成: {website_path}")

# APK下载二维码
apk_url = "https://luvoy.cn/Luvoy.apk"
qr_apk = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
)
qr_apk.add_data(apk_url)
qr_apk.make(fit=True)
img_apk = qr_apk.make_image(fill_color="black", back_color="white")
apk_path = os.path.join(output_dir, "qr_apk_download.png")
img_apk.save(apk_path)
print(f"APK下载二维码已生成: {apk_path}")

print("\n二维码内容:")
print(f"1. 网站体验: {website_url}")
print(f"2. APK下载: {apk_url}")
