# Miyabi256 (みやび二五六)

Miyabi256 は、バイナリデータをひらがな、カタカナ、および一部の漢字を含む256種類の日本語文字を使用してエンコード/デコードするPythonライブラリです。従来のBase64と同様に、画像やその他のバイナリデータを日本の美しい文字の羅列で表現できます。

## 特徴

-   **256文字の文字セット**: 1バイトを1文字に直接マッピングするため、Base64 (約75%) よりも効率的なエンコードが可能です。
-   **直感的なエンコード**: エンコード結果が日本語文字で構成されるため、日本語話者にとっては視覚的な親しみやすさがあります。
-   **ファイルI/O対応**: 画像ファイルなどのバイナリデータを直接エンコード/デコードできます。
-   **テキスト変換**: 特定のエンコーディング (UTF-8など) を指定してテキストデータを変換できます。
-   **複数行出力**: 長いエンコード結果を整形して出力する機能。

## PIP
https://pypi.org/project/miyabi256/0.1.0/

## インストール

pip を使用してインストールできます。

```bash
pip install miyabi256


## 使用方法

### 基本的なエンコードとデコード

```python
import miyabi256

# バイトデータをエンコード
data_bytes = b'Hello, world!'
encoded_string = miyabi256.encode_bytes(data_bytes)
print(f"エンコードされた文字列: {encoded_string}")

# 文字列をデコードしてバイトデータに戻す
decoded_bytes = miyabi256.decode_string(encoded_string)
print(f"デコードされたバイトデータ: {decoded_bytes}")

# テキストデータをエンコード/デコード (UTF-8)
text_string = "こんにちは、世界！"
encoded_text = miyabi256.encode_text(text_string)
decoded_text = miyabi256.decode_text(encoded_text)
print(f"元のテキスト: {text_string}")
print(f"エンコードされたテキスト: {encoded_text}")
print(f"デコードされたテキスト: {decoded_text}")
```

python setup.py sdist bdist_wheel