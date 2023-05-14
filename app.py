import datetime
import gspread
import json
import openai
import os
import pandas as pd
import prettytable
import requests
import telegram


from bs4 import BeautifulSoup as bs
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
from tchan import ChannelScraper
from scraper import CPI_PPI, payroll, renda, mes, beige_book, lista_per, meses 
from updates import payroll_2, texto_inf

TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
OPENAI_KEY = os.environ["OPENAI_KEY"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta) # sheets.new
planilha = api.open_by_key("1S_ztKSv_gjalYZCjrb5CvU1fQMjHEfLw1k9i50HomF8")
sheet = planilha.worksheet("US_Data")
app = Flask(__name__)
openai.api_key = OPENAI_KEY

@app.route("/")
def index():
  return "Olá, esse é um site de teste."

@app.route("/raspagem")
def raspagem():
  TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
  TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
  GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
  OPENAI_KEY = os.environ["OPENAI_KEY"]
  with open("credenciais.json", mode="w") as arquivo:
    arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
  conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
  api = gspread.authorize(conta)
  planilha = api.open_by_key("1S_ztKSv_gjalYZCjrb5CvU1fQMjHEfLw1k9i50HomF8")
  sheet = planilha.worksheet("US_Data")
  app = Flask(__name__)
  openai.api_key = OPENAI_KEY
      
   ### Montando a estrutura para formação de texto, de acordo com os dados dos EUA
  #dados = p.json()
  lista_CPI = CPI_PPI(0,1,2,3)
  lista_PPI = CPI_PPI(4,5,6,7)
  lista_vagas = payroll()
  lista_ganho = renda()
  
  ### definição do mês

  #p = 0 ---> dado do CPI
  #p = 4 ---> dado do PPI
  #p = 8 ---> dado do payroll

  mes0CPI = mes(0,0)
  mes1CPI = mes(0,1)
  mes2CPI = mes(0,2)

  mes0PPI = mes(4,0)
  mes1PPI = mes(4,1)
  mes2PPI = mes(4,2)

  mes0Pay = mes(8,0)
  mes1Pay = mes(8,1)
  mes2Pay = mes(8,2)
  
  #### O código abaixo limpa a minha planilha
  ranges = 'A3:Q16'
  lista_titulos = ["","dado bruto atual", "dado bruto anterior", "dado bruto não ajustado", "dado bruto há 12 meses","mensal (%)","anual (%)", "núcleo bruto", "núcleo bruto anterior", "núcleo bruto não ajustado", "núcleo bruto há 12 meses","núcleo/mensal (%)", "núcleo/anual (%)", "último mensal (%)", "último anual (%)", "último mensal núcleo (%)", "último anual núcleo (%)"]
  lista_meses_CPI = ["mês referência", mes0CPI, mes1CPI, mes0CPI, mes0CPI, mes0CPI, mes0CPI, mes0CPI, mes1CPI, mes0CPI, mes0CPI, mes0CPI, mes0CPI, mes1CPI, mes1CPI, mes1CPI, mes1CPI]
  lista_meses_PPI = ["mês referência", mes0PPI, mes1PPI, mes0PPI, mes0PPI, mes0PPI, mes0PPI, mes0PPI, mes1PPI, mes0PPI, mes0PPI, mes0PPI, mes0PPI, mes1PPI, mes1PPI, mes1PPI, mes1PPI]
  lista_vazia = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
  lista_payroll = ["payroll (merc. de trabalho)", "dado burto atual", "dado br. mês anterior", "dado br. dois meses antes", "total de vagas, em milhares", "total de vagas mês anterior, em milhares", "taxa de desemprego atual", "taxa de desemprego anterior"]
  lista_meses_pay = ["mês referência", mes0Pay, mes1Pay, mes2Pay, mes0Pay, mes1Pay, mes0Pay, mes1Pay, mes0Pay, mes1Pay]
  lista_payroll2 = ["ganho salarial", "ganho atual bruto", "ganho anterior bruto", "ganho há dois meses bruto", "ganho bruto 12 meses", "ganho bruto 13 meses", "ganho perc. atual", "ganho perc. anterior", "ganho acu. 12", "ganho acu. 12 anterior"]
  values =[lista_titulos, lista_meses_CPI, lista_CPI, lista_vazia, lista_meses_PPI, lista_PPI, lista_vazia, lista_meses_pay, lista_payroll, lista_vagas, lista_vazia, lista_meses_pay, lista_payroll2, lista_ganho]
  sheet.update(ranges, values)
  return "right"

