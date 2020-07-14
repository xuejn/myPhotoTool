#作者 薛建男
#QQ:546321106
#定义了图片的4种批量处理

import os
import sys 
from PIL import Image
import configparser
import plistlib

class PicEdit():
	"""docstring for Pic"""
	def __init__(self):
		curpath = os.path.dirname(os.path.realpath(__file__))#获取当前路径
		configpath = os.path.join(curpath, "config.ini")
		self.conf = configparser.ConfigParser()
		self.conf.read(configpath, encoding="utf-8")
		self.outputPath = self.conf.get("texturePacker", "OUTPUT_PATH")
		#sections = conf.sections()
		
	def batchRename(self, path, preFix=''):
		#path 表示需要重命名的文件夹路径
		#os.listdir() 方法用于返回指定的文件夹包含的文件或文件夹的名字的列表。这个列表以字母顺序
		if os.path.exists(path) == False: #判断文件夹是否存在
			print("fail 不存在的文件夹")
			return
		print("开始重命名...")
		fileList = os.listdir(path)
		totalNum = len(fileList) #获取文件夹内所有文件个数
		index = 1 #文件名字初始化
		newList = []
		newDict = {}
		for item in fileList:
			if item.endswith('.png') or item.endswith('.jpg'):
				# name = str(item).replace(" ", "") #去除空格
				# name = str(name).replace("_", "") 
				# name = str(name).replace("+", "") 
				name = os.path.splitext(item)[0] #分离文件名与扩展名 返回数组 取第0个
				#去除字母
				name = filter(lambda x: x in '0123456789', name)
				name2 = ""
				for i in name:
					name2 = name2 + i
				name = name2
				if name == "":
					name = 0
				newList.append(int(name))
				newDict[item] = int(name)
			else:
				file_path = os.path.join(os.path.abspath(path), item)
				if os.path.isdir(file_path):
					self.batchRename(file_path,preFix)
		newDict=sorted(newDict.items(),key=lambda x:x[1],reverse=False)
		
		for key in newDict:
			src = os.path.join(os.path.abspath(path), key[0])
			dst = os.path.join(os.path.abspath(path), preFix+str(index) + '.jpg')
			if item.endswith('.png'):
				dst = os.path.join(os.path.abspath(path), preFix+str(index) + '.png')
			try:
				os.rename(src, dst)
				index = index + 1
			except:
				print("rename fail 文件名" + key[0])
				continue

		print("完成重命名")

	def scale(self, path, scale): #缩放单张图片
		if os.path.exists(path) == False: #判断文件夹是否存在
			print("fail 不存在的图片")
			return
		print("开始缩放图片...")
		name = os.path.basename(path)
		if name.endswith('.png') or name.endswith('.jpg'):
			img = Image.open(path)
			size = img.size
			# Image.NEAREST ：低质量
			# Image.BILINEAR：双线性
			# Image.BICUBIC ：三次样条插值
			# Image.ANTIALIAS：高质量
			out = img.resize((int(size[0]*scale),int(size[1]*scale)), Image.ANTIALIAS) 
			out.save(path)
			print(name + "缩放完成")
		else:
			print("fail 不支持文件类型"+name)
		

	def batchScale(self, path, scale): #批量缩放图片
		if os.path.exists(path) == False: #判断文件夹是否存在
			print("fail 不存在的文件夹")
			return
		if os.path.isdir(path) == False:
			print("fail 不是文件目录")
			return
		print("开始批量缩放图片...")
		fileList = os.listdir(path)
		for item in fileList:
			if item.endswith('.png') or item.endswith('.jpg'):
				src = os.path.join(os.path.abspath(path), item)
				img = Image.open(src)
				size = img.size
				out = img.resize((int(size[0]*scale),int(size[1]*scale)), Image.ANTIALIAS) 
				out.save(src)
				print(item + "缩放完成")

			else:
				file_path = os.path.join(os.path.abspath(path), item)
				if os.path.isdir(file_path):
					self.batchScale(file_path, scale)

	def texPacker(self, path):
		if os.path.isdir(path) == False:
			print("fail textPacker不是文件目录"+path)
			return
		fileList = os.listdir(path)
		fileName = os.path.basename(path)

		if len(fileList) == 0:
			print("fail 没有图片")
			return

		if os.path.isdir(self.outputPath) == False:
			#os.mkdir(self.outputPath)
			print("请配置正确的输入路径")
			return

		TP = self.conf.get("texturePacker", "COMEND")

		# cmdtmp = TP + " " + allImage +\
		# 	" --data " + self.outputPath + os.sep + fileName + ".plist"\
		# 	" --sheet " + self.outputPath + os.sep + fileName + ".png"\
		# 	" --format " + "cocos2d"
		# os.system(cmdtmp) 
		# \表示这行还没结束   {参数}

		#texturePacker 参数详情
		# --trim-sprite-names  去除png等后缀
		# --multipack 多图片打包开起，避免资源图太多，生成图集包含不完全，开起则会生成多张图集。
		# --maxrects-heuristics macrect的算法  参数 Best ShortSideFit LongSideFit AreaFit BottomLeft ContactPoint
		# --enable-rotation 开起旋转，计算rect时如果旋转将会使用更优的算法来处理，得到更小的图集
		# --border-padding 精灵之间的间距
		# --shape-padding 精灵形状填充
		# --trim-mode Trim 删除透明像素，大下使用原始大小。 参数 None Trim Crop CropKeepPos Polygon
		# --basic-sort-by Name  按名称排序
		# --basic-order Ascending 升序
		# --texture-format 纹理格式
		# --data 输出纹理文件的信息数据路径 plist
		# --sheet 输出图集路径 png
		# --scale 1 缩放比例 主要用于低分辨率的机子多资源适配。
		# --max-size 最大图片像素 一般我是用的2048，超过2048以前的有些android机型不支持。
		# --size-constraints 结纹理进行大小格式化，AnySize 任何大小 POT 使用2次幂 WordAligned
		# --replace 正则表达式，用于修改plist加载后的名称
		# --pvr-quality PVRTC 纹理质量
		# --force-squared 强制使用方形
		# --etc1-quality ETC 纹理质量
		packCommand = TP + \
			" --multipack" \
			" --format cocos2d" \
			" --maxrects-heuristics best" \
			" --enable-rotation" \
			" --shape-padding 2" \
			" --border-padding 2" \
			" --trim-mode Trim" \
			" --basic-sort-by Name" \
			" --basic-order Ascending" \
			" --texture-format {textureFormat}" \
			" --data {outputSheetNamePath}{fileNameSuffix}.plist" \
			" --sheet {outputSheetNamePath}{fileNameSuffix}.{sheetSuffix}" \
			" --scale {scale}" \
			" --max-size {maxSize}" \
			" --opt {opt}" \
			" --size-constraints {sizeConstraints}" \
			" {inputPath}"

		# if sys.platform == "win32":
		# 	packCommand = packCommand + " --replace (.png)$=" \
		# 	" --replace \\b={sheetName}_" \
		# 	" --replace {sheetName}_$=.png"
		# else:
		# 	packCommand = packCommand + " --replace ^={sheetName}_"

		packCommand = packCommand.format(
			textureFormat="png",
			outputSheetNamePath=os.path.join(self.outputPath,fileName),
			sheetName=fileName,
			sheetSuffix='png',
			scale=1,
			maxSize=2048,
			opt='RGBA8888',
			sizeConstraints='AnySize',
			inputPath=path,
			fileNameSuffix="")
		os.system(packCommand)

		print("成功打包", fileName)

	def batchTexPacker(self, path):
		if os.path.isdir(path) == False:
			print("fail batchTextPacker不是文件目录")
			return
		fileList = os.listdir(path)
		if len(fileList) == 0:
			print("fail 没有目录")
			return

		if os.path.isdir(self.outputPath) == False:
			#os.mkdir(self.outputPath)
			print("请配置正确的输入路径")
			return

		print("开始打包...")

		TP = self.conf.get("texturePacker", "COMEND")

		for item in fileList:
			tmpPath = os.path.join(os.path.abspath(path), item)
			self.texPacker(tmpPath)

	#反解析
	def unTexPacker(self, plistPath, pngPath):
		if not (os.path.isfile(plistPath) and os.path.isfile(pngPath)):
			print("请输入正确文件路径")
			return
		filePath = plistPath.replace('.plist', '')
		image = Image.open(pngPath)
		root = plistlib.readPlist(plistPath)
		frames = root['frames']

		to_list = lambda x: x.replace('{','').replace('}','').split(',')
		to_int = lambda x:int(x)
		for frame in frames:
			framename = frame.replace('.png', '')
			#print(frames[frame])
			size =  frames[frame]['sourceColorRect']
			size = to_list(size)
			size = [int(x) for x in size]
			size = tuple(size)

			spriteSize = frames[frame]['sourceSize']
			spriteSize = to_list(spriteSize)
			spriteSize = [int(x) for x in spriteSize]
			spriteSize = tuple(spriteSize)

			textureRect = frames[frame]['frame']
			textureRect = to_list(textureRect)
			textureRect = [int(x) for x in textureRect]

			crop_box = [1,2,3,4]
			result_image = Image.new('RGBA', spriteSize, 0)
			if frames[frame]['rotated']:
				crop_box[0] = int(textureRect[0])
				crop_box[1] = int(textureRect[1])
				crop_box[2] = int(textureRect[0] + textureRect[3])
				crop_box[3] = int(textureRect[1] + textureRect[2])
			else:
				crop_box[0] = int(textureRect[0])
				crop_box[1] = int(textureRect[1])
				crop_box[2] = int(textureRect[0] + textureRect[2])
				crop_box[3] = int(textureRect[1] + textureRect[3])

			#print(crop_box, frames[frame]['rotated'], frame)
			rect_on_big = image.crop(crop_box)

			if frames[frame]['rotated']:
				rect_on_big = rect_on_big.transpose(Image.ROTATE_90)

			result_box = [1,2,3,4]
			result_box[0] = int(size[0])
			result_box[1] = int(size[1])
			result_box[2] = int(size[0] + size[2])
			result_box[3] = int(size[1] + size[3])

			result_image.paste(rect_on_big,result_box)
			
			if not os.path.isdir(filePath):
				os.mkdir(filePath)
			outfile = (filePath+'/' + framename+'.png')
			#print outfile, "generated"
			result_image.save(outfile)
		print("反解析成功", os.path.basename(plistPath))

	def batchUnTexPaker(self, path):
		if os.path.isdir(path) == False:
			print("fail 文件不存在")
			return
		fileList = os.listdir(path)
		if len(fileList) == 0:
			print("fail 空文件")
			return
		print("开始解析...")
		for item in fileList:
			if item.endswith('.plist'):
				filePath = os.path.join(os.path.abspath(path), item)
				pngPath = filePath.replace('.plist', '.png')
				if os.path.isfile(pngPath):
					self.unTexPacker(filePath, pngPath)
				else:
					print("fail 不存在png文件", pngPath)
				
			








