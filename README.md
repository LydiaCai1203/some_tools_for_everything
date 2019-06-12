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

### auto_follow_in_github
#### 这个小脚本该不会该死的要烂尾了吧哈哈哈哈哈 暂时并不想搞了，爸爸只想快点看书然后走人。
#### get_sesson_api: https://github.com/session post
```python
form:
    commit: Sign in
    utf8: ✓
    authenticity_token: pass
    password: pass
    webauthn-support: supported
```
#### login_api: https://github.com/login
```python

```

### broke__jsl_clearance
#### 这个项目主要针对的是破解银保监，破解加速乐的反爬虫机制
#### 不足：
> 1. 正则表达式写的不够高级，现在看上去还比较弱智，目前只是解决了基础问题
> 2. 虽然用了面向对象的写法，但是没有分文件写，看上去还是比较混乱，暂时不想管了
> 3. 因为我没学过js，所以无法通过使用python来实现js脚本相同功能，这是一个短板吧
#### 仅供个人学习参考，欢迎发邮件或者加QQ与我交流，如果合适的工作机会，当然也欢迎提供给我～～～～～哈哈哈哈




