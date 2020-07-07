import global_test as gs
import test1


if __name__ == '__main__':
	gs._init()
	gs.set_value('key','123456')
	print('before:' + gs.get_value('key'))
	test1.change_key()
	print('after:' + gs.get_value('key'))