@app.route("/raspagem1")
def raspagem1():
  TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
  TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
  GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
  OPENAI_KEY = os.environ["OPENAI_KEY"]
  with open("credenciais.json", mode="w") as arquivo:
    arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
  conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
  api = gspread.authorize(conta)
  planilha = api.open_by_key("1S_ztKSv_gjalYZCjrb5CvU1fQMjHEfLw1k9i50HomF8")
  sheet = planilha.worksheet("US_Data")
  app = Flask(__name__)
  openai.api_key = OPENAI_KEY
  
  ranges = 'A20:Q26'
  lista_mes_CPI = meses(0)
  lista_mes_PPI = meses(4)
  lista_vazia = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
  lista_CPI = lista_per(1)
  lista_PPI = lista_per(5)
  values =[lista_mes_CPI, lista_CPI, lista_vazia, lista_mes_PPI, lista_PPI]
  sheet.update(ranges, values)
  return "tudo certo"

@app.route("/raspagem2")
def raspagem2():
  GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
  OPENAI_KEY = os.environ["OPENAI_KEY"]
  with open("credenciais.json", mode="w") as arquivo:
    arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
  conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
  api = gspread.authorize(conta)
  planilha = api.open_by_key("1S_ztKSv_gjalYZCjrb5CvU1fQMjHEfLw1k9i50HomF8")
  sheet = planilha.worksheet("US_Data")
  app = Flask(__name__)
  livro_bege = beige_book()
  sheet.update_cell(18, 2, livro_bege)
  return "beleza"

