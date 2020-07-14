#使用方法:
#例如：python mytool.py fun arg
#        1 批量修改文件名 + 文件夹路径 + 前缀
#        2 缩放图片 + 文件夹路劲或是图片路劲 + 缩放大小
#........3.TexturePacker  散图打包成一张整图，或是多个文件夹打包成一张整图
#        4 批量打包   打包成多张整图
#        5.plist图片集反编译
#        6 plist图片集批量反编译

import sys
import os
import getopt

from picEdit import PicEdit

version = '1.0.0'

if __name__ == "__main__":
	try:
		opts,args = getopt.getopt(sys.argv[1:],'-h-f:-v',['help','funtion=','version'])
	except getopt.GetoptError:
		print ('输入 myTool.py --help 或是输入 myTool.py -h')
		exit(2)
	for opt_name,opt_value in opts:
		if opt_name in ('-h','--help'):
			print("使用方法:\n \
				1 批量修改文件名 + 文件夹路径 + 前缀 \n \
				2 缩放图片 + 文件夹路劲或是图片路劲 + 缩放大小 \n \
				3.TexturePacker  散图打包成一张整图，或是多个文件夹打包成一张整图 \n \
				4 批量打包   打包成多张整图 \n \
				5.plist图片集反编译 \n \
				6 plist图片集批量反编译")
			exit()
		elif opt_name in ('-v','--version'):
			print("myTool",version)
			exit()

	if len(sys.argv) == 1:
		print("没有参数")
		exit()
	fun = sys.argv[1]
	edit = PicEdit()
	if int(fun) == 1:
		path = sys.argv[2]
		if os.path.exists(path):
			if len(sys.argv) == 3:
				edit.batchRename(path)
			elif len(sys.argv) == 4:
				pre_fix = sys.argv[3]
				edit.batchRename(path, pre_fix)
		else:
			print("不存在路径")
	elif int(fun) == 2:
		path = sys.argv[2]
		scale = int(sys.argv[3])
		print(list(sys.argv))
		if os.path.exists(path):
			if os.path.isdir(path):
				edit.batchScale(path, scale)
			elif os.path.isfile(path):
				edit.scale(path, scale)
		else:
			print("不存在路径")
	elif int(fun) == 3:
		path = sys.argv[2]
		if os.path.exists(path):
			edit.texPacker(path)
		else:
			print("不存在路径")

	elif int(fun) == 4:
		path = sys.argv[2]
		if os.path.exists(path):
			edit.batchTexPacker(path)
		else:
			print("不存在路径")
	elif int(fun) == 5:
		file_path = sys.argv[2]
		png_path = sys.argv[3]
		edit.unTexPacker(file_path, png_path )
	elif int(fun) == 6:
		path = sys.argv[2]
		if os.path.exists(path):
			edit.batchUnTexPaker(path)
		else:
			print("不存在路径")












		