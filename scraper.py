import datetime
import gspread
import openai
import os
import pandas as pd
import prettytable
import requests
import json

from bs4 import BeautifulSoup as bs
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
from tchan import ChannelScraper

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta) # sheets.new
planilha = api.open_by_key("1S_ztKSv_gjalYZCjrb5CvU1fQMjHEfLw1k9i50HomF8")
sheet = planilha.worksheet("US_Data")
app = Flask(__name__)
OPENAI_KEY = os.environ["OPENAI_KEY"]
openai.api_key = OPENAI_KEY

headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ['CUSR0000SA0','CUUR0000SA0', 'CUSR0000SA0L1E','CUUR0000SA0L1E','WPSFD4','WPUFD4', 'WPSFD49104','WPUFD49104', 'CES0000000001','LNS14000000','CES0500000003'],"startyear":"2021", "endyear":"2023"})
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)
for series in json_data['Results']['series']:
    x=prettytable.PrettyTable(["series id","year","period","value","footnotes"])
    seriesId = series['seriesID']
    for item in series['data']:
        year = item['year']
        period = item['period']
        value = item['value']
        footnotes=""
        for footnote in item['footnotes']:
            if footnote:
                footnotes = footnotes + footnote['text'] + ','
        if 'M01' <= period <= 'M12':
            x.add_row([seriesId,year,period,value,footnotes[0:-1]])
    output = open(seriesId + '.txt','w')
    output.write (x.get_string())
    output.close()
      
### Montando a estrutura para formação de texto, de acordo com os dados dos EUA
dados = p.json()
def CPI_PPI(n,p,s,q):
###### Leituras recentes
  if n == 0:
    indice = "CPI"
  else:
    indice = "PPI"
  CPI_atual = dados['Results']['series'][n]['data'][0]['value'] ### dado ajustado
  CPI_anterior = dados['Results']['series'][n]['data'][1]['value']
  CPI_atual_una = dados['Results']['series'][p]['data'][0]['value'] ### dado não ajustado
  CPI_mes_atual_12 = dados['Results']['series'][p]['data'][12]['value']
  CPI_mensal = (float(CPI_atual) - float(CPI_anterior))*100/float(CPI_anterior)
  CPI_anual = (float(CPI_atual_una) - float(CPI_mes_atual_12))*100/float(CPI_mes_atual_12)
  CPI_mensal_ajustado ='%.1f' % CPI_mensal
  CPI_anual_ajustado ='%.1f' % CPI_anual

  ### Núcleo do CPI (sem energia e alimentos):
  NCPI_atual = dados['Results']['series'][s]['data'][0]['value']
  NCPI_anterior = dados['Results']['series'][s]['data'][1]['value']
  NCPI_atual_una = dados['Results']['series'][q]['data'][0]['value']
  NCPI_mes_atual_12 = dados['Results']['series'][q]['data'][12]['value']
  NCPI_mensal = (float(NCPI_atual) - float(NCPI_anterior))*100/float(NCPI_anterior)
  NCPI_anual = (float(NCPI_atual_una) - float(NCPI_mes_atual_12))*100/float(NCPI_mes_atual_12)
  NCPI_mensal_ajustado ='%.1f' % NCPI_mensal
  NCPI_anual_ajustado ='%.1f' % NCPI_anual

  ####### Leituras anteriores do CPI
  CPI_anterior = dados['Results']['series'][n]['data'][1]['value']
  CPI_anterior_una = dados['Results']['series'][p]['data'][1]['value']
  CPI_anterior_2 = dados['Results']['series'][n]['data'][2]['value']
  CPI_mes_anterior_12 = dados['Results']['series'][p]['data'][13]['value']
  CPI_mensal_anterior = (float(CPI_anterior) - float(CPI_anterior_2))*100/float(CPI_anterior_2)
  CPI_anual_anterior = (float(CPI_anterior_una) - float(CPI_mes_anterior_12))*100/float(CPI_mes_anterior_12)
  CPI_mensal_anterior_ajustado ='%.1f' % CPI_mensal_anterior
  CPI_anual_anterior_ajustado ='%.1f' % CPI_anual_anterior

  ####### Leituras anteriores do núcleo do CPI
  NCPI_anterior = dados['Results']['series'][s]['data'][1]['value']
  NCPI_anterior_una = dados['Results']['series'][q]['data'][1]['value']
  NCPI_anterior_2 = dados['Results']['series'][s]['data'][2]['value']
  NCPI_mes_anterior_12 = dados['Results']['series'][q]['data'][13]['value']
  NCPI_mensal_anterior = (float(NCPI_anterior) - float(NCPI_anterior_2))*100/float(NCPI_anterior_2)
  NCPI_anual_anterior = (float(NCPI_anterior_una) - float(NCPI_mes_anterior_12))*100/float(NCPI_mes_anterior_12)
  NCPI_mensal_anterior_ajustado ='%.1f' % NCPI_mensal_anterior
  NCPI_anual_anterior_ajustado ='%.1f' % NCPI_anual_anterior

  lista_dados = [indice, CPI_atual, CPI_anterior, CPI_atual_una, CPI_mes_atual_12, CPI_mensal_ajustado, CPI_anual_ajustado, NCPI_atual, NCPI_anterior, NCPI_atual_una, NCPI_mes_atual_12, NCPI_mensal_ajustado, NCPI_anual_ajustado, CPI_mensal_anterior_ajustado, CPI_anual_anterior_ajustado, NCPI_mensal_anterior_ajustado, NCPI_anual_anterior_ajustado]
  return lista_dados

