import re, json, os, unicodedata

proj = r"C:\Users\usuario\Desktop\biomagnetismo"
texts_dir = os.path.join(proj, 'pdf_texts')

def normalize(s):
    s = s.lower()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = s.replace('ñ', 'n')
    s = re.sub(r"[^a-z0-9\s-]", '', s)
    s = re.sub(r"\s+", ' ', s).strip()
    return s

# Load mapping from Guia de rastreo segundo nivel
map_file = os.path.join(texts_dir, 'Guia de rastreo segundo nivel.pdf.txt')
mapping = {}
name_to_num = {}
if os.path.exists(map_file):
    with open(map_file, encoding='utf-8') as f:
        for line in f:
            m = re.match(r"\s*(\d{1,3})\s+(.+)$", line)
            if m:
                num = int(m.group(1))
                name = m.group(2).strip()
                # clean name: remove trailing uppercase markers
                name = re.sub(r"\s+\b[A-Z ]+$", '', name).strip()
                n = normalize(name)
                mapping[num] = name
                name_to_num[n] = num
# Fallback: also parse 'Lista+de+pares+par' for numbered entries
other_map = os.path.join(texts_dir, 'Lista+de+pares+par.pdf.txt')
if os.path.exists(other_map):
    with open(other_map, encoding='utf-8') as f:
        for line in f:
            m = re.match(r"\s*(\d{1,3})\s*([A-Z].+)$", line)
            if m:
                num = int(m.group(1))
                name = m.group(2).strip()
                n = normalize(name)
                if n not in name_to_num:
                    name_to_num[n] = num
                    mapping[num] = name

# Load DISEASE_DATA JSON from disease_data.js
dd_file = os.path.join(proj, 'disease_data.js')
with open(dd_file, encoding='utf-8') as f:
    txt = f.read()
# extract JSON after 'const DISEASE_DATA = '
m = re.search(r"const DISEASE_DATA\s*=\s*(\{.*\})\s*;", txt, flags=re.S)
if not m:
    print('No pude localizar DISEASE_DATA en disease_data.js')
    raise SystemExit(1)
json_text = m.group(1)
DISEASES = json.loads(json_text)

# Combine content of relevant PDF texts
candidates = ['Pares por enfermedad.pdf.pdf.txt', 'Rastreo y Parescompletos.pdf.txt', 'LINDE 3-Guia-Pares-Biomagnetico-2do-nivel (1).pdf.txt', 'LINDE29-Bio-Magne-Tismo-Kronos (1).pdf.txt', 'Lista+de+pares+par.pdf.txt']
combined = ''
for name in candidates:
    path = os.path.join(texts_dir, name)
    if os.path.exists(path):
        combined += '\n' + open(path, encoding='utf-8').read().lower()

# For quick matching, also build normalized combined
combined_norm = normalize(combined)

changes = {}
for disease, info in DISEASES.items():
    if not info.get('pbs'):
        dname = normalize(disease)
        idx = combined_norm.find(dname)
        found_nums = set()
        if idx != -1:
            # take window around occurrence
            window = combined_norm[max(0, idx-500): idx+1500]
            # search for known mapped names in window
            for nname, num in name_to_num.items():
                if nname in window:
                    found_nums.add(num)
        else:
            # try searching disease words separately
            words = dname.split()
            for w in words[:3]:
                idx = combined_norm.find(w)
                if idx!=-1:
                    window = combined_norm[max(0, idx-200): idx+800]
                    for nname, num in name_to_num.items():
                        if nname in window:
                            found_nums.add(num)
        if found_nums:
            DISEASES[disease]['pbs'] = sorted(found_nums)
            changes[disease] = sorted(found_nums)

# Show summary
print('Found mappings for', len(changes), 'diseases')
for k,v in list(changes.items())[:50]:
    print(k, v)

# Write back disease_data.js with updated DISEASES
new_json = json.dumps(DISEASES, ensure_ascii=False, indent=2)
new_txt = re.sub(r"const DISEASE_DATA\s*=\s*\{.*\}\s*;", f"const DISEASE_DATA = {new_json};", txt, flags=re.S)
with open(dd_file, 'w', encoding='utf-8') as f:
    f.write(new_txt)

print('Wrote updated disease_data.js')
