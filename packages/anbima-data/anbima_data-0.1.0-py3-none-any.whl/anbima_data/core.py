from ._internals._utils import (
    _request_anbima,
    _request_ettj,
    _request_bonds,
    _request_ima_daily_portfolio,
    _dias_uteis_anteriores,
    _format_date_request,
    _validate_param,
    _parse_index_data,
    _parse_portfolio,
    _parse_ettj,
    _parse_bonds,
    _parse_ima_daily_portfolio,
    _extrair_dataframes,
    _parse_tabela_historico,
    _format_date_number,
    _get_previous_weekday,
    _graphone
)
import pandas as pd
from datetime import datetime
import requests

def get_index_performance(index: str, start_date: str, end_date:str, output:str = 'dataframe', column_name: str = None):

    """
    Retrieves performance data for ANBIMA market indices and returns it as a DataFrame or a graph.
    Data available from 06/01/2017 onwards.

    Parameters:
        - index (str): Name of the ANBIMA index to query. Examples include:
          "IRF-M P2", "IMA-GERAL-EX-C", "IMA-GERAL", "IRF-M 1", "IMA-S", "IMA-B 5",
          "IRF-M", "IRF-M 1+", "IMA-B", "IMA-C", "IMA-B 5+", "IMA-B 5 P2".
        - start_date (str): Start date for index performance query in 'DD/MM/YYYY' format.
        - end_date (str): End date for index performance query in 'DD/MM/YYYY' format.
        - output (str, optional): Defines the desired output type:
            - 'dataframe' (default): returns or displays the DataFrame with data.
            - 'graph': displays a graph for the specified `column_name`.
            - None: only displays the DataFrame.
        - column_name (str, optional): Column name from the DataFrame to use in the graph (required if `output` is 'graph').
          Valid columns:
            - variacao_diaria: Daily percentage variation of the index compared to the previous day.
            - variacao_mensal: Accumulated variation of the index in the current month.
            - numero_indice: Current numerical value of the index.
            - variacao_ult12m: Percentage variation accumulated over the last 12 months.
            - variacao_anual: Accumulated variation in the year (from the beginning of the year to the current date).
            - variacao_ult24: Percentage variation accumulated over the last 24 months.
    
    """
   
    indexes = {
            "IRF-M P2", "IMA-GERAL-EX-C", "IMA-GERAL", "IRF-M 1", "IMA-S", "IMA-B 5",
            "IRF-M", "IRF-M 1+", "IMA-B", "IMA-C", "IMA-B 5+", "IMA-B 5 P2"
    }
    
    try:
        _validate_param(index, indexes)
        
        url = "https://www.anbima.com.br/pt_br/anbima/jsonima/acionar"
        params = {'dataInicio': start_date,'dataFim': end_date}
        data = _request_anbima(url, params=params)
        df = _parse_index_data(data, index)
            
        if output is None or output == 'dataframe':
            return df
                
        elif output == 'graph' and column_name:
            if column_name not in df.columns:
                print( ValueError(f"A coluna '{column_name}' não existe no DataFrame."))
            
            graphone = _graphone(df, column_name,index)   
            print(graphone)
                    
        
    except ValueError as e:
        print(str(e)) 

def get_portfolio_composition(index):

    """
   Retrieves the current portfolio composition of the selected ANBIMA index.

    Parameters:
        - index (str): Name of the ANBIMA index to query.
          Examples: "IRF-M P2", "IMA-GERAL-EX-C", "IMA-GERAL", "IRF-M 1", "IMA-S", "IMA-B 5",
          "IRF-M", "IRF-M 1+", "IMA-B", "IMA-C", "IMA-B 5+", "IMA-B 5 P2".

    """
   
    indexes = {
            "IRF-M P2", "IMA-GERAL-EX-C", "IMA-GERAL", "IRF-M 1", "IMA-S", "IMA-B 5",
            "IRF-M", "IRF-M 1+", "IMA-B", "IMA-C", "IMA-B 5+", "IMA-B 5 P2"
    }
    
    try:
        _validate_param(index, indexes)
        df =  _parse_portfolio(index)
        df = df.reset_index(drop=True)
        return df
                
    except ValueError as e:
        print(str(e)) 

