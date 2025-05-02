import pandas as pd
from clickhouse_driver import Client

# 1) Load CSV, drop index column
df = pd.read_csv("data.csv", index_col=0)

# 2) Normalize column names: strip whitespace and replace non-breaking spaces
df.columns = df.columns.str.strip().str.replace('\u00A0', ' ')

# 3) Print columns for debug (remove or comment out after)
print("Columns before mapping:", df.columns.tolist())

# 4) Map last three columns by position to ensure capture
last3 = list(df.columns[-3:])
# Prepare mapping dict with position-based keys
col_map = {last3[0]: 'metro_built', last3[1]: 'control1', last3[2]: 'control2'}

# 5) Define general mapping for other columns based on keywords
def map_col(col):
    lower = col.lower()
    if 'uik' in lower:
        return 'uik'
    if 'registered' in lower and lower.endswith('x'):
        return 'registered_x'
    if 'indoors_x' in lower:
        return 'ballots_indoor_x'
    if 'home_x' in lower:
        return 'ballots_home_x'
    if 'valid_ballots_x' in lower:
        return 'valid_ballots_x'
    if 'путин' in lower and lower.endswith('x'):
        return 'putin_votes_x'
    if 'registered' in lower and lower.endswith('y'):
        return 'registered_y'
    if 'indoors_y' in lower:
        return 'ballots_indoor_y'
    if 'home_y' in lower:
        return 'ballots_home_y'
    if 'valid_ballots_y' in lower:
        return 'valid_ballots_y'
    if 'путин' in lower and lower.endswith('y'):
        return 'putin_votes_y'
    if 'явка' in lower and '2012' in lower:
        return 'turnout_2012'
    if 'поддержка' in lower and '2012' in lower:
        return 'support_2012'
    if 'явка' in lower and '2018' in lower:
        return 'turnout_2018'
    if 'поддержка' in lower and '2018' in lower:
        return 'support_2018'
    if 'coords' in lower:
        return 'coords'
    # fallback: return original
    return col

# 6) Build full mapping: general + positional override for last3
full_map = {col: map_col(col) for col in df.columns}
full_map.update(col_map)

# Apply rename
df = df.rename(columns=full_map)

# 7) Verify rename result
expected = ['uik','registered_x','ballots_indoor_x','ballots_home_x','valid_ballots_x','putin_votes_x',
            'registered_y','ballots_indoor_y','ballots_home_y','valid_ballots_y','putin_votes_y',
            'turnout_2012','support_2012','turnout_2018','support_2018',
            'metro_built','control1','control2','coords']
missing = [c for c in expected if c not in df.columns]
if missing:
    raise RuntimeError(f"Missing columns after rename: {missing}")

# 8) Parse coords into lat/lon
if 'coords' in df.columns:
    df[['lat','lon']] = (
        df['coords'].str.strip('()').str.split(',', expand=True).astype(float)
    )

# 9) Connect to ClickHouse
client = Client(host='localhost', database='default', user='default', password='default')

# 10) Create table
ddl = '''
CREATE TABLE IF NOT EXISTS election_data (
    uik String,
    registered_x UInt32,
    ballots_indoor_x UInt32,
    ballots_home_x UInt32,
    valid_ballots_x UInt32,
    putin_votes_x UInt32,
    registered_y UInt32,
    ballots_indoor_y UInt32,
    ballots_home_y UInt32,
    valid_ballots_y UInt32,
    putin_votes_y UInt32,
    turnout_2012 Float32,
    support_2012 Float32,
    turnout_2018 Float32,
    support_2018 Float32,
    metro_built UInt8,
    control1 UInt8,
    control2 UInt8,
    lat Float64,
    lon Float64
) ENGINE = MergeTree ORDER BY uik
'''
client.execute(ddl)

# 11) Insert data
cols = ['uik','registered_x','ballots_indoor_x','ballots_home_x','valid_ballots_x','putin_votes_x',
        'registered_y','ballots_indoor_y','ballots_home_y','valid_ballots_y','putin_votes_y',
        'turnout_2012','support_2012','turnout_2018','support_2018',
        'metro_built','control1','control2','lat','lon']
data = [tuple(row) for row in df[cols].itertuples(index=False)]
client.execute('INSERT INTO election_data VALUES', data)

print("✅ All data loaded with English names and positional last3 mapping")
