from .core import UrlLink

_tool = UrlLink()

def shorten_url(url):
    return _tool.shorten_url(url)

def generate_qrcode(data, save_path=None, size=200):
    return _tool.generate_qrcode(data, save_path, size)

__all__ = ["shorten_url", "generate_qrcode"]
