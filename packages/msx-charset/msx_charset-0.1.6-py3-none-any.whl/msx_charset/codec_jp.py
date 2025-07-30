from .codec_base import MSXCodecBase

# MSX-specific Japanese and symbol characters (0x80-0xFE)
MSX_CUSTOM_MAP_JP = {
    # Column 1 (0x80-0x9F): Special characters and hiragana
    0x80: '♠', 0x81: '♥', 0x82: '♣', 0x83: '♦',
    0x84: '○', 0x85: '●', 0x86: 'を', 0x87: 'ぁ',
    0x88: 'ぃ', 0x89: 'ぅ', 0x8A: 'ぇ', 0x8B: 'ぉ',
    0x8C: 'ゃ', 0x8D: 'ゅ', 0x8E: 'ょ', 0x8F: 'っ',
    0x90: '　', 0x91: 'あ', 0x92: 'い', 0x93: 'う',
    0x94: 'え', 0x95: 'お', 0x96: 'か', 0x97: 'き',
    0x98: 'く', 0x99: 'け', 0x9A: 'こ', 0x9B: 'さ',
    0x9C: 'し', 0x9D: 'す', 0x9E: 'せ', 0x9F: 'そ',

    # Column 2 (0xA0-0xBF): Symbols and katakana
    0xA0: '　', 0xA1: '。', 0xA2: '「', 0xA3: '」',
    0xA4: '、', 0xA5: '・', 0xA6: 'ヲ', 0xA7: 'ァ',
    0xA8: 'ィ', 0xA9: 'ゥ', 0xAA: 'ェ', 0xAB: 'ォ',
    0xAC: 'ャ', 0xAD: 'ュ', 0xAE: 'ョ', 0xAF: 'ッ',
    0xB0: 'ー', 0xB1: 'ア', 0xB2: 'イ', 0xB3: 'ウ',
    0xB4: 'エ', 0xB5: 'オ', 0xB6: 'カ', 0xB7: 'キ',
    0xB8: 'ク', 0xB9: 'ケ', 0xBA: 'コ', 0xBB: 'サ',
    0xBC: 'シ', 0xBD: 'ス', 0xBE: 'セ', 0xBF: 'ソ',

    # Column 3 (0xC0-0xDF): Katakana (continued)
    0xC0: 'タ', 0xC1: 'チ', 0xC2: 'ツ', 0xC3: 'テ',
    0xC4: 'ト', 0xC5: 'ナ', 0xC6: 'ニ', 0xC7: 'ヌ',
    0xC8: 'ネ', 0xC9: 'ノ', 0xCA: 'ハ', 0xCB: 'ヒ',
    0xCC: 'フ', 0xCD: 'ヘ', 0xCE: 'ホ', 0xCF: 'マ',
    0xD0: 'ミ', 0xD1: 'ム', 0xD2: 'メ', 0xD3: 'モ',
    0xD4: 'ヤ', 0xD5: 'ユ', 0xD6: 'ヨ', 0xD7: 'ラ',
    0xD8: 'リ', 0xD9: 'ル', 0xDA: 'レ', 0xDB: 'ロ',
    0xDC: 'ワ', 0xDD: 'ン', 0xDE: '゛', 0xDF: '゜',

    # Column 4 (0xE0-0xFE): Hiragana (continued)
    0xE0: 'た', 0xE1: 'ち', 0xE2: 'つ', 0xE3: 'て',
    0xE4: 'と', 0xE5: 'な', 0xE6: 'に', 0xE7: 'ぬ',
    0xE8: 'ね', 0xE9: 'の', 0xEA: 'は', 0xEB: 'ひ',
    0xEC: 'ふ', 0xED: 'へ', 0xEE: 'ほ', 0xEF: 'ま',
    0xF0: 'み', 0xF1: 'む', 0xF2: 'め', 0xF3: 'も',
    0xF4: 'や', 0xF5: 'ゆ', 0xF6: 'よ', 0xF7: 'ら',
    0xF8: 'り', 0xF9: 'る', 0xFA: 'れ', 0xFB: 'ろ',
    0xFC: 'わ', 0xFD: 'ん', 0xFE: '！'  # Full-width exclamation mark
}

# Graphic character mapping (2-byte characters)
GRAPHIC_CHAR_MAP_JP = {
    '月': (0x01, 0x41), '火': (0x01, 0x42), '水': (0x01, 0x43),
    '木': (0x01, 0x44), '金': (0x01, 0x45), '土': (0x01, 0x46),
    '日': (0x01, 0x47), '年': (0x01, 0x48), '円': (0x01, 0x49),
    '時': (0x01, 0x4A), '分': (0x01, 0x4B), '秒': (0x01, 0x4C),
    '百': (0x01, 0x4D), '千': (0x01, 0x4E), '万': (0x01, 0x4F),
    'π': (0x01, 0x50), '┴': (0x01, 0x51), '┬': (0x01, 0x52),
    '┤': (0x01, 0x53), '├': (0x01, 0x54), '┼': (0x01, 0x55),
    '│': (0x01, 0x56), '─': (0x01, 0x57), '┌': (0x01, 0x58),
    '┐': (0x01, 0x59), '└': (0x01, 0x5A), '┘': (0x01, 0x5B),
    '×': (0x01, 0x5C), '大': (0x01, 0x5D), '中': (0x01, 0x5E),
    '小': (0x01, 0x5F)
}