def payroll():
  mes_atual_mt = dados['Results']['series'][8]['data'][0]['value']
  mes_anterior_mt = dados['Results']['series'][8]['data'][1]['value']
  mes_antes_anterior_mt = dados['Results']['series'][8]['data'][2]['value']
  total_de_vagas = '%.0f' %((float(mes_atual_mt) - float(mes_anterior_mt)))
  total_de_vagas_antes = '%.0f' %((float(mes_anterior_mt) - float(mes_antes_anterior_mt))) 
  taxa_desemprego_atual = dados['Results']['series'][9]['data'][0]['value']
  taxa_desemprego_anterior = dados['Results']['series'][9]['data'][1]['value']
  lista_vagas = ["", mes_atual_mt, mes_anterior_mt, mes_antes_anterior_mt, total_de_vagas, total_de_vagas_antes, taxa_desemprego_atual, taxa_desemprego_anterior]
  return lista_vagas

def renda():
  ganho_atual = dados['Results']['series'][10]['data'][0]['value']
  ganho_anterior = dados['Results']['series'][10]['data'][1]['value']
  ganho_antes_ant = dados['Results']['series'][10]['data'][2]['value']
  ganho_12anterior = dados['Results']['series'][10]['data'][12]['value']
  ganho_13anterior = dados['Results']['series'][10]['data'][12]['value']
  ganho_perc_mes = '%.1f' % ((float(ganho_atual) - float(ganho_anterior))*100/float(ganho_anterior))
  ganho_perc_mes_ant = '%.1f' % ((float(ganho_anterior) - float(ganho_antes_ant))*100/float(ganho_antes_ant))
  ganho_perc_ano = '%.1f' % ((float(ganho_atual) - float(ganho_12anterior))*100/float(ganho_12anterior))
  ganho_perc_ano_ant = '%.1f' % ((float(ganho_anterior) - float(ganho_13anterior))*100/float(ganho_13anterior))
  lista_ganho = ["", ganho_atual, ganho_anterior, ganho_antes_ant, ganho_12anterior, ganho_13anterior, ganho_perc_mes, ganho_perc_mes_ant, ganho_perc_ano, ganho_perc_ano_ant]
  return lista_ganho

def mes(p,n):
    if dados['Results']['series'][p]['data'][n]['period'] == 'M01':
      mes_1 = 'janeiro'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M02':
      mes_1 = 'fevereiro'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M03':
      mes_1 = 'março'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M04':
      mes_1 = 'abril'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M05':
      mes_1 = 'maio'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M06':
      mes_1 = 'junho'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M07':
      mes_1 = 'julho'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M08':
      mes_1 = 'agosto'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M09':
      mes_1 = 'setembro'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M10':
      mes_1 = 'outubro'
    elif dados['Results']['series'][p]['data'][n]['period'] == 'M11':
      mes_1= 'novembro'
    else:
      mes_1 = 'dezembro'
    return mes_1
  
def beige_book():
  data_atual = datetime.datetime.now()
  dia_atual = data_atual.day
  mes_atual = data_atual.month

  if mes_atual <= 4:
    if dia_atual < 19:
      n = '03'

  elif mes_atual <= 5:
    if dia_atual < 30:
      n = '04'

  elif mes_atual <= 7:
    if dia_atual < 11:
      n = '05'

  elif mes_atual <= 9:
    if dia_atual < 5:
      n = '07'

  elif mes_atual <= 10:
    if dia_atual < 17:
      n = '09'

  elif mes_atual <= 11:
    if dia_atual < 28:
      n = '10'

  url = f'https://www.federalreserve.gov/monetarypolicy/beigebook2023{n}.htm'
  
  soup = bs(requests.get(url).content, "html.parser")
  abstract = soup.find("div", "col-xs-12 col-md-9").text
  palavra_inicial = 'Overall Economic Activity'
  palavra_final = 'Highlights by Federal Reserve District'
  pos_inicial = abstract.find(palavra_inicial) + len(palavra_inicial) + 1
  pos_final = abstract.find(palavra_final)
  subtexto = abstract[pos_inicial:pos_final].strip()
  
  prompt = "Considere o seguinte subtexto:"
  pauta = "\n Transforme este subtexto em uma notícia de dois parágrafos, com no máximo 400 caracteres."

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt= prompt + subtexto + pauta,
    temperature=0.0,
    max_tokens=500,
    top_p=1.0, 
    frequency_penalty=0.0,
    presence_penalty=0.0
  )
  livro_bege = response["choices"][0]["text"].strip()
  return livro_bege

def lista_per(x):
  def CPI_PPI_per(s,k):
    CPI_1 = dados['Results']['series'][s]['data'][k]['value']
    CPI_2 = dados['Results']['series'][s]['data'][int(k)+12]['value']
    CPI_per = '%.1f' % ((float(CPI_1) - float(CPI_2))*100/float(CPI_2))
    return str(CPI_per)
  
  lista_CPI_per = []  
  for w in range(0,12):
    inflacao_per = CPI_PPI_per(x,w)
    lista_CPI_per.append(inflacao_per)
  return lista_CPI_per

def meses(p):

  lista_meses_inf = []
  for f in range(0,12):
    mes_inflacao = dados['Results']['series'][p]['data'][f]['periodName']
    ano_inflacao = dados['Results']['series'][p]['data'][f]['year']
    data_inf = f'{mes_inflacao[:3]}.{ano_inflacao[2:]}'
    lista_meses_inf.append(data_inf)
  return lista_meses_inf
