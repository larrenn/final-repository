import socket
import threading
import time
import json

class TCPServer:
    def __init__(self, host='0.0.0.0', port=8080, on_data_received=None):
        self.host = host
        self.port = port
        self.on_data_received = on_data_received
        self.socket = None
        self.running = False
        
    def start(self):
        """Запуск TCP сервера"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.socket.settimeout(1.0)
            
            self.running = True
            print(f"TCP Server listening on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, client_address = self.socket.accept()
                    print(f"New connection from {client_address}")
                    
                    # Обработка клиента в отдельном потоке
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.timeout:
                    continue
                except OSError as e:
                    if self.running:
                        print(f"Socket error: {e}")
                    break
                    
        except Exception as e:
            print(f"TCP Server error: {e}")
        finally:
            self.stop()
    
    def _handle_client(self, client_socket, client_address):
        """Обработка клиентского соединения"""
        buffer = ""
        
        try:
            client_socket.settimeout(1.0)
            
            while self.running:
                try:
                    data = client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break
                    
                    buffer += data
                    
                    # Обработка полных сообщений (разделенных \n)
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        line = line.strip()
                        
                        if line:
                            if self.on_data_received:
                                self.on_data_received(line, client_address)
                                
                except socket.timeout:
                    continue
                except ConnectionResetError:
                    break
                except Exception as e:
                    print(f"Client handling error: {e}")
                    break
                    
        except Exception as e:
            print(f"Client thread error: {e}")
        finally:
            client_socket.close()
            print(f"Connection closed: {client_address}")
    
    def stop(self):
        """Остановка сервера"""
        self.running = False
        if self.socket:
            self.socket.close()
        print("TCP Server stopped")