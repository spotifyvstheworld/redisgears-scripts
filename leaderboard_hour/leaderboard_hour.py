import re
import os
from gearsclient import GearsRemoteBuilder as GearsBuilder
from gearsclient import execute, atomic
from dotenv import load_dotenv
import redis

load_dotenv()

channelName = lambda x: re.search('artist:(.*)', x).group(1)

# format dict before being run in foreach
def format(x):
    data = {}
    data["artist"] = x["key"]
    if 'max_count' in x["value"]:
        data["max_count"] = int(x['value']['max_count'])
    return data

# updates hourly leaderboard. Done by deleting it, filling it with the highest counts of
# each artist within the hour, and resetting the max counts field of each artist
def updateHourlyLeaderboard(x):
    with atomic():
        execute('DEL', 'leaderboard_hour')
        execute('ZADD', 'leaderboard_hour', x["max_count"], channelName(x["artist"]))
        execute('HSET', x["artist"], "max_count", 0)
    return x

conn = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"))
gb = GearsBuilder(reader='KeysReader', defaultArg='artist', r=conn)

gb \
 .map(format) \
 .foreach(updateHourlyLeaderboard)

res = gb.run('artist:*')

for r in res[0]:
    print(r)

# {'event': None, 'key': 'artist:disclosure', 'type': 'hash', 'value': {'count': '0', 'max_count': 3}}