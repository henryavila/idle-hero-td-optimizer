# Idle Hero TD Optimizer

Aplicativo local para gerar comandos de macro a partir de screenshots do Idle Hero TD.

O app nao executa cliques no jogo. Ele apenas:

1. recebe prints por drag-and-drop;
2. roda OCR por ensemble com consenso entre engines e estrategias;
3. infere ou pede confirmacao dos levels, `maxed` e `locked`;
4. roda o otimizador FARM ou Gold Prep;
5. entrega no topo o texto separado para copiar para sua macro.

## Instalar

```bash
./install.sh
```

Se quiser instalar as camadas OCR opcionais, EasyOCR e PaddleOCR/PP-OCRv5:

```bash
./install.sh --with-ocr
```

O alias antigo `./install.sh --with-easyocr` continua funcionando e instala o mesmo pacote opcional.

No macOS, o app tambem pode usar OCR via Vision quando `swiftc` estiver disponivel. Tesseract tambem funciona se estiver instalado no sistema.

Para melhor leitura automatica dos prints, especialmente quando a tela estiver recortada ou com texto pequeno, use as camadas opcionais:

```bash
./install.sh --with-ocr
```

O modo padrao `consensus` roda as engines disponiveis e combina `layout-slots` com `auto-lines`. Quando PaddleOCR esta instalado, ele entra como camada adicional `auto-lines` com PP-OCRv5 server, mas nao substitui as outras engines. Um level so e aceito quando camadas independentes concordam ou quando o efeito total confirma matematicamente a leitura; caso contrario, o item fica para revisao.

O upload nao redimensiona nem recomprime a imagem antes do OCR. O arquivo anexado e salvo byte a byte em `runs/.../uploads`; o tamanho menor exibido no app e apenas o preview visual.

## Rodar

```bash
./run.sh
```

Ou abra `run.command` pelo Finder.

O launcher mantem apenas uma instancia do app. Se ja houver um servidor deste projeto rodando, ele sera reiniciado na porta fixa `8501` em vez de abrir uma segunda instancia em `8502`.

O Streamlit abrira:

```text
http://localhost:8501
```

Na sidebar, `Selecionar pasta do Python` permite escolher a pasta onde esta o Python dos scripts. O app procura automaticamente caminhos como `.venv/bin/python`, `bin/python`, `python3` ou `Scripts/python.exe`; se nao encontrar, usa o Python atual do app.

## Fluxo

1. Arraste o print de Research na coluna `Energia / Research`.
2. Arraste o print de Prestige na coluna `Prestige / PowerUps`.
3. Informe Energy e/ou Prestige Points usando a escala do jogo, por exemplo `2,59M` e `1,21e20`. Um deles pode ficar `0`, mas nao os dois.
4. Clique em `Ler imagens e gerar macro`.
5. Se o OCR por consenso nao deixar pendencias, o app gera automaticamente os codigos no painel `Macro`, separados para `Energy / Research` e `Prestige / PowerUps`.
6. Se houver pendencias, resolva apenas os itens exibidos nos blocos separados de `Research / Energy` e `Prestige / PowerUps`. O app infere por familia/tier:
   - `locked`: item visivel com botao `Wave`/lock;
   - `locked`: item ausente que esta alem do limite visivel/destravado da familia;
   - `maxed`: item ausente antes de uma sequencia visivel consistente da mesma familia;
   - `review`: buraco ambiguo no meio dos tiers visiveis, para evitar confundir OCR falho com maxed;
   - `ignore`: item de uma tela que voce nao anexou.
7. Use `Abrir print em nova aba` se precisar conferir a imagem original. O thumbnail pequeno e apenas visual; o OCR usa o arquivo original.
8. Use `Ajustes avancados` apenas para override/debug; a tabela completa tambem fica separada por `Research` e `Prestige`:
   - `available`: upgrade disponivel e com level correto;
   - `locked`: upgrade bloqueado por wave;
   - `maxed`: upgrade omitido ou no maximo;
   - `ignore`: nao entra no estado;
   - `review`: precisa ser confirmado antes de gerar.
9. Use `Atualizar macro` ou `Recalcular macro` quando voce alterar recursos, objetivo ou algum ajuste manual depois do OCR. Nao precisa reprocessar as imagens se os levels nao mudaram.
10. Use o botao `Copiar Energy` ou `Copiar Prestige` para levar o texto ao seu app de macro.

## Passada residual

Se o jogo mostrou saldo arredondado antes da macro, como `2,59M`, o otimizador usa esse valor como entrada conservadora. Depois de executar a macro, se sobrar recurso real, informe o saldo em `Passada residual` e gere uma segunda macro curta.

## Estrutura

```text
ui/app.py                                      Streamlit UI
scripts/                                      motores validados de OCR, otimizacao e macro
IdleHeroTD-apk/apk_analysis/dados-consolidados dados de runtime empacotados no app
runs/                                         saidas locais geradas pela UI
```

## Portabilidade

O app deve ser autocontido para execucao. Ele pode ser movido para qualquer pasta e continuar funcionando sem depender da pasta `Games` nem de caminhos absolutos gravados em wrappers da `.venv`.

A pasta `Games/Idle Hero TD` continua sendo a base de conhecimento da IA e o workspace de investigacao do jogo. Quando a analise do APK gerar dados novos, sincronize para dentro deste repo apenas o subconjunto consolidado que o app realmente usa em runtime.

## Decisoes consolidadas

- A tela principal deve manter o fluxo completo na primeira dobra: recursos, uploads e saida da macro.
- A sidebar deve ficar apenas para configuracoes tecnicas.
- O app deve gerar macro automaticamente quando OCR e recursos estiverem validos.
- A leitura principal de levels deve vir de um ensemble entre slots de layout, linhas detectadas e validacao matematica por efeito total; leitura isolada e divergente deve virar revisao, nao level aceito.
- PaddleOCR/PP-OCRv5 entra como camada opcional conservadora do ensemble, nao como engine principal isolada.
- `maxed` e `locked` devem ser inferidos pelo padrao visual/tier sempre que for seguro, pedindo revisao apenas nos casos ambiguos.
- A imagem anexada deve ser preservada original para OCR; qualquer reducao deve ser somente preview visual.
- O preview deve permitir abrir o print original em nova aba, sem redimensionar o arquivo usado pelo OCR.
- A saida de macro deve ficar sempre separada entre `Energy / Research` e `Prestige / PowerUps`.

## Dados incluidos

Este repositorio inclui os dados consolidados necessarios para execucao do app, nao os dumps brutos do APK. Os principais arquivos operacionais sao:

```text
IdleHeroTD-apk/apk_analysis/dados-consolidados/formulas/csv/core_upgrade_formula_factors.csv
IdleHeroTD-apk/apk_analysis/dados-consolidados/formulas/csv/core_upgrade_cost_formula_classes.csv
IdleHeroTD-apk/apk_analysis/dados-consolidados/formulas/e2e_otimizacao_recursos.md
IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/upgrade_ocr_to_optimizer_pipeline.md
```

## Testes

```bash
.venv/bin/python scripts/test_run_script_portability.py
.venv/bin/python scripts/test_upgrade_cost_formulas.py
.venv/bin/python scripts/test_upgrade_ocr_strategies.py
.venv/bin/python -m compileall -q scripts ui
```
