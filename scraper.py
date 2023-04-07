import gspread
import os
import requests
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials

GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
    arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta) # sheets.new
planilha = api.open_by_key("1S_ztKSv_gjalYZCjrb5CvU1fQMjHEfLw1k9i50HomF8")
sheet = planilha.worksheet("US_Data")
linhas = sheet.get("A3:Q20")

#### CPI e PPI
def texto_inf(n):
    
    GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
    with open("credenciais.json", mode="w") as arquivo:
        arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
    conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
    api = gspread.authorize(conta) # sheets.new
    planilha = api.open_by_key("1S_ztKSv_gjalYZCjrb5CvU1fQMjHEfLw1k9i50HomF8")
    sheet = planilha.worksheet("US_Data")
    linhas = sheet.get("A3:Q20")
    
    if n == 2:
      mes = linhas[1][1]
      mes2 = linhas[1][2]
    
    if n == 5:
      mes = linhas[4][1]
      mes2 = linhas[4][2]
    
    if float(linhas[n][5]) > 0.0:
      verbo_1 = f"cresceu {linhas[n][5]}%"
    if float(linhas[n][5]) < 0.0:
      verbo_1 = f"retraiu {linhas[n][5]}%"
    else:
      verbo_1 = "ficou estável"

    if float(linhas[n][11]) > 0.0:
      verbo_1N = f"exibiu alta de {linhas[n][11]}%"
    elif float(linhas[n][11]) < 0.0:
      verbo_1N = f"registrou queda de {linhas[n][11]}%"
    else:
      verbo_1N = "ficou estável"

    #Mesma condição, mas para 12 meses:
    if linhas[n][3] > linhas[n][4]:
      verbo_2 = "avançou"
    elif linhas[n][3] < linhas[n][4]:
      verbo_2 = "retraiu"
    else:
      verbo_2 = "fica estável"

    if linhas[n][9] > linhas[n][10]:
      verbo_2N = "avançou"
    elif linhas[n][9] < linhas[n][10]:
      verbo_2N = "retraiu"
    else:
      verbo_2N = "fica estável"

    ## 2) Para indicar se houve aceleração ou desaceleração no avanço:

    if linhas[n][5] > linhas[n][13]:
      verbo_3 = (f"acelerando em relação à leitura anterior (já que a variação de {mes2} foi de {linhas[n][13]}%)")
    elif linhas[n][5] < linhas[n][13]:
      verbo_3 = (f"desacelerando em relação à leitura anterior (já que a variação de {mes2} foi de {linhas[n][13]}%)")
    else:
      verbo_3 = "mantendo o mesmo tamanho de avanço da leitura anterior"

    if linhas[n][11] > linhas[n][15]:
      verbo_3N = (f"acelerando (uma vez que o avanço de {mes2} foi de {linhas[n][15]}%)")
    elif linhas[n][11] < linhas[n][15]:
      verbo_3N = (f"desacelerando (uma vez que o avanço de {mes2} foi de {linhas[n][15]}%)")
    else:
      verbo_3N = f"mantendo o mesmo ritmo de avanço de {mes2}"

    #Mesma condição, mas para 12 meses:

    if linhas[n][6] > linhas[n][14]:
      verbo_4 = (f"acelerando em relação à leitura anterior (de {linhas[n][14]}% do mês passado)")
    elif linhas[n][6] < linhas[n][14]:
      verbo_4 = (f"desacelerando em relação à leitura anterior (de {linhas[n][14]}% do mês passado)")
    else:
      verbo_4 = "mantendo o mesmo tamanho de avanço do último mês"

    if linhas[n][12] > linhas[n][16]:
      verbo_4N = (f"acelerando da variação de {linhas[n][16]}% da leitura anterior")
    elif linhas[n][12] < linhas[n][16]:
      verbo_4N = (f"desacelerando da variação de {linhas[n][16]}% da leitura anterior")
    else:
      verbo_4N = "mantendo o mesmo tamanho de avanço do último mês"

    if n == 2:
      dado_principal = "O índice de preços ao consumidor (CPI, na sigla em inglês)"
      dado_secundario = "CPI"
    elif n == 5:
      dado_principal = "O índice de preços ao produtor (PPI, na sigla em inglês)"
      dado_secundario = "PPI"
      
    dado_inflacao = f'''{dado_principal} nos Estados Unidos {verbo_1} em {mes} na variação mensal, {verbo_3}, \
conforme apontou o Departamento do Trabalho americano. No acumulado em 12 meses, o indicador de {mes} {verbo_2} {linhas[n][6]}%, {verbo_4}.
 
Em relação ao núcleo do índice (que exclui as variações de alimento e energia), o {dado_secundario} {verbo_1N} em {mes} \
na variação mensal, {verbo_3N}. No acumulado em 12 meses, o núcleo do indicador \
de {mes} {verbo_2N} {linhas[n][12]}%, {verbo_4N}.'''

    return dado_inflacao

### Payroll - mercado de trabalho dos EUA

def payroll():
    
    GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
    with open("credenciais.json", mode="w") as arquivo:
        arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
    conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
    api = gspread.authorize(conta) # sheets.new
    planilha = api.open_by_key("1S_ztKSv_gjalYZCjrb5CvU1fQMjHEfLw1k9i50HomF8")
    sheet = planilha.worksheet("US_Data")
    linhas = sheet.get("A3:Q20")
    
    if linhas[9][1] > linhas[9][2]:
      substantivo_1 = "alta"
    elif linhas[9][1] < linhas[9][2]:
      substantivo_1 = "redução"
    else:
      substantivo_1 = "mantendo o mesmo tamanho de avanço"

      ### definição do adjetivo
    if linhas[9][6] > linhas[9][7]:
        adjetivo_1 = f"maior do que a leitura anterior, de {linhas[9][7]}%"
    elif linhas[9][6] < linhas[9][7]:
        adjetivo_1= f"menor do que a leitura anterior, de {linhas[9][7]}%"
    else:
        adjetivo_1 = "igual à leitura anterior"

    payroll_funcao = f'''O total de vagas de trabalho geradas no mês de {linhas [7][1]} nos Estados Unidos foi de {linhas[9][4]} mil, uma {substantivo_1} \
na criação de postos na relação com o mês anterior, que foi de {linhas[9][5]} mil. Já a taxa de desemprego no mês foi de \
{linhas[9][6]}%, {adjetivo_1}. 

Em relação ao ganho salarial, houve um aumento de {linhas[13][6]}% em {linhas[11][1]}, enquanto \
no acumulado em 12 meses o crescimento do salário foi de {linhas[13][8]}%.'''

    return payroll_funcao
