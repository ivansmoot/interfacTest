## 接口测试
- 用FastAIP本地起一个接口，随机返回，返回规则用一个dict传入
- 对该接口进行多次调用
- 启动本地接口  
`uvicorn interfaceServer:server --reload --port 6565`

### *#JMeter*  
`./jmeter -n -t "/Users/yifan/Desktop/lottery_get.jmx" -l /Users/yifan/desktop/lottery_get.jtl`
- 命令改一改就可以了，然后用JMeter新建一个线程组，建一个聚合报告，打开jtl文件就可以了