# Voiced sound mark and semi-voiced sound mark mapping
DAKUTEN_MAP = {
    'が': ('か', 0xDE), 'ぎ': ('き', 0xDE), 'ぐ': ('く', 0xDE),
    'げ': ('け', 0xDE), 'ご': ('こ', 0xDE),
    'ざ': ('さ', 0xDE), 'じ': ('し', 0xDE), 'ず': ('す', 0xDE),
    'ぜ': ('せ', 0xDE), 'ぞ': ('そ', 0xDE),
    'だ': ('た', 0xDE), 'ぢ': ('ち', 0xDE), 'づ': ('つ', 0xDE),
    'で': ('て', 0xDE), 'ど': ('と', 0xDE),
    'ば': ('は', 0xDE), 'び': ('ひ', 0xDE), 'ぶ': ('ふ', 0xDE),
    'べ': ('へ', 0xDE), 'ぼ': ('ほ', 0xDE),
    'ぱ': ('は', 0xDF), 'ぴ': ('ひ', 0xDF), 'ぷ': ('ふ', 0xDF),
    'ぺ': ('へ', 0xDF), 'ぽ': ('ほ', 0xDF),
    'ガ': ('カ', 0xDE), 'ギ': ('キ', 0xDE), 'グ': ('ク', 0xDE),
    'ゲ': ('ケ', 0xDE), 'ゴ': ('コ', 0xDE),
    'ザ': ('サ', 0xDE), 'ジ': ('シ', 0xDE), 'ズ': ('ス', 0xDE),
    'ゼ': ('セ', 0xDE), 'ゾ': ('ソ', 0xDE),
    'ダ': ('タ', 0xDE), 'ヂ': ('チ', 0xDE), 'ヅ': ('ツ', 0xDE),
    'デ': ('テ', 0xDE), 'ド': ('ト', 0xDE),
    'バ': ('ハ', 0xDE), 'ビ': ('ヒ', 0xDE), 'ブ': ('フ', 0xDE),
    'ベ': ('ヘ', 0xDE), 'ボ': ('ホ', 0xDE),
    'パ': ('ハ', 0xDF), 'ピ': ('ヒ', 0xDF), 'プ': ('フ', 0xDF),
    'ペ': ('ヘ', 0xDF), 'ポ': ('ホ', 0xDF)
}


class MSXJapaneseCodec(MSXCodecBase):
    """Japanese MSX character set codec"""

    def __init__(self):
        super().__init__('msx-jp', MSX_CUSTOM_MAP_JP, GRAPHIC_CHAR_MAP_JP)
        self.dakuten_map = DAKUTEN_MAP
        self.dakuten_reverse_map = {(v, m): k for k, (v, m) in DAKUTEN_MAP.items()}

    def encode(self, text, errors='strict'):
        """Convert UTF-8 string to MSX code byte sequence (Japanese)"""
        result = bytearray()
        for char in text:
            if char in self.graphic_map:
                result.extend(self.graphic_map[char])
            elif char in self.dakuten_map:
                base, mark = self.dakuten_map[char]
                result.extend([self.char_reverse_map.get(base, 0x3F), mark])
            else:
                result.append(self.char_reverse_map.get(char, 0x3F))
        return bytes(result), len(text)

    def decode(self, codes, errors='strict'):
        """Convert MSX code byte sequence to UTF-8 string"""
        result = []
        i = 0
        codes_len = len(codes)

        while i < codes_len:
            code = codes[i]

            # Handle graphic characters
            if code == 0x01 and i + 1 < codes_len:
                next_code = codes[i + 1]
                char = self.graphic_reverse_map.get((code, next_code))
                if char:
                    result.append(char)
                    i += 2
                    continue

            # Handle dakuten/handakuten
            if i + 1 < codes_len and codes[i + 1] in (0xDE, 0xDF):
                base_char = self.char_map.get(code)
                mark = codes[i + 1]
                composed = self.dakuten_reverse_map.get((base_char, mark))
                if composed:
                    result.append(composed)
                else:
                    mark_char = '゛' if mark == 0xDE else '゜'
                    result.append(base_char + mark_char)
                i += 2
            else:
                result.append(self.char_map.get(code, '?'))
                i += 1

        return ''.join(result), len(codes)


# Create codec instance
msx_codec_jp = MSXJapaneseCodec().codec_info
