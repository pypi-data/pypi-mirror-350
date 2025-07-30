# 🏛️ ANBIMA public data for Brazilian fixed income


[![PyPI version](https://img.shields.io/pypi/v/anbima-data.svg)](https://pypi.org/project/anbima-data/)
[![Build Status](https://github.com/seu-usuario/anbima-data/actions/workflows/python-package.yml/badge.svg)](https://github.com/seu-usuario/anbima-data/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Provides Python functions to retrieve public data from ANBIMA related to the Brazilian fixed income market. The package offers streamlined access to:**

- Historical and current performance of IMA indices.
- Portfolio compositions.
- The term structure of Brazilian interest rates and the implied inflation calculated by ANBIMA.
- Historical and projected values of IGP-M and IPCA inflation indices.
- The last five daily prices of Brazilian federal government bonds traded in the secondary market.
---
## 📋 Features

- **Inflation Index Projections**: Retrieve historical and consensus-based monthly projections for IGP-M and IPCA inflation indices (`get_macro_index_projections`).
- **Federal Bonds Data**: Access recent prices, reference rates, and intraday price ranges of Brazilian federal government bonds traded in the secondary market (`get_federal_bonds`).
- **Yield Curve**: Obtain the term structure of Brazilian interest rates with options for tabular or graphical output (`get_yield_curve`).
- **Daily Portfolio Performance**: Fetch daily market value-based performance data for IMA family fixed income indices (`get_daily_portfolio_performance`).
- **Portfolio Composition**: Retrieve current portfolio breakdowns for ANBIMA fixed income indices (`get_portfolio_composition`).
- **Index Performance Time Series**: Access historical time series data of ANBIMA fixed income indices with customizable output formats including graphs (`get_index_performance`).
- 
---
## ⚙️ How it works

### 🔧 Installation

Install the `anbima-data` package using one of the following options:

#### • PyPI (recommended)
```bash
pip install anbima-data
````
#### • Directly from GitHub
```bash
pip install git+https://github.com/seu-usuario/anbima-data.git
```

#### • Clone and install manually
```bash
git clone https://github.com/seu-usuario/anbima-data.git
cd anbima-data
pip install .
```

### 💡 Example of Usage

Below are examples demonstrating how to use the main functions provided by the package.


#### 1. 📈 Inflation Index Projections
```python
# 📥 Input
import anbima_data as anb

df_igpm_proj = anb.get_macro_index_projections(index="IGP-M", table="projecao_mes")

print(df_igpm_proj)
```
```python
# 📤 Output

Example:
1  Mês de Coleta       Data  Projeção (%) Data de Validade*
0  Abril de 2025 2025-04-29          0.29        2025-05-05
1   Maio de 2025 2025-05-12          0.14        2025-05-13
2   Maio de 2025 2025-05-20         -0.22        2025-05-21
```

#### 2. 💵 Federal Bonds Data
```python
# 📥 Input
import anbima_data as anb

df_bond = anb.get_federal_bonds(bond="ntn-b", output="dataframe")
print(df_bond)
```
```python
# 📤 Output
<DataFrame resumido — apenas algumas colunas e linhas>

Example:
Código SELIC Data Base/Emissão Data de Vencimento  Tx. Compra  Tx. Venda  \
0        760199        2000-07-15         2026-08-15      9.1260     9.0885   
1        760199        2000-07-15         2027-05-15      8.0595     8.0241   
2        760199        2000-07-15         2028-08-15      7.6046     7.5700   
3        760199        2000-07-15         2029-05-15      7.4005     7.3669   
4        760199        2000-07-15         2030-08-15      7.3901     7.3601   
..          ...               ...                ...         ...        ...   
```

#### 3. 📉 Yield Curve
When the output parameter is set to 'dataframe':
```python
# 📥 Input
import anbima_data as anb

df_yield = anb.get_yield_curve(output="dataframe")
print(df_yield)
```
```python
# 📤 Output
Example:
           ETTJ_IPCA  ETTJ_Prefixados  Inflação_implícita
Vértices                                                
252          9.5662          14.4570              4.4637
378          8.6342          14.0535              4.9885
504          8.1623          13.7907              5.2036
630          7.8871          13.6674              5.3577
756          7.7103          13.6422              5.5072
...             ...              ...                 ... 
```
When the output parameter is set to 'chart':
```python
# 📥 Input
import anbima_data as anb

df_yield = anb.get_yield_curve(output="chart", column_name = "ETTJ_IPCA")
print(df_yield)
```
#### 📤 Output
![Output gráfico do get_index_performance](images/plot_curve.png)

#### 4. 📊 Daily Portfolio Performance
```python
# 📥 Input
import anbima_data as anb

df_daily = anb.get_daily_portfolio_performance(index="ima-geral")
print(df_daily)
```
```python
# 📤 Output
Example:
Data Referência Referência Títulos Vencimento Código SELIC   Código ISIN  \
0       2025-05-23      TOTAL     LTN 2025-07-01       100000  BRSTNCLTN7Z6   
1       2025-05-23      TOTAL     LFT 2025-09-01       210100  BRSTNCLF1RD2   
2       2025-05-23      TOTAL     LTN 2025-10-01       100000  BRSTNCLTN863   
3       2025-05-23      TOTAL     LTN 2026-01-01       100000  BRSTNCLTN7U7   
4       2025-05-23      TOTAL     LFT 2026-03-01       210100  BRSTNCLF1RE0   
...             ...              ...                 ... 
```

#### 5. 🧾 Portfolio Composition
```python
# 📥 Input
import anbima_data as anb

df_portfolio = anb.get_portfolio_composition(index="IMA-GERAL")
print(df_portfolio)
```
```python
# 📤 Output
Example:
data_inicio   data_fim     indice       tipo_titulo peso_indice  data_vencimento
0   2025-05-05 2025-05-15  IMA-GERAL         LFT         7.14      2027-03-01
1   2025-05-05 2025-05-15  IMA-GERAL         LFT         7.00      2027-03-01
2   2025-05-05 2025-05-15  IMA-GERAL         LFT         6.09      2027-09-01
3   2025-05-05 2025-05-15  IMA-GERAL         LFT         5.98      2027-09-01
4   2025-05-05 2025-05-15  IMA-GERAL         LFT         4.61      2029-03-01
..         ...        ...        ...         ...          ...             ...
```

#### 6. 📆 Index Performance Time Series (get_index_performance)
When the output parameter is set to 'dataframe': 
```python
# 📥 Input
import anbima_data as anb

df_performance = anb.get_index_performance(
    index="IMA-GERAL",
    start_date="01/01/2024",
    end_date="31/01/2024",
    output="dataframe"
)
print(df_performance)
```
```python
# 📤 Output
Example:
               variacao_diaria  variacao_mensal  numero_indice  variacao_ult12m  \
2024-05-06            -0.08             0.29        8085.72            10.71   
2024-05-07             0.11             0.40        8094.56            10.83   
2024-05-08            -0.00             0.40        8094.29            10.85   
2024-05-09             0.07             0.47        8100.00            10.96   
2024-05-10            -0.03             0.44        8097.37            10.75   
...                     ...              ...            ...              ...     
```
When the output parameter is set to 'chart':
```python
# 📥 Input
import anbima_data as anb

df_performance_graph = anb.get_index_performance(
    index = "IMA-GERAL"
    start_date = "06/05/2024" 
    end_date = "23/05/2025"
    output="graph",
    column_name = "variacao_ult12m"
)
print(df_performance_graph)
```

#### 📤 Output
![Output gráfico do get_index_performance](images/output.png)


---
## 🧭 Disclaimer & Purpose

The purpose of the `anbima-data` package is purely educational, academic, and informative. It was created to facilitate access to reliable and publicly available financial data for students, researchers, investors, and the general public.

This package does **not**:
- Perform financial analysis or forecasting;
- Provide investment advice;
- Guarantee the accuracy or completeness of the data;
- Sell any services or financial products.

**All decisions based on the data retrieved using this package are the sole responsibility of the user.** Always consult a licensed professional for financial advice.

This package is open-source, free to use, and does not include any monetization or commercial intent.

## 🧭 Aviso Legal e Propósito

O pacote `anbima-data` tem caráter puramente educacional, acadêmico e informativo. Foi criado para facilitar o acesso a dados financeiros confiáveis e de domínio público por estudantes, pesquisadores, investidores e o público em geral.

Este pacote **não**:
- Realiza análises ou previsões financeiras;
- Oferece recomendações de investimento;
- Garante a precisão ou completude dos dados;
- Comercializa serviços ou produtos financeiros.

**Todas as decisões baseadas nos dados obtidos com este pacote são de responsabilidade exclusiva do usuário.** Sempre consulte profissionais licenciados para orientações financeiras.

Este pacote é open-source, gratuito e não possui fins comerciais ou de monetização.

---
## ⚠️ Aviso sobre os dados públicos utilizados

Este pacote faz uso de dados públicos provenientes de fonte oficial da ANBIMA (fonte: https://www.anbima.com.br/pt_br/pagina-inicial.htm#).

Embora o código esteja licenciado sob os termos da licença MIT e seja de uso livre, **os dados acessados podem estar sujeitos a restrições específicas de uso**, como proibição de revenda ou redistribuição para fins comerciais.

Recomenda-se consultar os termos de uso das fontes originais antes de utilizar os dados para finalidades além de estudos, projetos acadêmicos ou uso pessoal.

O autor deste pacote não se responsabiliza por qualquer uso inadequado ou indevido das informações acessadas.

## ⚠️ Notice About Public Data

This package uses publicly available financial data from official sources of ANBIMA (source: https://www.anbima.com.br/pt_br/pagina-inicial.htm#).

While the source code is licensed under the MIT License and is free to use, **the data itself may be subject to specific usage restrictions**, including limitations on resale or commercial redistribution.

Users are encouraged to review the original providers’ terms of use before using the data for purposes beyond personal, academic, or research use.

The author assumes no responsibility for any improper or unauthorized use of the retrieved data.

