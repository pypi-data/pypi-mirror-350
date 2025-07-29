from setuptools import setup, find_packages

setup(
    name="py2hackCraft",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "websocket-client>=1.6.0",
    ],
    author="masafumi_t",
    author_email="masafumi_t@0x48lab.com",  # 実際のメールアドレスに変更してください
    description="Python client library for hackCraft2",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/0x48lab/hackCraft2-python",  # 実際のリポジトリURLに変更してください
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)