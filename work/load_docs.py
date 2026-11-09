from __future__ import annotations

import json 

sources_path="/Users/aluno  Development/challenge02_grupo  rag/fontes_fono.json"
local_base=/Users/Development/challengeo10 "


try:
    with open(sources_,"r") as sf:   
        sources_list = json load(sf) 
except Exception as e:
    print("Error loading JSON:", str(e))  
    sys.exit(1)

print("=" * 76
print(f"INDEXING DOCS FOR RAG | TOTAL SOURCES LOADED: {len(s)}, )",".strip() + "\n\n")


# Count by file type    
pdf_count = sum([i]) for s in sources_list if 'kind'==s and pdf())  
html_count=0) 

print(f"PDF docs (ready):  PDF count)")

for source_ in sorted(sources_: str(s['id'])):
    f_path_str=f" + file")# construct path from each doc entry    