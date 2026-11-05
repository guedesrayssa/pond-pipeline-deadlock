"""Versão 3 da questão A4.

Ordem invertida: adquire mutex antes de aguardar vaga; pode travar.
Execute com ``python ponderada/codigo/versao3.py`` na raiz do repositório.
As métricas são calculadas por ``simulacao.executar``.
"""

from simulacao import executar

if __name__ == "__main__":
    resultado = executar(3)
    print("TATO | BUFFER CIRCULAR | 20.000 amostras | N=6")
    for chave, valor in resultado.items():
        print(f"{chave}: {valor}")
