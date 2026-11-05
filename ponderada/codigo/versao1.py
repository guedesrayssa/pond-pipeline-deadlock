"""Versão 1 da questão A4.

Sem sincronização: contador compartilhado com espera ocupada e corrida.
Execute com ``python ponderada/codigo/versao1.py`` na raiz do repositório.
As métricas são calculadas por ``simulacao.executar``.
"""

from simulacao import executar

if __name__ == "__main__":
    resultado = executar(1)
    print("TATO | BUFFER CIRCULAR | 20.000 amostras | N=6")
    for chave, valor in resultado.items():
        print(f"{chave}: {valor}")
