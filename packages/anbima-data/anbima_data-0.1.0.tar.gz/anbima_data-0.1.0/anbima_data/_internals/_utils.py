import re
import requests
import pandas as pd
import plotly.graph_objects as go
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from datetime import date
import requests
import numpy as np
import xml.etree.ElementTree as ET

def _request_anbima(url, params=None):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "pt-BR,pt;q=0.7",
        "adrum": "isAjax:true",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.anbima.com.br/pt_br/informar/precos-e-indices/indices/ima.htm",
        "sec-ch-ua": '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    cookies = {
        "lumClientId": "8A2AB28B943B830F01943D8362043AF8",
        "lumUserName": "Guest",
        "lumIsLoggedUser": "false",
        "lumUserLocale": "pt_BR",
        "JSESSIONID": "33DE36A2E7432FE9AEC8B01D5657C6D5.LumisProdB",
        "lumUserSessionId": "a5aSc9Zp32u9BWYUPdnVOyW70IfjU3_v"
    }

    response = requests.get(url, params=params, headers=headers, cookies=cookies)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro na requisição: {response.status_code}")

def _request_ettj():
        
    url = "https://www.anbima.com.br/informacoes/est-termo/CZ-down.asp"
    
    
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "pt-BR,pt;q=0.8",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.anbima.com.br",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.anbima.com.br/informacoes/est-termo/CZ.asp",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Brave";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "iframe",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    }
    
    cookies = {
        "lumClientId": "8A2AB28B943B830F01943D8362043AF8",
        "lumMonUid": "XE7XyMCepsHi5VH2PkfBngimGVFp9tvu",
        "lumMonUid": "ySF-cJJTZT7FQjJOp8gQG4sRwEdGFch2",
        "ASPSESSIONIDSCCRSSDS": "HBPDIFCDOCJJPCNHMNJFNCKK"
    }
    
    data = {
        "Idioma": "PT",
        "Dt_Ref": "",
        "saida": "xml",  
    }
    
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    
    if response.status_code == 200:
    
        tree = ET.ElementTree(ET.fromstring(response.text))
        root = tree.getroot()
        return root

    else:
        raise Exception(f"Erro na requisição: {response.status_code}")

def _request_bonds(bond, date):
    
    session = requests.Session()
    
    initial_url = f"https://www.anbima.com.br/informacoes/merc-sec/resultados/msec_{date}_{bond}.asp"
    session.get(initial_url)
    
    
    target_url = initial_url
    
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "pt-BR,pt;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": initial_url,
        "sec-ch-ua": '"Brave";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "iframe",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }
    
    # Agora, acessamos a página desejada com cookies válidos já armazenados
    response = session.get(target_url, headers=headers)
    
    if response.ok:
        return response.text
    else:
        print(f"Erro: {response.status_code}")

def _extrair_dataframes():
    url = "https://www.anbima.com.br/pt_br/informar/estatisticas/precos-e-indices/projecao-de-inflacao-gp-m.htm"
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0"}
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    content_area = soup.find("main")  # área principal da página
    elementos = content_area.find_all(["p", "table"])

    dataframes = []

    for el in elementos:
        if el.name == "table":
            linhas_html = el.find_all("tr")
            linhas = []
            for linha_html in linhas_html:
                celulas = linha_html.find_all(["td", "th"])
                texto_linha = [celula.get_text(strip=True) for celula in celulas]
                if texto_linha:
                    linhas.append(texto_linha)

            if not linhas or len(linhas) < 2:
                continue

            texto_tabela = " ".join([" ".join(l) for l in linhas]).lower()
            
            df = pd.DataFrame(linhas)
            df.columns = df.iloc[1]  # Assume segunda linha como cabeçalho
            df = df.drop(index=[0, 1]).reset_index(drop=True)

           
            dataframes.append(df)

    return dataframes

