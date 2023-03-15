from flask import Flask

app = Flask(__name__)

menu = """
<a href="/">Página Inicial</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>"""

indice = """<img src="https://gifs.eco.br/wp-content/uploads/2022/11/gifs-do-smilinguido-0.gif">""""
sobre = """<img src="https://pbs.twimg.com/profile_images/1623393254153543686/SiIQ1MKu_400x400.jpg">""""
contato = """<img src="https://media.tenor.com/QPDDG_qlvKkAAAAC/tata-werneck-trolala.gif">""""


@app.route("/")
def index():
  return menu + "Olá, mundo! Esse é meu site. (Arthur Cagliari)" + indice

@app.route("/sobre")
def sobre():
  return menu + "Aqui vai o conteúdo da página Sobre" + sobre

@app.route("/contato")
def contato():
  return menu + "Aqui vai o conteúdo da página Contato" + contato


