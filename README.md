# Idle Hero TD Optimizer

Aplicativo local para gerar comandos de macro a partir de screenshots do Idle Hero TD.

O app nao executa cliques no jogo. Ele apenas:

1. recebe prints por drag-and-drop;
2. roda OCR por ensemble com consenso entre engines e estrategias;
3. infere ou pede confirmacao dos levels, `maxed` e `locked`, com ajustes avancados persistidos para overrides;
4. roda o otimizador para os alvos selecionados: `DMG`, `Gold` e/ou `Prestige`;
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

Para desenvolvimento e teste local, inicie sempre por `./run.sh` ou `run.command`. Nao rode `streamlit run` manualmente em outra porta; o launcher gerencia o restart na mesma porta e respeita `IDLE_HERO_TD_PORT` quando essa variavel estiver definida.

O Streamlit abrira:

```text
http://localhost:8501
```

Na sidebar, `Selecionar pasta do Python` permite escolher a pasta onde esta o Python dos scripts. O app procura automaticamente caminhos como `.venv/bin/python`, `bin/python`, `python3` ou `Scripts/python.exe`; se nao encontrar, usa o Python atual do app.

## Fluxo

1. Arraste o print de Research na coluna `Energia / Research`.
2. Arraste o print de Prestige na coluna `Prestige / PowerUps`.
3. Informe Energy e/ou Prestige Points usando a escala do jogo, por exemplo `2,59M` e `1,21e20`. Um deles pode ficar `0`, mas nao os dois.
4. Selecione 1 a 3 alvos em `Otimizar upgrades`: `DMG`, `Gold` e/ou `Prestige`.
5. Clique em `Ler imagens e gerar macro`.
6. Se o OCR por consenso nao deixar pendencias, o app gera automaticamente os codigos no painel `Macro`, separados para `Energy / Research` e `Prestige / PowerUps`.
7. Se houver pendencias, resolva apenas os itens exibidos nos blocos separados de `Research / Energy` e `Prestige / PowerUps`. O app infere por familia/tier:
   - `locked`: item visivel com `Lv. 0` e botao `Wave`/lock;
   - `locked`: item ausente alem do limite visivel/destravado da familia;
   - `maxed`: item ausente antes de uma sequencia visivel consistente da mesma familia;
   - `review`: buraco ambiguo no meio dos tiers visiveis, para evitar confundir OCR falho com maxed;
   - `ignore`: item de uma tela que voce nao anexou.
8. Use `Abrir print em nova aba` se precisar conferir a imagem original. O thumbnail pequeno e apenas visual; o OCR usa o arquivo original.
9. Use `Ajustes avancados` para override/debug, inclusive antes de processar imagens. A tabela completa fica separada por `Research` e `Prestige`, e os overrides salvos em `user_state/advanced_overrides.json` sao reaplicados nos proximos OCRs:
   - `available`: upgrade disponivel e com level correto;
   - `locked`: upgrade travado por Wave/limite visivel ou forcado manualmente;
   - `maxed`: upgrade omitido ou no maximo;
   - `ignore`: nao entra no estado;
   - `review`: precisa ser confirmado antes de gerar.
10. Use `Atualizar macro` ou `Recalcular macro` quando voce alterar recursos, alvos ou algum ajuste manual depois do OCR. Nao precisa reprocessar as imagens se os levels nao mudaram.
11. Use o botao `Copiar Energy` ou `Copiar Prestige` para levar o texto ao seu app de macro.

## Ajustes avancados

`Ajustes avancados` e o unico controle manual persistente para status e level dos upgrades principais. Ele fica visivel mesmo antes de processar imagens, para permitir preparar excecoes como `maxed`, `locked`, `available`, `ignore` ou `review`.

Os ajustes sao salvos em `user_state/advanced_overrides.json` e reaplicados sempre que a UI monta o estado:

- antes do OCR: a tabela mostra todos os upgrades como base nao processada; overrides salvos aparecem imediatamente, mas a macro ainda nao e liberada;
- depois do OCR: o app reconstrui a base a partir da leitura atual e aplica os overrides por cima;
- se voce voltar uma linha para o mesmo `status` e `level` inferidos pela base atual, o override daquela linha e removido;
- `maxed` ignora o level digitado na hora de montar o estado do otimizador e usa o `max_level` conhecido;
- `locked` sem level vira level `0` e entra em `locked_upgrades`;
- `ignore` nao entra no estado enviado ao otimizador;
- qualquer mudanca em `Ajustes avancados` invalida a macro anterior; use `Atualizar macro` ou `Recalcular macro`.

Compatibilidade: se `user_state/advanced_overrides.json` ainda nao existir, o app importa os bloqueios antigos de `user_state/locked_upgrades.json` como overrides `locked`. Depois que o arquivo novo existir, ele passa a ser a fonte de verdade.

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
- `maxed` e `locked` podem ser inferidos pelo padrao visual/tier quando for seguro; ajustes avancados persistidos servem para corrigir ou forcar excecoes.
- O app deve ser iniciado por `./run.sh` ou `run.command`, sem abrir portas alternativas manualmente; o launcher reinicia a instancia atual na mesma porta.
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

Suite rapida para alteracoes de UI, estado e otimizador:

```bash
.venv/bin/python scripts/test_ui_state_conversion.py
.venv/bin/python scripts/test_run_script_portability.py
.venv/bin/python scripts/test_upgrade_cost_formulas.py
.venv/bin/python scripts/test_optimizer_target_metrics.py
.venv/bin/python -m compileall -q scripts ui
```

Suite OCR completa, mais lenta e dependente das engines/modelos instalados:

```bash
.venv/bin/python scripts/test_upgrade_ocr_strategies.py
```
