import pandas as pd
from clickhouse_driver import Client

# Загружаем CSV
df = pd.read_csv("/Users/sergeybudygin/Desktop/micha/itog_with_groups.csv", index_col=0)  # замени на свой путь

# Парсим координаты
df[['lat', 'lon']] = df['coords_x'].str.strip("()").str.split(",", expand=True).astype(float)
# Подключение
client = Client(host='localhost', database="default", password="default")



client.execute('DROP TABLE IF EXISTS election_data')
# Создаём таблицу
client.execute('''
CREATE TABLE IF NOT EXISTS election_data (
    uik String,
    num_of_registered_voters_x UInt32,
    num_of_ballots_given_away_on_voting_day_indoors_x UInt32,
    num_of_ballots_given_away_on_voting_day_at_home_x UInt32,
    num_of_valid_ballots_x UInt32,
    putin_votes_x UInt32,
    coords_x String,
    num_of_registered_voters_y UInt32,
    num_of_ballots_given_away_on_voting_day_indoors_y UInt32,
    num_of_ballots_given_away_on_voting_day_at_home_y UInt32,
    num_of_valid_ballots_y UInt32,
    putin_votes_y UInt32,
    turnout_2012 Float32,
    support_2012 Float32,
    turnout_2018 Float32,
    support_2018 Float32,  
    metro_build UInt32,
    kont_1 UInt32,
    kont_2 UInt32,
    lat Float64,
    lon Float64
) ENGINE = MergeTree ORDER BY uik
''')

# Подготовка к вставке
records = df.to_dict('records')
data = [tuple(rec.values()) for rec in records]

# Вставка данных
client.execute('''
INSERT INTO election_data VALUES
''', data)

print("✅ Данные успешно загружены в ClickHouse")



# Построено метро - было постояно метро с 2012 по 2018
# Контрольная1 - метро было до 2012 построено
# Контрольная2  - не было метро до 2018

# постой нам регрессия в графаче через sql запрос - определи оси x и y
# наша задача понять изменение в к-во голосов в зависимости от гот опостроили метро или нет - как нам быть