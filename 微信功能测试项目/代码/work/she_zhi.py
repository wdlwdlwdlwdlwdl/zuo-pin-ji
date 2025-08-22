import uiautomator2 as u2
import time

class WeChatProfileEditor:
    def __init__(self, device_serial=None):
        self.d = u2.connect(device_serial) if device_serial else u2.connect()
        print(f"已连接设备: {self.d.info['productName']}")

    def start_wechat(self):
        self.d.app_start("com.tencent.mm", stop=True)
        time.sleep(3)
        if self.d(text="微信").exists or self.d(text="WeChat").exists:
            print("微信已成功启动")
            return True
        else:
            print("微信启动失败")
            return False

    def navigate_to_profile(self):
        print("导航至个人信息页...")
        if self.d(description="我").exists:
            self.d(description="我").click()
        elif self.d(text="我").exists:
            self.d(text="我").click()
        else:
            print("未找到“我”标签")
            return False
        time.sleep(1)

        if self.d(resourceId="com.tencent.mm:id/a_4").exists:
            self.d(resourceId="com.tencent.mm:id/a_4").click()
            time.sleep(1)
            return True
        else:
            print("未找到“个人信息”入口")
            return False

    def change_nickname(self, new_nickname):
        print(f"正在修改昵称为：{new_nickname}")
        if self.d(text="名字").exists:
            self.d(text="名字").click()
            time.sleep(1)
            if self.d(className="android.widget.EditText").exists:
                self.d(className="android.widget.EditText").set_text(new_nickname)
                time.sleep(2)
                if self.d(text="保存").exists:
                    self.d(text="保存").click()
                    print("昵称修改完成")
                    time.sleep(1)
            else:
                print("未找到昵称输入框")

    def change_signature(self, new_signature):
        print(f"正在修改个性签名为：{new_signature}")

        self.d(text="更多信息").click()
        time.sleep(1)

        if self.d(text="个性签名").exists:
            self.d(text="个性签名").click()
            time.sleep(1)
            if self.d(className="android.widget.EditText").exists:
                self.d(className="android.widget.EditText").set_text(new_signature)
                time.sleep(1)
                if self.d(text="保存").exists:
                    self.d(text="保存").click()
                    time.sleep(1)
                    print("个性签名修改完成")
            else:
                print("未找到签名输入框")
        self.d.press("back")

    def change_avatar(self):
        print(f"正在尝试更换头像")
        if self.d(resourceId="com.tencent.mm:id/a_4").exists:
            self.d(resourceId="com.tencent.mm:id/a_4").click()
            time.sleep(1)

            # 假设已自动打开最近相册，点击第一张图
            if self.d(className="android.widget.ImageView").exists:
                self.d(className="android.widget.ImageView").click()
                time.sleep(2)

                if self.d(text="确定").exists:
                    self.d(text="确定").click()
                    time.sleep(5)
                    print("头像更换完成")
            else:
                print("未找到图片选择界面")
        else:
            print("未找到头像入口")

    def close_wechat(self):
        self.d.app_stop("com.tencent.mm")
        print("微信已关闭")


def main():
    bot = WeChatProfileEditor()
    try:
        if not bot.start_wechat():
            return
        if not bot.navigate_to_profile():
            return

        bot.change_nickname("ડꪊꪕ໌້ᮨꦿ๑҉")
        bot.change_signature("") #个性签名
        bot.change_avatar()  # 注意：需确保头像图片已提前放到手机指定路径
    finally:
        bot.close_wechat()


if __name__ == "__main__":
    main()