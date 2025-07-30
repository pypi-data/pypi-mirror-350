import socket
import threading
import json
import time
import random
import os
from datetime import datetime
import requests
import uuid
import subprocess
import platform

def open_port_5000():
    """Abre el puerto 5000 en el firewall"""
    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            # Verificar si el puerto está en uso
            result = subprocess.run(['lsof', '-i', ':5000'], capture_output=True, text=True)
            if result.stdout:
                print("El puerto 5000 ya está en uso")
                return False
            
            # Abrir puerto en macOS
            subprocess.run(['sudo', 'pfctl', '-f', '/etc/pf.conf'], capture_output=True)
            subprocess.run(['sudo', 'pfctl', '-e'], capture_output=True)
            subprocess.run(['sudo', 'pfctl', '-f', '/etc/pf.conf'], capture_output=True)
            print("Puerto 5000 abierto en macOS")
            return True
            
        elif system == "Linux":
            # Verificar si el puerto está en uso
            result = subprocess.run(['netstat', '-tuln'], capture_output=True, text=True)
            if ':5000' in result.stdout:
                print("El puerto 5000 ya está en uso")
                return False
            
            # Abrir puerto en Linux
            subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', '5000', '-j', 'ACCEPT'], capture_output=True)
            print("Puerto 5000 abierto en Linux")
            return True
            
        elif system == "Windows":
            # Verificar si el puerto está en uso
            result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
            if ':5000' in result.stdout:
                print("El puerto 5000 ya está en uso")
                return False
            
            # Abrir puerto en Windows
            subprocess.run(['netsh', 'advfirewall', 'firewall', 'add', 'rule', 'name=Open Port 5000', 'dir=in', 'action=allow', 'protocol=TCP', 'localport=5000'], capture_output=True)
            print("Puerto 5000 abierto en Windows")
            return True
            
    except Exception as e:
        print(f"Error al abrir el puerto: {e}")
        return False

class ChatRoom:
    def __init__(self, creator_name):
        self.creator_name = creator_name
        self.users = {}  # {socket: username}
        self.messages = []
        self.created_at = datetime.now()
        self.node_id = str(uuid.uuid4())  # Identificador único para el nodo

class ChatServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.room = None  # Solo una sala por servidor
        self.server_socket = None
        self.running = False
        self.public_ip = self._get_public_ip()
        print(f"IP pública detectada: {self.public_ip}")

    def _get_public_ip(self):
        """Obtiene la IP pública del servidor usando múltiples servicios"""
        ip_services = [
            'https://api.ipify.org?format=json',
            'https://ifconfig.me/ip',
            'https://icanhazip.com'
        ]
        
        for service in ip_services:
            try:
                if service.endswith('json'):
                    response = requests.get(service, timeout=5)
                    return response.json()['ip']
                else:
                    response = requests.get(service, timeout=5)
                    return response.text.strip()
            except Exception as e:
                print(f"Error al obtener IP de {service}: {e}")
                continue
        
        # Si todos los servicios fallan, intentar obtener IP local
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "127.0.0.1"

    def create_room(self, creator_name):
        """Crea una nueva sala de chat"""
        self.room = ChatRoom(creator_name)
        return True

    def join_room(self, username, client_socket):
        """Une un usuario a la sala"""
        if self.room:
            self.room.users[client_socket] = username
            # Enviar historial de mensajes al nuevo usuario
            for msg in self.room.messages:
                client_socket.send(json.dumps(msg).encode())
            # Notificar a todos los usuarios
            self.broadcast_message(f"{username} se ha unido a la sala", "Sistema")
            # Enviar confirmación al usuario
            client_socket.send(json.dumps({
                'type': 'join_success',
                'message': 'Te has unido a la sala exitosamente'
            }).encode())
            return True
        # Enviar error al usuario
        client_socket.send(json.dumps({
            'type': 'error',
            'message': 'Sala no encontrada'
        }).encode())
        return False

    def leave_room(self, client_socket):
        """Saca a un usuario de la sala"""
        if self.room and client_socket in self.room.users:
            username = self.room.users[client_socket]
            del self.room.users[client_socket]
            self.broadcast_message(f"{username} ha salido de la sala", "Sistema")
            return True
        return False

    def broadcast_message(self, message, username):
        """Envía un mensaje a todos los usuarios de la sala"""
        if self.room:
            timestamp = datetime.now().strftime("%H:%M:%S")
            message_data = {
                'type': 'message',
                'username': username,
                'content': message,
                'timestamp': timestamp
            }
            self.room.messages.append(message_data)
            
            # Enviar mensaje a todos los usuarios
            for client_socket in self.room.users:
                try:
                    client_socket.send(json.dumps(message_data).encode())
                except:
                    pass

    def start(self):
        """Inicia el servidor"""
        try:
            # Intentar abrir el puerto
            if not open_port_5000():
                print("No se pudo abrir el puerto 5000. Intentando continuar...")
            
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            
            # Configuración de keepalive compatible con todos los sistemas
            if hasattr(socket, 'TCP_KEEPIDLE'):
                self.server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
            if hasattr(socket, 'TCP_KEEPINTVL'):
                self.server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
            if hasattr(socket, 'TCP_KEEPCNT'):
                self.server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 6)
            
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"\nServidor iniciado en:")
            print(f"IP pública: {self.public_ip}")
            print(f"Puerto: {self.port}")
            print("\nEste servidor es accesible desde cualquier parte del mundo")
            
            listen_thread = threading.Thread(target=self._listen_for_connections)
            listen_thread.daemon = True
            listen_thread.start()
        except Exception as e:
            print(f"\nError al iniciar el servidor: {e}")
            print("Asegúrate de que el puerto 5000 no esté en uso")
            self.running = False
            raise

    def _listen_for_connections(self):
        """Escucha conexiones entrantes"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                if self.running:
                    print(f"Error al aceptar conexión: {e}")

    def _handle_client(self, client_socket, address):
        """Maneja la conexión de un cliente"""
        username = None
        
        try:
            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                    
                message = json.loads(data.decode())
                message_type = message.get('type')
                
                if message_type == 'join':
                    username = message.get('username')
                    if self.join_room(username, client_socket):
                        print(f"{username} se ha unido a la sala")
                        # Enviar confirmación inmediata
                        client_socket.send(json.dumps({
                            'type': 'join_success',
                            'message': 'Te has unido a la sala exitosamente'
                        }).encode())
                
                elif message_type == 'message' and username:
                    content = message.get('content')
                    self.broadcast_message(content, username)
        
        except Exception as e:
            print(f"Error con cliente {address}: {e}")
            if username:
                print(f"El usuario {username} se ha desconectado")
        
        finally:
            if username:
                self.leave_room(client_socket)
            client_socket.close()

    def stop(self):
        """Detiene el servidor"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("Servidor detenido")

