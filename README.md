# Tato | do pipeline ao deadlock

**Rayssa Guedes França** · Análise de arquitetura, concorrência e decisão de produto para uma pulseira sensorial.

## Executar os experimentos

Requer Python 3, sem bibliotecas externas. Na raiz do repositório:

```bash
python ponderada/codigo/versao1.py
python ponderada/codigo/versao2.py
python ponderada/codigo/versao3.py
```

Cada comando executa uma rodada de 20.000 amostras com buffer de 6 posições. Os valores variam conforme o escalonamento. `travou: True` significa ausência de consumo por 1 segundo; a versão 3 força um cenário de buffer cheio. A análise e as nove rodadas registradas estão em [ponderada-tato.md](ponderada/ponderada-tato.md).
