# auto-reserve
技术结构：python + selenium + schedule + 阿里云邮件服务

### 项目结构

`/code_ubuntu`：服务器（阿里云ubuntu）的代码

`/code_windows`：windows下的代码

`/pre`：几个模块的demo

`/requests`：预约、登录request分析

### 项目总结

#### 基本思路

我的初步思路是想通过抓取登录、预约、签到的网络通信包，分析包中的各个参数并通过requests库手动构造出request，从而实现自动预约和签到

**但是！！！**

在构造request的过程中，必须要包含一个`ASP.NET_SessionId`字段，而该字段的获得必须要登录到预约端并查询座位列表之后，才可以获得该字段。而由于**HTTP是无状态协议**，当我发送登录请求进入预约端之后，不能（或者是很麻烦）采用查询座位列表的方式来获取到该字段，我直接放弃了通过request来得到`ASP.NET_SessionId`字段。

接下来，我使用了自动化测试工具`selenium`，直接模拟浏览器（本想模拟到能够获取到`ASP.NET_SessionId`，再使用`request`方法，奈何这个思路较我之前的思路简单多了），**并最终将问题解决**！

#### selenium

selenium的使用分启动/停止浏览器、元素定位、和元素交互三大块内容，具体内容见其文档：`https://selenium-python.readthedocs.io/index.html`

##### 启动/停止浏览器

两个注意点：

- **chromedriver的配置**：若没有配置环境变量，则需要指定`executable_path`，值为chromedriver的位置
- **无头浏览器的配置**（常用于命令行终端）：需要额外指定`chrome_options`，使用如下：

```python
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox') # 这个配置很重要
driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='/home/jyc/softwares/chromedriver')
```

##### 定位元素

定位元素根据**定位的方式**可分为：xpath、css_selector、id、classname、tagname、name等

> tips：使用chrome的元素定位可以直接获取到xpath和css_selector，但是往往都会比较麻烦，一般都是倾向于自己来找！

特别的，在定位元素时（不止于此）可以使用**显示和隐式等待**，实现方式如下：

```python
driver.implicitly_wait(10)  # 隐式等待
WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'username')))  # 显示等待
```

##### 和元素交互

能够交互的内容：

- 获取元素属性
- 填写内容：下拉框和基本输入框
- 点击
- ·······

特别需要注意的！！**当页面发生变化之后，元素是会过期的**！！因此，最好还是取一个就用一个（尤其是循环时），避免出现元素过期的情况！！

#### schedule

> schedule：An in-process scheduler for periodic jobs that uses the builder pattern for configuration. Schedule lets you run Python functions (or any other callable) periodically at pre-determined intervals using a simple, human-friendly syntax.
>
> API：https://schedule.readthedocs.io/en/stable/

简单来说，schedule就是一个**计时器**，适用于**各种定时任务**，包含了根据时间间隔、特定时间点重复任务，**使用极其简单**，当然也有一些缺陷，比如**不能处理有返回值的任务**

其他计时器的实现：

- `threading.timer`
- `APScheduler`：使用也同样很简单

#### 其他知识

##### 加密

- 前端可以使用`encrypt.js`进行加密解密，也可以加入`sault`值
- `https`的加密：内部是aes系列的非对称加密
- 解密：彩虹表（AES的“打表”）、各种在线解密网站

##### linux下后台执行任务

- screen：很强大，相当于新建了一个窗口，常用的几个命令：
  `screen -S name` 启动一个名字为name的screen
  `screen -S name -X quit` 删除某个session
  `screen -ls` 列出所有的screen
  `screen -r name或者id`，回到某个screen了（如不行先detached： screen -d name）
  `ctrl + a + d` 可以回到前一个screen，当时在当前screen运行的程序不会停止
- nohup：会将程序的输入和输出放到nohup.hut文件夹中，不适合需要交互的程序
- &：直接后台运行，但同样不适合交互

##### session和cookie

在实际的BS架构中是一个非常常见且实用的点，以后开发也要采用！

##### python的共享变量

类内部的共享：使用`global`关键字修饰即可

模块内部及跨模块的共享：定义一个共享变量管理类，具体内容见`module_share_var\`的demo

##### 阿里云的邮箱服务

域名：腾讯云的域名，1块/首年！

邮箱服务：邮箱服务端口使用80，25默认关闭的！每天200条以内免费！

SSL：阿里云免费！

##### python ide选择

数据分析和机器学习：jupyter

其他：sublime text

