import global_test as gs


def change_key():
	print('test1: ' + gs.get_value('key'))
	gs.set_value('key','123')
	print('test1 set key to: ',gs.get_value('key'))