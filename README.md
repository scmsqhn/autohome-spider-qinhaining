# zhihu_spider
### 大规模知乎用户爬虫
* （１）使用python的request模块获取html页面，注意要修改自己的cookie，使得我们更像是使用浏览器访问
* （２）使用xpath模块从html中提取需要的关键信息（姓名，职业，居住地，关注人等）
* （３）使用redis作为队列，很好的解决并发和大规模数据的问题（可以分布式）
* （４）使用bfs宽度优先搜索，使得程序得以不断扩展持续搜索用户
* （５）数据存储至no-sql数据库：mongodb（高效轻量级并且支持并发）
* （６）使用python的进程池模块提高抓取速度
* （７）使用csv,pandas,matplotlib模块进行数据处理（需要完善）
    
### 联系作者
* 具体可以参考我的博客：http://blog.csdn.net/nk_test/article/details/51330971
* 运行的时候需要指定参数 ： print_data_out 表示输出至屏幕；store_data_to_mongo代表存入mongodb数据库
  同时依赖redis,mongodb以及python的部分模块，请自行安装。
     

### 数据展示：
![image](https://github.com/Tachone/zhihu_spider/blob/master/career.png)
![image](https://github.com/Tachone/zhihu_spider/blob/master/city.png)
![image](https://github.com/Tachone/zhihu_spider/blob/master/title.png)
---
# 汽车之家爬虫
## 使用ipproxys 搭建一个完整的爬虫框架
## 品牌价值 车辆价格预测

## 数据清洗方式 
1. number 计入单项
2. 非number展开选项,使用one-hot码

## 关键数据项
厂商
发动机
变速箱
车身结构
综合油耗
车身结构
油箱容积
行李箱容积
排量
进气形式
气缸数
每缸气门数
最大马力
最大功率
燃油标号
档位个数
轮胎规格
后轮胎规格
主副驾驶气囊
前后排侧气囊
前后排头部气囊
膝部气囊
胎压监测
零胎压继续行驶
安全带提示
儿童座椅接口
abs
制动力分配
刹车辅助
牵引力控制
车身稳定控制
并线辅助
车道偏离预警系统
主动刹车
夜视系统
前后驻车雷达
倒车视频
全景摄像头
定速巡航
自适应巡航
自动泊车
发动机启停
上坡辅助
自动注册
