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
        if conditions:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(self.params.get(key) == conditions.get(key))
            conditions = conditon_list
        pass
