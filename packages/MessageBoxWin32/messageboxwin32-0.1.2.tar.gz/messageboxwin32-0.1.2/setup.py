import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
long_description = (HERE / "README.md").read_text(encoding="utf-8")

setup(
    name="MessageBoxWin32",
    version="0.1.2",
    description="Caixas de diálogo Windows MessageBox via ctypes (sem Tkinter, porém especificamente para Windows).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Leonardo Henrique Rangon Paulino",
    author_email="leonardo@lhrp.com.br",
    url="https://github.com/lhrp/messageboxwin32",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
    install_requires=[
        "wxPython==4.2.3"
    ],
)