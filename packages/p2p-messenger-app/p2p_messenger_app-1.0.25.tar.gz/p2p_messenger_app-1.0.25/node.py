import socket
import threading
import json
import time
import random
import os
from datetime import datetime
import requests
import uuid

class ChatRoom:
    def __init__(self, room_id, creator_name):
        self.room_id = room_id
        self.creator_name = creator_name
        self.users = {}  # {socket: username}
        self.messages = []
        self.created_at = datetime.now()
        self.node_id = str(uuid.uuid4())  # Identificador único para el nodo

class ChatServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.rooms = {}  # {room_id: {'room': ChatRoom, 'ip': ip_address}}
        self.server_socket = None
        self.running = False
        self.public_ip = self._get_public_ip()
        self.known_nodes = set()
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
        room_id = f"{random.randint(1000, 9999)}"
        self.rooms[room_id] = {
            'room': ChatRoom(room_id, creator_name),
            'ip': self.public_ip
        }
        return room_id

    def join_room(self, room_id, username, client_socket):
        """Une un usuario a una sala"""
        if room_id in self.rooms:
            self.rooms[room_id]['room'].users[client_socket] = username
            # Enviar historial de mensajes al nuevo usuario
            for msg in self.rooms[room_id]['room'].messages:
                client_socket.send(json.dumps(msg).encode())
            # Notificar a todos los usuarios
            self.broadcast_message(room_id, f"{username} se ha unido a la sala", "Sistema")
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

    def leave_room(self, room_id, client_socket):
        """Saca a un usuario de la sala"""
        if room_id in self.rooms and client_socket in self.rooms[room_id]['room'].users:
            username = self.rooms[room_id]['room'].users[client_socket]
            del self.rooms[room_id]['room'].users[client_socket]
            self.broadcast_message(room_id, f"{username} ha salido de la sala", "Sistema")
            return True
        return False

    def broadcast_message(self, room_id, message, username):
        """Envía un mensaje a todos los usuarios de la sala"""
        if room_id in self.rooms:
            timestamp = datetime.now().strftime("%H:%M:%S")
            message_data = {
                'type': 'message',
                'username': username,
                'content': message,
                'timestamp': timestamp
            }
            self.rooms[room_id]['room'].messages.append(message_data)
            
            # Enviar mensaje a todos los usuarios
            for client_socket in self.rooms[room_id]['room'].users:
                try:
                    client_socket.send(json.dumps(message_data).encode())
                except:
                    pass

    def start(self):
        """Inicia el servidor con mejor manejo de errores"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            self.server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
            self.server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
            self.server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 6)
            
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"\nServidor iniciado en:")
            print(f"IP pública: {self.public_ip}")
            print(f"Puerto: {self.port}")
            print("\nEste servidor es accesible desde cualquier parte del mundo")
            print("Asegúrate de que el puerto 5000 esté abierto en tu firewall/router")
            print("\nPara abrir el puerto en tu router:")
            print("1. Accede a la configuración de tu router")
            print("2. Busca la sección de 'Port Forwarding' o 'Redirección de puertos'")
            print("3. Añade una regla para el puerto 5000 TCP")
            print("4. Asigna la redirección a la IP local de este dispositivo")
            
            listen_thread = threading.Thread(target=self._listen_for_connections)
            listen_thread.daemon = True
            listen_thread.start()

            discovery_thread = threading.Thread(target=self._discovery_loop)
            discovery_thread.daemon = True
            discovery_thread.start()
        except Exception as e:
            print(f"\nError al iniciar el servidor: {e}")
            print("Asegúrate de que el puerto 5000 no esté en uso")
            self.running = False
            raise

    def _discovery_loop(self):
        """Loop para descubrir otros nodos y salas en la red"""
        while self.running:
            try:
                # Intentar conectarse a nodos conocidos
                for node in self.known_nodes:
                    try:
                        node_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        node_socket.settimeout(2)
                        node_socket.connect((node, 5000))
                        
                        # Enviar solicitud de descubrimiento
                        discovery_message = {
                            'type': 'discovery',
                            'rooms': {room_id: data['ip'] for room_id, data in self.rooms.items()}
                        }
                        node_socket.send(json.dumps(discovery_message).encode())
                        
                        # Recibir respuesta
                        response = node_socket.recv(4096)
                        if response:
                            response_data = json.loads(response.decode())
                            if response_data.get('type') == 'discovery_response':
                                # Actualizar lista de salas conocidas
                                for room_id, ip in response_data.get('rooms', {}).items():
                                    if room_id not in self.rooms:
                                        self.rooms[room_id] = {'ip': ip}
                        
                        node_socket.close()
                    except:
                        self.known_nodes.remove(node)
            except:
                pass
            time.sleep(30)  # Esperar 30 segundos antes de la siguiente ronda

    def _listen_for_connections(self):
        """Escucha conexiones entrantes"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                # Añadir el nodo a la lista de nodos conocidos
                self.known_nodes.add(address[0])
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
        current_room = None
        username = None
        
        try:
            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                    
                message = json.loads(data.decode())
                message_type = message.get('type')
                
                if message_type == 'discovery':
                    # Responder con nuestras salas
                    response = {
                        'type': 'discovery_response',
                        'rooms': {room_id: data['ip'] for room_id, data in self.rooms.items()}
                    }
                    client_socket.send(json.dumps(response).encode())
                    continue
                
                elif message_type == 'join':
                    room_id = message.get('room_id')
                    username = message.get('username')
                    
                    # Si la sala no está en nuestro servidor, intentar redirigir
                    if room_id not in self.rooms:
                        client_socket.send(json.dumps({
                            'type': 'redirect',
                            'ip': self.rooms.get(room_id, {}).get('ip')
                        }).encode())
                        continue
                    
                    if self.join_room(room_id, username, client_socket):
                        current_room = room_id
                        print(f"{username} se ha unido a la sala {room_id}")
                
                elif message_type == 'message' and current_room:
                    content = message.get('content')
                    self.broadcast_message(current_room, content, username)
        
        except Exception as e:
            print(f"Error con cliente {address}: {e}")
        
        finally:
            if current_room:
                self.leave_room(current_room, client_socket)
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
                    server = ChatServer()
                    server.start()
                    room_id = server.create_room(username)
                    
                    print(f"\nCódigo de la sala: {room_id}")
                    print(f"IP pública del servidor: {server.public_ip}")
                    print("\nComparte esta información para que otros se unan:")
                    print(f"Código: {room_id}")
                    print(f"IP: {server.public_ip}")
                    print("\nEscribe tus mensajes (escribe 'exit' para salir):")
                    
                    # Unir al creador a su propia sala
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
                    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
                    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 6)
                    
                    client_socket.connect(('127.0.0.1', server.port))
                    
                    # Enviar solicitud de unión
                    join_message = {
                        'type': 'join',
                        'room_id': room_id,
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
                room_id = input("Código de la sala: ").strip()
                if not room_id:
                    print("El código no puede estar vacío")
                    continue
                
                username = input("Tu nombre: ").strip()
                if not username:
                    print("El nombre no puede estar vacío")
                    continue
                
                print("\n¿Tienes la IP del servidor?")
                print("1. Sí, tengo la IP")
                print("2. No, intentar descubrir automáticamente")
                ip_option = input("Elige una opción (1-2): ").strip()
                
                server_ip = None
                if ip_option == "1":
                    server_ip = input("IP del servidor: ").strip()
                    if not server_ip:
                        print("La IP no puede estar vacía")
                        continue
                
                try:
                    if server_ip:
                        print(f"\nIntentando conectar directamente a {server_ip}:5000...")
                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
                        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
                        client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 6)
                        client_socket.settimeout(10)
                        
                        try:
                            client_socket.connect((server_ip, 5000))
                            print("Conexión establecida")
                            
                            # Enviar solicitud de unión
                            join_message = {
                                'type': 'join',
                                'room_id': room_id,
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
                                    print("\nEscribe tus mensajes (escribe 'exit' para salir):")
                                    connected = True
                        except Exception as e:
                            print(f"\nError al conectar directamente: {e}")
                            print("Intentando descubrimiento automático...")
                            server_ip = None
                    
                    if not server_ip:
                        print("\nBuscando sala...")
                        # Intentar conectar a nodos conocidos
                        connected = False
                        for node in ['127.0.0.1']:  # Empezar con localhost
                            try:
                                print(f"Intentando conectar a {node}...")
                                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
                                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
                                client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 6)
                                client_socket.settimeout(5)
                                
                                client_socket.connect((node, 5000))
                                
                                # Enviar solicitud de unión
                                join_message = {
                                    'type': 'join',
                                    'room_id': room_id,
                                    'username': username
                                }
                                client_socket.send(json.dumps(join_message).encode())
                                
                                # Esperar respuesta
                                response = client_socket.recv(4096)
                                if response:
                                    response_data = json.loads(response.decode())
                                    if response_data.get('type') == 'redirect':
                                        # Si recibimos una redirección, intentar con la nueva IP
                                        new_ip = response_data.get('ip')
                                        if new_ip:
                                            print(f"Redirigiendo a {new_ip}...")
                                            client_socket.close()
                                            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                            client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                                            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
                                            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
                                            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 6)
                                            client_socket.settimeout(5)
                                            client_socket.connect((new_ip, 5000))
                                            client_socket.send(json.dumps(join_message).encode())
                                            response = client_socket.recv(4096)
                                            if response:
                                                response_data = json.loads(response.decode())
                                    
                                    if response_data.get('type') == 'error':
                                        print(f"\nError: {response_data.get('message')}")
                                        client_socket.close()
                                        continue
                                    elif response_data.get('type') == 'join_success':
                                        print("\nConexión establecida")
                                        print("\nEscribe tus mensajes (escribe 'exit' para salir):")
                                        connected = True
                                        break
                            except:
                                continue
                    
                    if not connected:
                        print("\nNo se pudo encontrar la sala")
                        print("Asegúrate de que:")
                        print("1. El código de la sala sea correcto")
                        print("2. El servidor esté en ejecución")
                        print("3. Si tienes la IP del servidor, úsala en la opción 1")
                        continue
                    
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
                    
                except Exception as e:
                    print(f"\nError al conectar: {e}")
                    print("Asegúrate de que el código de la sala sea correcto")
                
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