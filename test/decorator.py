#!usr/bin/env python
# -*- coding: utf-8 -*-
# fileName: decorator.py
# time: 2019/12/17 01:11

__author__ = '33504'
# /usr/bin/env Python3
# -*- encoding:UTF-8 -*-
# decoretor.py

import functools  # 导入 functools 模块


def verification(level):  # 是否验证用户名和密码  True or False
	def decorator(func):  # 装饰器 func是要被装饰的 函数
		@functools.wraps(func)  # 我们可以对func进行装饰重写的同时，保持func本身不发生改变
		def login(User, Pwd, **others):  # 针对登录模块 进行判断用户和密码 -- 装饰开始
			"""Here's a doc login"""
			nStatu = 0  # 登录状态 0：失败  1：成功
			if level:
				print('开启用户和密码验证：')
				if User == 'appleyk' and Pwd == '123456':
					print('登录成功！')
					nStatu = 1
				else:
					print('登录失败！')
					nStatu = 0
			else:
				print('不开启验证，直接登录！')
				nStatu = 1
			print('用户名：', User, ',密码：', Pwd)
			func(User, Pwd, **others)  # 这里我们打印最开始func定义的功能,其实执行的就是Test_login，这里是什么也不输出（Pass）
			print('登录过程结束.........decorator is over！')  # func结束后，我们装饰的目的也就结束了
			return nStatu  # 登录判断 返回一下 登录状态值

		return login  # 返回这个装饰效果（登录验证函数--属于扩展功能）

	return decorator  # 返回装饰器（包装函数，这个函数在func运行期间，对其进行了扩展）


@verification(False)  # 注意 verification返回的是一个装饰器，这个装饰器对函数Test_login实现功能扩展
def test_login(User, Pwd, **others):
	"""Here's a doc Test_login"""
	pass


n = test_login('appleyk', '123456')
print("登录状态：", n)
print(test_login.__name__, ',注释标记：', test_login.__doc__)
