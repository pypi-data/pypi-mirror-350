from setuptools import setup, find_packages

setup(
    name='OneLLMAPI',  # 包名
    version='1.0',  # 版本号
    packages=find_packages(),  # 自动查找包
    install_requires=[
        'copy',
        'requests',
        'hashlib',
        'time',
        'json',
        'openai',
        'dashscope',
        'baidubce'

    ],  # 依赖项
    author='Zhang Lan,Zhou Yu Qing',  # 作者
    author_email='dragonlan6@outlook.com',  # 作者邮箱
    description='A package that integrates the APIs of multiple major language model manufacturers.',  # 包描述
    long_description=open('README.md', encoding='utf-8').read(),  # 长描述（通常从 README.md 读取）
    long_description_content_type='text/markdown',  # 长描述格式
    url='https://gitee.com/DragonLan666/OneLLM',  # 项目地址
    license='MIT',  # 许可证
    license_file='LICENSE.txt',
    classifiers=[  # 分类器，用于 PyPI
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # Python 版本要求
)