def _get_previous_weekday():
    """
    Calculates the previous weekday date relative to the current date.
    If the previous day is a weekend or Monday, returns the date of the previous Friday.

    Returns:
        datetime: The date of the previous weekday.
    """
    today = datetime.now()
    previous_day = today

    if previous_day.weekday() >= 5 or previous_day.weekday() == 0:
        days_to_friday = (previous_day.weekday() - 4) % 7
        previous_day -= timedelta(days=days_to_friday)

    return previous_day

def _request_ima_daily_portfolio(index):
    """
    Realiza uma requisição POST para o site da Anbima carteira diária IMA,
    simulando o comportamento do curl fornecido.
    
    Retorna:
        response.text: Conteúdo HTML da resposta, caso o status seja 200.
    
    Lança:
        Exception: Se o status da resposta não for 200.
    """
    url = "https://www.anbima.com.br/informacoes/ima/ima-carteira.asp"

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "pt-BR,pt;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.anbima.com.br",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.anbima.com.br/informacoes/ima/ima-carteira.asp",
        "sec-ch-ua": '"Chromium";v="136", "Brave";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    }

    cookies = {
        "lumClientId": "8A2AB28B943B830F01943D8362043AF8",
        "lumMonUid": "bTV9-GeEL3vNG2suEF0rOOePbgPDUBWF",
        "lumUserLocale": "pt_BR",
        "JSESSIONID": "FA14D4DF712A4F8A87566CB88F431A7A.LumisProdB",
        "lumUserSessionId": "1LUgGnvA0FCkw64fZbHStriw5zOJ_6J0",
        "lumUserName": "Guest",
        "lumIsLoggedUser": "false",
        "ASPSESSIONIDQQRBTTQQ": "PLLPKEGAIOKKHHGKHLHPHJPK"
    }

    previous_day = _get_previous_weekday()
    data_ref = previous_day.strftime('%d%m%Y')
    index = index.lower()

    data = {
        "Tipo": "0",
        "Indice": index,
        "DataRef": data_ref,
        "Pai": "ima_carteira",
        "Consulta": "Carteira",
        "Info1": "true",
        "Info2": "",
        "Info3": "true",
        "Info4": "true",
        "Info5": "true",
        "Info6": "true",
        "Info7": "true",
        "Info8": "true",
        "Info9": "true",
        "Info10": "",
        "Info11": "true",
        "Info12": "true",
        "Info13": "true",
        "Info14": "true",
        "Info15": "true",
        "Info16": "true",
        "Info17": "true",
        "Info18": "true",
        "Info19": "true",
        "Info20": "true",
        "Info21": "",
        "Info22": "true",
        "Info23": "true",
        "Info24": "true",
        "Info25": "true",
        "Info26": "true",
        "Info27": "true",
        "Info28": "true",
        "Info29": "true",
        "Info30": "true",
        "Info31": "true",
        "Info32": "true",
        "Info33": "true",
        "Info34": "true",
        "Info35": "true",
        "Info36": "true",
        "Info37": "true",
        "Info38": "true",
        "Info39": "true",
    }

    response = requests.post(url, headers=headers, cookies=cookies, data=data)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Erro na requisição: {response.status_code}")
    
def _dias_uteis_anteriores(n_dias=5, data_base=None, feriados=None):
    """
    Retorna uma lista com os n_dias úteis anteriores à data_base -1D,
    considerando feriados e finais de semana.

    Parâmetros:
    - n_dias (int): quantidade de dias úteis a retornar.
    - data_base (date): data de referência (padrão: hoje).
    - feriados (list[date]): lista de feriados a considerar.
    """
    if data_base is None:
        data_base = datetime.today().date()
    
    if feriados is None:
        feriados = []

    data_ref = data_base - timedelta(days=1)

    while data_ref.weekday() >= 5 or data_ref in feriados:
        data_ref -= timedelta(days=1)

    dias_uteis = []
    while len(dias_uteis) < n_dias:
        if data_ref.weekday() < 5 and data_ref not in feriados:
            dias_uteis.append(data_ref)
        data_ref -= timedelta(days=1)

    return dias_uteis[::-1]

