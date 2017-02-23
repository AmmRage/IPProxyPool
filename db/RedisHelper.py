# coding:utf-8
from db.ISqlHelper import ISqlHelper
import redis
from config import DB_CONFIG


class RedisHelper(ISqlHelper):
    def __init__(self):
        self.r = redis.StrictRedis.from_url(DB_CONFIG['DB_CONNECT_STRING'])
        self.storeSetName = 'proxys'

    def init_db(self):
        pass

    def drop_db(self):
        self.r.delete(self.storeSetName)

    def insert(self, value):
        self.r.sadd(self.storeSetName, value)

    def delete(self, conditions=None):
        deleteNum = 0
        if conditions:
            for proxy in self.r.smembers(self.storeSetName):
                if conditions['ip'] == proxy['ip'] and conditions['port'] == proxy['port']:
                    self.r.srem(self.storeSetName, proxy)
                    deleteNum = 1
                    break
        else:
            deleteNum = 0
        return ('deleteNum', deleteNum)

    def update(self, conditions, scoreValue):
        updateNum = 0
        if conditions:
            for proxy in self.r.smembers(self.storeSetName):
                if conditions['ip'] == proxy['ip'] and conditions['port'] == proxy['port']:
                    self.r.srem(self.storeSetName, proxy)
                    proxy['score'] = scoreValue
                    self.r.sadd(self.storeSetName, proxy)
                    updateNum = 1
                    break
        else:
            updateNum = 0
        return {'updateNum': updateNum}

    def select(self, count=None, conditions=None):
        retList = list()

        if conditions:
            count = conditions['count']

            types = conditions['types']
            protocol = conditions['protocol']
            country = conditions['country']
            area = conditions['area']

            for proxy in self.r.smembers(self.storeSetName):
                if types:
                    if proxy ['type'] != types:
                        continue
                if protocol:
                    if proxy ['protocol'] != protocol:
                        continue
                if country:
                    if proxy ['country'] != country:
                        continue
                if area:
                    if proxy ['area'] != area:
                        continue
                retList.append(proxy)

            if len(retList) > count:
                return retList[0:count]
            else:
                return retList
        return retList

    def close(self):
        pass


if __name__ == '__main__':
    r = redis.StrictRedis.from_url(DB_CONFIG['DB_CONNECT_STRING'])
    # print(r.sadd('foo', 'bar'))
    # print(r.srem('foo', 'bar'))
    # print(len(r.keys()))

    proxys = r.smembers('proxys')
    print(len(proxys))
    for proxy in proxys:
        print(proxy)
