import json,re
f=open('C:/Users/usuario/Desktop/biomagnetismo/disease_data.js',encoding='utf-8').read()
m=re.search(r"const DISEASE_DATA\s*=\s*(\{.*\})\s*;",f,flags=re.S)
D=json.loads(m.group(1))
empt=[k for k,v in D.items() if not v.get('pbs')]
print(len(empt))
for k in empt:
    print(k)