def _format_date_request(date):
    meses_abreviados = {
    1: 'jan', 2: 'fev', 3: 'mar', 4: 'abr',
    5: 'mai', 6: 'jun', 7: 'jul', 8: 'ago',
    9: 'set', 10: 'out', 11: 'nov', 12: 'dez'}
    return f"{date.day:02d}{meses_abreviados[date.month]}{date.year}" 

def _validate_param(index: str, dic: set):
    if index not in dic:
        raise ValueError(f"Invalid param: '{index}'. Use um dos seguintes: {', '.join(dic)}")
    
def _parse_index_data(data, index):        
    date = data['datas']
    
    for key in data[index].keys():
        data[index][key] = [item.replace(',', '.') for item in data[index][key]]
        
        
    df = pd.DataFrame(data[index], index = date)
    df.index = pd.to_datetime(df.index, format='%d/%m/%Y')
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def _parse_portfolio(index,params=None):
    url = "https://www.anbima.com.br/pt_br/anbima/jsoncarteira/acionar"    
    data = _request_anbima(url)
    df =_parse_data_portfolio(data)
    carteira = df[df['indice'] == index]  
    carteira = carteira.sort_values(by="peso_indice", ascending=False)
    return carteira

def _parse_data_portfolio(data):
    
    processed_data = []
    
    for item in data:
        if item is None:
            continue  # Ignora os itens None
        indice = item['indice']
        for ref in item['referencias']:
            processed_data.append({
                'data_inicio': item['data_inicio'],
                'data_fim': item['data_fim'],
                'indice': indice,
                'tipo_titulo': ref['tipo_titulo'],
                'peso_indice': ref['peso_indice'].replace(',', '.'),  # Substitui vírgula por ponto
                'data_vencimento': ref['data_vencimento']
            })
   
    # Criando o DataFrame
    df = pd.DataFrame(processed_data)
    df["data_inicio"] = pd.to_datetime(df["data_inicio"], format='%d/%m/%Y')
    df["data_fim"] = pd.to_datetime(df["data_fim"], format='%d/%m/%Y')
    df["data_vencimento"] = pd.to_datetime(df["data_vencimento"], format='%d/%m/%Y')
    df["peso_indice"] = pd.to_numeric(df["peso_indice"], errors='coerce')
    return df

def _parse_ettj(root):
    # Extraindo dados da tag <ETTJ>
    vertices = []
    for vertice in root.findall('.//VERTICES'):
        vertice_value = vertice.get('Vertice')
        ipca = vertice.get('IPCA')
        prefixados = vertice.get('Prefixados')
        inflacao = vertice.get('Inflacao')
        vertices.append([vertice_value, ipca, prefixados, inflacao])

    # Criando um DataFrame para os dados dos VERTICES
    df = pd.DataFrame(vertices, columns=['Vértices', 'ETTJ_IPCA', 'ETTJ_Prefixados', 'Inflação_implícita'])
    df = df.set_index('Vértices')

    for column in df.columns:
            # Se a coluna for do tipo string, substituímos as vírgulas por pontos
            if df[column].dtype == 'object':
                df[column] = df[column].str.replace(',', '.', regex=False)
            
            # Convertendo para valores numéricos (float ou int) onde for possível
            df[column] = pd.to_numeric(df[column], errors='coerce')
    
    return df

