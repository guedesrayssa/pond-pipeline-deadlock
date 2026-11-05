"""Versão 2 da questão A4.

Semáforos: aguarda vaga antes de adquirir o mutex.
Execute com ``python ponderada/codigo/versao2.py`` na raiz do repositório.
As métricas são calculadas por ``simulacao.executar``.
"""

from simulacao import executar

if __name__ == "__main__":
    resultado = executar(2)
    print("TATO | BUFFER CIRCULAR | 20.000 amostras | N=6")
    for chave, valor in resultado.items():
        print(f"{chave}: {valor}")
