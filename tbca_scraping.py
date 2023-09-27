import requests
import pandas as pd
from tqdm import tqdm
import os


links = []

for page in range(1, 58):
    link = 'http://www.tbca.net.br/base-dados/composicao_alimentos.php?pagina={}&atuald=1'.format(page)
    links.append(link)

df = pd.DataFrame()

progress = tqdm(links)

for link in progress:
    response = requests.get(link)
    if response.status_code == 200:
        html = response.content
        data = pd.read_html(html)
        df = pd.concat([df, data[0]], ignore_index=True)
    progress.update()

column = df['Código']
codigos = column.tolist()

links_ingredientes = []

for cod in codigos:
    link = 'http://www.tbca.net.br/base-dados/int_composicao_alimentos.php?cod_produto={}'.format(cod)
    links_ingredientes.append(link)

df_final = pd.DataFrame()
progress_1 = tqdm(links_ingredientes)

for link in progress_1:
    response = requests.get(link)
    if response.status_code == 200:
        html = response.content.decode('utf-8')
        html = html.replace(',', '.')
        data = pd.read_html(html, decimal='.')
        cod_produto = link.split("=")[-1]
        data[0]['cod_produto'] = cod_produto
        df_final = pd.concat([df_final, data[0]], ignore_index=True)

    progress_1.update()


current_directory = os.getcwd()
file_name = 'tbca_data.csv'
full_path = os.path.join(current_directory, file_name)
df_final.to_csv(full_path)
