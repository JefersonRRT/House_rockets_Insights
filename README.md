# Projeto: House Rockets Insights de Negócio
![image](https://user-images.githubusercontent.com/117123482/210768853-80756bef-8bfd-4590-8257-c0365cef8453.png)

- (in process)
## Descrição
- A empresa fictícia House Rockets, que atua com o ramo imobiliário, tem por objetivo através da análise de dados selecionar os melhores imóveis para negociação, com intuito de maximizar os lucros tanto na venda quanto na compra de imóveis. Então o CEO solicitou aos analistas que criassem um método para acessar o dashboard pelo celular, e onde o mesmo pudesse selecionar imóveis de diferentes regiões, de diferentes valores, entre outras requisições.

## Dataset
- O dataset utilizado foi encontrado no link: https://www.kaggle.com/datasets/harlfoxem/housesalesprediction
- Esse dataset possui os preços de casas em King County, sede que fica em Seattle nos Estados Unidos. Ele inclui as casas que foram vendidas entre maio de 2014 e maio de 2015.

Variável | Definição
------------ | -------------
|id | Identificador de cada propriedade.|
|date | Data em que a propriedade ficou disponível.|
|price | O preço de cada imóvel, considerado como preço de compra.|
|bedrooms | Número de quartos.|
|bathrooms | O número de banheiros, o valor 0,5 indica um quarto com banheiro, mas sem chuveiro. O valor 0,75 ou 3/4 banheiro representa um banheiro que contém uma pia, um vaso sanitário e um chuveiro ou banheira.|
|sqft_living | Pés quadrados do interior das casas.|
|sqft_lot | Pés quadrados do terreno das casas.|
|floors | Número de andares.|
|waterfront | Uma variável fictícia para saber se a casa tinha vista para a orla ou não, '1' se a propriedade tem uma orla, '0' se não.|
|view | Vista, Um índice de 0 a 4 de quão boa era a visualização da propriedade.|
|condition | Um índice de 1 a 5 sobre o estado das moradias, 1 indica propriedade degradada e 5 excelente.|
|grade | Uma nota geral é dada à unidade habitacional com base no sistema de classificação de King County. O índice de 1 a 13, onde 1-3 fica aquém da construção e design do edifício, 7 tem um nível médio de construção e design e 11-13 tem um nível de construção e design de alta qualidade.|
|sqft_above | Os pés quadrados do espaço habitacional interior acima do nível do solo.|
|sqft_basement | Os pés quadrados do espaço habitacional interior abaixo do nível do solo.|
|yr_built | Ano de construção da propriedade.|
|yr_renovated | Representa o ano em que o imóvel foi reformado. Considera o número ‘0’ para descrever as propriedades nunca renovadas.|
|zipcode | Um código de cinco dígitos para indicar a área onde se encontra a propriedade.|
|lat | Latitude.|
|long | Longitude.|
|sqft_living15 | O tamanho médio em pés quadrados do espaço interno de habitação para as 15 casas mais próximas.|
|sqft_lot15 | Tamanho médio dos terrenos em metros quadrados para as 15 casas mais próximas.|


## Planejamento da Solução do Problema de Negócio:
- Coleta do dataset - Kaggle
- Entendimento do problema de negócio
- Limpeza dos dados
- Modelagem e processamento de dados
- Transformação e criação de variáveis
- Exploração dos dados

## Ferramentas Utilizadas:
- Python 3.9.7 
- Jupyter Notebook
- PyCharm

## Entrega:
- Visualização utilizando um aplicativo no StreamLit
