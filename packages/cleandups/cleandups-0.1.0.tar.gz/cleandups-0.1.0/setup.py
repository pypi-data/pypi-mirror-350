from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cleandups",
    version="0.1.0",
    author="Flaymie",
    author_email="funquenop@gmail.com",
    description="Инструмент для поиска и удаления дубликатов файлов",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Flaymie/cleandups",
    packages=find_packages(),
    install_requires=[
        "send2trash>=1.8.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "cleandups=cleandups.cleandups:main",
        ],
    },
    python_requires=">=3.6",
) 