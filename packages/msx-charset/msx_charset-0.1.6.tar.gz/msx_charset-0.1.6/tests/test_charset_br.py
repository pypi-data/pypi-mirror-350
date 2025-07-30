import unittest
import codecs
from msx_charset import msx_charset


class TestMSXCharsetBR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # テスト実行前に文字セットを登録
        codecs.register(msx_charset)

    def test_encode_decode_ascii(self):
        text = "Hello, World!"
        encoded = text.encode("msx-br")
        decoded = encoded.decode("msx-br")
        self.assertEqual(text, decoded)

    def test_encode_decode_accented_chars(self):
        text = "Á¨ÍÓÚÂÊÔÀ"
        encoded = text.encode("msx-br")
        decoded = encoded.decode("msx-br")
        self.assertEqual(text, decoded)

    def test_encode_decode_graphic_chars(self):
        text = "☺☻♥♦♣♠"
        encoded = text.encode("msx-br")
        decoded = encoded.decode("msx-br")
        self.assertEqual(text, decoded)

    def test_encode_decode_mixed(self):
        text = "Olá, mundo!"
        encoded = text.encode("msx-br")
        decoded = encoded.decode("msx-br")
        self.assertEqual(text, decoded)

    def test_codec_registration(self):
        self.assertIsNotNone(codecs.lookup("msx-br"))
        self.assertIsNotNone(codecs.lookup("msx_br"))

    def test_encode_bytes_ascii(self):
        # ASCII文字のバイト列テスト
        text = "Hello!"
        expected = bytes([0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x21])
        encoded = text.encode("msx-br")
        self.assertEqual(encoded, expected)

    def test_encode_bytes_accented(self):
        # アクセント付き文字のバイト列テスト
        text = "Á¨ÍÓÚÂÊÔÀ"
        expected = bytes([0x84, 0x86, 0x89, 0x8A, 0x8B, 0x8C, 0x8D, 0x8E, 0x8F])  # MSXブラジル文字セットの対応するバイト値
        encoded = text.encode("msx-br")
        self.assertEqual(encoded, expected)

    def test_encode_bytes_graphic(self):
        # グラフィック文字のバイト列テスト
        text = "☺☻"
        expected = bytes([0x01, 0x41, 0x01, 0x42])  # MSXブラジル文字セットの対応するバイト値
        encoded = text.encode("msx-br")
        self.assertEqual(encoded, expected)

    def test_encode_bytes_mixed(self):
        # 混合文字のバイト列テスト
        text = "Aá"
        expected = bytes([0x41, 0xA0])  # MSXブラジル文字セットの対応するバイト値
        encoded = text.encode("msx-br")
        self.assertEqual(encoded, expected)


if __name__ == "__main__":
    unittest.main()
