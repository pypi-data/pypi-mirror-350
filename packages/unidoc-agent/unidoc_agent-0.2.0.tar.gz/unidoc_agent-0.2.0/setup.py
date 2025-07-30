from setuptools import setup, find_packages

setup(
    name="unidoc_agent",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "python-docx",
        "PyMuPDF",
        "pytesseract",
        "pandas",
        "openpyxl",
        "ollama",
    ],
    author="Vedansh Bhatnagar",
    description="Universal Document Agent for extracting and analyzing various documents with Ollama support",
    keywords=["document", "pdf", "docx", "text", "code", "extract", "ollama", "chatbot"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    license="MIT"
)
