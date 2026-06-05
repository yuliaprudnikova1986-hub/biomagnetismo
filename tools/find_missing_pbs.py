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

# Load mapping from Guia
mapping_files = ['Guia de rastreo segundo nivel.pdf.txt', 'Lista+de+pares+par.pdf.txt']
name_to_num = {}
num_set = set()
for mf in mapping_files:
    path = os.path.join(texts_dir, mf)
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            for line in f:
                m = re.match(r"\s*(\d{1,3})\s+(.+)$", line)
                if m:
                    num = int(m.group(1))
                    name = m.group(2).strip()
                    name_clean = re.sub(r"\s+\b[A-Z ]+$", '', name).strip()
                    n = normalize(name_clean)
                    name_to_num[n] = num
                    num_set.add(num)

# Load disease_data
dd_file = os.path.join(proj, 'disease_data.js')
with open(dd_file, encoding='utf-8') as f:
    txt = f.read()
m = re.search(r"const DISEASE_DATA\s*=\s*(\{.*\})\s*;", txt, flags=re.S)
if not m:
    print('DISEASE_DATA not found')
    raise SystemExit(1)
DISEASES = json.loads(m.group(1))

# Combined text
candidates = [f for f in os.listdir(texts_dir) if f.endswith('.txt')]
combined = ''
for name in candidates:
    with open(os.path.join(texts_dir, name), encoding='utf-8') as f:
        combined += '\n' + f.read().lower()
combined_norm = normalize(combined)

updated = {}
not_found = []
for disease, info in DISEASES.items():
    if info.get('pbs'):
        continue
    dnorm = normalize(disease)
    found_nums = set()
    # strategy 1: exact disease name in combined_norm
    idx = combined_norm.find(dnorm)
    if idx!=-1:
        window = combined_norm[max(0, idx-300): idx+800]
        # find explicit numbers in window
        for num in re.findall(r"\b(\d{1,3})\b", window):
            nint = int(num)
            if nint in num_set:
                found_nums.add(nint)
        # find pair-name matches
        for pname, pnum in name_to_num.items():
            if pname in window:
                found_nums.add(pnum)
    else:
        # strategy 2: search by keywords (split disease)
        parts = dnorm.split()
        for p in parts[:3]:
            idx2 = combined_norm.find(p)
            if idx2!=-1:
                window = combined_norm[max(0, idx2-200): idx2+600]
                for num in re.findall(r"\b(\d{1,3})\b", window):
                    nint = int(num)
                    if nint in num_set:
                        found_nums.add(nint)
                for pname, pnum in name_to_num.items():
                    if pname in window:
                        found_nums.add(pnum)
    # strategy 3: disease appears in 'Pares por enfermedad' with colon or heading
    if not found_nums:
        ppe = os.path.join(texts_dir, 'Pares por enfermedad.pdf.pdf.txt')
        if os.path.exists(ppe):
            txtppe = open(ppe, encoding='utf-8').read().lower()
            idx3 = txtppe.find(dnorm)
            if idx3!=-1:
                w = txtppe[max(0, idx3-300): idx3+800]
                for num in re.findall(r"\b(\d{1,3})\b", w):
                    nint = int(num)
                    if nint in num_set:
                        found_nums.add(nint)
    if found_nums:
        DISEASES[disease]['pbs'] = sorted(found_nums)
        updated[disease] = sorted(found_nums)
    else:
        not_found.append(disease)

# write back
new_json = json.dumps(DISEASES, ensure_ascii=False, indent=2)
new_txt = re.sub(r"const DISEASE_DATA\s*=\s*\{.*\}\s*;", f"const DISEASE_DATA = {new_json};", txt, flags=re.S)
with open(dd_file, 'w', encoding='utf-8') as f:
    f.write(new_txt)

print('Updated', len(updated), 'diseases')
for k,v in updated.items():
    print('-', k, v)
print('\nNot found for', len(not_found), 'diseases')
for d in not_found[:50]:
    print('-', d)
