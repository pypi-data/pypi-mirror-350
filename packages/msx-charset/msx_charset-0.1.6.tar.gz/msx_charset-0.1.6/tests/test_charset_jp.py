import unittest
import codecs
from msx_charset import msx_charset


class TestMSXCharsetJP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # テスト実行前にコーデックを登録
        codecs.register(msx_charset)

    def test_encode_decode_ascii(self):
        text = "Hello, World!"
        encoded = text.encode("msx-jp")
        decoded = encoded.decode("msx-jp")
        self.assertEqual(text, decoded)

    def test_encode_decode_hiragana(self):
        text = "こんにちは"
        encoded = text.encode("msx-jp")
        decoded = encoded.decode("msx-jp")
        self.assertEqual(text, decoded)

    def test_encode_decode_katakana(self):
        text = "コンニチハ"
        encoded = text.encode("msx-jp")
        decoded = encoded.decode("msx-jp")
        self.assertEqual(text, decoded)

    def test_encode_decode_dakuten(self):
        text = "がぎぐげご"
        encoded = text.encode("msx-jp")
        decoded = encoded.decode("msx-jp")
        self.assertEqual(text, decoded)

    def test_encode_decode_handakuten(self):
        text = "ぱぴぷぺぽ"
        encoded = text.encode("msx-jp")
        decoded = encoded.decode("msx-jp")
        self.assertEqual(text, decoded)

    def test_encode_decode_graphic_chars(self):
        text = "月火水木金土日"
        encoded = text.encode("msx-jp")
        decoded = encoded.decode("msx-jp")
        self.assertEqual(text, decoded)

    def test_encode_decode_mixed(self):
        text = "Hello、こんにちは！"
        encoded = text.encode("msx-jp")
        decoded = encoded.decode("msx-jp")
        self.assertEqual(text, decoded)

    def test_codec_registration(self):
        self.assertIsNotNone(codecs.lookup("msx-jp"))
        self.assertIsNotNone(codecs.lookup("msx_jp"))

    def test_encode_bytes_ascii(self):
        # ASCII文字のバイト列テスト
        text = "Hello!"
        expected = bytes([0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x21])
        encoded = text.encode("msx-jp")
        self.assertEqual(encoded, expected)

    def test_encode_bytes_hiragana(self):
        # ひらがなのバイト列テスト
        text = "こんにちは"
        expected = bytes([0x9A, 0xFD, 0xE6, 0xE1, 0xEA])
        encoded = text.encode("msx-jp")
        self.assertEqual(encoded, expected)

    def test_encode_bytes_katakana(self):
        # カタカナのバイト列テスト
        text = "コンニチハ"
        expected = bytes([0xBA, 0xDD, 0xC6, 0xC1, 0xCA])
        encoded = text.encode("msx-jp")
        self.assertEqual(encoded, expected)

    def test_encode_bytes_dakuten(self):
        # 濁点文字のバイト列テスト
        text = "がぎ"
        expected = bytes([0x96, 0xDE, 0x97, 0xDE])
        encoded = text.encode("msx-jp")
        self.assertEqual(encoded, expected)

    def test_encode_bytes_handakuten(self):
        # 半濁点文字のバイト列テスト
        text = "ぱぴ"
        expected = bytes([0xEA, 0xDF, 0xEB, 0xDF])
        encoded = text.encode("msx-jp")
        self.assertEqual(encoded, expected)

    def test_encode_bytes_graphic(self):
        # グラフィック文字のバイト列テスト
        text = "月火"
        expected = bytes([0x01, 0x41, 0x01, 0x42])
        encoded = text.encode("msx-jp")
        self.assertEqual(encoded, expected)

    def test_encode_bytes_mixed(self):
        # 混合文字のバイト列テスト
        text = "A、あ"
        expected = bytes([0x41, 0xA4, 0x91])
        encoded = text.encode("msx-jp")
        self.assertEqual(encoded, expected)


if __name__ == "__main__":
    unittest.main()
