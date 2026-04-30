from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
import base64
from core.constants import ZW_ZERO, ZW_ONE, ZW_SPACE


class SteganographyEngine:
    @staticmethod
    def generate_fernet_key(seed: bytes | None = None) -> bytes:
        if not seed:
            return Fernet.generate_key()
        digest = hashes.Hash(hashes.SHA256())
        digest.update(seed)
        key = digest.finalize()
        return base64.urlsafe_b64encode(key[:32])

    @staticmethod
    def encrypt(key: bytes, text: str) -> str:
        fernet = Fernet(key)
        encrypted = fernet.encrypt(text.encode('utf-8'))
        return encrypted.decode('utf-8')

    @staticmethod
    def decrypt(key: bytes, text: str) -> str:
        fernet = Fernet(key)
        try:
            decrypted = fernet.decrypt(text.encode('utf-8'))
            return decrypted.decode('utf-8')
        except InvalidToken:
            raise ValueError("Invalid decryption key or corrupted data")

    @staticmethod
    def text_to_binary(key: bytes, text: str) -> str:
        encrypted = SteganographyEngine.encrypt(key, text)
        binary_chunks = [format(ord(char), '08b') for char in encrypted]
        return ' '.join(binary_chunks)

    @staticmethod
    def binary_to_text(key: bytes, binary: str) -> str:
        if not binary.strip():
            raise ValueError("Empty binary data")
        
        binary_chunks = binary.split()
        encrypted_chars = []
        
        for chunk in binary_chunks:
            if len(chunk) != 8:
                raise ValueError(f"Invalid binary chunk length: {len(chunk)} (expected 8)")
            if not all(c in '01' for c in chunk):
                raise ValueError(f"Invalid binary character in chunk: {chunk}")
            encrypted_chars.append(chr(int(chunk, 2)))
        
        encrypted_text = ''.join(encrypted_chars)
        return SteganographyEngine.decrypt(key, encrypted_text)

    @staticmethod
    def binary_to_zero_width(binary: str) -> list:
        result = []
        for char in binary:
            if char == '0':
                result.append(ZW_ZERO)
            elif char == '1':
                result.append(ZW_ONE)
            elif char == ' ':
                result.append(ZW_SPACE)
            else:
                raise ValueError(f"Invalid binary character: {char}")
        return result

    @staticmethod
    def zero_width_to_binary(text: str) -> str:
        binary_chars = []
        for char in text:
            if char == ZW_ZERO:
                binary_chars.append('0')
            elif char == ZW_ONE:
                binary_chars.append('1')
            elif char == ZW_SPACE:
                binary_chars.append(' ')
        return ''.join(binary_chars)

    @staticmethod
    def has_zero_width_chars(text: str) -> bool:
        return any(char in (ZW_ZERO, ZW_ONE, ZW_SPACE) for char in text)

    @staticmethod
    def hide_message(key: bytes, secret: str, carrier: str) -> str:
        if not secret:
            raise ValueError("No secret message to hide")
        if not carrier:
            raise ValueError("No carrier text provided")
        binary_msg = SteganographyEngine.text_to_binary(key, secret)
        zw_chars = SteganographyEngine.binary_to_zero_width(binary_msg)
        carrier_list = list(carrier)
        for i, zw_char in enumerate(zw_chars):
            carrier_list.insert(1 + i, zw_char)
        
        return ''.join(carrier_list)

    @staticmethod
    def extract_message(key: bytes, combined: str) -> str:
        if not SteganographyEngine.has_zero_width_chars(combined):
            raise ValueError("No hidden message found in the text")
        binary_msg = SteganographyEngine.zero_width_to_binary(combined)
        if not binary_msg.strip():
            raise ValueError("No binary data found")
        return SteganographyEngine.binary_to_text(key, binary_msg)
