import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as symmetric_padding
from cryptography.hazmat.primitives.asymmetric import rsa

# Tải khóa riêng tư từ file PEM
def load_private_key(private_key_path):
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())
    return private_key

# Giải mã file, ghi đè lên file goc
def decrypt_file(file_path, private_key):
    # Đọc dữ liệu từ file đã mã hóa
    with open(file_path, "rb") as f:
        encrypted_aes_key = f.read(256)  # Khóa AES đã mã hóa (RSA)
        iv = f.read(16)  # IV cho AES
        encrypted_data = f.read()  # Dữ liệu đã mã hóa

    # Giải mã khóa AES bằng khóa riêng tư RSA
    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Giải mã dữ liệu bằng AES
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Giải mã dữ liệu và loại bỏ padding
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = symmetric_padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    # Ghi dữ liệu đã giải mã vào file (ghi đè lên file gốc)
    with open(file_path, "wb") as f:
        f.write(data)
    print(f"File '{file_path}' đã được giải mã và ghi đè lên file gốc.")

# Quét và giải mã các file trong một thư mục
def decrypt_directory(directory_path, private_key):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Đang giải mã file: {file_path}")
            decrypt_file(file_path, private_key)

# Quét tất cả các ổ đĩa trên hệ thống Windows
def get_all_drives():
    drives = []
    for drive_letter in range(65, 91):  # Kiểm tra các ổ từ A: đến Z:
        drive = chr(drive_letter) + ":\\"
        if os.path.exists(drive):  # Kiểm tra xem ổ đĩa có tồn tại không
            drives.append(drive)
    return drives

# Chạy chương trình giải mã
if __name__ == "__main__":
    private_key_path = "C:/path/to/your/private_key.pem"  # Thay thế bằng đường dẫn tới file khóa riêng tư PEM
    private_key = load_private_key(private_key_path)  # Tải khóa riêng tư từ file PEM
    drives = get_all_drives()  # Lấy tất cả các ổ đĩa

    for drive in drives:
        print(f"Đang quét ổ đĩa: {drive}")
        decrypt_directory(drive, private_key)  # Giải mã toàn bộ thư mục trong ổ đĩa
