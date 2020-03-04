## Dependent
* python3 
* pip 
* sqlite3

## Quick start
### 创建测试数据库和数据
```shell script
make test-data
```
### 启动服务
```shell script
make start
```
默认5000端口

### 调用接口
example:
获取user_id为1的用户的信息流
```shell script
curl 127.0.0.1:5000/api/my_feed/1/1
```