def _parse_bonds(response, date):
    html = response #response.content.decode("latin1")
    soup = BeautifulSoup(html, "html.parser")
    
    tables = soup.find_all('table')
    rows = tables[2].find_all("tr")
    
    codigo_selic = []
    data_inicio = []
    data_fim = [] 
    tx_compra = []
    tx_venda = []
    tx_indicativas = []
    pu = []
    min_d0 = []
    max_d0 = []
    min_d1 = []
    max_d1 = []
    
    for row in rows:
        dates = row.find_all(string = re.compile(r"\b\d{2}/\d{2}/\d{4}\b"))
        cod_selic = row.find_all(string=re.compile(r"\b\d{6}\b"))
        codigo_selic.append(cod_selic[0])
        values = row.find_all(string=re.compile(r"\b-?\d+,\d+\b"))
        data_inicio.append(str(dates[0]))
        data_fim.append(str(dates[1]))
        tx_compra.append(values[0])
        tx_venda.append(values[1])
        tx_indicativas.append(values[2])
        pu.append(values[3])
        min_d0.append(values[4])
        max_d0.append(values[5])
        min_d1.append(values[6])
        max_d1.append(values[7])
    
    # Criando o DataFrame
    dic = {
        "Código SELIC": codigo_selic,
        "Data Base/Emissão": data_inicio,
        "Data de Vencimento": data_fim,
        "Tx. Compra": tx_compra,
        "Tx. Venda": tx_venda,
        "Tx. Indicativas": tx_indicativas,
        "PU": pu,
        "Mínimo (D0)": min_d0,
        "Máximo (D0)": max_d0,
        "Mínimo (D+1)": min_d1,
        "Máximo (D+1)": max_d1
    }
    
    df = pd.DataFrame(dic)
    
    
    df["Data Base/Emissão"] = pd.to_datetime(df["Data Base/Emissão"], format='%d/%m/%Y')
    df["Data de Vencimento"] = pd.to_datetime(df["Data de Vencimento"], format='%d/%m/%Y')
    df["Data de referência"] = date
    
    colunas_float = [
        "Tx. Compra", "Tx. Venda", "Tx. Indicativas",
        "Mínimo (D0)", "Máximo (D0)", "Mínimo (D+1)", "Máximo (D+1)"
    ]
    
    for col in colunas_float:
        df[col] = df[col].str.replace(",", ".").astype(float)
    
    df["PU"] = (
        df["PU"]
        .str.replace(".", "", regex=False)     # remove separador de milhar
        .str.replace(",", ".", regex=False)    # substitui vírgula por ponto
        .astype(float)
    )
    
    df = df.drop_duplicates().reset_index(drop=True)
    
    return df

def _parse_tabela_historico(df):
    df = df.copy()
    df.replace("None", np.nan, inplace=True)
    
    
    
    # Vamos encontrar as linhas onde as colunas -1 e -2 são NaN
    mask = df.iloc[:, -1].isna() & df.iloc[:, -2].isna()
    
    # Para cada linha que atende a condição, vamos deslocar os valores das colunas 0,1,2 para frente
    for idx in df[mask].index:
        df.iloc[idx, 1:4] = df.iloc[idx, 0:3].values
        df.iloc[idx, 0] = np.nan
    
    # Para cada linha, se a coluna 0 for NaN, pegamos o valor da linha anterior
    for i in range(1, len(df)):
        if pd.isna(df.iloc[i, 0]):
            df.iloc[i, 0] = df.iloc[i - 1, 0]
    
    # Corrigindo os valores faltantes (None ou NaN) com o valor anterior
    for i in range(1, len(df)):
        if pd.isna(df.iloc[i, -1]):
            df.iloc[i, -1] = df.iloc[i - 1, -1]
      
    return df 

def _format_date_number(df):
    for col in df.columns:
        amostra = df[col].dropna().astype(str).head(5)

        # Verifica se todos os valores da amostra parecem datas brasileiras
        if amostra.str.match(r"\d{2}/\d{2}/\d{2,4}").all():
            try:
                df[col] = pd.to_datetime(df[col], format="%d/%m/%y", errors='coerce')
                if df[col].isna().all():
                    df[col] = pd.to_datetime(df[col], format="%d/%m/%y", errors='coerce')
            except:
                pass  # Se falhar, mantém como está

        # Verifica se todos os valores parecem números com vírgula
        elif amostra.str.match(r"^-?\d+,\d+$").all():
            try:
                df[col] = df[col].str.replace(',', '.', regex=False).astype(float)
            except:
                pass  # Se falhar, mantém como está

    return df

