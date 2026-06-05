import os, sys
from PyPDF2 import PdfReader

indir = "C:\\Users\\usuario\\Downloads\\3_Биомагнетизм_BQ\\Маркеры_негатива\\libros biomag\\"
outdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pdf_texts'))
os.makedirs(outdir, exist_ok=True)

for fname in os.listdir(indir):
    if fname.lower().endswith('.pdf'):
        path = os.path.join(indir, fname)
        try:
            reader = PdfReader(path)
            text = []
            for page in reader.pages:
                txt = page.extract_text()
                if txt:
                    text.append(txt)
            outname = os.path.join(outdir, fname + '.txt')
            with open(outname, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(text))
            print(f'Wrote {outname}')
        except Exception as e:
            print('ERROR', path, e)
