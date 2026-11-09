from pathlib import Path
import runpy,json,subprocess,hashlib,zipfile,io,shutil
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin,quote
B=Path(__file__).resolve().parents[1]
m=runpy.run_path(str(Path(__file__).with_name('coletor_base.py')),run_name='collector'); m['download'].__globals__['BASE']=B

def get(url):
 r=subprocess.run(['curl','-fLsS','--max-time','80','--max-filesize','60000000',quote(url,safe=':/?=&%')],capture_output=True,timeout=90)
 if r.returncode:raise ValueError(r.stderr.decode().strip())
 return r.stdout
sources=[
('presidencia_redacao','Manual de Redação da Presidência da República — 3ª edição','Presidência da República','eixo4_gramatica','redação formal','Concordância, pronomes e ambiguidades no registro formal','https://www.gov.br/cidades/pt-br/midia/documentos/pdf/manualderedacao.pdf',False),
('senado_comunicacao','Manual de Comunicação — 2023','Senado Federal','eixos1e2','comunicadores','Redação, estilo, qualidade e públicos; registro CC0 no repositório institucional','https://www2.senado.leg.br/bdsf/bitstream/handle/id/646463/Manual_comunicacao_2023.pdf',False),
('mme_escuta','Guia básico de acolhimento','MME — acervo institucional','eixo1_escuta','acolhimento no trabalho','Escuta ativa; contexto de acolhimento específico','https://www.gov.br/mme/pt-br/assuntos/conselhos-e-comites/cogemmev/biblioteca/prevencao-e-enfrentamento-de-quaisquer-violencias-no-trabalho/publicacoes/guia_basico_acolhimento_web1.pdf',False),
('ms_oficina_vida','Oficina de Vida','Ministério da Saúde','eixo1_comunicacao','educação em saúde','Comunicação, escuta e interação em contexto educativo','https://bvsms.saude.gov.br/bvs/publicacoes/oficina_vida_imp.pdf',False),
('mg_restaurativa','Cartilha Programa Justiça Restaurativa nas Escolas — Nós','Governo MG','eixo1_cnv','comunidades escolares','Observação, sentimentos, necessidades e pedidos; preservar contexto escolar','https://acervodenoticias.educacao.mg.gov.br/images/documentos/Cartilha%20Programa%20Justi%C3%A7a%20Restaurativa%20nas%20Escolas%20-%20N%C3%B3s.pdf',False),
('egov_oratoria_2025','Oratória para cursos e palestras','EGOV-DF','eixo2_oratoria','profissionais','Planejar palestras, público e ideia central','https://www.egov.df.gov.br/wp-content/uploads/2025/03/apostila_2503181.pdf',False),
('nilcmetrix_slides','NILC-Metrix — apresentação técnica','NILC','pesquisa','pesquisadores','Documentação das métricas linguísticas; não é rubrica de assertividade','https://raw.githubusercontent.com/nilc-nlp/nilcmetrix/main/static/NILC-Metrix_Slides_16_04_2021.pdf',False),
]
try:
 page=get('https://esesp.es.gov.br/trilhacomunicacao');p=m['Parser']();p.feed(page.decode(errors='replace'))
 for n,url in enumerate(dict.fromkeys(p.links)):
  sources.append((f'esesp_comunicacao_{n+1}','Apostila de Comunicação — '+url.split('/')[-1],'ESESP','eixo2_comunicacao','servidores e comunicadores','Documento da trilha de comunicação; título deve ser confirmado na primeira página',urljoin('https://esesp.es.gov.br/',url),False))
except Exception as e:print('ESESP:',e)
with ThreadPoolExecutor(max_workers=4) as pool: rows=[r for group in pool.map(m['download'],sources) for r in group]
(B/'fontes_ampliacao.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
D=B/'datasets';D.mkdir(exist_ok=True)
manifest=[]
for id,repo,license in [('complexidade','gazzola/corpus_readability_nlp_portuguese','CC BY 4.0 declarada no README'),('nilcmetrix','nilc-nlp/nilcmetrix','AGPLv3; preservar licença do código e componentes')]:
 try:
  meta=json.loads(get('https://api.github.com/repos/'+repo));branch=meta['default_branch'];commit=json.loads(get('https://api.github.com/repos/'+repo+'/commits/'+branch))['sha']
  data=get('https://api.github.com/repos/'+repo+'/zipball/'+commit)
  path=D/(id+'.zip');path.write_bytes(data)
  files=zipfile.ZipFile(io.BytesIO(data)).infolist();total=sum(x.file_size for x in files)
  record=dict(id=id,url='https://github.com/'+repo,commit=commit,license=license,file=str(path.relative_to(B)),sha256=hashlib.sha256(data).hexdigest(),entries=len(files),uncompressed_bytes=total,status='downloaded')
  if id=='complexidade':
   # Arquivos de dados reais, extraídos com proteção de caminhos.
   z=zipfile.ZipFile(io.BytesIO(data));root=D/'complexidade';root.mkdir(exist_ok=True)
   for info in files:
    parts=Path(info.filename).parts[1:]
    if not parts or info.is_dir():continue
    dest=root.joinpath(*parts)
    if not dest.resolve().is_relative_to(root.resolve()):raise ValueError('Caminho ZIP inválido')
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(info))
   record['data_files']=sum(1 for p in root.rglob('*.txt'))
  manifest.append(record);print('DATA',id,len(data),record.get('data_files'),flush=True)
 except Exception as e:manifest.append(dict(id=id,status='failed',error=str(e)))
# CORAA: documentação e licença originais; áudios são distribuídos por links externos do projeto.
for file in ['README.md','LICENSE']:
 try:
  data=get('https://raw.githubusercontent.com/nilc-nlp/CORAA/main/'+file);p=D/'coraa'/file;p.parent.mkdir(exist_ok=True);p.write_bytes(data)
 except Exception as e:print('CORAA',str(e))
(B/'datasets_manifesto.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('DOCS',len(rows),sum(r['status']=='downloaded' for r in rows))
