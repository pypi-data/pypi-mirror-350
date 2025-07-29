import setuptools

with open(file="README.md", mode="r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="ossSign",
    version="1.7",
    author="zhangchaolei",
    author_email="creazy_stone@hotmail.com",
    description="oss文件上传签名计算",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires='>=3.10',
)