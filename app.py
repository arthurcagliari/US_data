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
  
  GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
  with open("credenciais.json", mode="w") as arquivo:
    arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
  conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
  api = gspread.authorize(conta) # sheets.new
  planilha = api.open_by_key("1S_ztKSv_gjalYZCjrb5CvU1fQMjHEfLw1k9i50HomF8")
  sheet = planilha.worksheet("US_Data")
  linhas = sheet.get("A3:Q20")

 #### Condições: 
  ## 1) Para indicar que houve avanço, recuo ou estabilidade no índice de inflação:
  
  
  def texto_inf(n):
    
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
  
  #### definindo as variáveis com os textos de inflação
  texto_CPI = texto_inf(2)
  texto_PPI = texto_inf(5)
  
  #### aqui começa o código do payroll
  
  def payroll():
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
  payroll_text = payroll()
  
  #### ajustando o conteúdo do Livro Bege
  
  def beige_book():
    livro_texto = linhas[15][1]
    return print(livro_texto)
  
  livro_bege = beige_book()
  
  #### ajustando as respostas de acordo com os conteúdos explorados até agora
  update = request.json
  chat_id = update["message"]["chat"]["id"]
  message = update["message"]["text"]
  nova_mensagem = {"chat_id" : chat_id, "text" : message}
  
  
  if message in ("/start", "oi", "Olá", "ola", "Ola", "Oi", "oie", "Oie", "oie!", "oieeee", "Olá!", "olá", "Oi!", "Bom dia", "Opa", "Opa!", "opa", "oi!", "0", 0):
    nova_mensagem = {"chat_id" : chat_id, "text" : f'''Olá, seja bem-vindo(a) ao US Data Robot! Digite o número que indique o dado dos EUA que você quer conhecer: \n 
    1 - CPI (índice de preços ao consumidor);
    2 - PPI (índice de preços ao produtor); 
    3 - Payroll (dados do mercado de trabalho);\n  
    4 - Livro Bege\n\n'''}
  elif message == "1":
     nova_mensagem = {"chat_id" : chat_id, "text" : f'{texto_CPI} \n\n Digite "0" para voltar ao menu inicial.'}
  elif message == "2":
     nova_mensagem = {"chat_id" : chat_id, "text" : f'{texto_PPI} \n\n Digite "0" para voltar ao menu inicial.'}
  elif message in ("Obrigado", "obrigado", "obrigado!", "Obrigado!", "Obrigada", "obrigada", "obrigada!", "Obrigada!", "Valeu", "valeu", "valeu!", "Valeu!", "tks", "thanks", "Opa, valeu!"):
     nova_mensagem = {"chat_id" : chat_id, "text" : "Estamos aqui para isso!"}
  elif message == "3":
    nova_mensagem = {"chat_id" : chat_id, "text" : f'{payroll_text} \n\n (Este texto foi resumido e redigido por uma inteligência artificial) \n\n Digite "0" para voltar ao menu inicial.'}
  elif message == "4":
     nova_mensagem = {"chat_id" : chat_id, "text" : f'{livro_bege} \n\n Digite "0" para voltar ao menu inicial.'}
  elif message == "5":
    nova_mensagem = {"chat_id" : chat_id, "text" : "Ainda estamos desenvolvendo esta opção. Aguarde!"}
  elif message in ("tchau", "Tchau", "xau", "Xau"):
    nova_mensagem = {"chat_id" : chat_id, "text" : "Tchau, tchau! Até mais!"}
  else:
    nova_mensagem = {"chat_id" : chat_id, "text" : "Aguarde, estou pensando ainda ou não entendi essa coordenada. Se eu demorar, escreva 'oi' ou 'olá' para conhecer as instruções corretas."}
  requests.post(f"https://api.telegram.org./bot{TELEGRAM_API_KEY}/sendMessage", data=nova_mensagem)
  return "ok"
