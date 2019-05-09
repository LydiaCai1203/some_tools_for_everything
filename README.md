# some_tools_for_everything
some tools for becoming a better developer(实际上是因为开直播不能总鸽大家所以特意开了个库放直播中写的小脚本,或者是自己觉得有意思的，平时实用性会比较高的脚本。)

### cheat_checkin_out
##### 这个脚本实现的时间大概是两个月以前了
```python
1. app: E-Mobile
2. params: USERNAME PASSWORD 分别写自己的用户名和密码
3. tips: 
    a. 可能不同的公司使用的host不同 BASE_URL = 'http://106.15.179.143:89/client.do' 中的host部分可能需要替换
    b. 打卡的原理就是在请求体中传入正确的经纬度参数
    float: latitude      # 经度
    float: longitude     # 纬度
4. 第一版比较粗糙没有判断周六日和节假日，没有换掉ip，配置文件写死等问题，第二版的时候我会修复这些问题
```




