import socket
import threading
import time

def test_client(message):
    """Тестовый клиент для проверки сервера"""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", 12345))
        
        client_socket.send(message.encode())
        
        response = client_socket.recv(4096).decode()
        print(response)
        
        client_socket.close()
        
    except Exception as e:
        print(f"Ошибка клиента: {e}")

def multiple_clients_test():
    """Тест нескольких клиентов"""
    clients = []
    for i in range(15):
        message=f"Привет сервер-{i}"
        thread = threading.Thread(
            target=test_client(message),
            args=(),
            name=f"Client-{i+1}",
        )
        clients.append(thread)
        thread.start()
        time.sleep(0.1)  # задержка между подключениями
    
    for thread in clients:
        thread.join()

if __name__ == "__main__":
    multiple_clients_test()