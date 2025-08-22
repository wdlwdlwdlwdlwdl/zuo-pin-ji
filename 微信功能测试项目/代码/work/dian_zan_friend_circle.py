import uiautomator2 as u2
import time


class dian_zan_friend_circle:
    def __init__(self, target=10, scroll_times=25):
        # 连接设备
        self.d=u2.connect()
        # 设置目标点赞数量
        self.target = target
        # 设置最大滑动次数
        self.scroll_times = scroll_times
        # 记录已点赞数量
        self.recorded = 0
        # 获取屏幕尺寸
        self.width, self.height = self.d.window_size()




    def start_wechat(self):
        print("正在启动微信...")
        self.d.app_start("com.tencent.mm",stop=True)

        time.sleep(3)

        # 确认微信是否已启动
        if self.d(text="微信").exists:
            print("微信已成功启动")
            return True
        else:
            print("微信启动失败，请确认微信已安装")
            return False


    def to_friend_circle(self):
        print("正在进入到朋友圈...")

        # 直接点击"发现"
        if self.d(text="发现").exists:
            print("点击'发现'按钮")
            self.d(text="发现").click()
            time.sleep(1.5)  # 等待发现页面加载

            # 点击"朋友圈"
            if self.d(text="朋友圈").exists:
                print("点击'朋友圈'按钮")
                self.d(text="朋友圈").click()
                time.sleep(2)
                print("成功进入朋友圈页面")
                return True

        print("导航到朋友圈失败")
        return False


    def find_and_like_moments(self):
        print(f"开始查找朋友圈并点赞，目标点赞数量: {self.target}")
        # 当前的滑动次数
        scroll_count = 0
        while self.recorded < self.target and scroll_count < self.scroll_times:
            # 点赞
            self.dian_zan()
            # 如果还没达到目标点赞数，滑动查看更多朋友圈
            if self.recorded < self.target:
                # 向下滑动
                self._scroll_down()
                scroll_count += 1
                time.sleep(1.5)

        print(f"点赞完成，共点赞 {self.recorded} 条朋友圈")
        return self.recorded
    

    def dian_zan(self):
        # 根据精确的resourceId定位点赞按钮
        # 查找按钮 - 根据resourceId="com.tencent.mm:id/r2"
        comment_buttons = self.d(resourceId="com.tencent.mm:id/r2")

        # 获取可点赞朋友圈的数量
        button_count = len(comment_buttons)
        print(f"在当前页面找到 {button_count} 个可能的点赞评论按钮")

        for i in range(button_count):
            if self.recorded >= self.target:
                break

            # 点击两个点的按钮
            comment_button = comment_buttons[i]
            comment_button.click()
            time.sleep(1)

            # 如果已经点赞，会显示'取消'
            if self.d(text="取消").exists:
                time.sleep(0.5)
                continue

            # 点击"赞"按钮
            if self.d(text="赞").exists:
                print("点击'赞'按钮")
                self.d(text="赞").click()
                self.recorded += 1
                print(f"成功点赞第 {self.recorded} 条朋友圈")
            # 或者尝试通过resourceId找到点赞按钮
            elif self.d(resourceId="com.tencent.mm:id/qd").exists:
                print("通过resourceId点击点赞按钮")
                self.d(resourceId="com.tencent.mm:id/qd").click()
                self.recorded += 1
                print(f"成功点赞第 {self.recorded} 条朋友圈")
            else:
                # 向下滑动
                self._scroll_down()
                time.sleep(1.5)

            time.sleep(1)




    # 这是修改后的代码，可以滑动更大的距离
    def _scroll_down(self):
        # 向下滑动
        # 增大滑动距离，从屏幕中更下部向更上部滑动
        self.d.swipe(
            self.width * 0.5,  # x 坐标保持不变
            self.height * 0.8,  # 起始 y 坐标和之前的 0.7 相比更靠下
            self.width * 0.5,  # 结束 x 坐标保持不变
            self.height * 0.2,  # 结束 y 坐标和之前的 0.3 相比更靠上
            duration=0.3  # 滑动时长保持不变
        )




    def run(self):
        # 运行点赞程序

        # 启动微信
        if not self.start_wechat():
            print("启动微信失败，程序终止")
            return False

        # 进入到朋友圈页面
        if not self.to_friend_circle():
            print("进入朋友圈失败，程序终止")
            return False

        time.sleep(2)
        # 执行点赞
        recorded = self.find_and_like_moments()

        return recorded > 0




def main():
    example=dian_zan_friend_circle()

    # 想要点赞的个数
    example.target=10

    # 运行点赞程序
    result = example.run()

    if result:
        print("自动点赞程序执行成功")
    else:
        print("自动点赞程序执行失败")


# 程序入口点
if __name__ == "__main__":
    main()