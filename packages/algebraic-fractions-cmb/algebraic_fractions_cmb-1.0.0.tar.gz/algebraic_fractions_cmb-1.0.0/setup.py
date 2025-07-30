from setuptools import setup, find_packages

setup(
    name="algebraic-fractions-cmb",            # уникальное имя пакета на PyPI
    version="1.0.0",                        # текущая версия
    author="Artsiom",                      # автор
    author_email="artyomageyko@gmail.com",
    url="https://github.com/Redditask/algebraic-fractions",
    description="Аппроксимация и сжатие данных дробями Чебышева–Маркова и Бернштейна",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(exclude=["tests*", "demo*"]),
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.20",
        "matplotlib>=3.3",
        "joblib>=1.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Mathematics"
    ],
    entry_points={
        # если будут консольные скрипты — можно добавить здесь
    },
)
