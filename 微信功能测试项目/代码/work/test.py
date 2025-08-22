import re
import uiautomator2 as u2
import time
import subprocess
import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime


class WeChatVideoPerformanceTest:
    def __init__(self, device_ip=None, total_memory_mb=4096):
        # 连接设备
        self.d = u2.connect()

        self.package_name = "com.tencent.mm"  # 微信包名
        self.performance_data = []
        self.total_memory_mb = total_memory_mb

        # 记录不同性能指标
        self.timestamps = []
        self.cpu_usages = []
        self.memory_usages = []


    def start_app(self):
        print("启动微信应用...")
        self.d.app_start(self.package_name, stop=True)
        time.sleep(3)  # 等待应用完全启动
        return self


    def navigate_to_video(self):
        """导航到视频号
        步骤：点击"发现"，点击"视频号"
        """
        print("正在导航到视频号...")
        # 点击"发现" 选项卡
        if self.d(text="发现").exists:
            self.d(text="发现").click()
            time.sleep(1)
        else:
            print("未找到'发现'选项卡")
            return False

        # 点击"视频号"
        if self.d(text="视频号").exists:
            self.d(text="视频号").click()
            time.sleep(2)  # 等待视频号页面加载
            return True
        else:
            print("未找到'视频号'选项")
            return False


    def get_cpu_usage(self):
        try:
            # 执行 adb shell top 命令，获取所有线程信息
            result = subprocess.check_output(['adb', 'shell', 'top', '-H', '-n', '1'], encoding='utf-8')

            # 匹配所有包含 com.tencent.mm 的行
            lines = [line for line in result.splitlines() if 'com.tencent.mm' in line]

            total_cpu = 0.0
            for line in lines:
                # 提取 CPU 使用率字段
                parts = line.split()
                for part in parts:
                    # 匹配形如 4.0、0.0 的浮点数
                    if re.fullmatch(r'\d+\.\d+', part):
                        cpu_value = float(part)
                        if 0 < cpu_value <= 100:
                            total_cpu += cpu_value
                            break  # 只取第一个匹配的 CPU 值

            return round(total_cpu, 2)

        except subprocess.CalledProcessError as e:
            print("ADB 命令执行失败:", e)
        except Exception as e:
            print("发生错误:", e)
        return 0.0


    def get_memory_usage(self):
        """获取内存使用情况 (MB 和百分比)"""
        try:
            # 获取微信应用的内存使用情况
            cmd = f"adb shell dumpsys meminfo {self.package_name} | findstr TOTAL"
            result = subprocess.getoutput(cmd)

            if result:
                # 解析输出以获取内存使用量（KB）
                parts = result.split()
                for i, part in enumerate(parts):
                    if part.isdigit():
                        total_kb = int(part)
                        memory_mb = total_kb / 1024  # 转换为MB
                        memory_percent = (memory_mb / self.total_memory_mb) * 100
                        return memory_mb, memory_percent

            # 备用方法
            result = subprocess.getoutput(f"adb shell dumpsys meminfo | grep {self.package_name}")
            if result:
                parts = result.split()
                for i, part in enumerate(parts):
                    if part.isdigit() and i < len(parts) - 1 and parts[i + 1].lower() == 'k':
                        total_kb = int(part)
                        memory_mb = total_kb / 1024  # 转换为MB
                        memory_percent = (memory_mb / self.total_memory_mb) * 100
                        return memory_mb, memory_percent
        except Exception as e:
            print(f"获取内存使用率时出错: {e}")
        return 0.0, 0.0


    def monitor_performance(self, duration=30, interval=1):
        """监测应用性能
        Args:
            duration: 监测持续时间（秒）
            interval: 数据采集间隔（秒）
        """
        print(f"开始监测性能，持续 {duration} 秒...")
        print("时间戳, CPU使用率(%), 内存使用(MB), 内存使用率(%)")

        # 监测性能
        end_time = time.time() + duration
        while time.time() < end_time:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.timestamps.append(timestamp)

                # 获取CPU使用率
                cpu_percent = self.get_cpu_usage()
                self.cpu_usages.append(cpu_percent)

                # 获取内存使用情况
                memory_mb, memory_percent = self.get_memory_usage()
                self.memory_usages.append(memory_percent)

                # 保存性能数据
                self.performance_data.append({
                    'timestamp': timestamp,
                    'cpu_percent': cpu_percent,
                    'memory_mb': memory_mb,
                    'memory_percent': memory_percent
                })

                print(f"{timestamp}, {cpu_percent:.2f}%, {memory_mb:.2f}MB, {memory_percent:.2f}%")

                time.sleep(interval)
            except Exception as e:
                print(f"监测性能时出错: {str(e)}")
                break

        return True


    def save_results(self, filename=None):
        """保存性能测试结果到CSV文件
        Args:
            filename: 文件名，如果为None则使用默认名称
        """
        if not filename:
            filename = f"wechat_video_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=[
                    'timestamp', 'cpu_percent',
                    'memory_mb', 'memory_percent'
                ])
                writer.writeheader()
                writer.writerows(self.performance_data)

            print(f"性能数据已保存到 {filename}")
            return True
        except Exception as e:
            print(f"保存结果时出错: {str(e)}")
            return False


    def plot_results(self):
        """绘制性能测试结果图表"""
        if not self.performance_data:
            print("没有可绘制的数据")
            return False

        # 准备时间轴（X轴数据）
        x = list(range(1, len(self.timestamps) + 1))

        plt.figure(figsize=(15, 8))

        # CPU使用率图表
        plt.subplot(2, 1, 1)
        plt.plot(x, self.cpu_usages, label='CPU Usage (%)', color='red', marker='o', markersize=4)
        plt.xlabel('Sample Index')
        plt.ylabel('CPU Usage (%)')
        plt.title('CPU Usage Over Time')
        plt.grid(True)

        # 内存使用率图表
        plt.subplot(2, 1, 2)
        plt.plot(x, self.memory_usages, label='Memory Usage (%)', color='green', marker='s', markersize=4)
        plt.xlabel('Sample Index')
        plt.ylabel('Memory Usage (%)')
        plt.title('Memory Usage Over Time')
        plt.grid(True)

        plt.tight_layout()

        # 保存图表
        plot_filename = f"wechat_video_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(plot_filename)
        print(f"性能图表已保存到 {plot_filename}")

        # 显示图表
        plt.show()
        return True


def main():
    # 传入设备总内存大小，用于计算内存使用百分比
    test = WeChatVideoPerformanceTest(total_memory_mb=12288)  # 12GB内存设备

    # 定义性能监测时长（秒）
    monitoring_duration = 30

    # 执行测试步骤
    test.start_app()

    if test.navigate_to_video():
        # 监测性能指标
        test.monitor_performance(duration=monitoring_duration, interval=1)

        # 保存测试结果CSV
        test.save_results()

        # 绘制并保存性能图表
        test.plot_results()


if __name__ == "__main__":
    main()