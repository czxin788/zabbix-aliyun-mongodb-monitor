# 功能
  zabbix通过阿里云api自动发现阿里云mongodb的性能监控
# 使用方法
## 环境要求
 python2或者python3
## 模块安装
`pip install aliyun-python-sdk-core`

`pip install aliyun-python-sdk-rds==2.4.9`

`pip install aliyun-python-sdk-dds==3.5.2`
## 使用方法
从阿里云控制台获取 AccessKey ,并修改两个脚本中的 ID 与 Secret
修改区域 RegionId
将两个脚本放置于以下目录

```
/etc/zabbix/scripts
chmod +x /etc/zabbix/scripts/*
```

修改zabbix-agentd.conf，添加以下内容
```
#aliyun mongodb montor
UserParameter=aliyun.mongodb.discovery,python /etc/zabbix/scripts/discovery_mongodb.py
UserParameter=check.aliyun.mongodb[*],python /etc/zabbix/scripts/check_aliyun_mongo.py $1 $2 $3 $4
```

重启zabbix-agent
zabbix控制台导入模板，并关联主机
## 效果图
![image](https://user-images.githubusercontent.com/13861904/143971718-d390e456-e4ce-401c-b099-d6d01abd3763.png)

