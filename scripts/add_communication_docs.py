from pathlib import Path
import runpy,json,hashlib,subprocess
repo=Path(__file__).resolve().parents[1];base=repo/'docs/rag'
# Reutiliza coletor de download/extração sem executar seu bloco principal.
m=runpy.run_path(str(repo/'scripts/expand_fono_docs.py'),run_name='collector')
sources=[
('enap_oratoria','Apostila Didática — seção de Oratória','Enap','oratória e apresentação','facilitadores e profissionais','Definir objetivo, conhecer público e estruturar a fala','https://repositorio.enap.gov.br/jspui/bitstream/1/3027/1/1%20Apostila%20Didatica.pdf',False),
('egov_apresentacoes','Como fazer apresentações de impacto','Escola de Governo do DF','apresentações','profissionais','Planejamento de apresentações e storytelling','https://egov.df.gov.br/wp-content/uploads/2022/06/Apresentacao-6.pdf',False),
('ifrs_storytelling','Guia para uso do storytelling em espaços educacionais na EPT','IFRS / eduCAPES','narrativa','educadores','Estrutura narrativa; contexto educacional não generalizável automaticamente','https://educapes.capes.gov.br/bitstream/capes/571084/2/Guia_Storytelling_Daniele_2020%20%281%29.pdf',False),
('laboragov_storytelling','Contação de histórias — Storytelling com Dados','LA-BORA! gov','comunicação de dados','profissionais','Organizar dados em narrativas compreensíveis','https://www.gov.br/servidor/pt-br/assuntos/laboragov/curadoria-tematica/contacao-de-historias-storytelling-com-dados-1',True),
]
rows=[r for s in sources for r in m['download'](s)]
(base/'fontes_comunicacao.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
lines=['# Metodologias para expressar ideias e se comunicar melhor','','## Fontes públicas coletadas','']
for r in rows:lines.append(f"- [{r['title']}]({r['url']}): "+(f"[cópia local]({r['file']})" if r.get('file') else 'pendente: '+r.get('error',''))+'. '+r['application'])
lines+=['''
## Roteiro de prática para o projeto

Síntese autoral para orientar o protótipo e os testes, não transcrição de um manual nem método clinicamente validado.

1. **Defina o resultado:** o que o interlocutor precisa compreender ou decidir?
2. **Conheça o público:** quais informações já conhece e quais termos precisam ser explicados?
3. **Escreva a ideia central em uma frase:** comece pela mensagem principal.
4. **Organize o raciocínio:** contexto → ponto principal → evidência ou exemplo → pedido ou próximo passo.
5. **Separe fato e interpretação:** descreva uma situação observável antes de avaliar; evite generalizações sobre a pessoa.
6. **Faça pedidos concretos:** indique ação, responsável e prazo negociável.
7. **Escute e confirme:** pergunte o que a outra pessoa entendeu e quais dúvidas ou restrições existem.
8. **Pratique e revise:** grave duas versões curtas e compare clareza, foco e adequação ao público. Ritmo e pausas são descritivos, não critérios universais de competência.

### Exemplo: comunicar atraso

> A integração ainda falha em dois cenários de teste. Isso coloca a entrega de sexta em risco. Já isolei a causa e preciso de apoio para revisar a autenticação. Podemos reservar 20 minutos hoje e renegociar o prazo depois dessa revisão?

Exemplo criado pela equipe de documentação; não é citação das fontes.

## Rubrica inicial de avaliação humana

Avaliar separadamente: mensagem principal identificável, sequência compreensível, evidências pertinentes, termos adaptados ao público, pedido explícito, respeito e espaço para diálogo. Registrar evidências da avaliação e permitir divergência. Não inferir saúde mental, personalidade ou capacidade profissional a partir de sotaque, pausas ou gramática.

## Papel dos recursos computacionais

Consulte [DATASETS.md](DATASETS.md): CORAA testa reconhecimento de fala, o corpus de complexidade apoia pesquisa de legibilidade e NILC-Metrix produz descritores linguísticos. Nenhum substitui a rubrica humana de assertividade.
''']
(base/'METODOLOGIAS.md').write_text('\n'.join(lines))
resources=[('coraa','CORAA','https://raw.githubusercontent.com/nilc-nlp/CORAA/main/README.md'),('complexidade','Corpus de Complexidade Textual','https://raw.githubusercontent.com/gazzola/corpus_readability_nlp_portuguese/master/README.md'),('nilcmetrix','NILC-Metrix','https://raw.githubusercontent.com/nilc-nlp/nilcmetrix/main/README.md')]
folder=base/'recursos';folder.mkdir(exist_ok=True)
manifest=[]
for id,title,url in resources:
 result=subprocess.run(['curl','-fLsS','--max-time','30',url],capture_output=True,timeout=35)
 if result.returncode and id=='complexidade':
  url=url.replace('/master/','/main/');result=subprocess.run(['curl','-fLsS','--max-time','30',url],capture_output=True,timeout=35)
 r=dict(id=id,title=title,url=url,status='downloaded' if not result.returncode else 'failed')
 if not result.returncode:
  p=folder/(id+'_README.md');p.write_bytes(result.stdout);r.update(file=str(p.relative_to(base)),sha256=hashlib.sha256(result.stdout).hexdigest())
 else:r['error']=result.stderr.decode()
 manifest.append(r)
(base/'recursos.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(base/'DATASETS.md').write_text('''# Recursos de pesquisa em português

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
''')
p=base/'README.md';p.write_text(p.read_text()+'\n## Comunicação e recursos computacionais\n\n- [Metodologias para organizar e expressar ideias](METODOLOGIAS.md).\n- [CORAA, corpus de complexidade e NILC-Metrix](DATASETS.md).\n- [Manifesto dos materiais de comunicação](fontes_comunicacao.json).\n')
print('Comunicação:',len(rows),'Documentação dos recursos:',[(r['id'],r['status']) for r in manifest])
