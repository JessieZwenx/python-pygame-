import os
import sys
import time
import subprocess
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PygameHotReloadHandler(FileSystemEventHandler):
    def __init__(self, script_path):
        self.script_path = script_path
        self.process = None
        self.start_process()
    
    def start_process(self):
        """启动Pygame进程"""
        if self.process:
            print("🔄 停止当前进程...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("⚠️ 进程未正常退出，强制终止")
                self.process.kill()
        
        print("🎮 启动Pygame应用...")
        self.process = subprocess.Popen(
            [sys.executable, self.script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 启动输出监控线程
        output_thread = threading.Thread(target=self.monitor_output)
        output_thread.daemon = True
        output_thread.start()
    
    def monitor_output(self):
        """监控子进程输出"""
        while self.process and self.process.poll() is None:
            output = self.process.stdout.readline()
            if output:
                print(f"[Pygame] {output.strip()}")
    
    def on_modified(self, event):
        """文件修改时触发"""
        if event.src_path.endswith('.py') and not event.src_path.endswith('dev_reloader.py'):
            print(f"📁 检测到文件变化: {os.path.basename(event.src_path)}")
            print("🔄 重新启动Pygame应用...")
            self.start_process()

def main():
    if len(sys.argv) != 2:
        print("❌ 用法: python dev_reloader.py your_pygame_script.py")
        print("💡 在VSCode中按 F5 选择 'Python: Pygame 自动重载'")
        return
    
    script_path = sys.argv[1]
    
    if not os.path.exists(script_path):
        print(f"❌ 文件不存在: {script_path}")
        return
    
    print("🚀 Pygame 热重载开发服务器启动!")
    print(f"📂 监控文件: {script_path}")
    print("💡 修改代码并保存后会自动重启Pygame窗口")
    print("⏹️ 按 Ctrl+C 停止服务器")
    
    event_handler = PygameHotReloadHandler(script_path)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 停止开发服务器...")
        observer.stop()
        if event_handler.process:
            event_handler.process.terminate()
    
    observer.join()

if __name__ == "__main__":
    main()