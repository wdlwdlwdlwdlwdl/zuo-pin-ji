import uiautomator2 as u2
import time


class tian_jia_peng_you:
    def __init__(self):
        # 连接设备
        self.d = u2.connect()


    def start_wechat(self):
        print("正在启动微信...")
        # 尝试启动微信
        self.d.app_start("com.tencent.mm",stop=True)

        time.sleep(5)

        # 确认微信是否已启动
        if self.d(text="通讯录").exists:
            print("微信已成功启动")
            return True
        print("微信启动失败")
        return False


    def to_tong_xun_lu(self):
        # 进入到通讯录界面
        # 法1：通过文本确认
        if self.d(text="通讯录").exists:
            self.d(text="通讯录").click()
            print("通过 text=通讯录 进入通讯录")

        # 法2：通过ResourceId
        elif self.d(resourceId="com.tencent.mm:id/h5y").exists:
            self.d(resourceId="com.tencent.mm:id/h5y").click()
            print("通过 resourceId 进入通讯录")

        return True



    def search_and_add_friend(self, wechat_id):
        # 搜索并添加好友
        # wechat_id: 要添加的手机号
        print(f"开始搜索并添加好友: {wechat_id}")

        # 1. 点击搜索按钮（多等几秒）
        for i in range(10):
            if self.d(resourceId="com.tencent.mm:id/jha").exists:
                self.d(resourceId="com.tencent.mm:id/jha").click()
                print("通过resourceId点击搜索按钮")
                break
            elif self.d(text="新的朋友").exists:
                self.d(text="新的朋友").click()
                print("通过text点击新的朋友按钮")
                break
            elif self.d(description="新的朋友").exists:
                self.d(description="新的朋友").click()
                print("通过desc点击新的朋友按钮")
                break
            time.sleep(1)
        else:
            print("找不到新的朋友按钮")
            return False

        # 2. 等待输入框出现并输入手机号
        for i in range(10):
            if self.d(className="android.widget.EditText").exists:
                self.d(className="android.widget.EditText").set_text(wechat_id)
                print(f"已输入手机号: {wechat_id}")
                break
            time.sleep(1)
        else:
            print("找不到输入框")
            return False

        time.sleep(2)

        # 3. 点击搜索结果(手机是旧版本的)
        if self.d(text="查找手机/QQ号:" + wechat_id).exists:
            self.d(text="查找手机/QQ号:" + wechat_id).click()
            time.sleep(2)
        else:
            print("找不到搜索结果")
            return False

        # 4. 点击添加到通讯录
        if self.d(text="添加到通讯录").exists:
            self.d(text="添加到通讯录").click()
            time.sleep(2)
        elif self.d(text="发消息").exists:
            print(f"{wechat_id} 已经是你的好友了")
            return True
        else:
            print("找不到添加到通讯录按钮")
            return False

        # 5. 验证是否发送成功
        time.sleep(3)
        if self.d(text="发送").exists:
            self.d(text="发送").click()
            time.sleep(6)
            print("好友请求发送成功")
            return True
        else:
            print("好友请求发送失败")
            return False



def main():
    example = tian_jia_peng_you()
    
    if not example.start_wechat():
        print("启动微信失败")
        return

    if not example.to_tong_xun_lu():
        print("进入通讯录失败")
        return

    # 要添加的手机号
    wechat_id = "18362095726"

    # 搜索并添加好友
    success = example.search_and_add_friend(wechat_id)
    if success:
        print("添加好友成功")
    else:
        print("添加好友失败")


if __name__ == "__main__":
    main()