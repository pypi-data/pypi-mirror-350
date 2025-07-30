from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setup(
    name='fastapi_basic', # 模組名稱
    version='0.1.9', # 版號版號
    description='A short description of your module', # 模塊描述
    long_description=open('README.md').read(), # 詳細描述，通常是 README 文件的内容
    long_description_content_type='text/markdown', # markdown 格式
    author='szx21023', # 作者訊息
    author_email='szx21023@gmail.com', # 作者郵箱
    url='https://github.com/szx21023/fastapi-base', # 項目連結
    packages=find_packages(), # 自動查找包
    classifiers=[ # 分類標籤
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires = [req.strip() for req in requirements],
    python_requires='>=3.6', # 支持的 Python 版本
)