def get_daily_portfolio_performance(index):

    """
    Daily results for the IMA family of indices (ANBIMA Market Indices),
    calculated based on the market value evolution of portfolios composed of
    fixed-rate government bonds, SELIC-linked bonds (LFT), IPCA-linked bonds (NTN-B),
    and IGP-M-linked bonds (NTN-C).

    Parameters:
        - index (str): Code of the desired IMA index (e.g. "irf-m 1", "irf-m 1+", "ima-b", "ima-b 5",
          "ima-b 5+", "ima-c", "ima-s", "ima-geral", "ima-geral ex-c").

    Returns:
        pandas.DataFrame: Structured table with the daily data of the requested index.

                          
    """

    index = index.lower()
    
    indexes = [
        "irf-m",
        "irf-m 1",
        "irf-m 1+",
        "ima-b",
        "ima-b 5",
        "ima-b 5+",
        "ima-c",
        "ima-s",
        "ima-geral",
        "ima-geral ex-c"
    ]

    try:
        _validate_param(index, indexes)
        response = _request_ima_daily_portfolio(index)
        df = _parse_ima_daily_portfolio(response)

        return df
                
    except ValueError as e:
        print(str(e)) 

def get_yield_curve(output: str = 'dataframe', column_name: str = None):
    """
    Function to retrieve yield data curve.

    Parameters:
        - output (str): Desired output type ('dataframe' or 'graph'). Default is 'dataframe'.
        - column_name (str): Column name for the graph (required if 'graph' is selected).

    Returns:
        DataFrame with data or a graph.
    """
    
    try:
        root = _request_ettj()  
        df = _parse_ettj(root)  

       
        if output == 'dataframe':
            return df

        elif output == 'graph':
            if column_name is None:
                raise ValueError("Você deve fornecer o nome da coluna para o gráfico.")
            
            if column_name not in df.columns:
                raise ValueError(f"A coluna '{column_name}' não existe no DataFrame.")

            if column_name in ["Prefixados","Inflacao"]:
                df = df.dropna()
                           
            # Gera o gráfico e o retorna
            index = "CURVA ZERO CUPOM"
            graphone = _graphone(df, column_name, index)   
            return graphone

        else:
            raise ValueError(f"Output desconhecido: {output}. Use 'dataframe' ou 'graph'.")
    
    except ValueError as e:
        # Captura qualquer erro de valor e exibe uma mensagem amigável
        print(f"Erro: {str(e)}")
    except Exception as e:
        # Captura quaisquer outros erros e exibe uma mensagem genérica
        print(f"Ocorreu um erro: {str(e)}")

