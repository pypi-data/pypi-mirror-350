from setuptools import setup, find_packages

# README.md を長い説明文として読み込むなら
long_description = open('README.md', encoding='utf-8').read()

setup(
    name='Unicorn_Links',              # PyPIに出す名前（ご自身のパッケージ名）
    version='0.2.4',                 # バージョン番号
    packages=find_packages(),        # 自動でパッケージディレクトリを探す
    install_requires=[],             # 依存ライブラリがあればリストに入れる
    author='Gingyer',
    description='リアルタイムで”ユニコーンプログラミング”ができます。',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
