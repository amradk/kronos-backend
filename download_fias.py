import requests
import os.path
from unrar import rarfile
from clint.textui import progress

fias_url = 'https://fias-file.nalog.ru/ExportDownloads?file=5158f5b0-3e7a-44a4-acf9-efaddee71fe2'
fias_file = 'fias_db.rar'

def extract_addrob(file_path):
    r_file = rarfile.RarFile(file_path)
    for f in r_file.infolist():
        if f.filename.startswith('ADDROB'):
            #print (f.filename, f.file_size)
            r_file.extract(f)

if not os.path.isfile(fias_file): 

    r = requests.get(fias_url, allow_redirects=True, stream=True)
    
    with open("fias_db.rar", "wb") as Pypdf:
        total_length = int(r.headers.get('content-length'))
        for ch in progress.bar(r.iter_content(chunk_size = 1024), expected_size=(total_length/1024) + 1):
            if ch: 
                Pypdf.write(ch)
    
extract_addrob(fias_file)
