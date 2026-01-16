Tool được viết ra với mục đích chia sẻ và học tập. Nên cân nhắc trước khi sử dụng.  
Tool Mewmew có gì :  
    - Chạy trực tiếp không cần cài đặt  
    - Tool không có giao diện ( tránh bị nghi ngờ )  
    - Mã hoá file bằng public key , chỉ có nắm giữ private key mới có thể giải mã.  
    - Có khả năng quét toàn bộ ổ đĩa và mã hoá file  
Demo:  
[Video Demo](Images/demo_videos.mp4)  

Đây là một chương trình mã hóa dữ liệu các tệp trong hệ thống bằng cách sử dụng mã hóa lai (hybrid encryption), kết hợp giữa mã hóa bất đối xứng (RSA) và mã hóa đối xứng (AES). Sau đây là cách thức hoạt động của chương trình:

### 1\. Tải khóa công khai (RSA)

*   Hàm load\_public\_key() tải khóa công khai RSA từ một chuỗi đã được mã hóa base64. Khóa công khai này sẽ được dùng để mã hóa khóa AES (khóa dùng để mã hóa dữ liệu thực tế trong các tệp).
    

### 2\. Mã hóa tệp với AES và RSA

*   **AES Key Generation**: Trong hàm encrypt\_file, một khóa AES ngẫu nhiên 256-bit và một IV (Initialization Vector) ngẫu nhiên 128-bit được tạo ra. Khóa này sẽ được dùng để mã hóa nội dung của file.
    
*   **AES Encryption**: Nội dung file được mã hóa bằng thuật toán AES ở chế độ CBC (Cipher Block Chaining). Để đảm bảo dữ liệu đủ độ dài, chương trình sử dụng padding PKCS7.AES yêu cầu dữ liệu đầu vào phải có kích thước là bội số của độ dài khối (block size, 128-bit hoặc 16 bytes). Tuy nhiên, dữ liệu trong tệp không phải lúc nào cũng đủ độ dài. Do đó, chương trình sử dụng một kỹ thuật gọi là "padding" để thêm dữ liệu phụ vào cuối nội dung, giúp nó đạt đủ độ dài yêu cầu.  
    
*   **RSA Encryption of AES Key**: Khóa AES ngẫu nhiên này được mã hóa bằng khóa công khai RSA, đảm bảo rằng chỉ có người giữ khóa riêng RSA tương ứng mới có thể giải mã và truy cập vào khóa AES.
    
*   **Save Encrypted Data**: Tệp mã hóa cuối cùng chứa:
    
    *   Khóa AES đã mã hóa (bằng RSA)
        
    *   IV
        
    *   Nội dung tệp đã mã hóa bằng AES
        

### 3\. Đổi đuôi file

*   Sau khi mã hóa thành công, chương trình sẽ đổi đuôi file thành .mewmew.
    

### 4\. Mã hóa các file trong một thư mục hoặc ổ đĩa

*   Hàm encrypt\_directory quét qua tất cả các file trong thư mục và mã hóa từng file.
    
*   Hàm get\_all\_drives liệt kê tất cả các ổ đĩa trong hệ thống Windows. Chương trình sẽ mã hóa tất cả các file trong tất cả các ổ đĩa.
    

### Cơ chế mã hóa chính:

*   **Hybrid Encryption** (Mã hóa lai): Sử dụng RSA để mã hóa khóa AES và AES để mã hóa dữ liệu thực tế trong file, nhằm tối ưu hóa tốc độ và bảo mật.
                        
#### Stargazers over time
[![Stargazers over time](https://starchart.cc/netease-im/camellia.svg?variant=adaptive)](https://starchart.cc/netease-im/camellia)

                    
