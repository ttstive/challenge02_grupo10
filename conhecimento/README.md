# Acervo de conhecimento em português

Branch de dados independente: somente a pasta `conhecimento/`, sem código da aplicação. Coleta em 09/11/2026. Este conjunto amplia o acervo anterior, mas não representa cobertura completa ou validação clínica.

## Conteúdo verificado

- 31 PDFs (30 conteúdos únicos por SHA-256), com 1431 páginas no total de arquivos.
- 2076 arquivos TXT do corpus de complexidade textual, com repositório de origem e atribuição preservados.
- Bosque/Universal Dependencies: arquivos de treino, desenvolvimento e teste em CoNLL-U, com README e licença originais. Contagens por split: {'pt_bosque-ud-test.conllu': 1167, 'pt_bosque-ud-dev.conllu': 1172, 'pt_bosque-ud-train.conllu': 7018}.
- Snapshot do código NILC-Metrix, não um dataset, com licença e componentes preservados no ZIP.
- CORAA: documentação e licença, **sem áudios**. Os links oficiais estão no README; não apresentamos a documentação como se fosse o corpus baixado.
- Sete cursos catalogados; páginas de curso não equivalem a apostilas completas.
- Três referências audiovisuais com fichas autorais em PDF: **nenhuma transcrição integral foi obtida**. As fichas se baseiam nas páginas editoriais, sem alegar análise integral dos vídeos.

## Organização

- `originais/`: documentos externos preservados; consultar `inventario_pdfs.json` para hashes, páginas e duplicatas.
- `textos/`: extrações derivadas, sujeitas a erros de layout e fontes; não usar sem revisão.
- `datasets/`: dados reais e snapshots; descrições e origens em `datasets_manifesto.json`.
- `videos/`: caderno PDF e metadados, explicitamente sem transcrições integrais.
- `paginas/`: snapshots HTML; remover navegação antes de indexar.
- `matriz_20_topicos.csv`: mapeamento exploratório por palavras; candidatos não são comprovação de cobertura.
- `FONOAUDIOLOGIA.md`, `CURSOS.md`, `METODOLOGIAS.md`: catálogos temáticos anteriores.
- `fontes*.json`, `recursos.json`, `cursos.json`: proveniência do acervo anterior e das ampliações.

## Uso dos dados

Complexidade: o repositório de origem declara CC BY 4.0; preserve sua atribuição e consulte suas referências. Bosque: preserve `LICENSE.txt`, autoria e condições aplicáveis. NILC-Metrix: preservar AGPLv3 e conferir componentes; o pacote não foi executado ou instalado. Os datasets não possuem rótulos de boa comunicação, assertividade ou ansiedade.

Não misturar dados de avaliação com treinamento. Não indexar READMEs de código, páginas de matrícula e fichas de vídeo como evidência de comunicação clínica. Documentos podem ser antigos ou destinados a professores/crianças: preservar público, versão e contexto. Exercícios musculares e vocais não são recomendações universais.

## Pendências de coleta

- Manual de Comunicação — 2023: Era esperado PDF; recebida página HTML. Fonte: https://www2.senado.leg.br/bdsf/bitstream/handle/id/646463/Manual_comunicacao_2023.pdf
- Oficina de Vida: curl: (56) Maximum file size exceeded. Fonte: https://bvsms.saude.gov.br/bvs/publicacoes/oficina_vida_imp.pdf
- Cartilha Programa Justiça Restaurativa nas Escolas — Nós: Era esperado PDF; recebida página HTML. Fonte: https://acervodenoticias.educacao.mg.gov.br/images/documentos/Cartilha%20Programa%20Justi%C3%A7a%20Restaurativa%20nas%20Escolas%20-%20N%C3%B3s.pdf
- Oratória para cursos e palestras: curl: (22) The requested URL returned error: 404. Fonte: https://www.egov.df.gov.br/wp-content/uploads/2025/03/apostila_2503181.pdf

## Transparência

Nenhum modelo foi treinado; os novos arquivos não foram adicionados automaticamente ao índice do Hermes. Alguns PDFs têm codificações tipográficas que geram avisos de extração. A presença de termos na matriz não valida metodologias ou exercícios. O caderno de vídeo é documentação de pesquisa, não fala transcrita.
