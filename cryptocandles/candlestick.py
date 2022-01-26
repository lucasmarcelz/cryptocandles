from datetime import datetime, timedelta

import pymysql.cursors

from cryptocandles.settings import logger
from cryptocandles.settings import settings


class Candlestick:
    db_connection = pymysql.connect(host=settings.database_host, user=settings.database_user,
                                    password=settings.database_password, database=settings.database_name,
                                    port=settings.database_port)

    # Conexão com o banco de dados, optei por esta arquitetura como um atributo indepedente
    # da classe pois estabeleço uma única conexão, com o mesmo endereço de memória

    def __init__(self, crypto: str, frequency: int):
        """Atribui valores iniciais para as propriedades do candle
        :param crypto: Moeda definida
        :param frequency: Período definido
        """
        self.crypto = crypto
        self.frequency = frequency
        self.opening: float = 0.0
        self.minimum: float = 0.0
        self.maximum: float = 0.0
        self.close: float = 0.0
        self.initial_time: datetime = datetime.now()

    def save_candle_if_complete(self, current_price: float):
        """Salva o candle no banco de dados quando o periodo se encerra. Isso através de uma condição onde é verificado
        se o tempo atual é igual ou maior(em questão de milisegundos) que o tempo de fechamento de candle(definido
        pelo método define_finishing_time()
        :param: Valor atual da criptomoeda
        """
        if self.time_now().replace(microsecond=0) >= self.define_finishing_time():
            self.send_database()
            self.initial_time = self.time_now()
            self.opening = current_price
            self.minimum = current_price
            self.maximum = current_price
            self.close = current_price
            # Repare que após os dados serem enviados ao banco de dados, chamamos os valores atuais para a lógica
            # do candle continuar sendo definida corretamente
            logger.info(f"CANDLE de {self.crypto} com período {self.frequency} registrado")

    def set_attributes(self, current_price: float):
        """
        Atribui os valores ao candle dado baseado no retorno da API Poloniex e condições do metódo
        :param current_price: Valor atual da criptomoeda
        """
        if self.opening == 0.0:
            self.opening = current_price
        if self.minimum == 0.0:
            self.minimum = current_price
        if current_price < self.minimum:
            self.minimum = current_price
        if current_price > self.maximum:
            self.maximum = current_price
        if self.close != current_price:
            self.close = current_price
        logger.info(f"Candle de {self.crypto} no periodo {self.frequency} processado")

    def time_now(self):
        """
        :return: Retorna a hora atual
        """
        time = datetime.now()
        return time

    def define_finishing_time(self):
        """Define o momento de fechamento do Candle. O metódo recebe o horário atual e dependendo do período do Candle
        analisado, retorna o momento em que ele deve fechar. Se o Candle for 5 por exemplo, e o horário
        for 12:38, é fechado um Candle de 5 minutos ás 12:40 para que o ciclo ocorra de acordo com o modelo comum de
        Candlesticks.
        :return: Retorna o momento em que o candle deve ser finalizado
        """
        candle_time = self.initial_time
        minute = int(candle_time.strftime("%M"))
        if minute % self.frequency != 0:
            while minute % self.frequency != 0:
                minute += 1
            # Essa condição garante que caso o horario atual + período seja maior que 59 minutos, a hora é trocada
            # e o minuto definido como 0
            if minute >= 60:
                candle_time = candle_time + timedelta(minutes=self.frequency)
                minute = 0
        else:
            minute += self.frequency
            if minute >= 60:
                candle_time = candle_time + timedelta(minutes=self.frequency)
                minute = 0
        return candle_time.replace(minute=minute, second=0, microsecond=0)

    def send_database(self):
        """Verifica se a conexão com o banco de dados esta estabelecida para então realizar o envio das
        informações"""
        with Candlestick.db_connection.cursor() as cursor:
            time_for_sql = self.time_now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(f"""insert into candlestick values (default, '{self.crypto}',
                {self.frequency}, '{time_for_sql}', {self.opening}, {self.maximum}, {self.minimum}, {self.close});""")
            Candlestick.db_connection.commit()

