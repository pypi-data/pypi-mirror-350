import os
from pathlib import Path

def Code() -> str:
    # Caminho da pasta que você quer ler
    CAMINHO_PASTA = Path("C:/Users/guilh_43osqzc/Desktop/codigos/python/SYLPH/Ia")

    # Lista todos os arquivos .py
    arquivos = [f for f in CAMINHO_PASTA.glob("*.py") if f.is_file()]

    # Lê cada arquivo e junta os conteúdos
    todos_os_codigos = ""
    for arquivo in arquivos:
        print(f"\n🔍 Lendo: {arquivo.name}")
        with open(arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read()
            todos_os_codigos += f"\n\n# Arquivo: {arquivo.name}\n" + conteudo

    return todos_os_codigos

if __name__ == "__main__":
    print("Code: ")
    print(Code())
