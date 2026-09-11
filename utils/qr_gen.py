import os
import qrcode
from io import BytesIO
from PIL import Image

def generate_qr_code(url: str, output_path: str = "static/judge_qr.png") -> str:
    """
    Generates a high-contrast QR code for the judges and evaluation team.
    Saves the image to disk and returns the relative path.
    """
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="#0F172A", back_color="#FFFFFF")
    img.save(output_path)
    return output_path

def get_qr_code_image(url: str) -> Image.Image:
    """Generates and returns a PIL Image for direct embedding in Streamlit UI."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color="#0F172A", back_color="#FFFFFF").convert("RGB")

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8501"
    out = generate_qr_code(target)
    print(f"[+] Successfully generated QR Code for judges pointing to '{target}' at '{out}'")