def _parse_ima_daily_portfolio(response):    
    
    soup = BeautifulSoup(response, 'html.parser')
    
    tbody = soup.find('tbody')

    dados = []
    
    
    for linha in tbody.find_all('tr'):
        colunas = linha.find_all('td')
        valores = [col.text.strip() for col in colunas if col.text.strip()]
        if valores:
            dados.append(valores)
    
    
    colunas = [
        "Data Referência", "Referência", "Títulos", "Vencimento", "Código SELIC",
        "Código ISIN", "Taxa Indicativa", "PU", "PU Juros (R$)", "Quantidade (mil)",
        "Quantidade Teórica", "Carteira a Mercado (R$ mil)", "Peso (%)", "Prazo (d.u.)",
        "Duration (d.u.)", "Nº Operações", "Quant. Negociada (1000 títulos", "Valor Negociado (R$ mil)",
        "PMR", "Convexidade"
    ]
    
    df = pd.DataFrame(dados, columns=colunas)
    columns_numbers = ["Taxa Indicativa", "PU", "PU Juros (R$)", "Quantidade (mil)",
        "Quantidade Teórica", "Carteira a Mercado (R$ mil)", "Peso (%)", "Prazo (d.u.)",
        "Duration (d.u.)", "Nº Operações", "Quant. Negociada (1000 títulos", "Valor Negociado (R$ mil)",
        "PMR", "Convexidade"]
    for column in columns_numbers:
        df[column] = df[column].str.replace(',', '.', regex=False)
        df[column] = pd.to_numeric(df[column], errors='coerce')

    columns_date = ["Data Referência", "Vencimento"]
    for column in columns_date:
        df[column] = pd.to_datetime(df[column], format='%d/%m/%Y')
    
    return df

def _graphone(df, column_name, index=""):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[column_name],
        mode='lines+markers',
        name=column_name,
        line=dict(color='#78BE20', width=2),  # Verde ANBIMA
        hovertemplate='%{x} dias<br>%{y:.2f}'
    ))

    fig.update_layout(
        title=dict(
            text=f"{index} - {column_name}",
            font=dict(family="Arial", size=25, color="#231F20", weight="bold"),  # Texto escuro ANBIMA
            x=0.0,
            xanchor="left",
            xref="paper"
        ),
        xaxis_title="",
        yaxis_title="",
        height=500,
        width=1000,
        plot_bgcolor="#FFFFFF",   # Fundo branco ANBIMA
        paper_bgcolor="#FFFFFF",  # Fundo branco ANBIMA

        font=dict(family="Arial", size=13, color="#231F20"),  # Texto escuro

        hovermode="closest",

        xaxis=dict(
            showline=False,
            showgrid=True,
            gridcolor="#e0e0e0",
            gridwidth=0.5,
            ticks="",
            showticklabels=True,
            tickfont=dict(family="Arial", size=12, color="#231F20"),  # Texto escuro
            ticklabelposition="outside top",
            automargin=True,
            showspikes=True,
            spikemode="toaxis",
            spikesnap="cursor",
            spikethickness=1,
            spikedash="dot",
            spikecolor="#999"
        ),
        yaxis=dict(
            showline=False,
            showgrid=True,
            gridcolor="#e0e0e0",
            gridwidth=0.5,
            ticks="",
            showticklabels=True,
            tickfont=dict(family="Arial", size=12, color="#231F20"),  # Texto escuro
            ticklabelposition="outside right",
            automargin=True,
            showspikes=True,
            spikemode="toaxis",
            spikesnap="cursor",
            spikethickness=1,
            spikedash="dot",
            spikecolor="#999"
        ),

        hoverlabel=dict(
            bgcolor="#333",
            bordercolor="rgba(0,0,0,0)",
            font_size=12,
            font_family="Arial",
            font_color="#FFFFFF"
        )
    )

    return fig.show()
