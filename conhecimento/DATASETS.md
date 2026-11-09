# Atualização do pacote

Os dados reais de complexidade textual e Bosque estão agora em `datasets/`. Consulte README.md e datasets_manifesto.json. O texto abaixo é a ficha histórica da primeira coleta.

# Recursos de pesquisa em português

Foram preservadas cópias dos READMEs oficiais em `recursos/`, não os corpora completos nem modelos. Eles são documentação externa e não instruções do projeto. URLs e hashes estão em `recursos.json`. Licenças de dados, código e componentes devem ser conferidas individualmente antes do uso.

| Recurso | Finalidade no projeto | Limites | Documentação local |
|---|---|---|---|
| [CORAA — NILC](https://github.com/nilc-nlp/CORAA) | Avaliar transcrição de fala em português brasileiro; comparar erros com transcrições de referência e perfis de gravação | Não fornece rótulos de assertividade ou ansiedade. Selecionar amostra e verificar licença dos dados | [README](recursos/coraa_README.md) |
| [Corpus de Complexidade Textual](https://github.com/gazzola/corpus_readability_nlp_portuguese) | Experimentos de legibilidade e complexidade textual em português | O repositório declara CC BY 4.0. Nível escolar e complexidade não equivalem a clareza contextual ou assertividade | [README](recursos/complexidade_README.md) |
| [NILC-Metrix](https://github.com/nilc-nlp/nilcmetrix) | Extrair descritores de coesão, coerência e complexidade para análise exploratória | Ferramenta, não dataset. Não mede diretamente confiança, personalidade ou qualidade interpessoal. Repositório declara AGPLv3 | [README](recursos/nilcmetrix_README.md) |

## Experimento sugerido

1. Selecionar uma amostra pequena e autorizada de áudio e transcrição para avaliar STT.
2. Manter os conjuntos de treino e teste separados.
3. Medir erros de transcrição sem convertê-los em notas de comunicação.
4. Usar descritores textuais como informações auxiliares.
5. Avaliar clareza e assertividade por rubrica humana contextualizada; comparar sugestões antes e depois do feedback.

Não incluir os READMEs técnicos no mesmo índice de recomendações educativas sem separar o domínio de recuperação.
