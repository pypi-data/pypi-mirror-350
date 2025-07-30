from setuptools import setup, find_packages

setup(
    name="MessageBoxWin32",
    version="0.1.0",
    description="Caixas de diálogo Windows MessageBox via ctypes (sem Tkinter, porém especificamente para Windows).",
    long_description="Este pacote permite criar caixas de diálogo do Windows usando a função MessageBox da API do Windows, sem depender de Tkinter. É ideal para aplicações que precisam de uma interface simples de alerta ou confirmação no Windows.",
    author="Leonardo Henrique Rangon Paulino",
    author_email="leonardo@lhrp.com.br",
    url="https://github.com/lhrp/messageboxwin32",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
)