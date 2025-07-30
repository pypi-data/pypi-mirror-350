import codecs
from .codec_jp import msx_codec_jp
from .codec_intl import msx_codec_intl
from .codec_br import msx_codec_br
from ._version import __version__

__all__ = ["msx_codec_jp", "msx_codec_intl", "msx_codec_br"]


def msx_charset(name):
    if name.lower() in ('msx-jp', 'msx_jp'):
        return msx_codec_jp
    elif name.lower() in ('msx-intl', 'msx_intl'):
        return msx_codec_intl
    elif name.lower() in ('msx-br', 'msx_br'):
        return msx_codec_br
    raise LookupError(f"unknown encoding: {name}")


# Register codec
codecs.register(msx_charset)
