# setup.py

from setuptools import setup, find_packages

setup(
    name='miyabi256',
    version='0.1.0',
    author='eightman',
    author_email='eightman124@gmail.com',
    description='A Base64-like encoder/decoder using 256 Japanese characters (Hiragana, Katakana, Kanji).',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/eightman999/Miyabi256',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
)