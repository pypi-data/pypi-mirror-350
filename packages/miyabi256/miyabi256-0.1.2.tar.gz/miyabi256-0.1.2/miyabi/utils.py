# miyabi256/utils.py

from .core import encode_bytes, decode_string

def encode_file(filepath: str) -> str:
    """
    指定されたファイルのバイナリデータを「みやび二五六」文字列にエンコードします。
    """
    with open(filepath, 'rb') as f:
        data = f.read()
    return encode_bytes(data)

def decode_to_file(encoded_string: str, output_filepath: str):
    """
    「みやび二五六」文字列をデコードし、指定されたファイルにバイナリデータとして書き込みます。
    """
    decoded_data = decode_string(encoded_string)
    with open(output_filepath, 'wb') as f:
        f.write(decoded_data)

def encode_text(text: str, encoding: str = 'utf-8') -> str:
    """
    テキスト文字列を特定のエンコーディングでバイトデータに変換し、
    それを「みやび二五六」文字列にエンコードします。
    """
    data_bytes = text.encode(encoding)
    return encode_bytes(data_bytes)

def decode_text(encoded_string: str, encoding: str = 'utf-8') -> str:
    """
    「みやび二五六」文字列をバイトデータにデコードし、
    それを特定のエンコーディングでテキスト文字列に変換します。
    """
    decoded_bytes = decode_string(encoded_string)
    return decoded_bytes.decode(encoding)

def encode_lines(data: bytes, line_length: int = 76) -> str:
    """
    バイトデータを「みやび二五六」文字列にエンコードし、指定された行の長さで改行を挿入します。
    """
    encoded_string = encode_bytes(data)
    lines = []
    for i in range(0, len(encoded_string), line_length):
        lines.append(encoded_string[i:i + line_length])
    return "\n".join(lines)

def decode_lines(encoded_string_with_newlines: str) -> bytes:
    """
    改行を含む「みやび二五六」文字列をデコードします。
    デコード前に改行文字を除去します。
    """
    cleaned_string = encoded_string_with_newlines.replace('\n', '').replace('\r', '')
    return decode_string(cleaned_string)