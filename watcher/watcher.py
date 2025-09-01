import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# =========================================================
# 1. 定义监控路径和目标脚本
# =========================================================
# 获取脚本所在的父目录的绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 监控目录，使用绝对路径
WATCH_DIRECTORY = os.path.join(BASE_DIR, '../market_analysis/output')
# 待运行的脚本，使用绝对路径
TARGET_SCRIPT = os.path.join(BASE_DIR, '../content_creation/landing_page_writer.py')


# =========================================================
# 2. 定义事件处理器
# =========================================================
class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        """
        当目录中发生任何文件事件时触发此方法。
        """
        # 确保事件是文件创建或修改，并且文件以 .txt 结尾
        if not event.is_directory and (
                event.event_type == 'created' or event.event_type == 'modified') and event.src_path.endswith('.txt'):
            print("--------------------------------------------------")
            print(f"✅ 文件变化已检测到: {event.src_path}")
            print("➡️ 正在启动落地页文案脚本...")

            # 构建完整的命令
            command = ["python", TARGET_SCRIPT, event.src_path]
            print(f"    收到的文件路径参数: {event.src_path}")
            print(f"    完整命令: {' '.join(command)}")

            try:
                # 运行第二个脚本
                subprocess.run(command, check=True)
                print("✅ 脚本已成功启动并完成。")
            except subprocess.CalledProcessError as e:
                print(f"❌ 脚本启动失败，错误代码: {e.returncode}")
                print(f"❌ 错误输出: {e.output.decode('utf-8')}")
            print("--------------------------------------------------")


# =========================================================
# 3. 启动监听器
# =========================================================
if __name__ == "__main__":
    print(f"文件监听器已启动，正在监控目录: {os.path.abspath(WATCH_DIRECTORY)}")

    # 确保输出目录存在
    os.makedirs(WATCH_DIRECTORY, exist_ok=True)

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()