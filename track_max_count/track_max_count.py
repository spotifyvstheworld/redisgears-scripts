import re
import os
from gearsclient import GearsRemoteBuilder as GearsBuilder
from gearsclient import execute, atomic
from dotenv import load_dotenv
import redis

load_dotenv()

def format(x):
    channelName = lambda x: re.search('artist:(.*)', x).group(1)
    data = {}
    data["artist"] = x["key"]
    if 'count' in x["value"]:
        data["count"] = int(x['value']['count'])
    return data

# updates max listener count of artist
def updateMaxCount(x):
    with atomic():
        maxCount = execute('hget', x["artist"], "max_count")
        if maxCount == None or int(x["count"]) > int(maxCount):
            execute('HSET', x["artist"], "max_count", x["count"])
    return x

conn = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"))
gb = GearsBuilder(reader='KeysReader', defaultArg='artist', r=conn)

gb \
 .map(format) \
 .foreach(updateMaxCount)

res = gb.register('artist:*')
print(res)
# res = gb.run('artist:*')

# for r in res[0]:
#     print(r)


# {'event': None, 'key': 'artist:disclosure', 'type': 'hash', 'value': {'count': '0'}}