from setuptools import setup, find_packages

setup(
    name="iremdict",
    version="0.1.6",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "iremdict": ["data/sozluk.txt"]
    },
    install_requires=[
        "re","os"
    ],
    author="İrem Yılmaz",
    author_email="iremyilmaz@example.com",  # Gerçek mail adresinle değiştir
    description="Türkçe metin temizleme için kelime sözlüğü paketi",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kullaniciadi/iremdict",  # GitHub repo (varsa) veya boş bırakabilirsin
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Natural Language :: Turkish",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT",
    python_requires=">=3.7",
)
