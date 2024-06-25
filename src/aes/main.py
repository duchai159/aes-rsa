from aes import AES
import base64
def main():
    # Khóa master_key
    master_key = b'Sixteen byte key'
    
    # Khởi tạo đối tượng AES
    aes = AES(master_key)
    
    # Plaintext cần mã hóa
    plaintext = b'Hello AES! This is a plaintext'
    
    # Initialization Vector (IV) cho CBC mode
    iv = b'\x00' * 16  
    
    # Mã hóa và giải mã sử dụng ECB mode
    encrypted_ecb = aes.encrypt_ecb(plaintext)
    decrypted_ecb = aes.decrypt_ecb(encrypted_ecb)
    encrypted_base64 = base64.b64encode(encrypted_ecb).decode('utf-8')
    print(f'Plaintext: {plaintext}')
    print(f'Encrypted ECB: {encrypted_base64}')
    print(f'Decrypted ECB: {decrypted_ecb}')
    
    # Mã hóa và giải mã sử dụng CBC mode
    encrypted_cbc = aes.encrypt_cbc(plaintext, iv)
    decrypted_cbc = aes.decrypt_cbc(encrypted_cbc, iv)
    encrypted_base64 = base64.b64encode(encrypted_cbc).decode('utf-8')
    print(f'Encrypted CBC: {encrypted_base64}')
    print(f'Decrypted CBC: {decrypted_cbc}')

if __name__ == "__main__":
    main()