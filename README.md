# US_data

Este repositório apresenta o projeto de um robô desenvolvido para <i>raspar dados econômicos dos Estados Unidos</i>, salvá-los em uma planilha do Google Sheets e depois, desta planilha, enviá-los para um bot no Telegram. A ideia do projeto é facilitar o trabalho de produção de textos sobre tais indicadores econômicos. Por ora, o robô apresenta três informações oriundas do site <a href="https://www.bls.gov/">BLS (Departamento de Trabalho dos EUA)</a> e informações do Livro Bege, do <a href="https://www.federalreserve.gov/monetarypolicy/publications/beige-book-default.htm">Federal Reserve (Fed)</a>.

Inicialmente, na elaboração deste projeto, o código fazia a raspagem de dados diretamente dos sites e os enviava ao bot do Telegram, toda vez que um determinado caractere fosse acionado pelo usuário. Mas, tendo em vista que em algum momento a quantidade de requisições para a raspagem poderia criar um bloqueio no envio dos dados, optou-se por compilar as informações em um documento do Google Sheets. Dessa forma, o robô passa a raspar a página indicada somente uma vez por dia e leva o material ao documento no Sheets. Já este último material pode ser consultado quantas vezes o usuário quiser, sem sofrer algum tipo de bloqueio.

Esse método que utiliza o Google Sheets como um intermediário na comunicação com o robô do Telegram foi uma solução não apenas para a raspagem, mas também para o uso da inteligência artificial do <i>openai</i>. Já que há um custo na requisição do robô para que a inteligência do openai produza um texto, para evitar gastos, optou-se por solicitar um resumo de um texto raspado do site do Fed uma única vez ao mês --já que o documento tem uma periodicidade de 45 dias.

Por fim, cabe dizer que este robô não apenas raspa os dados do BLS, mas os compara e utiliza o verbo adequado <i>(aumentou/diminuiu/acelerou/desacelerou)</i> para indicar o movimento observado na última leitura do indicador. 

Assim sendo, este repositório irá apresentar:
- raspagem de dados de inflação ao consumidor (CPI) e ao produtor (PPI) nos EUA;
- raspagem de dados do payroll (da criação de vagas, da taxa de desemprego e do ganho salarial nos EUA);
- comparação dos números, indicando se houve um avanço ou um recuo do indicador em relação à leitura anterior;
- identificação dos meses e da variação acumulada nos últimos 12 meses;
- o envio de tais informações para um documento no Google Sheets;
- a extração dessas informações do Google Sheets e o envio delas para um robô no Telegram.

### Conteúdos

Com o objetivo de deixar o fluxo dos códigos mais claro e direto, optou-se por separar os códigos em três pares:
- <i>app.py</i>: é a estrutura principal do código, em que estabelece as principais atividades do robô (enviar informações para o Sheets, extrai-las quando necessário e reenviá-las ao Telegram);
- <i>scraper.py</i>: é a estrutura de códigos referente a raspagem de dados do site do BLS. Aqui nesta parte estão as funções referentes a retirada dos dados de inflação e meracdo de trabalho dos EUA, além da função que solicita a inteligência artificial do openai para resumir a introdução do Livro Bege;
- <i>updates.py</i>: é a estrutura do código que vai comparar os dados extraídos no trecho anterior e que estavam dispostos no Google Sheets. O código também apresenta um caminho para que essa comparação permita o uso adequado do verbo e substantivo relativo ao movimento observado no mês (queda, alta, acelerar ou desacelerar). Nesta etapa os dados são também compilados e enviados para o Telegram a partir de determinadas solicitações.

Observações importantes: para ter um robô bastante responsivo (quase simultâneo, dado que há algum delay nas primeiras requisições do usuário), foi utilizada na consstrução deste robô a plataforma <a href="https://dashboard.render.com/">Render</a> e a tecnologia de comunicação entre aplicações Webhook. No caso desta último é MUITO IMPORTANTE lembrar que é preciso acionar um gatilho para que o robô do Telegram utilize o Webhook como atualizador das solcitiações --Daí a criação do arquivo <i>gatilho_webhook.py. (Este deve ser o primeiro passo)</i>. Por fim, depois de usar o Render na criação de páginas que atualizassem os materais quando acessadas, foi preciso criar uma forma de acessá-las periodicamente. Para isso, utilizou-se a plataforma <a href="https://pipedream.com/">Pipedream</a>. Como a atualização dos códigos do BLS não ocorrerão na mesa frequência que o código do Federal Reserve, foi preciso também criar dois comandos (e, portanto, dois endereços de URLs) para que houvesse atualizações em períodos distintos.






