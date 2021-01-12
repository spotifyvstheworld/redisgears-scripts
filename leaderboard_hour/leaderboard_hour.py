import re
from gearsclient import GearsRemoteBuilder as GearsBuilder
from gearsclient import execute
from dotenv import dotenv_values
import redis

config = dotenv_values(".env")

def clean(x):
    channelName = lambda x: re.search('{channel:artist_channel/(.*)}', x).group(1)
    foo = {}
    foo["artist"] = channelName(x["key"])
    if 'fake_subscribers' in x["value"]:
        foo["count"] = int(x['value']['fake_subscribers']) 
    return foo

def leaderboard(x):
    print(x)
    execute('SET', 'working', 'yes')
    if 'artist' in x:
        execute('ZADD', 'leaderboard_hour', x["count"], x["artist"])

conn = redis.Redis(host=config["REDIS_HOST"], port=config["REDIS_PORT"])
gb = GearsBuilder(reader='KeysReader', defaultArg='{channel:artist_channel/*}', r=conn)

gb \
 .map(clean)

gb.foreach(leaderboard)

res = gb.run('{channel:artist_channel/*}')

for r in res[0]:
    print(r)
    print('{}: {}'.format(r['artist'], r['count']))