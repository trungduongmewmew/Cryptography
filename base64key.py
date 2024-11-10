import base64

# Đọc khóa công khai PEM từ file
with open("public_key.pem", "rb") as f:
    public_key_pem = f.read()

# Mã hóa khóa công khai thành base64
public_key_base64 = base64.b64encode(public_key_pem).decode('utf-8')

# In ra chuỗi base64 của khóa công khai
print(public_key_base64)
