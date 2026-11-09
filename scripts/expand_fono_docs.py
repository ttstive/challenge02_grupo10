from pathlib import Path
import json, hashlib, subprocess, io
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from urllib.parse import quote,urljoin
from html.parser import HTMLParser
from pypdf import PdfReader
REPO=Path(__file__).resolve().parents[1]
BASE=REPO/'docs/rag'
SOURCES=[
('mg_saude_vocal','Cartilha Saúde Vocal','SEPLAG-MG','saúde vocal','professores','Orientações sobre produção e cuidados com a voz','https://www.portaldoservidor.mg.gov.br/sites/default/files/pdf_servicos/CARTILHA%20SAUDE%20VOCAL.pdf',False),
('caragua_vocal','Cartilha Saúde Vocal do Professor','Prefeitura de Caraguatatuba','saúde vocal','professores','Prevenção e uso profissional da voz','https://www.caraguatatuba.sp.gov.br/pmc/wp-content/uploads/2021/04/Cartilha-Saude-Vocal-do-Professor.pdf',False),
('ebook_voz_professor','Fonoaudiologia: o que fazer com a voz do professor?','CEREST Registro — acervo público','voz profissional','profissionais e professores','Livro técnico com práticas e fundamentos; revisão especializada antes de recomendar exercícios','https://registro.sp.gov.br/cerest/arquivos/biblioteca/127/e-book-voz-do-professor.pdf',False),
('rio_manual_voz','Manual da Voz — Programa de Saúde Vocal do Professor','Prefeitura do Rio de Janeiro','saúde vocal','professores','Material histórico de orientação vocal; revisar atualidade das recomendações','https://rio.rj.gov.br/dlstatic/10112/4679376/4122203/manualdavoz_site.pdf',False),
('ms_dvrt','Distúrbio de Voz Relacionado ao Trabalho — DVRT','Ministério da Saúde','voz e trabalho','profissionais de saúde','Referência técnica para riscos e limites do sistema; não usar como diagnóstico automatizado','https://bvsms.saude.gov.br/bvs/publicacoes/disturbio_voz_relacionado_trabalho_dvrt.pdf',False),
('sbfa_disfluencia','Disfluências comuns e gagueira','Sociedade Brasileira de Fonoaudiologia','fluência','profissionais e equipe de pesquisa','Diferenciar disfluências comuns de sinais clínicos; evitar penalização indiscriminada','https://fonoaudiologia.sbfa.org.br/_files/ugd/ead516_dfc28d33faaa4586b594a6f036391500.pdf',False),
('abra_gagueira','Cartilha sobre Gagueira','Abra Gagueira','fluência e inclusão','público geral','Informação e redução do estigma','https://www.abragagueira.org.br/wp-content/uploads/2020/03/CARTILHA-GAGUEIRA-FINAL-PARA-IMPRESS%C3%83O-2108.pdf',False),
('cffa_sus','Contribuição da Fonoaudiologia para o avanço do SUS','Conselho Federal de Fonoaudiologia','fundamentos profissionais','equipe de pesquisa','Entender áreas de atuação e limites profissionais','https://fonoaudiologia.org.br/wp-content/uploads/2019/09/Contribuicao-Fonoaudiologia-Avancao-do-Sus.pdf',False),
('alece_saude_vocal','Manual de Saúde Vocal — 2024','ALECE / INESP / DSAS','saúde vocal','profissionais da voz','Uso apropriado da voz e prevenção','https://www.al.ce.gov.br/edicoes-inesp/download/130',False),
('ifpr_saude_vocal','Saúde Vocal para Professores EBTT','IFPR / eduCAPES','saúde vocal','professores','Livro educacional complementar','https://educapes.capes.gov.br/handle/capes/584558',True),
('sbfa_guias_fluencia','Guias: Fluência e seus transtornos / Gagueira na infância','Sociedade Brasileira de Fonoaudiologia','fluência','fonoaudiólogos','Referências especializadas; infância não deve ser generalizada a adultos','https://fonoaudiologia.sbfa.org.br/linguagem',True),
]
class Parser(HTMLParser):
 def __init__(self): super().__init__();self.links=[];self.text=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t=='a' and '.pdf' in dict(a).get('href','').lower(): self.links.append(dict(a)['href'])
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.text.append(d.strip())
def download(source):
 id,title,org,theme,audience,use,url,follow=source
 rec=dict(id=id,title=title,institution=org,theme=theme,audience=audience,application=use,url=url,license_status='Revisar no documento antes de redistribuir',review_status='Coletado; curadoria de conteúdo pendente',accessed_at=datetime.now(timezone.utc).isoformat())
 children=[]
 try:
  dest=BASE/'originais'/f'{id}.pdf'
  if dest.exists(): data=dest.read_bytes()
  else:
   r=subprocess.run(['curl','--fail','--location','--silent','--show-error','--max-time','55','--max-filesize','50000000',quote(url,safe=':/?=&%')],capture_output=True,timeout=60)
   if r.returncode:raise ValueError(r.stderr.decode().strip())
   data=r.stdout
  if data.startswith(b'%PDF-'):
   reader=PdfReader(io.BytesIO(data));dest.write_bytes(data)
   parts=[f'## Página {n}\n\n{p.extract_text() or "[Necessita OCR]"}' for n,p in enumerate(reader.pages,1)]
   text='\n\n'.join(parts);rec.update(pages=len(reader.pages),kind='pdf')
  else:
   html=data.decode('utf-8',errors='replace')
   if '<html' not in html.lower() and '<!doctype' not in html.lower():raise ValueError('Resposta não reconhecida como PDF/HTML')
   parser=Parser();parser.feed(html)
   dest=BASE/'paginas'/f'{id}.html';dest.write_bytes(data);text='\n\n'.join(parser.text);rec['kind']='page'
   if follow:
    for n,link in enumerate(dict.fromkeys(parser.links)):
     # Somente anexos explicitamente ligados pela página selecionada, limite 2.
     if n>=2:break
     child=download((id+f'_anexo{n+1}',title+f' — anexo {n+1}',org,theme,audience,use,urljoin(url,link),False));children.extend(child)
   else:raise ValueError('Era esperado PDF; recebida página HTML')
  (BASE/'textos'/f'{id}.md').write_text(f'# {title}\n\nFonte: {url}\n\nPúblico: {audience}\n\n'+text)
  rec.update(status='downloaded',file=str(dest.relative_to(BASE)),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
 except Exception as error:rec.update(status='failed',error=str(error))
 print(id,rec['status'],flush=True)
 return [rec]+children
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=4) as pool: results=[r for group in pool.map(download,SOURCES) for r in group]
 (BASE/'fontes_fono.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
 rows=['# Acervo ampliado de fonoaudiologia','', 'Materiais educativos, técnicos e de referência. A coleta não significa revisão clínica ou autorização de redistribuição. Materiais infantis e de professores têm contexto específico; preservar público e limitações na indexação.','', '| Material | Instituição / tema | Aplicação e público | Arquivo / situação |','|---|---|---|---|']
 for r in results:
  file=f"[Arquivo]({r['file']})" if r['status']=='downloaded' else 'Download pendente (ver manifesto)'
  rows.append(f"| [{r['title']}]({r['url']}) | {r['institution']} / {r['theme']} | {r['application']}. Público: {r['audience']} | {file} |")
 (BASE/'FONOAUDIOLOGIA.md').write_text('\n'.join(rows)+'\n')
 print('TOTAL',len(results),'SUCESSO',sum(r['status']=='downloaded' for r in results))