@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
  
  GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
  with open("credenciais.json", mode="w") as arquivo:
    arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
  conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
  api = gspread.authorize(conta)
  planilha = api.open_by_key("1S_ztKSv_gjalYZCjrb5CvU1fQMjHEfLw1k9i50HomF8")
  sheet = planilha.worksheet("US_Data")
  linhas = sheet.get("A3:Q26")
  
  #### definindo as variáveis com os textos de inflação e mercado de trabalho
  texto_CPI = texto_inf(2)
  texto_PPI = texto_inf(5)
  payroll_text = payroll_2()
  bandeira_EUA = '\U0001F1FA\U0001F1F8'
  beige_bk = '\U0001F4D6'
  
  #### ajustando o conteúdo do Livro Bege
  livro_bege = linhas[15][1]
    
  #### ajustando as respostas de acordo com os conteúdos explorados até agora
  update = request.json
  chat_id = update["message"]["chat"]["id"]
  message = update["message"]["text"]
  nova_mensagem = {"chat_id" : chat_id, "text" : message}
  
  
  if message in ("/start", "oi", "Olá", "ola", "Ola", "Oi", "oie", "Oie", "oie!", "oieeee", "Olá!", "olá", "Oi!", "Bom dia", "Opa", "Opa!", "opa", "oi!", "0", 0):
    nova_mensagem = {"chat_id" : chat_id, "text" : f'Olá, seja bem-vindo(a) ao US Data Robot! Digite o número que indique o dado dos EUA que você quer conhecer: \n1 - CPI (índice de preços ao consumidor); \n2 - PPI (índice de preços ao produtor); \n3 - Payroll (mercado de trabalho); \n4 - Livro Bege'}
  elif message == "1":
    nova_mensagem = {
       "chat_id" : chat_id, 
       "text" : f'<b><u>CPI dos EUA {bandeira_EUA}</u></b> \n\n{texto_CPI} \n\n<u>Se quiser ver o histórico do acumulado de 12 meses do CPI, escreva "+CPI" ou "mais CPI".</u> \n\n <i><b>Digite "0" para voltar ao menu inicial.</b></i>',
       "parse_mode": "HTML"}
  elif message in ("+CPI", "maisCPI", "mais CPI", "MAISCPI", "MaisCPI", "Maiscpi", "Mais CPI"):
    nova_mensagem = {
       "chat_id" : chat_id, 
       "text" : f'''<b><u>Acumulado de 12 meses do CPI</u></b> \n
\U0001f4c8 {linhas[17][1]} \u2192 {linhas[18][1]}% \n\U0001f4c8 {linhas[17][2]} \u2192 {linhas[18][2]}% 
\U0001f4c8 {linhas[17][3]} \u2192 {linhas[18][3]}% \n\U0001f4c8 {linhas[17][4]} \u2192 {linhas[18][4]}%
\U0001f4c8 {linhas[17][5]} \u2192 {linhas[18][5]}% \n\U0001f4c8 {linhas[17][6]} \u2192 {linhas[18][6]}%
\U0001f4c8 {linhas[17][7]} \u2192 {linhas[18][7]}% \n\U0001f4c8 {linhas[17][8]} \u2192 {linhas[18][8]}%
\U0001f4c8 {linhas[17][9]} \u2192 {linhas[18][9]}% \n\U0001f4c8 {linhas[17][10]} \u2192 {linhas[18][10]}%
\U0001f4c8 {linhas[17][11]} \u2192 {linhas[18][11]}% \n\U0001f4c8 {linhas[17][12]} \u2192 {linhas[18][12]}%
\n<i>Digite "0" para voltar ao menu inicial.</i>''',
       "parse_mode": "HTML"}
  elif message in ("+PPI", "maisPPI", "mais PPI", "MAISPPI", "MaisPPI", "Maisppi", "Mais PPI"):
    nova_mensagem = {
       "chat_id" : chat_id, 
       "text" : f'''<b><u>Acumulado de 12 meses do PPI</u></b> \n
\U0001f4c8 {linhas[20][1]} \u2192 {linhas[21][1]}% \n\U0001f4c8 {linhas[20][2]} \u2192 {linhas[21][2]}% 
\U0001f4c8 {linhas[20][3]} \u2192 {linhas[21][3]}% \n\U0001f4c8 {linhas[20][4]} \u2192 {linhas[21][4]}%
\U0001f4c8 {linhas[20][5]} \u2192 {linhas[21][5]}% \n\U0001f4c8 {linhas[20][6]} \u2192 {linhas[21][6]}%
\U0001f4c8 {linhas[20][7]} \u2192 {linhas[21][7]}% \n\U0001f4c8 {linhas[20][8]} \u2192 {linhas[21][8]}%
\U0001f4c8 {linhas[20][9]} \u2192 {linhas[21][9]}% \n\U0001f4c8 {linhas[20][10]} \u2192 {linhas[21][10]}%
\U0001f4c8 {linhas[20][11]} \u2192 {linhas[21][11]}% \n\U0001f4c8 {linhas[20][12]} \u2192 {linhas[21][12]}%
\n<i>Digite "0" para voltar ao menu inicial.</i>''',
       "parse_mode": "HTML"}
  elif message == "2":
    nova_mensagem = {
       "chat_id" : chat_id, 
       "text" : f'<b><u>PPI dos EUA {bandeira_EUA}</u></b> \n\n{texto_PPI} \n\n <u>Se quiser ver o histórico do acumulado de 12 meses do CPI, escreva "+PPI" ou "mais PPI".</u> \n\n <i><b>Digite "0" para voltar ao menu inicial.</b></i>',
       "parse_mode": "HTML"}
  elif message in ("Obrigado", "obrigado", "obrigado!", "Obrigado!", "Obrigada", "obrigada", "obrigada!", "Obrigada!", "Valeu", "valeu", "valeu!", "Valeu!", "tks", "thanks", "Opa, valeu!"):
    nova_mensagem = {
       "chat_id" : chat_id, 
       "text" : "Estamos aqui para isso!"}
  elif message == "3":
    nova_mensagem = {
      "chat_id" : chat_id, 
      "text" : f'<b><u>Payroll dos EUA {bandeira_EUA}</u></b> \n <i>(Mercado de trabalho)</i> \n\n{payroll_text} \n\n <i>Digite "0" para voltar ao menu inicial.</i>',
      "parse_mode" : "HTML"}
  elif message == "4":
    nova_mensagem = {
       "chat_id" : chat_id, 
       "text" : f'<b><u> Livro Bege (Fed) {beige_bk}</u></b> \n\n{livro_bege} \n\n <i>(Este texto foi resumido e redigido por uma inteligência artificial)</i> \n\n <i>Digite "0" para voltar ao menu inicial.</i>', 
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
