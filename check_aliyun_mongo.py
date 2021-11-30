#coding=UTF-8
from aliyunsdkcore import client
from aliyunsdkdds.request.v20151201.DescribeDBInstancePerformanceRequest import DescribeDBInstancePerformanceRequest
import json,sys,datetime


ID = '<ID>'
Secret = '<Secret>'
RegionId = 'cn-beijing'

clt = client.AcsClient(ID,Secret,RegionId)

Type = sys.argv[1]
DBInstanceId = sys.argv[2]
Key = sys.argv[3]
ReplicaSetRole = sys.argv[4]

# 阿里云返回的数据为UTC时间，因此要转换为东八区时间。其他时区同理。
UTC_End = datetime.datetime.today() - datetime.timedelta(hours=8)
UTC_Start = UTC_End - datetime.timedelta(minutes=25)

StartTime = datetime.datetime.strftime(UTC_Start, '%Y-%m-%dT%H:%MZ')
EndTime = datetime.datetime.strftime(UTC_End, '%Y-%m-%dT%H:%MZ')

def GetResourceUsage(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole):
    Performance = DescribeDBInstancePerformanceRequest()
    Performance.set_accept_format('json')
    Performance.set_DBInstanceId(DBInstanceId)
    Performance.set_Key(MasterKey)
    Performance.set_StartTime(StartTime)
    Performance.set_EndTime(EndTime)
    Performance.set_ReplicaSetRole(ReplicaSetRole)
    PerformanceInfo = clt.do_action_with_exception(Performance)
    Info = json.loads(PerformanceInfo)
    # print(Info)
    Value = Info['PerformanceKeys']['PerformanceKey'][0]['PerformanceValues']['PerformanceValue'][-1]['Value']
    # print(Value)
    Value = str(Value).split('&')[IndexNum]
    # print Value
    print(float(Value) * 1048576)

def GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole):
    Performance = DescribeDBInstancePerformanceRequest()
    Performance.set_accept_format('json')
    Performance.set_DBInstanceId(DBInstanceId)
    Performance.set_Key(MasterKey)
    Performance.set_StartTime(StartTime)
    Performance.set_EndTime(EndTime)
    Performance.set_ReplicaSetRole(ReplicaSetRole)
    PerformanceInfo = clt.do_action_with_exception(Performance)
    Info = json.loads(PerformanceInfo)
    # print(Info)
    Value = Info['PerformanceKeys']['PerformanceKey'][0]['PerformanceValues']['PerformanceValue'][-1]['Value']
    # print(Value)
    print(str(Value).split('&')[IndexNum])

