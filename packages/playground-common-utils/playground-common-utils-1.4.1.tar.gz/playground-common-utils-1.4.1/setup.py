# setup.py

from setuptools import setup, find_packages

setup(
    name='playground-common-utils',          # パッケージ名
    version='1.4.1',            # バージョン
    packages=find_packages(),  # packagesに自動でplayground_common_utils/が入る
    install_requires=["requests", 
                      "flask"],        # 外部ライブラリ
    author='Hiroki Umatani',        
    author_email='h.umatani@playground.style',
    description='汎用ユーティリティ（ファイル操作、ログ出力など）',
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',
    url='https://github.com/HirokiUmatani/playground-common-utils',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
