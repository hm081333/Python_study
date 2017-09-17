# Encoding: UTF-8
import os


def dir_or_file(path):
	if (os.path.isdir(path)):
		# print path
		ly_path(path)
		pass
	elif (os.path.isfile(path)):
		# print os.path.dirname(path)
		if (os.path.dirname(path) == study_py_path):
			# print path
			print os.path.basename(path)
			pass
		else:
			# print '--', path
			print '--', os.path.basename(path)
			pass


def ly_path(path):
	# print os.walk(path)
	for f in os.walk(path):
		print f
		# all_path_file = os.path.join(path, '?')
		# print glob.glob(all_path_file)
		# for p in glob.glob(all_path_file):
		#     dir_or_file(p)
		#     pass


study_py_path = 'D:\\PY'

ly_path(study_py_path)
