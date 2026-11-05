"""Executa a versão 1 da simulação de sincronização da Tato."""

from simulacao import executar

if __name__ == "__main__":
    resultado = executar(1)
    print("TATO | BUFFER CIRCULAR | 20.000 amostras | N=6")
    for chave, valor in resultado.items():
        print(f"{chave}: {valor}")
