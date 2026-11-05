"""Simulação didática do buffer circular da pulseira Tato (N=6)."""

import argparse
import collections
import threading
import time

N = 6
TOTAL = 20_000


def executar(versao):
    """Execute a versão 1, 2 ou 3; retorne um dicionário com os resultados.

    versao: número da estratégia de sincronização. O monitor encerra o
    experimento após um segundo sem consumo; threads são daemons para que
    uma versão em deadlock não impeça o encerramento do processo.
    """
    buffer = [None] * N
    estado = {'entrada': 0, 'saida': 0, 'ocupados': 0, 'ultimo': time.monotonic()}
    recebidas = []
    parar = threading.Event()
    vazio = threading.Semaphore(N)
    cheio = threading.Semaphore(0)
    mutex = threading.Semaphore(1)

    def produtor():
        """Produza inteiros sequenciais; sem parâmetros ou valor retornado."""
        for amostra in range(TOTAL):
            if parar.is_set():
                return
            if versao == 1:
                while estado['ocupados'] >= N and not parar.is_set():
                    time.sleep(0)  # cede a CPU, mas continua sondando o contador
                if parar.is_set():
                    return
                buffer[estado['entrada']] = amostra
                estado['entrada'] = (estado['entrada'] + 1) % N
                antigo = estado['ocupados']
                time.sleep(0)
                estado['ocupados'] = antigo + 1
            else:
                if versao == 3:
                    mutex.acquire()
                    vazio.acquire()
                else:
                    vazio.acquire()
                    mutex.acquire()
                buffer[estado['entrada']] = amostra
                estado['entrada'] = (estado['entrada'] + 1) % N
                mutex.release()
                cheio.release()

    def consumidor():
        """Consuma até TOTAL itens ou interrupção; não recebe nem retorna valor."""
        # Na versão 3, o atraso reproduz um consumidor temporariamente ocupado.
        if versao == 3:
            time.sleep(0.05)
        while len(recebidas) < TOTAL and not parar.is_set():
            if versao == 1:
                while estado['ocupados'] <= 0 and not parar.is_set():
                    time.sleep(0)  # espera ocupada cooperativa
                if parar.is_set():
                    return
                item = buffer[estado['saida']]
                estado['saida'] = (estado['saida'] + 1) % N
                antigo = estado['ocupados']
                time.sleep(0)
                estado['ocupados'] = antigo - 1
            else:
                cheio.acquire()
                mutex.acquire()
                item = buffer[estado['saida']]
                estado['saida'] = (estado['saida'] + 1) % N
                mutex.release()
                vazio.release()
            recebidas.append(item)
            estado['ultimo'] = time.monotonic()

    threads = [threading.Thread(target=produtor, daemon=True),
               threading.Thread(target=consumidor, daemon=True)]
    for thread in threads:
        thread.start()
    while len(recebidas) < TOTAL and time.monotonic() - estado['ultimo'] < 1:
        time.sleep(0.01)
    travou = len(recebidas) < TOTAL
    parar.set()
    # Na versão 1, permita que os laços observem a parada antes de contar.
    if versao == 1:
        for thread in threads:
            thread.join(timeout=0.2)
    contagem = collections.Counter(x for x in recebidas if isinstance(x, int) and 0 <= x < TOTAL)
    return {'versao': versao, 'consumidas': len(recebidas),
            'perdidas': TOTAL - len(contagem),
            'duplicadas': sum(n - 1 for n in contagem.values()),
            'invalidas': len(recebidas) - sum(contagem.values()), 'travou': travou}


def main():
    """Leia a versão da linha de comando e imprima a medição; sem retorno."""
    parser = argparse.ArgumentParser()
    parser.add_argument('versao', type=int, choices=(1, 2, 3))
    args = parser.parse_args()
    resultado = executar(args.versao)
    print('TATO | BUFFER CIRCULAR | 20.000 amostras | N=6')
    for chave, valor in resultado.items():
        print(f'{chave}: {valor}')


if __name__ == '__main__':
    main()
