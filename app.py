import gspread
import os
import requests
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
planilha = api.open_by_key("1ZDyxhXlCtCjMbyKvYmMt_8jAKN5JSoZ7x3MqlnoyzAM")
sheet = planilha.worksheet("Sheet1")
app = Flask(__name__)

def ultimas_promocoes():
  scraper = ChannelScraper()
  contador = 0
  resultado = []
  for message in scraper.messages("promocoeseachadinhos"):
    contador += 1
    texto = message.text.strip().splitlines()[0]
    resultado.append(f"{message.created_at} {texto}")
    if contador == 10:
      return resultado

    
menu = """
<a href="/">Página inicial</a> | <a href="/promocoes">Promoções</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>
<br>
"""

indice = """<br><img src="https://cdn-dejpn.nitrocdn.com/uxismCAJKdZklcCeScRYXbxxVTZIsrib/assets/static/optimized/rev-58a7024/wp-content/uploads/2021/08/FANI-slider-02.png"><br>"""
imagem = """<br><img src="https://media.tenor.com/QPDDG_qlvKkAAAAC/tata-werneck-trolala.gif"><br>"""


@app.route("/")
def index():
  return indice + menu + "Olá, mundo! Esse é meu site. (Arthur Cagliari)"

@app.route("/sobre")
def sobre():
  return menu + "Aqui vai o conteúdo da página Sobre"

@app.route("/contato")
def contato():
  return menu + "Aqui vai o conteúdo da página Contato" + imagem

@app.route("/promocoes")
def promocoes():
  conteudo = menu + """
  Encontrei as seguintes promoções no <a href="https://t.me/promocoeseachadinhos">@promocoeseachadinhos</a>:
  <br>
  <ul>
  """
  for promocao in ultimas_promocoes():
    conteudo += f"<li>{promocao}</li>"
  return conteudo + "</ul>"


@app.route("/promocoes2")
def promocoes2():
  conteudo = menu + """
  Encontrei as seguintes promoções no <a href="https://t.me/promocoeseachadinhos">@promocoeseachadinhos</a>:
  <br>
  <ul>
  """
  scraper = ChannelScraper()
  contador = 0
  for message in scraper.messages("promocoeseachadinhos"):
    contador += 1
    texto = message.text.strip().splitlines()[0]
    conteudo += f"<li>{message.created_at} {texto}</li>"
    if contador == 10:
      break
  return conteudo + "</ul>"

@app.route("/dedoduro")
def dedoduro():
  mensagem = {"chat_id": TELEGRAM_ADMIN_ID, "text": "Alguém acessou a página dedo duro!"}
  requests.post(f'https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage', data=mensagem)
  return "Mensagem enviada!"

@app.route("/dedoduro2")
def dedoduro2():
  sheet.append_row(["Arthur", 33, "Sorocabano", "Jornalista"])
  return "Planilha escrita!"


@app.route("/telegram-bot", methods=["POST"])
def telegram_bot():
  conta = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDENTIALS)
  api = gspread.authorize(conta)
  planilha = api.open_by_key("PLANILHA")
  sheet = planilha.worksheet("US_Data")
  linhas = sheet.get("A3:Q6")

 #### Condições: 
  ## 1) Para indicar que houve avanço, recuo ou estabilidade no índice de inflação:
  def texto_inf(n):
    if linhas[n][1] > linhas[n][2]:
      verbo_1 = "cresceu"
    elif linhas[n][1] < linhas[n][2]:
      verbo_1 = "retraiu"
    else:
      verbo_1 = "ficou estável"

    if linhas[n][7] > linhas[n][8]:
      verbo_1N = "exibiu alta"
    elif linhas[n][7] < linhas[n][8]:
      verbo_1N = "registrou queda"
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
      verbo_3 = (f"acelerando em relação à leitura anterior (já que a variação do mês passado foi de {linhas[n][13]}%)")
    elif linhas[n][5] < linhas[n][13]:
      verbo_3 = (f"desacelerando em relação à leitura anterior (já que a variação do mês passado foi de {linhas[n][13]}%)")
    else:
      verbo_3 = "mantendo o mesmo tamanho de avanço da leitura anterior"

    if linhas[n][11] > linhas[n][15]:
      verbo_3N = (f"acelerando (uma vez que o avanço do mês passado foi de {linhas[n][15]}%)")
    elif linhas[n][11] < linhas[n][15]:
      verbo_3N = (f"desacelerando (uma vez que o avanço do mês passado foi de {linhas[n][15]}%)")
    else:
      verbo_3N = "mantendo o mesmo ritmo de avanço do mes passado"

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
    elif n == 3:
      dado_principal = "O índice de preços ao produtor (PPI, na sigla em inglês)"
      dado_secundario = "PPI"

    dado_inflacao = f'{dado_principal} nos Estados \
  Unidos {verbo_1} {linhas[n][5]}% em {mes} na variação mensal, {verbo_3}, \
  conforme apontou o Departamento do Trabalho em nota. No acumulado em 12 meses, o indicador \
  de {mes} {verbo_2} {linhas[n][6]}%, {verbo_4}. Em relação ao núcleo do índice (que exclui as variações de alimento e energia), \
  o {dado_secundario} {verbo_1N} {linhas[n][11]}% em {mes} na variação mensal, {verbo_3N}. No acumulado em 12 \
  meses, o núcleo do indicador de {mes} {verbo_2N} {linhas[n][12]}%, {verbo_4N}.'

    return dado_inflacao
  
  #### definindo as variáveis com os textos de inflação
  texto_CPI = texto_inf(2)
  texto_PPI = texto_inf(3)

  #### ajustando as respostas de acordo com os conteúdos explorados até agora
  update = request.json
  chat_id = update["message"]["chat"]["id"]
  message = update["message"]["text"]
  nova_mensagem = {"chat_id" : chat_id, "text" : message}
  
  
  if message in ("/start", "oi", "Olá", "Oi", "oie", "Oie", "oie!", "oieeee", "Olá!", "olá", "Oi!", "Bom dia", "Opa", "Opa!", "opa", "oi!"):
    nova_mensagem = {"chat_id" : chat_id, "text" : "Olá, seja bem-vindo(a) ao US Data Robot! Digite o número que indique o dado dos EUA que quer conhecer: \n\n  1 - CPI (índice de preços ao consumidor); \n  2 - PPI (índice de preços ao produtor)"}
  elif message == "1":
     nova_mensagem = {"chat_id" : chat_id, "text" : texto_CPI}
  elif message == "2":
     nova_mensagem = {"chat_id" : chat_id, "text" : texto_PPI}
  elif message in ("Obrigado", "obrigado", "obrigado!", "Obrigado!", "Obrigada", "obrigada", "obrigada!", "Obrigada!", "Valeu", "valeu", "valeu!", "Valeu!", "tks", "thanks", "Opa, valeu!"):
     nova_mensagem = {"chat_id" : chat_id, "text" : "Estamos aqui para isso!"}
  elif message == "3":
    nova_mensagem = {"chat_id" : chat_id, "text" : "Ainda estamos desenvolvendo esta opção. Aguarde!"}
  else:
    nova_mensagem = {"chat_id" : chat_id, "text" : "Não entendi essa coordenada. Escreva 'oi' ou 'olá' para conhecer as instruções corretas."}
  requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
  return "ok"
