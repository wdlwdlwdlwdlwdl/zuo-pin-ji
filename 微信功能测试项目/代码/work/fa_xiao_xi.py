import re
import uiautomator2 as u2
import time
import matplotlib.pyplot as plt
import subprocess
import matplotlib

# 避免中文乱码
matplotlib.rcParams['font.family'] = 'Arial'

# 数据列表
send_delays = []
cpu_usages = []
memory_usages = []


# 获取 CPU 使用率
def get_cpu_usage():
    # 执行“ adb shell top -H -n 1 ”命令，获取所有线程信息，此时刻的CPU信息
    result = subprocess.check_output(['adb', 'shell', 'top', '-H', '-n', '1'], encoding='utf-8')

    # 匹配所有包含 com.tencent.mm 的行
    lines = [line for line in result.splitlines() if 'com.tencent.mm' in line]

    total_cpu = 0.0
    for line in lines:
        # 提取 CPU 使用率字段 在倒数第三列
        parts = line.split()
        for part in parts:
            # 匹配形如 4.0、0.0 的浮点数
            if re.fullmatch(r'\d+\.\d+', part):
                cpu_value = float(part)
                if 0 < cpu_value <= 100:
                    total_cpu += cpu_value
                    break  # 只取第一个匹配的 CPU 值

    return round(total_cpu, 2)



# 获取内存使用率（假设设备总内存 12G）
def get_memory_usage():
    result = subprocess.getoutput("adb shell dumpsys meminfo com.tencent.mm | findstr TOTAL")
    if result:
        # total_kb - 微信占用的内存
        total_kb = int(result.strip().split()[1].replace('K', ''))
        mem_percent = total_kb / (12288 * 1024) * 100 #设备是 12G == 12 X 1024 =12288，微信内存占总内存的百分比
        return round(mem_percent, 2) #保留两位小数
    return None



# 发送消息
def send_message(d, contact_name, message):
    print("打开微信。。。")
    d.app_start('com.tencent.mm', stop=True)
    time.sleep(5)

    if not d.xpath(f'//*[@text="{contact_name}"]').exists:
        print(f"联系人：'{contact_name}' 没有找到")
        return
    # 在整个页面中查找任何 text 属性值等于 contact_name 变量值的元素。
    d.xpath(f'//*[@text="{contact_name}"]').click()
    time.sleep(2)

    for i in range(10):
        full_message = f"{message} {i+1}"
        start_time = time.time()

        if d(className="android.widget.EditText").exists:
            d(className="android.widget.EditText").set_text(full_message)
            time.sleep(0.1)

            d.xpath('//*[@resource-id="com.tencent.mm:id/bql"]').click()
            end_time = time.time()

            delay = end_time - start_time
            send_delays.append(delay)

            cpu_usage = get_cpu_usage()
            cpu_usages.append(cpu_usage)

            mem_usage = get_memory_usage()
            memory_usages.append(mem_usage)

            print(f"Message {i+1} sent | Delay: {delay:.2f}s | CPU: {cpu_usage:.2f}% | Memory: {mem_usage:.2f}%")
        else:
            print("EditText not found, skipping this message.")
        time.sleep(0.1)



# 绘制图表
def plot_results():
    x = list(range(1, len(send_delays) + 1))

    plt.figure(figsize=(18, 5))

    # 延迟
    plt.subplot(1, 3, 1)
    plt.plot(x, send_delays, label='Delay (s)', color='blue', marker='o')
    plt.xlabel('Message Index')
    plt.ylabel('Delay (seconds)')
    plt.title('Message Sending Delay')
    plt.grid(True)

    # CPU
    plt.subplot(1, 3, 2)
    plt.plot(x, cpu_usages[:len(x)], label='CPU Usage (%)', color='red', marker='x')
    plt.xlabel('Message Index')
    plt.ylabel('CPU Usage (%)')
    plt.title('CPU Usage Over Time')
    plt.grid(True)

    # 内存
    plt.subplot(1, 3, 3)
    plt.plot(x, memory_usages[:len(x)], label='Memory Usage (%)', color='green', marker='s')
    plt.xlabel('Message Index')
    plt.ylabel('Memory Usage (%)')
    plt.title('Memory Usage Over Time')
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# 主函数
def test_send_message():
    # 连接设备
    d = u2.connect()
    if d:
        send_message(d, "大学-汪海涛", "帅")
        plot_results()
    else:
        print("Test aborted: Device not connected.")

if __name__ == "__main__":
    test_send_message()