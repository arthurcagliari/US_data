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
from scraper import payroll
from scraper import texto_inf

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
