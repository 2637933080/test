import subprocess
import time
import sys
import os

def run_server_and_test():
    # 启动服务器
    print("正在启动服务器...")
    server_process = subprocess.Popen([sys.executable, 'app.py'], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE,
                                    text=True)
    
    # 等待服务器启动
    time.sleep(3)
    
    # 检查服务器是否仍在运行
    if server_process.poll() is None:
        print("服务器已启动，正在运行测试...")
        
        # 运行测试
        test_process = subprocess.run([sys.executable, 'test_updated.py'], 
                                    capture_output=True, 
                                    text=True)
        
        print("测试输出:")
        print(test_process.stdout)
        if test_process.stderr:
            print("测试错误:")
            print(test_process.stderr)
            
        # 终止服务器
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
        
        print("服务器已关闭")
    else:
        print("服务器启动失败")
        stdout, stderr = server_process.communicate()
        print("服务器输出:")
        print(stdout)
        if stderr:
            print("服务器错误:")
            print(stderr)

if __name__ == "__main__":
    run_server_and_test()