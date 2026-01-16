import socket
import threading
import sys

import time

class IRCClient():
    def __init__(self, server, port, nickname, channel, callback):
        self.server = server
        self.port = port
        self.nickname = nickname
        self.channel = channel
        self.sock = None
        self.running = False
        self.callback = callback
    
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.server, self.port))
            # IRC Handshake
            self.send_raw(f"USER {self.nickname} {self.nickname} {self.nickname} :Python Client")
            self.send_raw(f"NICK {self.nickname}")
            
            self.running = True
            
            # Start background listener
            t = threading.Thread(target=self.recieve)
            t.daemon = True
            t.start()
            
            self.callback(f"[-] Connected to {self.server}")
            
        except Exception as e:
            self.callback(f"[!] Connection failed: {e}")

    def send_raw(self, command):
        if self.sock:
            self.sock.sendall((command + "\r\n").encode("utf-8"))

    def send_message(self, message):
        self.send_raw(f"PRIVMSG {self.channel} :{message}")
    
    def recieve(self):
        buffer = ""
        while self.running:
            try:
                data = self.sock.recv(4096).decode("utf-8",errors='ignore')
                if not data:
                    self.running = False
                    break   
                
                buffer += data

                while "\r\n" in buffer:
                    line, buffer = buffer.split("\r\n", 1)
                    self.parse_line(line)
            
            except:
                break

    def parse_line(self, line):
        # 1. PING/PONG
        if line.startswith("PING"):
            challenge = line.split()[1]
            self.send_raw(f"PONG {challenge}")
            print(f"[-] Sent PONG {challenge}")
        
        # 2. JOIN confirmation
        elif " 001 " in line:
            self.send_raw(f"JOIN {self.channel}")
            self.callback(f"[-] Joined {self.channel}")

        # 3. Chat Messages
        elif "PRIVMSG" in line:
            try:
                parts = line.split(" :", 1)
                header = parts[0]
                msg_content = parts[1]
                sender_nick = header.split("!")[0][1:]
                
                # Pass clean data to the UI
                self.callback(f"{sender_nick}: {msg_content}")
            except:
                pass
    
    def disconnect(self):
        self.send_raw("QUIT :Goodbye!")
        time.sleep(0.5) # Give time for the message to be sent
        self.running = False
        if self.sock:
            self.sock.close()
    
    def join_channel(self, channel):
        self.send_raw(f"JOIN {channel}")
        self.callback(f"[-] Joined {channel}")