def main():
    print("=== Chat P2P Global ===")
    print("\n1. Crear sala")
    print("2. Unirse a sala")
    print("3. Salir")
    
    while True:
        try:
            option = input("\nElige una opción (1-3): ").strip()
            
            if option == "1":
                username = input("Tu nombre: ").strip()
                if not username:
                    print("El nombre no puede estar vacío")
                    continue
                
                try:
                    # Iniciar servidor
                    server = ChatServer()
                    server.start()
                    server.create_room(username)
                    
                    print(f"\nIP pública del servidor: {server.public_ip}")
                    print("\nComparte esta información para que otros se unan:")
                    print(f"IP: {server.public_ip}")
                    print("\nEscribe tus mensajes (escribe 'exit' para salir):")
                    
                    # Unir al creador a su propia sala
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    
                    # Configuración de keepalive compatible con todos los sistemas
                    if hasattr(socket, 'TCP_KEEPIDLE'):
                        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
                    if hasattr(socket, 'TCP_KEEPINTVL'):
                        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
                    if hasattr(socket, 'TCP_KEEPCNT'):
                        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 6)
                    
                    client_socket.connect(('127.0.0.1', server.port))
                    
                    # Enviar solicitud de unión
                    join_message = {
                        'type': 'join',
                        'username': username
                    }
                    client_socket.send(json.dumps(join_message).encode())
                    
                    # Esperar confirmación
                    response = client_socket.recv(4096)
                    if response:
                        response_data = json.loads(response.decode())
                        if response_data.get('type') == 'error':
                            print(f"\nError: {response_data.get('message')}")
                            server.stop()
                            break
                        elif response_data.get('type') == 'join_success':
                            print("\nConectado exitosamente a la sala")
                    
                    # Thread para escuchar mensajes
                    def listen_for_messages():
                        while server.running:
                            try:
                                data = client_socket.recv(4096)
                                if not data:
                                    break
                                message = json.loads(data.decode())
                                if message['type'] == 'message':
                                    timestamp = message.get('timestamp', '')
                                    sender = message.get('username', 'Sistema')
                                    content = message.get('content', '')
                                    if sender != username:  # No mostrar mensajes propios
                                        print(f"\n[{timestamp}] {sender}: {content}")
                            except Exception as e:
                                if server.running:
                                    print(f"\nError al recibir mensaje: {e}")
                                break
                        if server.running:
                            print("\nDesconectado del servidor")
                    
                    listen_thread = threading.Thread(target=listen_for_messages)
                    listen_thread.daemon = True
                    listen_thread.start()
                    
                    while server.running:
                        try:
                            message = input()
                            if message.lower() == 'exit':
                                break
                            # Mostrar mensaje propio inmediatamente
                            timestamp = datetime.now().strftime("%H:%M:%S")
                            print(f"\n[{timestamp}] {username}: {message}")
                            
                            message_data = {
                                'type': 'message',
                                'content': message
                            }
                            client_socket.send(json.dumps(message_data).encode())
                        except Exception as e:
                            print(f"\nError al enviar mensaje: {e}")
                            break
                    
                    server.stop()
                    break
                except Exception as e:
                    print(f"\nError al iniciar el servidor: {e}")
                    print("Asegúrate de que el puerto 5000 no esté en uso")
                    continue
            
            elif option == "2":
                username = input("Tu nombre: ").strip()
                if not username:
                    print("El nombre no puede estar vacío")
                    continue
                
                server_ip = input("IP del servidor: ").strip()
                if not server_ip:
                    print("La IP no puede estar vacía")
                    continue
                
                try:
                    print(f"\nIntentando conectar a {server_ip}:5000...")
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    
                    # Configuración de keepalive compatible con todos los sistemas
                    if hasattr(socket, 'TCP_KEEPIDLE'):
                        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
                    if hasattr(socket, 'TCP_KEEPINTVL'):
                        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
                    if hasattr(socket, 'TCP_KEEPCNT'):
                        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 6)
                    
                    client_socket.settimeout(10)
                    
                    client_socket.connect((server_ip, 5000))
                    print("Conexión establecida")
                    
                    # Enviar solicitud de unión
                    join_message = {
                        'type': 'join',
                        'username': username
                    }
                    client_socket.send(json.dumps(join_message).encode())
                    
                    # Esperar respuesta
                    response = client_socket.recv(4096)
                    if response:
                        response_data = json.loads(response.decode())
                        if response_data.get('type') == 'error':
                            print(f"\nError: {response_data.get('message')}")
                            client_socket.close()
                            continue
                        elif response_data.get('type') == 'join_success':
                            print("\nConectado exitosamente a la sala")
                            print("\nEscribe tus mensajes (escribe 'exit' para salir):")
                            
                            # Thread para escuchar mensajes
                            def listen_for_messages():
                                while True:
                                    try:
                                        data = client_socket.recv(4096)
                                        if not data:
                                            break
                                        message = json.loads(data.decode())
                                        if message['type'] == 'message':
                                            timestamp = message.get('timestamp', '')
                                            sender = message.get('username', 'Sistema')
                                            content = message.get('content', '')
                                            if sender != username:  # No mostrar mensajes propios
                                                print(f"\n[{timestamp}] {sender}: {content}")
                                    except Exception as e:
                                        print(f"\nError al recibir mensaje: {e}")
                                        break
                                print("\nDesconectado del servidor")
                            
                            listen_thread = threading.Thread(target=listen_for_messages)
                            listen_thread.daemon = True
                            listen_thread.start()
                            
                            # Enviar mensajes
                            while True:
                                try:
                                    message = input()
                                    if message.lower() == 'exit':
                                        break
                                    
                                    # Mostrar mensaje propio inmediatamente
                                    timestamp = datetime.now().strftime("%H:%M:%S")
                                    print(f"\n[{timestamp}] {username}: {message}")
                                    
                                    message_data = {
                                        'type': 'message',
                                        'content': message
                                    }
                                    client_socket.send(json.dumps(message_data).encode())
                                except Exception as e:
                                    print(f"\nError al enviar mensaje: {e}")
                                    break
                    
                except socket.timeout:
                    print("\nError: Tiempo de espera agotado al conectar con el servidor")
                    print("Asegúrate de que:")
                    print("1. La IP del servidor sea correcta")
                    print("2. El servidor esté en ejecución")
                    print("3. El puerto 5000 esté abierto en el firewall/router del servidor")
                except ConnectionRefusedError:
                    print("\nError: Conexión rechazada por el servidor")
                    print("Asegúrate de que:")
                    print("1. La IP del servidor sea correcta")
                    print("2. El servidor esté en ejecución")
                    print("3. El puerto 5000 esté abierto en el firewall/router del servidor")
                except Exception as e:
                    print(f"\nError al conectar: {e}")
                    print("Asegúrate de que la IP sea correcta y el servidor esté en ejecución")
                
                break
            
            elif option == "3":
                break
            
            else:
                print("Opción no válida")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main() 