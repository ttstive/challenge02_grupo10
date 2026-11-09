from pathlib import Path
import subprocess,json,hashlib
from concurrent.futures import ThreadPoolExecutor
BASE=Path(__file__).resolve().parents[1]/'docs/rag'
courses=[
 ('evg_1347','Comunicação Assertiva: Oratória, Retórica e Técnicas de Apresentação',50,'Receita Federal / Enap','Aberto, gratuito, com certificado','Fundamentos, contextos culturais, retórica e oratória, linguagem corporal, argumentação e escrita assertiva. É o curso de 50h identificado na pesquisa.','https://www.escolavirtual.gov.br/curso/1347'),
 ('evg_463','Comunicação não violenta',20,'Receita Federal / Enap','Aberto, gratuito, com certificado','Observar, sentir, reconhecer necessidades e pedir; aplicação cotidiana.','https://www.escolavirtual.gov.br/curso/463'),
 ('evg_315','Primeiros passos para uso de Linguagem Simples',8,'Enap','Aberto','Modelo Comunica Simples, empatia na escrita, hierarquia das informações e palavras acessíveis.','https://www.escolavirtual.gov.br/curso/315'),
 ('evg_332','Linguagem simples aproxima o governo das pessoas. Como usar?',20,'Prefeitura de São Paulo / Enap','Aberto, gratuito, com certificado','Conhecer, usar e compartilhar linguagem simples.','https://www.escolavirtual.gov.br/curso/332'),
 ('enap_1289','Comunicação Assertiva e Gestão das Emoções',28,'Enap','Restrito ao público-alvo de servidores e empregados públicos federais; depende de turma','Comunicação corporativa, argumentação e competências socioemocionais.','https://suap.enap.gov.br/vitrine/curso/1289/'),
 ('enap_2367','Escutatória e Comunicação Assertiva',24,'Enap','Restrito a lideranças públicas no perfil definido pela instituição; depende de turma','16h ao vivo e 8h assíncronas; escuta, empatia, negociação e conversas com foco.','https://suap.enap.gov.br/vitrine/curso/2367/'),
 ('mg_vocal_curso','Programa de Saúde Vocal — curso EAD',20,'SEPLAG / SEE-MG','Restrito a professores estaduais efetivos e não efetivos','Uso da voz, prevenção e saúde vocal; acesso e turmas pela Escola de Formação.','https://portaldoservidor.mg.gov.br/node/126640'),
]
def collect(c):
 id,title,hours,org,access,summary,url=c
 r=dict(id=id,title=title,hours=hours,institution=org,access=access,summary=summary,url=url,verification_date='2026-11-09',download_scope='Somente página pública; módulos internos não baixados')
 result=subprocess.run(['curl','--fail','--location','--silent','--show-error','--max-time','25',url],capture_output=True,timeout=30)
 if result.returncode==0 and b'<html' in result.stdout.lower():
  p=BASE/'paginas'/f'{id}.html';p.write_bytes(result.stdout);r.update(status='page_downloaded',file=str(p.relative_to(BASE)),sha256=hashlib.sha256(result.stdout).hexdigest())
 else:r.update(status='reference_only',error=result.stderr.decode().strip() or 'Resposta não HTML')
 # Registro de curadoria é documentação autoral; nunca simular apostila original.
 (BASE/'textos'/f'{id}_ficha.md').write_text(f'# Ficha de referência: {title}\n\nInstituição: {org}\n\nCarga horária: {hours}h\n\nAcesso: {access}\n\nFonte: {url}\n\nResumo de curadoria: {summary}\n\nEsta ficha não é transcrição nem apostila do curso. Materiais internos dependem de acesso pela plataforma.\n')
 return r
with ThreadPoolExecutor(max_workers=4) as pool: records=list(pool.map(collect,courses))
(BASE/'cursos.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
lines=['# Cursos e trilhas de estudo','','O curso de 50 horas foi identificado na Enap/EV.G. Não foi encontrada evidência nesta pesquisa para atribuí-lo ao INEP. As cargas horárias abaixo foram verificadas nas páginas institucionais em 09/11/2026; disponibilidade de turmas e condições podem mudar.','','| Curso | Horas | Instituição e acesso | Conteúdo | Situação local |','|---|---:|---|---|---|']
for r in records: lines.append(f"| [{r['title']}]({r['url']}) | {r['hours']} | {r['institution']}; {r['access']} | {r['summary']} | {r['status']} |")
lines+=['','## Uso no RAG','','Páginas de matrícula e fichas de referência ficam no catálogo de formação da equipe. Não substituem apostilas e não devem ser indexadas como se ensinassem todo o curso. Para adicionar módulos, obter os arquivos oficiais por acesso autorizado e registrar origem, versão e condições de uso. Não foram feitos login ou matrícula.']
(BASE/'CURSOS.md').write_text('\n'.join(lines)+'\n')
print('Cursos catalogados:',len(records),'Páginas baixadas:',sum(r['status']=='page_downloaded' for r in records))
