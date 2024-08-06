import socket
import threading
import logging
import os
import time
from colorama import Fore, Style


print(Fore.RED + """

  ______ _____  _____ ____
 (_-< -_) __/ |/ / -_) __/
/___|__/_/  |___/\__/_/ 1.0 """)

print(Fore.YELLOW + """
producer  〔coded by enesxsec〕
instagram 〔xsecit〕
github    〔https://github.com/ghost0x02〕""")

print(Style.RESET_ALL)

logging.basicConfig(filename='data.log', level=logging.INFO)

def log_request(address, data):
    logging.info(f"Address: {address}, Data: {data}")

def authenticate_client(client_socket):
    client_socket.send("Kullanıcı adı girin: ".encode('utf-8'))
    username = client_socket.recv(1024).decode('utf-8').strip()
    client_socket.send("Şifre girin: ".encode('utf-8'))
    password = client_socket.recv(1024).decode('utf-8').strip()

    if username == "admin" and password == "connect":
        client_socket.send("Başarıyla giriş yaptınız!".encode('utf-8'))
        return True
    else:
        client_socket.send("Giriş başarısız!".encode('utf-8'))
        return False

def handle_tcp_client(client_socket):
    if authenticate_client(client_socket):
        request = client_socket.recv(1024)
        if request:
            print(f"Gelen İstek: {request.decode('utf-8')}")
            response = "Sunucuya bağlandınız!"
            client_socket.send(response.encode('utf-8'))
            log_request(str(client_socket.getpeername()), request.decode('utf-8'))
        client_socket.close()
    else:
        client_socket.close()

def start_tcp_server(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    print(f"TCP sunucu {ip}:{port} adresinde dinleniyor...")

    connection_attempts = 0
    max_attempts = 3

    while connection_attempts < max_attempts:
        try:
            client_socket, addr = server.accept()
            connection_attempts += 1
            print(f"Bağlantı geldi: {addr}")
            client_handler = threading.Thread(target=handle_tcp_client, args=(client_socket,))
            client_handler.start()
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
            break

    print("Maksimum bağlantı deneme sınırına ulaşıldı. Sunucu kapanıyor.")
    server.close()

def main():

    username = input("Kullanıcı adı girin: ")
    password = input("Şifre girin: ")
    time.sleep(3)
    os.system("clear")

    if username != "admin" or password != "connect":
        print("Kimlik doğrulama başarısız! Program sonlandırılıyor.")
        return
    print(Fore.MAGENTA + "")
    os.system("figlet connect")
    ip_address = input("TCP sunucu IP adresini girin: ")
    port = int(input("Port numarasını girin: "))
    start_tcp_server(ip_address, port)

if __name__ == "__main__":
    main()
