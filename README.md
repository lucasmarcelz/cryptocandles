# CRYPTO CANDLES

## Sobre

<h4>Agregador de cotações de criptmoedas que utiliza API Poloniex parar gerar Candlesticks e registra-los no banco de
dados.</h4>

## Funcionamento

Algumas decisões de arquitetura incluiam a não multiplicação de objetos, dessa forma, a classe Candlestick que detém
todas as propriedades do programa, é instanciada uma única vez dentro do main. A aplicação atua de maneira simples,
agregando dados em seus devidos atributos, através da API Poloniex como parametro do método: Set_Attributes. Com os
dados definidos, o programa compara o horário atual com o de fechamento previsto do Candle, o horário de previsão é
calibrado de modo a corrigir o ciclo do Candle.

Ex: (BTC_ETH, 5). Se são 15:33, o primeiro candle é finalizado ás 15:35, e se mantendo consistente no futuro. Assim
estando dentro do padrão para comparações com outros gráficos.

A cotação é enviada ao banco de dados MYSQL e os valores são atualizados para a geração do próximo Candle.

## Como utilizar

Com o Docker instalado, dentro do diretório utilize o seguinte comando para começar a rodar

```shell
docker-compose up
```

Por padrão, os Candles de 1, 5 e 10 minutos são gerados, para as criptmoedas 'BTC_ADA' e 'USDT_ADA', porém, isso é
facilmente alterável!

O usuário pode mudar o entrypoint do container dentro de docker-compose.yaml para definir as criptomoedas desejadas

```dockerfile
 entrypoint: ['poetry', 'run' ,'start', '--tickers', 'BTC_ETH', 'USDT_ADA']
```

O Usuário se desejar pode visualizar o help do programa inserindo o parametro `--help`

`poetry run start --help`

```shell
usage: CryptoCandle [-h] [-v] --tickers TICKERS [TICKERS ...]

Data aggregation in Candlesticks through the Poloniex API for sending to the Database

required arguments:
  --tickers TICKERS [TICKERS ...]
                        List of tickers to be observed

help:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  
```

## Bibliotecas utilizadas

#### Poetry

#### PyMySQl

#### Requests

#### Pydantic

## Dores e díficuldades

A falta de experiência com Docker acabou consumindo muito tempo, e dado o prazo, outras features e melhoras planejadas
terão de ser implementadas no futuro.

Fiquei empacado por um tempo pensando em como fazer os Candles terem o comportamento de se manter em horarios fixos
(ex: 13:00, 13:05, 13:10) sem que houvesse grande perda de informação, já que o programa pode ser executado a qualquer
momento e gerar inconsistencias no primeiro candle de cada periodo, como por exemplo não registrar o valor máximo dentro
do minuto antes da execução. Então, ao invés de despachar o primeiro Candle finalizado, optei por conservar seus dados,
dessa forma o primeiro Candle é finalizado, o gráfico é gerado mais rapidamente e ele logo se adequa ao ciclo ideal de
seu Periodo.

### Obrigado, @SmarttBot, pela oportunidade de realizar o teste! =)





