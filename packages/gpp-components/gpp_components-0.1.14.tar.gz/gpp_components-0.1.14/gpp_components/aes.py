from Crypto.Cipher import AES
import base64


class Aes:
    def __init__(self, KEY: str, IV: str):
        self._key = KEY
        self._iv = IV

    def pad(self, data):
        text = data + chr(16 - len(data) % 16) * (16 - len(data) % 16)
        return text

    def cbc_encrypt(self, txt):
        key = self._key.encode("utf-8")
        iv = self._iv.encode("utf-8")
        txt = self.pad(txt)
        txt = str(txt).encode("utf-8")
        aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)  # 创建解密对象
        ciphertext = base64.b64encode(aes.encrypt(txt))
        return str(ciphertext, "utf-8")

    def cbc_decrypt(self, txt):  # CBC模式的解密函数，data为密文，key为16字节密钥
        key = self._key.encode("utf-8")
        iv = self._iv.encode("utf-8")
        aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)  # 创建解密对象
        plaintext = aes.decrypt(base64.b64decode(txt))
        # return str(plaintext, "unicode_escape").strip("\x00")
        return plaintext.decode("utf-8").strip('\x00')
