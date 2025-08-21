import uiautomator2 as u2
import time


class post_friend_circle:
    def __init__(self):
        # 连接设备
        self.d = u2.connect()


    def start_wechat(self):
        # 启动微信
        print("正在启动微信...")
        self.d.app_start("com.tencent.mm",stop=True)
        time.sleep(3)
        if self.d(text="微信").exists:
            print("微信已成功启动。")
            return True
        else:
            print("微信启动失败，请确认微信已安装!")
            return False


    def to_friend_circle(self):
        # 导航到朋友圈页面
        if self.d(text="发现").exists:
            self.d(text="发现").click()
            time.sleep(1)
            # 点击朋友圈
            if self.d(text="朋友圈").exists:
                self.d(text="朋友圈").click()
                time.sleep(2)
                return True

        print("没能进入朋友圈")
        return False


    def post(self, text=None, image_count=0):
        # 发布朋友圈
        # text: 要发布的文字内容
        # image_count: 要选择的图片数量，只能发一张
        print("开始发布朋友圈...")
        width, height = self.d.window_size()
        # 根据是否有图片选择不同的发布方式
        if image_count > 0:
            # 需要发布带图片的朋友圈，点击右上角的相机按钮
            # 点击右上角的相机按钮
            if self.d(resourceId="com.tencent.mm:id/coz").exists:  # 相机图标的ID会变化
                self.d(resourceId="com.tencent.mm:id/coz").click()
            else:
                # 尝试点击右上角位置（相机图标）
                self.d.click(width * 0.9, height * 0.07)
            time.sleep(2)

            # 点击"从相册选择"按钮
            if self.d(text="从相册选择").exists:
                self.d(text="从相册选择").click()

            time.sleep(2)

            selected_count = 0

            # 选择手机相册中的图片，
            for i in range(image_count):
                if self.d(resourceId="com.tencent.mm:id/jdh").exists:
                    self.d(resourceId="com.tencent.mm:id/jdh").click()
                    selected_count += 1
                    print("已选择1张图片")
                    time.sleep(0.5) 

            # 点击"完成(1)"按钮
            if selected_count > 0:
                print("选择1张图片，点击完成按钮")
                if self.d(text="完成(1)").exists:
                    self.d(text="完成(1)").click()
                # elif self.d(text="完成(" + str(selected_count) + ")").exists:
                #     self.d(text="完成(" + str(selected_count) + ")").click()
                time.sleep(2)
            else:
                print("未有选择到图片，代码出错")
                time.sleep(1)
                return False

        # 这边是只发布文字内容的朋友圈
        else:
            # 只发布文字内容，长按右上角的相机按钮
            width, height = self.d.window_size()
            print("准备发布纯文字朋友圈...")
            if self.d(resourceId="com.tencent.mm:id/coz").exists:  # 相机图标的ID会变化
                self.d(resourceId="com.tencent.mm:id/coz").long_click(duration=1.0)  # 长按1秒
            else:   #由于相机图标的resourceId会变化，添加下面的逻辑
                # 长按右上角位置（相机图标）
                self.d.long_click(width * 0.9, height * 0.07, duration=1.0)
            time.sleep(2)

        # 添加文字（无论是纯文字还是带图片）
        if text:
            # 找到文本编辑框并输入
            if self.d(className="android.widget.EditText").exists:
                self.d(className="android.widget.EditText").set_text(text)
                print(f"已输入文字: {text}")
            else:
                print("找不到文本编辑框")

        # 点击发表按钮
        print("点击发表按钮")
        if self.d(text="发表").exists:
            self.d(text="发表").click()

        # 等待发布完成
        time.sleep(5)
        print("朋友圈已发布")
        return True



def main():
    # 创建实例
    example = post_friend_circle()

    # 启动微信
    if not example.start_wechat():
        print("启动微信失败")
        return

    # 进入朋友圈页面
    if not example.to_friend_circle():
        print("进入朋友圈失败")
        return

    # 文本内容
    moment_text = "你好，这是我发的一条自动发朋友圈的测试案例！"

    # 设置要选择的图片数量-0或1
    # 如果设置为0，则发布纯文字朋友圈
    # 选择图片image_count只能设置为1，多了不好定位
    image_count = 0

    # 发布朋友圈
    success = example.post(text=moment_text, image_count=image_count)
    if success:
        print("朋友圈发布成功")
    else:
        print("朋友圈发布失败")


if __name__ == "__main__":
    main()