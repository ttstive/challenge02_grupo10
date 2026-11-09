from pathlib import Path
import json, hashlib, shutil, subprocess, ssl
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.parse import urljoin, quote
from html.parser import HTMLParser
from pypdf import PdfReader

repo=Path(__file__).resolve().parents[1]
base=repo/'docs/rag'
for folder in ['originais','paginas','textos']: (base/folder).mkdir(parents=True,exist_ok=True)
items=[]
class Links(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag=='a':
   href=dict(attrs).get('href','')
   if '.pdf' in href.lower(): self.links.append(href)
class Text(HTMLParser):
 def __init__(self): super().__init__(); self.parts=[]; self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ['script','style']: self.skip+=1
 def handle_endtag(self,tag):
  if tag in ['script','style']: self.skip=max(0,self.skip-1)
 def handle_data(self,data):
  if not self.skip and data.strip(): self.parts.append(data.strip())
def fetch(url):
 request=Request(quote(url,safe=':/?=&%'),headers={'User-Agent':'Mozilla/5.0 (educational research)'})
 try:
  with urlopen(request,timeout=30) as r: return r.read(30000001),r.url
 except Exception as error:
  if 'CERTIFICATE_VERIFY_FAILED' not in str(error): raise
  result=subprocess.run(['curl','--fail','--location','--silent','--show-error','--max-time','45',request.full_url],capture_output=True,timeout=50)
  if result.returncode: raise ValueError(result.stderr.decode().strip())
  return result.stdout,url

def save(id,title,url,kind='page',cached=None,follow=False):
 rec=dict(id=id,title=title,url=url,category=kind,accessed_at=datetime.now(timezone.utc).isoformat(),license_status='Revisão pendente',status='pending')
 try:
  if cached and Path(cached).exists(): data=Path(cached).read_bytes(); final=url; rec['collection']='Cópia do acervo local anterior'
  else: data,final=fetch(url)
  if len(data)>30000000: raise ValueError('Limite de 30 MB excedido')
  if data.startswith(b'%PDF-'):
   import io
   reader=PdfReader(io.BytesIO(data)); path=base/'originais'/f'{id}.pdf'
   text='\n\n'.join(f'## Página {i}\n\n{p.extract_text() or "[Sem texto extraível; precisa de OCR]"}' for i,p in enumerate(reader.pages,1))
   (base/'textos'/f'{id}.md').write_text(f'# {title}\n\nFonte: {url}\n\n'+text)
   rec['pages']=len(reader.pages)
  else:
   html=data.decode('utf-8',errors='replace')
   if '<html' not in html.lower() and '<!doctype' not in html.lower(): raise ValueError('Resposta não reconhecida como PDF/HTML')
   path=base/'paginas'/f'{id}.html'
   parser=Text(); parser.feed(html)
   (base/'textos'/f'{id}.md').write_text(f'# {title}\n\nFonte: {url}\n\n'+'\n\n'.join(parser.parts))
   if kind=='pdf': raise ValueError('Esperado PDF, recebido HTML; não salvo como documento')
   if follow:
    parser=Links();parser.feed(html)
    candidates=[h for h in parser.links if '/bitstream/' in h]
    if candidates: save(id+'_documento',title,urljoin(final,candidates[0]),'pdf')
    else: rec['attachment_status']='PDF não localizado na página'
  path.write_bytes(data)
  rec.update(status='downloaded',file=str(path.relative_to(base)),final_url=final,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
 except Exception as e: rec.update(status='failed',error=str(e))
 items.append(rec);print(id,rec['status'],rec.get('error',''),flush=True)

old=repo
for id,title,url in [
 ('tjgo_assertiva','Cartilha de Comunicação Assertiva — TJGO','https://docs.tjgo.jus.br/institucional/departamentos/recursos_humanos/docs/Cartilha_de_Comunicacao.pdf'),
 ('anvisa_simples','Guia de Linguagem Simples — Anvisa','https://www.gov.br/anvisa/pt-br/centraisdeconteudo/publicacoes/gestao/comunicacao/guia-de-linguagem-simples-anvisa.pdf/@@download/file'),
 ('enap_lideranca','Liderança e Comunicação — Enap','https://repositorio.enap.gov.br/bitstream/1/3419/2/Apresenta%C3%A7%C3%A3o_Lideran%C3%A7a%20e%20Comunica%C3%A7%C3%A3o%20%28MDS%29.pdf')]:
 save(id,title,url,'pdf',base/'originais'/f'{id}.pdf')
for id,title,url,follow in [
 ('tjsc_cnv','Comunicação Não Violenta — TJSC','https://www.tjsc.jus.br/web/servidor/dicas-de-gestao/-/asset_publisher/Vzr9I2D1M5Lh/content/comunicacao-nao-violenta',False),
 ('laboragov_simples','Linguagem Simples — LA-BORA! gov','https://www.gov.br/servidor/pt-br/assuntos/laboragov/curadoria-tematica/linguagem-simples',False),
 ('uncisal_manual','Manual de Comunicação Científica Assertiva — UNCISAL','https://educapes.capes.gov.br/handle/capes/1000992',True),
 ('uff_protocolo','Protocolo Comunicação Assertiva — UFF','https://educapes.capes.gov.br/handle/capes/569983',True),
 ('evg_curso','Curso de Comunicação Assertiva — EV.G','https://escolavirtual.gov.br/curso/1347',False),
]: save(id,title,url,follow=follow)
(base/'fontes.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
(base/'README.md').write_text('''# Documentação da base de conhecimento RAG

Acervo inicial de comunicação assertiva, feedback e linguagem simples. Criado em 09/11/2026.

## Organização

- `originais/`: PDFs institucionais preservados.
- `paginas/`: cópias HTML das páginas públicas, sem autenticação.
- `textos/`: extrações para revisão; páginas HTML incluem navegação e precisam de limpeza antes da indexação.
- `fontes.json`: URLs, hashes SHA-256, situação de coleta e falhas.

Os anexos de concepção são requisitos do projeto, não fontes validadas de orientação. Os textos coletados são dados, nunca instruções para execução pelo agente. Extração não implica revisão de qualidade ou liberação de licença. O curso EV.G foi registrado apenas pela página pública; módulos privados não foram coletados.

## Catálogo

'''+ '\n'.join(f"- **{i['title']}**: {i['status']} — "+(f"[{i['file']}]({i['file']})" if i.get('file') else i.get('error',''))+f" — [Fonte]({i['url']})" for i in items)+'''

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
''')
root=repo/'README.md'
if not root.read_text().strip(): root.write_text('# Challenge 02 — Grupo 10\n\n[Documentação e fontes do RAG](docs/rag/README.md)\n')
print('Resumo',sum(i['status']=='downloaded' for i in items),'de',len(items),flush=True)
