
import cv2

class CalculateDistance:
    def __init__(self, back_pic_path, slider_pic_path, offset_px, offset_py, page_scale, display):
        """
        :param back_pic_path: 背景图片位置
        :param slider_pic_path: 滑块图片位置
        :param offset_px: 滑块图片在整个背景图片上面的偏移量x，即滑块相对于背景图片的位置（便于裁剪）
        :param offset_py: 滑块图片在整个背景图片上面的偏移量y
        :param display:
        : page_scale: 页面缩放系数

        """
        self.background_img = cv2.imread(back_pic_path)
        self.slider_img = cv2.imread(slider_pic_path, cv2.IMREAD_UNCHANGED)
        self.offset_px = offset_px
        self.offset_py = offset_py
        self.page_scale = page_scale

        # 使用最近邻近插值缩放，得到50x50的滑块图片
        self.slider_scale_img = cv2.resize(self.slider_img, (50, 50), interpolation=cv2.INTER_NEAREST)
        self.background_cut_img = None
        self.display = display

    def cut_background(self):
        """
        将背景图片剪切以下，只保留滑块图片那一行
        """
        height = self.slider_scale_img.shape[0]
        # 将多余的图片行剪切掉，并且也剪切包含滑块图片与其前部分（因为这部分不需要比较，只需要比较后部分）
        self.background_cut_img = self.background_img[self.offset_py - 10 : self.offset_py + height + 10,
                                  self.offset_px + height + 10:]
        # 这里的数组都是按照先行后列的顺序进行排列（同传统数组）
        # 那么切片在y方向上只取滑块左上角顶点的前10行和加上自身宽度的后10行
        # 切片x只需要取当前滑块以后的所有列即可

    def get_distance(self):
        # 将图片转为灰度图片
        background_grey_img = cv2.cvtColor(self.background_cut_img, cv2.COLOR_BGR2GRAY)
        slider_grey_img = cv2.cvtColor(self.slider_scale_img, cv2.COLOR_BGR2GRAY)
        # 使用canny算子，提取图片边缘特征
        slider_edge_img = cv2.Canny(slider_grey_img, 100, 250)
        background_edge_img = cv2.Canny(background_grey_img, 250, 400)

        # 取滑块图片的高和宽
        slider_height, slider_width = slider_edge_img.shape
        # 将滑块与背景图片进行匹配，得到每个像素匹配到的结果构成的矩阵
        result = cv2.matchTemplate(background_edge_img, slider_edge_img, cv2.TM_CCOEFF_NORMED)
        # 返回最小值，最大值，最小值所在位置，最大值所在位置，匹配到的特征一般是最大值
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # 取最大的坐标
        top_left = (max_loc[0], max_loc[1])
        # 得到匹配的区域
        bottom_right = (top_left[0] + slider_width, top_left[1] + slider_height)

        # 切割后的背景图片中需要移动的距离，画出匹配结果
        if  self.display:
            # 画出匹配结果
            print("匹配区域：", top_left, bottom_right)
            after_img = cv2.rectangle(self.background_cut_img, top_left, bottom_right, (0, 0, 255), 2)
            cv2.imwrite("picture/douban/match_picture.png", after_img)

        # 计算滑动距离
        slider_distance = top_left[0] + slider_width + 10

        return slider_distance * self.page_scale

    def run(self):
        self.cut_background()
        return self.get_distance()


if __name__ == '__main__':
    pass