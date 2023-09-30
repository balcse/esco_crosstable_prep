# Preparing the crosstable of eurostat

import pandas as pd
import requests
from pyquery import PyQuery    
from more_itertools import chunked
import time

path_eu_conv = 'data/ONET_(Occupations)_0_updated.csv'
path_output = 'output/esco_hash_{}_{}.csv'

# df_aioe = pd.read_excel(path_aioe,sheet_name=1)

dfe = pd.read_csv(path_eu_conv,skiprows=16)
urls = dfe['ESCO or ISCO URI'].unique().tolist()

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36'
headers = {'User-Agent': user_agent}
baseurl = 'https://esco.ec.europa.eu/en/classification/occupation?uri={}'

output = {'hash':[],'esco':[]}

def query(url):
    req = requests.get(baseurl.format(url),headers=headers)
    if req.status_code != 200:
        print(req.status_code)
    pq = PyQuery(req.text)
    tag = pq('a.menu_active').text()
    output['hash'].append(url.split('/')[-1])
    output['esco'].append(tag.split(' - ')[0])

counter = 0
batchsize = 500

batches = list(chunked(urls[:15],batchsize))

for i in range(len(batches)):
    print('Batch {} of {}'.format(i+1,len(batches)))
    for url in batches[i]:
        query(url)
    time.sleep(5)

    df = pd.DataFrame.from_dict(output)
    df = df.set_index('hash')

    df.to_csv(path_output.format(str(batchsize),str(i+1)))
    print('finished')