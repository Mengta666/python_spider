import cv2
path = r"E:\python\spider\selenium\zhihu_login\login_pic.png".encode('utf-8').decode('utf-8')
img = cv2.imread(path)
if img is None:
    print("OpenCV 无法读取图片，可能为中文路径问题")
else:
    print("图片读取成功")