import requests
import textract
import re
import pandas as pd

def download_taxonomy_document(url, filename):
    r = requests.get(url, stream=True)

    with open(filename, 'wb') as f:
        f.write(r.content)

def process_pdf(filename):
    all_text = []
    text = textract.process(filename, encoding='utf_8')
    decoder = textract.parsers.utils.BaseParser()
    split_text = re.split(r'\n\n', decoder.decode(text))
    for line in split_text:
        removed_dots = re.sub(r'\.{2,}','',line)
        if len(removed_dots) >= 200:
            new_line = removed_dots.replace('\n•',' ').replace('\n', ' ').replace('', ' ').replace('•',' ')
            t = re.split(r'(\W+)',new_line)
            if t[0] != '':
                all_text.append(f"{''.join(t)}")
    with open(filename[:-3]+'out', 'w') as ff:
        ff.write(''.join(all_text))
    return all_text

def create_df(data, name):
    df = pd.DataFrame(data, columns=[name])
    return df

if __name__ == "__main__":
    filename = '200309-sustainable-finance-teg-final-report-taxonomy-annexes_en.pdf'
    url = f'https://ec.europa.eu/info/sites/info/files/business_economy_euro/banking_and_finance/documents/{filename}'
    download_taxonomy_document(url, filename)
    data = process_pdf(filename)
    df = create_df(data, 'paragraph')
    print(df)