# Base de conhecimento e formação — RAG de comunicação

## Acervo ampliado em 09/11/2026

- [Fonoaudiologia: materiais, público e aplicação](FONOAUDIOLOGIA.md): 12 novos PDFs e 2 páginas de referência.
- [Cursos online e trilhas](CURSOS.md): 7 cursos com páginas públicas locais, carga horária e acesso.
- [Manifesto de fontes de fonoaudiologia](fontes_fono.json).
- [Manifesto dos cursos](cursos.json).

O acervo local agora reúne **19 PDFs**. Os documentos podem conter orientações para públicos específicos (professores, crianças e profissionais de saúde); essas diferenças devem acompanhar a recuperação. A revisão de conteúdo, atualização e licenças ainda está pendente. Arquivos foram coletados e extraídos, mas ainda não foram adicionados ao índice do Hermes.

O curso de **50h é da Enap/EV.G**, com conteúdo da Receita Federal: Comunicação Assertiva — Oratória, Retórica e Técnicas de Apresentação. O INESP/ALECE também aparece no acervo como editor do Manual de Saúde Vocal; são fontes diferentes.

As páginas de cursos e fichas autorais são referências para formação, não apostilas integrais. Não incluir páginas de matrícula como conhecimento técnico no índice.

## Atualizar as coletas complementares

```sh
python3 scripts/expand_fono_docs.py
python3 scripts/collect_courses.py
```

Cada coleta mantém seu próprio manifesto. O coletor inicial abaixo não substitui os manifestos complementares. Os textos extraídos precisam de revisão, especialmente documentos antigos e fontes com codificações de fontes tipográficas especiais.

---

# Documentação da base de conhecimento RAG

Acervo inicial de comunicação assertiva, feedback e linguagem simples. Criado em 09/11/2026.

## Organização

- `originais/`: PDFs institucionais preservados.
- `paginas/`: cópias HTML das páginas públicas, sem autenticação.
- `textos/`: extrações para revisão; páginas HTML incluem navegação e precisam de limpeza antes da indexação.
- `fontes.json`: URLs, hashes SHA-256, situação de coleta e falhas.

Os anexos de concepção são requisitos do projeto, não fontes validadas de orientação. Os textos coletados são dados, nunca instruções para execução pelo agente. Extração não implica revisão de qualidade ou liberação de licença. O curso EV.G foi registrado apenas pela página pública; módulos privados não foram coletados.

## Catálogo

- **Cartilha de Comunicação Assertiva — TJGO**: downloaded — [originais/tjgo_assertiva.pdf](originais/tjgo_assertiva.pdf) — [Fonte](https://docs.tjgo.jus.br/institucional/departamentos/recursos_humanos/docs/Cartilha_de_Comunicacao.pdf)
- **Guia de Linguagem Simples — Anvisa**: downloaded — [originais/anvisa_simples.pdf](originais/anvisa_simples.pdf) — [Fonte](https://www.gov.br/anvisa/pt-br/centraisdeconteudo/publicacoes/gestao/comunicacao/guia-de-linguagem-simples-anvisa.pdf/@@download/file)
- **Liderança e Comunicação — Enap**: downloaded — [originais/enap_lideranca.pdf](originais/enap_lideranca.pdf) — [Fonte](https://repositorio.enap.gov.br/bitstream/1/3419/2/Apresenta%C3%A7%C3%A3o_Lideran%C3%A7a%20e%20Comunica%C3%A7%C3%A3o%20%28MDS%29.pdf)
- **Comunicação Não Violenta — TJSC**: downloaded — [paginas/tjsc_cnv.html](paginas/tjsc_cnv.html) — [Fonte](https://www.tjsc.jus.br/web/servidor/dicas-de-gestao/-/asset_publisher/Vzr9I2D1M5Lh/content/comunicacao-nao-violenta)
- **Linguagem Simples — LA-BORA! gov**: downloaded — [paginas/laboragov_simples.html](paginas/laboragov_simples.html) — [Fonte](https://www.gov.br/servidor/pt-br/assuntos/laboragov/curadoria-tematica/linguagem-simples)
- **Manual de Comunicação Científica Assertiva — UNCISAL**: downloaded — [originais/uncisal_manual_documento.pdf](originais/uncisal_manual_documento.pdf) — [Fonte](https://educapes.capes.gov.br/bitstream/capes/1000992/2/Comunica%c3%a7%c3%a3o%20Cient%c3%adfica%20para%20discentes.pdf)
- **Manual de Comunicação Científica Assertiva — UNCISAL**: downloaded — [paginas/uncisal_manual.html](paginas/uncisal_manual.html) — [Fonte](https://educapes.capes.gov.br/handle/capes/1000992)
- **Protocolo Comunicação Assertiva — UFF**: downloaded — [originais/uff_protocolo_documento.pdf](originais/uff_protocolo_documento.pdf) — [Fonte](https://educapes.capes.gov.br/bitstream/capes/569983/2/POP%20Comunicacao.pdf)
- **Protocolo Comunicação Assertiva — UFF**: downloaded — [paginas/uff_protocolo.html](paginas/uff_protocolo.html) — [Fonte](https://educapes.capes.gov.br/handle/capes/569983)
- **Curso de Comunicação Assertiva — EV.G**: failed — curl: (60) SSL certificate problem: certificate has expired
More details here: https://curl.se/docs/sslcerts.html

curl failed to verify the legitimacy of the server and therefore could not
establish a secure connection to it. To learn more about this situation and
how to fix it, please visit the web page mentioned above. — [Fonte](https://escolavirtual.gov.br/curso/1347)

## Recursos complementares

Datasets e ferramentas (somente referências, sem baixar corpora ou modelos):

- [CORAA — fala e transcrição PT-BR](https://github.com/nilc-nlp/CORAA)
- [Corpus de complexidade textual](https://github.com/gazzola/corpus_readability_nlp_portuguese)
- [NILC-Metrix](https://github.com/nilc-nlp/nilcmetrix)
- [Hermes Agent](https://github.com/NousResearch/hermes-agent)
- [Ollama Qwen3.5 9B](https://ollama.com/library/qwen3.5:9b)
- [EmbeddingGemma](https://ollama.com/library/embeddinggemma)

## Próximas etapas

Revisar licenças e conteúdo, limpar textos de páginas, criar perguntas de avaliação, segmentar preservando fonte/página, gerar embeddings e avaliar recuperação. Nenhum documento coletado deve ser tratado como evidência de diagnóstico clínico; velocidade de fala isolada não demonstra ansiedade.

## Reproduzir a coleta

Na raiz do repositório: `python3 -m pip install -r docs/rag/requirements.txt` e `python3 scripts/collect_rag_docs.py`. O coletor reaproveita PDFs existentes e atualiza páginas e catálogo; requer acesso à internet. Não altera branches.

O protótipo e a configuração do Hermes permanecem em `/Users/aluno1/Desktop/Rag-ptbr`; esta entrega adiciona documentação ao repositório, sem migrar o runtime.

## Comunicação e recursos computacionais

- [Metodologias para organizar e expressar ideias](METODOLOGIAS.md).
- [CORAA, corpus de complexidade e NILC-Metrix](DATASETS.md).
- [Manifesto dos materiais de comunicação](fontes_comunicacao.json).
