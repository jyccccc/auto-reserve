# auto-reserve
用Python实现的自动预约

### 项目准备

#### 基本思路

我的初步思路是想通过抓取登录、预约、签到的网络通信包，分析包中的各个参数并通过requests库手动构造出request，从而实现自动预约和签到

**但是！！！**

在构造request的过程中，必须要包含一个`ASP.NET_SessionId`字段，而该字段的获得必须要登录到预约端并查询座位列表之后，才可以获得该字段。而由于**HTTP是无状态协议**，当我发送登录请求进入预约端之后，不能（或者是很麻烦）采用查询座位列表的方式来获取到该字段，我直接放弃了通过request来得到`ASP.NET_SessionId`字段。

接下来，我使用了自动化测试工具`selenium`，直接模拟浏览器（本想模拟到能够获取到`ASP.NET_SessionId`，再使用`request`方法，奈何这个思路较我之前的思路简单多了），**并最终将问题解决**！

##### 预约请求

见`/requests/*.har`

##### 登录验证

encrypt.js 加密

- 盐值：var pwdDefaultEncryptSalt = "aBlilcaTuIWjSL0k";

![image-20200702105348638](C:\Users\Mar.J\AppData\Roaming\Typora\typora-user-images\image-20200702105348638.png)

##### 签到/签退

每个教室位置：

```
#calendar_637292801495025777 > div > div.fp_content.fp-show-guides.fp-hide-obj-title > div.fp-user.fp-user-con > div:nth-child(1)
#calendar_637292801495025777 > div > div.fp_content.fp-show-guides.fp-hide-obj-title > div.fp-user.fp-user-con > div:nth-child(2)
······
```

研修教室162：`http://update.unifound.net/wxnotice/s.aspx?c=100460316_Seat_101088490_1CM`

研修教室161：`http://update.unifound.net/wxnotice/s.aspx?c=100460316_Seat_101088489_1CM`

研修教室160：`http://update.unifound.net/wxnotice/s.aspx?c=100460316_Seat_101088488_1CM`

url格式：

- `http://update.unifound.net/wxnotice/s.aspx?c=100460316_Seat_{seat_id}_1CM`
- 参数：seat_id