#coding=UTF-8
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
import json

from aliyunsdkcore import client
from  aliyunsdkdds.request.v20151201 import DescribeDBInstancesRequest
import json

ID = '<ID>'
Secret = '<Secret>'
RegionId = 'cn-beijing'

clt = client.AcsClient(ID,Secret,RegionId)

DBInstanceIdList = []
DBInstanceIdDict = {}
ZabbixDataDict = {}

def GetMongoList():
    MongoRequest = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
    MongoRequest.set_accept_format('json')
    MongoInfo = clt.do_action_with_exception(MongoRequest)
    for MongoInfoJson in json.loads(MongoInfo)['DBInstances']['DBInstance']:
        DBInstanceIdDict = {}
        try:
            DBInstanceIdDict["{#DBINSTANCEID}"] = MongoInfoJson['DBInstanceId']
            DBInstanceIdDict["{#DBINSTANCEDESCRIPTION}"] = MongoInfoJson['DBInstanceDescription']
            DBInstanceIdList.append(DBInstanceIdDict)
        except Exception as e:
            print(Exception, ":", e)
            print("Please check the Mongodb alias !Alias must not be the same as DBInstanceId！！！")

GetMongoList()
ZabbixDataDict['data'] = DBInstanceIdList
print(json.dumps(ZabbixDataDict))