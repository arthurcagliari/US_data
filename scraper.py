import gspread

GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
    arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta) # sheets.new
planilha = api.open_by_key("1S_ztKSv_gjalYZCjrb5CvU1fQMjHEfLw1k9i50HomF8")
sheet = planilha.worksheet("US_Data")
linhas = sheet.get("A3:Q20")
  
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
