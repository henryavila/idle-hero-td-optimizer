# Idle Hero TD Optimizer

Aplicativo local para gerar comandos de macro a partir de screenshots do Idle Hero TD.

O app nao executa cliques no jogo. Ele apenas:

1. recebe prints por drag-and-drop;
2. roda OCR deterministico;
3. infere ou pede confirmacao dos levels, `maxed` e `locked`;
4. roda o otimizador FARM ou Gold Prep;
5. entrega no topo o texto separado para copiar para sua macro.

## Instalar

```bash
./install.sh
```

Se quiser instalar EasyOCR tambem:

```bash
./install.sh --with-easyocr
```

No macOS, o app tambem pode usar OCR via Vision quando `swiftc` estiver disponivel. Tesseract tambem funciona se estiver instalado no sistema.

Para melhor leitura automatica dos prints, especialmente quando a tela estiver recortada ou com texto pequeno, use EasyOCR:

```bash
./install.sh --with-easyocr
```

Sem EasyOCR, o modo `auto` pode cair para macOS Vision. Isso funciona sem dependencia pesada, mas pode deixar mais linhas em `review` para voce confirmar manualmente.

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
5. Se o OCR nao deixar pendencias, o app gera automaticamente os codigos no painel `Macro`, separados para `Energy / Research` e `Prestige / PowerUps`.
6. Se houver pendencias, resolva apenas os itens exibidos nos blocos separados de `Research / Energy` e `Prestige / PowerUps`. O app infere por familia/tier:
   - `locked`: item visivel com botao `Wave`/lock;
   - `locked`: item ausente que esta alem do limite visivel/destravado da familia;
   - `maxed`: item ausente antes de uma sequencia visivel consistente da mesma familia;
   - `review`: buraco ambiguo no meio dos tiers visiveis, para evitar confundir OCR falho com maxed;
   - `ignore`: item de uma tela que voce nao anexou.
7. Use `Ampliar print` se precisar conferir a imagem original em modal. O thumbnail pequeno e apenas visual; o OCR usa o arquivo original.
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
IdleHeroTD-apk/apk_analysis/dados-consolidados referencias extraidas e consolidadas do APK
runs/                                         saidas locais geradas pela UI
.ai/memory/                                  aprendizados consolidados para futuras sessoes
```

## Decisoes consolidadas

- A tela principal deve manter o fluxo completo na primeira dobra: recursos, uploads e saida da macro.
- A sidebar deve ficar apenas para configuracoes tecnicas.
- O app deve gerar macro automaticamente quando OCR e recursos estiverem validos.
- `maxed` e `locked` devem ser inferidos pelo padrao visual/tier sempre que for seguro, pedindo revisao apenas nos casos ambiguos.
- A imagem anexada deve ser preservada original para OCR; qualquer reducao deve ser somente preview visual.
- O modal de `Ampliar print` renderiza a imagem em HTML/CSS para ocupar a largura do dialog sem cortar horizontalmente.
- A saida de macro deve ficar sempre separada entre `Energy / Research` e `Prestige / PowerUps`.

## Dados incluidos

Este repositorio inclui os dados consolidados, nao os dumps brutos do APK. Os principais arquivos operacionais sao:

```text
IdleHeroTD-apk/apk_analysis/dados-consolidados/formulas/csv/core_upgrade_formula_factors.csv
IdleHeroTD-apk/apk_analysis/dados-consolidados/formulas/csv/core_upgrade_cost_formula_classes.csv
IdleHeroTD-apk/apk_analysis/dados-consolidados/formulas/e2e_otimizacao_recursos.md
IdleHeroTD-apk/apk_analysis/dados-consolidados/upgrades/upgrade_ocr_to_optimizer_pipeline.md
```

## Testes

```bash
source .venv/bin/activate
python scripts/test_upgrade_cost_formulas.py
python -m compileall -q scripts ui
```
