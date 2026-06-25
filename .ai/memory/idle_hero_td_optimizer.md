# Idle Hero TD Optimizer

## Objetivo do App

O app transforma screenshots das telas `Research` e `Prestige` do Idle Hero TD em texto de macro para upgrades. Ele nao clica no jogo; a saida e copiada pelo usuario para um app de macro externo.

O caminho feliz precisa ser:

1. anexar os dois prints;
2. informar `Energy` e/ou `Prestige Points`;
3. clicar em `Ler imagens e gerar macro`;
4. copiar os blocos separados de `Energy / Research` e `Prestige / PowerUps` no topo da pagina.

## Decisoes de UX

- A tela principal usa tres colunas: print de Research, print de Prestige e saida da macro.
- Os recursos e o objetivo ficam no topo, nao escondidos na sidebar.
- A sidebar deve ficar restrita a configuracao tecnica, como Python e engine de OCR.
- A configuracao de Python deve usar seletor de pasta e detectar o executavel automaticamente; evitar input manual de caminho quando possivel.
- Previews dos prints devem ser pequenos para economizar espaco.
- `Ampliar print` usa modal real e renderiza a imagem em HTML/CSS na largura do modal; `st.image` dentro do dialog pode deixar a imagem pequena demais.
- Se nao houver pendencias de OCR e houver recurso informado, a macro deve ser gerada automaticamente apos ler as imagens.
- Se recursos/objetivo mudarem sem mudar os levels, o usuario deve poder recalcular a macro sem reprocessar os prints.

## OCR e Estado dos Upgrades

- O upload nunca deve redimensionar ou recomprimir a imagem antes do OCR. O arquivo anexado e salvo byte a byte em `runs/.../uploads`.
- O preview visual pode ser pequeno; isso nao pode afetar OCR.
- Itens visiveis com botao `Wave`/lock sao `locked`.
- Itens ausentes antes de uma sequencia visivel consistente da mesma familia sao inferidos como `maxed`.
- Itens ausentes depois do limite visivel/destravado da familia sao inferidos como `locked`.
- Buracos ambiguos no meio dos tiers visiveis ficam em `review`.
- Itens de uma tela nao anexada ficam como `ignore`.

## Otimizacao e Macro

- `FARM` prioriza alocacao real de recursos para maximizar o resultado final relevante do farm.
- `GOLD_PREP` e uma segunda estrategia focada em preparar push via Kill Gold.
- Os recursos aceitam escala do jogo, como `2,59M`, `1,21e20`, `850K`.
- Um recurso pode ser `0`, mas nao os dois ao mesmo tempo.
- A saida de macro deve ficar separada por tela:
  - `Energy / Research`
  - `Prestige / PowerUps`
- Textareas de macro usam chave derivada do conteudo para evitar texto antigo preso no widget depois de recalcular.

## Publicacao

- Repo publico: `idle-hero-td-optimizer`.
- Nao commitar `runs/`, `.venv/`, logs, screenshots locais, `.env` ou credenciais.
- Dados consolidados do APK podem ficar versionados; dumps brutos e saidas locais devem continuar fora do repo publico.
