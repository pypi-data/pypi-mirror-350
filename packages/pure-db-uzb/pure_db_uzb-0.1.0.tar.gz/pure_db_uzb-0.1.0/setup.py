from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pure-db-uzb",  # PyPI'dagi nomi
    version="0.1.0",
    author="Salohiddin",
    author_email="salohiddinsalohiddin123@gmail.com",
    description="Oddiy faylga asoslangan va serverga ulanadigan yani global ma'lumotlarni saqlay oladigan ma'lumotlar bazasi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
