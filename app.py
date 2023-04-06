import datetime
import gspread
import json
import openai
import os
import pandas as pd
import prettytable
import requests

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
planilha = api.open_by_key("1ZDyxhXlCtCjMbyKvYmMt_8jAKN5JSoZ7x3MqlnoyzAM")
sheet = planilha.worksheet("Sheet1")
app = Flask(__name__)

@app.route("/")
def index():
  return indice + menu + "Olá, esse é um site de teste."

@app.route("/raspagem_US")
def raspagem():
  GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
  with open("credenciais.json", mode="w") as arquivo:
    arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
  conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
  api = gspread.authorize(conta)
  planilha = api.open_by_key("1S_ztKSv_gjalYZCjrb5CvU1fQMjHEfLw1k9i50HomF8")
  sheet = planilha.worksheet("US_Data")
  linhas = sheet.get("A3:Q20")
  
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
   dados = p.json()
  return "right"

@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
  
  GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
  with open("credenciais.json", mode="w") as arquivo:
    arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
  conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
  api = gspread.authorize(conta)
  planilha = api.open_by_key("1S_ztKSv_gjalYZCjrb5CvU1fQMjHEfLw1k9i50HomF8")
  sheet = planilha.worksheet("US_Data")
  linhas = sheet.get("A3:Q20")
  
  #### definindo as variáveis com os textos de inflação e mercado de trabalho
  texto_CPI = texto_inf(2)
  texto_PPI = texto_inf(5)
  payroll_text = payroll()
  
  #### ajustando o conteúdo do Livro Bege
  livro_bege = linhas[15][1]
    
  #### ajustando as respostas de acordo com os conteúdos explorados até agora
  update = request.json
  chat_id = update["message"]["chat"]["id"]
  message = update["message"]["text"]
  nova_mensagem = {"chat_id" : chat_id, "text" : message}
  
  
  if message in ("/start", "oi", "Olá", "ola", "Ola", "Oi", "oie", "Oie", "oie!", "oieeee", "Olá!", "olá", "Oi!", "Bom dia", "Opa", "Opa!", "opa", "oi!", "0", 0):
    nova_mensagem = {"chat_id" : chat_id, "text" : f'''Olá, seja bem-vindo(a) ao US Data Robot! Digite o número que indique o dado dos EUA que você quer conhecer: \n 
    1 - CPI (índice de preços ao consumidor);
    2 - PPI (índice de preços ao produtor); 
    3 - Payroll (mercado de trabalho);  
    4 - Livro Bege'''}
  elif message == "1":
     nova_mensagem = {
       "chat_id" : chat_id, 
       "text" : f'<b><u>CPI dos EUA</b></u> \n\n {texto_CPI} \n\n <i>Digite "0" para voltar ao menu inicial.</i>',
       "parse_mode":"HTML"}
  elif message == "2":
     nova_mensagem = {
       "chat_id" : chat_id, 
       "text" : f'<b><u>PPI dos EUA</u></b> \n\n {texto_PPI} \n\n <i>Digite "0" para voltar ao menu inicial.</i>',
       "parse_mode": "HTML"}
  elif message in ("Obrigado", "obrigado", "obrigado!", "Obrigado!", "Obrigada", "obrigada", "obrigada!", "Obrigada!", "Valeu", "valeu", "valeu!", "Valeu!", "tks", "thanks", "Opa, valeu!"):
     nova_mensagem = {
       "chat_id" : chat_id, 
       "text" : "Estamos aqui para isso!"}
  elif message == "3":
    nova_mensagem = {
      "chat_id" : chat_id, 
      "text" : f'<b><u>Payroll dos EUA</u></b> \n <i>(Mercado de trabalho)</i> \n\n {payroll_text} \n\n <i>Digite "0" para voltar ao menu inicial.</i>',
      "parse_mode" : "HTML"}
  elif message == "4":
     nova_mensagem = {
       "chat_id" : chat_id, 
       "text" : f'<b><u> Livro Bege (Fed)</b></u> \n\n {livro_bege} \n\n <i>(Este texto foi resumido e redigido por uma inteligência artificial)</i> \n\n <i>Digite "0" para voltar ao menu inicial.</i>', 
       "parse_mode": "HTML"}
  elif message == "5":
    nova_mensagem = {
      "chat_id" : chat_id, 
      "text" : "Ainda estamos desenvolvendo esta opção. Aguarde!"}
  elif message in ("tchau", "Tchau", "xau", "Xau"):
    nova_mensagem = {
      "chat_id" : chat_id, 
      "text" : "Tchau. Até mais!"}
  else:
    nova_mensagem = {
      "chat_id" : chat_id, 
      "text" : "Aguarde, estou pensando ainda. Ou não entendi essa coordenada. Se eu demorar, escreva 'oi' ou 'olá' para conhecer as instruções corretas."}
  requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
  return "ok"
