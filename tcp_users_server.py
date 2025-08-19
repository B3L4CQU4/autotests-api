import socket
import logging
from threading import Thread, Lock

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)

class TCPServer:
    def __init__(self, host="127.0.0.1", port=12345, max_connections=10):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.messages = []
        self.lock = Lock()
        self.running = False
        
    def start(self):
        """Запуск TCP сервера"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(self.max_connections)
            
            self.running = True
            logging.info(f"Сервер запущен на {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    logging.info(f"Пользователь с адресом: {client_address} подключился к серверу")

                    client_thread = Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except OSError as e:
                    if self.running:
                        logging.error(f"Ошибка при принятии подключения: {e}")
                    break
                    
        except Exception as e:
            logging.error(f"Ошибка при запуске сервера: {e}")
        finally:
            self.stop()
    
    def handle_client(self, client_socket, client_address):
        """Обработка клиентского подключения"""
        try:
            with client_socket:
                while self.running:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    
                    message = data.decode().strip()
                    logging.info(f"Пользователь с адресом: {client_address} отправил сообщение: {message}")
                    
                    with self.lock:
                        self.messages.append(message)
                    
                    response = "\n".join(self.messages) + "\n"
                    client_socket.send(response.encode())
                    
        except ConnectionResetError:
            logging.warning(f"Пользователь {client_address} отключился неожиданно")
        except Exception as e:
            logging.error(f"Ошибка при обработке клиента {client_address}: {e}")
        finally:
            logging.info(f"Пользователь с адресом: {client_address} отключился от сервера")
    
    def stop(self):
        """Остановка сервера"""
        self.running = False
        try:
            if hasattr(self, "server_socket"):
                self.server_socket.close()
                logging.info("\n" + "Сервер остановлен")
        except Exception as e:
            logging.error(f"Ошибка при остановке сервера: {e}")

def main():
    """Основная функция"""
    server = TCPServer()
    
    try:
        server.start()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()