if (Type == 'Disk'):
    #总使用空间
    if (Key == 'total_used_size'):
        MasterKey = 'MongoDB_DetailedSpaceUsage'
        IndexNum = 0
        GetResourceUsage(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #数据磁盘使用空间
    if (Key == 'data_size'):
        MasterKey = 'MongoDB_DetailedSpaceUsage'
        IndexNum = 1
        GetResourceUsage(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #日志磁盘使用空间
    if (Key == 'log_size'):
        MasterKey = 'MongoDB_DetailedSpaceUsage'
        IndexNum = 2
        GetResourceUsage(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #WiredTiger平均每秒钟从内存读取的数据量
    if (Key == 'byres_read_into_cache'):
        MasterKey = 'MongoDB_Wt_Cache'
        IndexNum = 0
        GetResourceUsage(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #WiredTiger平均每秒钟写入到内存中的数据量
    if (Key == 'bytes_written_from_cache'):
        MasterKey = 'MongoDB_Wt_Cache'
        IndexNum = 1
        GetResourceUsage(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #WiredTiger设置的最大内存量（Bytes）
    if (Key == 'maximun_bytes_configured'):
        MasterKey = 'MongoDB_Wt_Cache'
        IndexNum = 2
        GetResourceUsage(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
elif (Type == 'Performance'):
    #CPU使用率
    if (Key == 'cpuusage'):
        MasterKey = 'CpuUsage'
        IndexNum = 0
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #CPU使用率
    elif (Key == 'memoryusage'):
        MasterKey = 'MemoryUsage'
        IndexNum = 0
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #IOPS使用量 
    elif (Key == 'mongodb_iops'):
        MasterKey = 'MongoDB_IOPS'
        IndexNum = 0
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #IOPS使用率 
    elif (Key == 'iops_usage'):
        MasterKey = 'IOPSUsage'
        IndexNum = 0
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #平均每秒Insert语句执行个数
    elif (Key == 'insert'):
        MasterKey = 'MongoDB_Opcounters'
        IndexNum = 0
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #平均每秒query语句执行个数 
    elif (Key == 'query'):
        MasterKey = 'MongoDB_Opcounters'
        IndexNum = 1
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #平均每秒update语句执行个数
    elif (Key == 'update'):
        MasterKey = 'MongoDB_Opcounters'
        IndexNum = 2
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #平均每秒delete语句执行个数
    elif (Key == 'delete'):
        MasterKey = 'MongoDB_Opcounters'
        IndexNum = 3
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #平均每秒getmore语句执行个数
    elif (Key == 'getmore'):
        MasterKey = 'MongoDB_Opcounters'
        IndexNum = 4
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #平均每秒command语句执行个数
    elif (Key == 'command'):
        MasterKey = 'MongoDB_Opcounters'
        IndexNum = 5
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole) 
    #当前总连接数
    elif (Key == 'total_conn'):
        MasterKey = 'MongoDB_Connections'
        IndexNum = 0
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #Cursors total_open
    elif (Key == 'cursors_total_open'):
        MasterKey = 'MongoDB_Cursors'
        IndexNum = 0
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #Cursors timed_out
    elif (Key == 'cursors_timed_out'):
        MasterKey = 'MongoDB_Cursors'
        IndexNum = 1
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #平均每秒钟的输入流量
    elif (Key == 'mongodb_network_in'):
        MasterKey = 'MongoDB_Network'
        IndexNum = 0
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #平均每秒钟的输出流量
    elif (Key == 'mongodb_network_out'):
        MasterKey = 'MongoDB_Network'
        IndexNum = 1
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #平均每秒钟的请求量
    elif (Key == 'mongodb_network_num_request'):
        MasterKey = 'MongoDB_Network'
        IndexNum = 2
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #所有全局锁的等待队列长度
    elif (Key == 'mongodb_global_lock_current_queue_total'):
        MasterKey = 'MongoDB_Global_Lock_Current_Queue'
        IndexNum = 0
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #全局读锁的等待队列长度
    elif (Key == 'mongodb_global_lock_current_queue_readers'):
        MasterKey = 'MongoDB_Global_Lock_Current_Queue'
        IndexNum = 1
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #全局写锁的等待队列长度
    elif (Key == 'mongodb_global_lock_current_queue_writers'):
        MasterKey = 'MongoDB_Global_Lock_Current_Queue'
        IndexNum = 2
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    
    #主备延时
    elif (Key == 'mongodb_repl_lag'):
        MasterKey = 'MongoDB_Repl_Lag'
        IndexNum = 0
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #IO延迟
    elif (Key == 'mongodb_iocheck_cost'):
        MasterKey = 'MongoDB_Iocheck_Cost'
        IndexNum = 0
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    
    #磁盘空间使用率
    elif (Key == 'diskusage'):
        MasterKey = 'DiskUsage'
        IndexNum = 0
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #写并发请求数
    elif (Key == 'write_concurrent_trans_out'):
        MasterKey = 'MongoDB_Wt_Concurrent_Trans'
        IndexNum = 0
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #读并发请求数
    elif (Key == 'read_concurrent_trans_out'):
        MasterKey = 'MongoDB_Wt_Concurrent_Trans'
        IndexNum = 1
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #可用的写并发请求数
    elif (Key == 'write_concurrent_trans_available'):
        MasterKey = 'MongoDB_Wt_Concurrent_Trans'
        IndexNum = 2
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
    #可用的读并发请求数
    elif (Key == 'read_concurrent_trans_available'):
        MasterKey = 'MongoDB_Wt_Concurrent_Trans'
        IndexNum = 3
        GetPerformance(DBInstanceId,MasterKey,IndexNum,StartTime,EndTime,ReplicaSetRole)
        
        
    

