from flask import Flask

app = Flask(__name__)

menu = """
<a href="/">Página Inicial</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>"""

indice = """<img src="https://cdn-dejpn.nitrocdn.com/uxismCAJKdZklcCeScRYXbxxVTZIsrib/assets/static/optimized/rev-58a7024/wp-content/uploads/2021/08/FANI-slider-02.png">"""
foto = """<img src="https://pbs.twimg.com/profile_images/1623393254153543686/SiIQ1MKu_400x400.jpg">"""
imagem = """<img src="https://media.tenor.com/QPDDG_qlvKkAAAAC/tata-werneck-trolala.gif">"""


@app.route("/")
def index():
  return indice + menu + "Olá, mundo! Esse é meu site. (Arthur Cagliari)"

@app.route("/sobre")
def sobre():
  return menu + "Aqui vai o conteúdo da página Sobre" + foto

@app.route("/contato")
def contato():
  return menu + "Aqui vai o conteúdo da página Contato" + imagem


