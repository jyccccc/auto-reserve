def init_vars(path):
	res = []
	with open(path, "r",encoding="utf-8") as f:
		for line in f:
			# print(line)
			res.append(line)
	for i in res:
		if(i != "\n"):
			print(i)
init_vars("..//input//input.txt")


def tips():
	username = input("输入学号：")
	password = input("输入密码（办事大厅）：")
	start_date = int(input("输入开始预约的日期："))
	end_date = int(input("输入结束预约的日期（不包含该天）："))
	area = input("输入预约的区域：")
	pos = input("输入预约的位置：")
	email = input("输入发送的邮件通知：")
	url = input("输入座位的二维码地址：")
	aliyun_u = input("输入阿里云邮箱服务的发件人地址：")
	aliyun_p = input("输入阿里云邮箱服务的发件人密码：")
	aliyun_r = input("输入阿里云邮箱服务的回复地址：")