def get_federal_bonds(bond:str, output: str = 'dataframe', column_name: str = None, bond_date:str = None):
    """
    ollects reference rates and unit prices of federal public bonds
    disclosed by ANBIMA for the secondary market.

    Returns data for the last 5 business days, including indicative ranges
    of intraday price fluctuations.

    Parameters:
        - bond (str): Name of the bond, e.g., "lft", "ltn", "ntn-c", "ntn-b", "ntn-f".
        - output (str): Desired output type ('dataframe' or 'graph'). Default is 'dataframe'.
        - column_name (str): Column name for the graph (required if 'graph' is selected).
          Available columns in the DataFrame: "Tx. Compra", "Tx. Venda", "Tx. Indicativas",
          "PU", "Mínimo (D0)", "Máximo (D0)", "Mínimo (D+1)", "Máximo (D+1)".
        - bond_date (str): Bond maturity date (see "Data de Vencimento" column),
          format 'yyyy-mm-dd', e.g., '2031-01-01' (required if 'graph' is selected).

    Returns:
        DataFrame or graph of the selected bond data.
  
    """
    bond = bond.lower()
    bonds = ["lft", "ltn", "ntn-c", "ntn-b", "ntn-f"]
    _validate_param(bond, bonds)

    try:
        feriados_b3_2025 = ['01/01/2025', '03/03/2025', '04/03/2025', '18/04/2025', '21/04/2025',
                            '01/05/2025', '19/06/2025', '20/11/2025', '24/12/2025', '25/12/2025', '31/12/2025']
        feriados_b3_2025 = [datetime.strptime(d, "%d/%m/%Y").date() for d in feriados_b3_2025]
        dates = _dias_uteis_anteriores(n_dias=6, feriados=feriados_b3_2025)
        
        dfs = []
        print("Consultando os valores referentes aos últimos cinco dias úteis de negociação...")
        print('-------------------------------------------------------')

        for index, date in enumerate(dates, start=1):
    
            print(f"Downloading date {date} and processing files: ({index}/{len(dates)})")
    
            date_to_request = _format_date_request(date)
            response = _request_bonds(bond, date_to_request)
            df = _parse_bonds(response, date)
   
            dfs.append(df)
    
            print('-------------------------------------------------------')
    
        df_bonds = pd.concat(dfs, ignore_index=True)


        # Se o output for dataframe, apenas retorna o DataFrame
        if output == 'dataframe':
            return df_bonds

        # Se o output for graph, gera o gráfico
        elif output == 'graph':
            columns_df = ["Tx. Compra", "Tx. Venda", "Tx. Indicativas", "PU", "Mínimo (D0)", "Máximo (D0)", "Mínimo (D+1)", "Máximo (D+1)"]
            if (column_name is None) or (bond_date is None):
                raise ValueError(
                    f"Para o modo 'graph', é necessário fornecer os parâmetros:\n"
                    f"  - 'column_name': selecionar uma das colunas {columns_df}\n"
                    f"  - 'bond_date': selecionar uma data na coluna 'Data de Vencimento' do título."
                )

         
            if column_name not in columns_df:
                raise ValueError(f"A coluna '{column_name}' não existe no DataFrame.")
              
            # Gera o gráfico e o retorna
            #bond_date = pd.to_datetime(bond_date).date()
            df = df_bonds[df_bonds["Data de Vencimento"] == bond_date]
            df = df.set_index("Data de referência")

            index = bond.upper()
            graph_bond = _graphone(df, column_name, index)

            return graph_bond

        else:
            raise ValueError(f"Output desconhecido: {output}. Use 'dataframe' ou 'graph'.")
    
    except ValueError as e:
        # Captura qualquer erro de valor e exibe uma mensagem amigável
        print(f"Erro: {str(e)}")
    except Exception as e:
        # Captura quaisquer outros erros e exibe uma mensagem genérica
        print(f"Ocorreu um erro: {str(e)}")

def get_macro_index_projections(index:str, table:str):
    """
    Fetches inflation index projection or historical data for IGP-M and IPCA indices.
    Provides projections for both index based on the consensus 
    from the Anbima Permanent Macroeconomic Advisory Group.

    Parameters:
        - index (str): The inflation index to query. Accepted values are "IGP-M" and "IPCA".
        - table (str): The type of table to return. Options:
                     - "projecao_mes": Monthly projections
                     - "projecao_posterior": Projections for subsequent month
                     - "historico": Historical series data

    Returns:
        pandas.DataFrame: A cleaned and formatted DataFrame containing the requested data.

    """
    index = index.upper()
    table = table.lower()
    indexes = ["IGP-M", "IPCA"]
    tables = ["projecao_mes","projecao_posterior","historico"]

    try:
        _validate_param(index, indexes)
        _validate_param(table, tables)

        dfs = _extrair_dataframes()
        
        if index =="IGP-M" and table == "projecao_mes":
            df = dfs[0]
            
        elif index =="IGP-M" and table == "projecao_posterior":
            df = dfs[1]
            
        elif index =="IGP-M" and table == "historico":
            df = dfs[2]
            df = _parse_tabela_historico(df)
            df = _format_date_number(df)
    
        elif index =="IPCA" and table == "projecao_mes":
            df = dfs[3]
            
        elif index =="IPCA" and table == "projecao_posterior":
            df = dfs[4]
            
        elif index =="IPCA" and table == "historico":
            df = dfs[5]
            df = _parse_tabela_historico(df)
        
        df = _format_date_number(df)
            
        return df
             
    except ValueError as e:
        print(str(e))   
