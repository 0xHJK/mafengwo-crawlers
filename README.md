# 马蜂窝分布式爬虫系统

设计这个爬虫系统的主要目的是，完整快速地获取国内所有旅游目的地和旅游景点，包括名称、介绍、图片、相关攻略等。

主要使用到的技术（工具／语言／库）包括：Docker, Redis, MySQL, Python, requests, peewee等。

# 使用方式

下载程序
```
git clone https://github.com/0xHJK/mafengwo-crawlers
```

修改`src/common/chameleon.py`里的代理列表（因为代理具有时效性），代理获取方式可以参考：

<https://github.com/0xHJK/proxy-spider>

运行
```
docker-compose up
```

扩展节点数量（根据自己需要扩展）
```
#扩展获取城市列表节点为10个
docker-compose scale citylist=10

#扩展获取景点列表节点为20个
docker-compose scale citylist=20

#扩展获取景点信息节点为30个
docker-compose scale citylist=30
```

重新运行
```
docker-compose up
```

# 运行效果
![](./preview/1.png)
![](./preview/2.png)
![](./preview/3.png)
![](./preview/4.png)
![](./preview/5.png)
![](./preview/6.png)
![](./preview/7.png)
![](./preview/8.png)
![](./preview/9.png)
![](./preview/10.png)
![](./preview/11.png)
![](./preview/12.png)
![](./preview/13.png)



