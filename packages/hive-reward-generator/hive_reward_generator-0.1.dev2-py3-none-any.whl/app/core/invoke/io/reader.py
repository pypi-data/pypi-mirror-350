import urllib.parse
import urllib.request


def reader(url):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme:
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read()
        except Exception as e:
            raise IOError(f"无法读取远程 URL: {e}") from e
    else:
        try:
            with open(url, 'rb') as f:
                content = f.read()
        except Exception as e:
            raise IOError(f"无法打开本地文件: {e}") from e
    try:
        return content.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("文件内容不是有效的 UTF-8 编码文本") from None
