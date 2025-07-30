from setuptools import setup, find_packages
import pathlib

# Чтение long_description из README.md
current_dir = pathlib.Path(__file__).parent
long_description = (current_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="tobytearray",
    version="0.1.0",  
    author="rulllet",
    author_email="kuvardin.ru@gmail.com",
    description="Tool to convert files to binary arrays for embedded systems with multi-language support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rulllet/tobytearray",
    license="MIT",
    
    # Классификаторы PyPI
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    
    # Ключевые слова для поиска
    keywords="embedded resources converter cpp python go rust webp",
    
    # Структура пакета
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.7",
    
    # Зависимости
    install_requires=[
        "typing-extensions;python_version<'3.8'",
    ],
    
    # Дополнительные зависимости
    extras_require={
        "dev": [
            "pytest>=6.0",
            "twine>=3.0",
            "wheel>=0.36",
        ],
    },
    
    # Точки входа (консольные команды)
    entry_points={
        "console_scripts": [
            "resource-converter=resource_converter.converter:main",
        ],
    },
    
    # Дополнительные файлы для включения
    package_data={
        "resource_converter": ["*.json"],
    },
    
    # Метаданные проекта
    project_urls={
        "Bug Reports": "https://github.com/yourusername/resource-converter/issues",
        "Source": "https://github.com/yourusername/resource-converter",
    },
)