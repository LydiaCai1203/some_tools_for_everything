# some_tools_for_everything
some tools for becoming a better developer(实际上是因为开直播不能总鸽大家所以特意开了个库放直播中写的小脚本,或者是自己觉得有意思的，平时实用性会比较高的脚本。)

---
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

---
### auto_follow_in_github
##### 大概是一个月前开的坑吧 现在才填上 这个脚本主要实现 关注 拥有50stars以上的repo的大佬
##### 非要说意义在哪里的话 意义就是... 关注起来比较方便一点吧
```python
1. python follow_all_i_want.py
2. 输入你的github账号和密码以及你想要关注的前多少页的人。
```

---
### broke__jsl_clearance
#### 这个项目主要针对的是破解银保监，破解加速乐的反爬虫机制
#### 不足：
> 1. 正则表达式写的不够高级，现在看上去还比较弱智，目前只是解决了基础问题
> 2. 虽然用了面向对象的写法，但是没有分文件写，看上去还是比较混乱，暂时不想管了
> 3. 因为我没学过js，所以无法通过使用python来实现js脚本相同功能，这是一个短板吧

---
### jingdong_captcha_break
#### 这个项目也是之前做的 开源出来 破解了京东的滑块验证码
#### 这个东西的意义....
> 1. 你完全可以写一个爬虫，爬取折扣力度大的商品，然后再转手放到闲鱼上面卖，做中间商赚差价
> 2. 我快毕业啦！！！！！！
> 3. 在启动这个项目之前你需要装chromedriver 有一些环境都需要安装....最近一次试验大概是半个月前，也就是2019年6月，有时候不能一次成功，需要多来几遍。


---
### ip_ihuan_me
#### 这个项目主要是为了建立一个高可用的ip_pool服务的
#### 基本思路：
#### 1. 抓到ip.ihuan.me网站的验证码图片，然后运用在github上面找到的开源项目进行机器学习
#### 2. 由于ip.ihuan.me上面的代理都还算是高可用的ip，所以想用这个做一个ip_pool为反爬措施做的比较好的网站做服务
#### 3. 目前完成度只是抓到了ip.ihuan.me上面的验证码图片
#### 4. 但是验证码上面的字符不是固定的， 有5个，有6个字符的，进行机器学习的时候还是需要好好研究一下的
#### 5. 意义的话总觉得对于公司来说的话不是很大，但是对于个人开发者来说还是有用的，毕竟代理也挺贵的


---
### 
#### go_working
#### 主要是给王叔用来催别人干活用的
#### 基本思路:
> 1. 没什么思路，就是用itchat写一个小脚本，设置不同的催工语句，随机选择发一条，可以设置催工的时间间隔
> 2. 不需要什么反馈机制，毕竟回复的话微信app端也是看得见的

-----
## 如果有问题欢迎加我的QQ:1125862926，或者发邮件给我。
## 如果对你有帮助就给我点个star吧555555555




