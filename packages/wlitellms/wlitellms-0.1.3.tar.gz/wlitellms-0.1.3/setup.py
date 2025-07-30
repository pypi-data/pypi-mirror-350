from setuptools import setup, find_packages

setup(
    name="wlitellms",
    version="0.1.3",
    packages=find_packages(),
    install_requires=["numpy>=1.18.0"],  # 依赖项（可选）
    author="bullgooo",
    description="A short description",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bullgooo/wlitellms",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.12",
)
