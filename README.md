# US_data

Este repositório apresenta o projeto de um robô desenvolvido para <i>raspar dados econômicos dos Estados Unidos</i>, salvá-los em uma planilha do Google Sheets e 
depois, desta planilha, enviá-los para um bot no Telegram. A ideia do projeto é facilitar o trabalho de produção de textos sobre tais indicadores econômicos.
Por ora, o robô apresenta três informações oriundas do site <a href="https://www.bls.gov/">BLS (Departamento de Trabalho dos EUA)</a> e informações do Livro Bege, do <a href="https://www.federalreserve.gov/monetarypolicy/publications/beige-book-default.htm">Federal Reserve (Fed)</a>.

Inicialmente, na elaboração deste projeto, o código fazia a raspagem de dados diretamente dos sites e os enviava ao bot do Telegram, toda vez que um determinado caractere fosse acionado 
pelo usuário. Mas, tendo em vista que em algum momento a quantidade de requisições para a raspagem poderia criar um bloqueio no envio dos dados, optou-se por compilar as informações
em um documento do Google Sheets. Dessa forma, o robô passa a raspar a página indicada somente uma vez por dia e leva o material ao documento no Sheets. Já este último material pode ser
consultado quantas vezes o usuário quiser, sem sofrer algum tipo de bloqueio.

Esse método que utiliza o Google Sheets como um intermediário na comunicação com o robô do Telegram foi uma solução não apenas para a raspagem, mas também para o uso da inteligência artificial
do <i>openai</i>. Já que há um custo na requisição do robô para que a inteligência do openai produza um texto, para evitar gastos, optou-se por solicitar um resumo de um texto raspado do site do 
Fed uma única vez ao mês --já que o documento tem uma periodicidade de 45 dias.

