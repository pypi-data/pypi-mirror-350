import socket
import threading
import json
import time
import random
import os
from datetime import datetime

class ChatRoom:
    def __init__(self, room_id, creator_name):
        self.room_id = room_id
        self.creator_name = creator_name
        self.users = {}  # {socket: username}
        self.messages = []
        self.created_at = datetime.now()

class ChatServer:
    def __init__(self, host='0.0.0.0', port=0):
        self.host = host
        self.port = port
        self.rooms = {}  # {room_id: ChatRoom}
        self.server_socket = None
        self.running = False

    def create_room(self, creator_name):
        """Crea una nueva sala de chat"""
        room_id = f"{random.randint(1000, 9999)}"
        self.rooms[room_id] = ChatRoom(room_id, creator_name)
        return room_id

    def join_room(self, room_id, username, client_socket):
        """Une un usuario a una sala"""
        if room_id in self.rooms:
            self.rooms[room_id].users[client_socket] = username
            # Enviar historial de mensajes al nuevo usuario
            for msg in self.rooms[room_id].messages:
                client_socket.send(json.dumps(msg).encode())
            # Notificar a todos los usuarios
            self.broadcast_message(room_id, f"{username} se ha unido a la sala", "Sistema")
            return True
        return False

    def leave_room(self, room_id, client_socket):
        """Saca a un usuario de la sala"""
        if room_id in self.rooms and client_socket in self.rooms[room_id].users:
            username = self.rooms[room_id].users[client_socket]
            del self.rooms[room_id].users[client_socket]
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
            self.rooms[room_id].messages.append(message_data)
            
            # Enviar mensaje a todos los usuarios
            for client_socket in self.rooms[room_id].users:
                try:
                    client_socket.send(json.dumps(message_data).encode())
                except:
                    pass

    def start(self):
        """Inicia el servidor"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.port = self.server_socket.getsockname()[1]
        self.server_socket.listen(5)
        self.running = True
        
        print(f"Servidor iniciado en {self.host}:{self.port}")
        
        # Iniciar thread para escuchar conexiones
        listen_thread = threading.Thread(target=self._listen_for_connections)
        listen_thread.daemon = True
        listen_thread.start()

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
        current_room = None
        username = None
        
        try:
            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                    
                message = json.loads(data.decode())
                message_type = message.get('type')
                
                if message_type == 'join':
                    room_id = message.get('room_id')
                    username = message.get('username')
                    if self.join_room(room_id, username, client_socket):
                        current_room = room_id
                        print(f"{username} se ha unido a la sala {room_id}")
                    else:
                        client_socket.send(json.dumps({
                            'type': 'error',
                            'message': 'Sala no encontrada'
                        }).encode())
                
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
    print("=== Chat P2P ===")
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
                
                server = ChatServer()
                server.start()
                room_id = server.create_room(username)
                
                print(f"\nCódigo de la sala: {room_id}")
                print("Comparte este código para que otros se unan")
                print("\nEscribe tus mensajes (escribe 'exit' para salir):")
                
                # Unir al creador a su propia sala
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect(('127.0.0.1', server.port))
                server.join_room(room_id, username, client_socket)
                
                while server.running:
                    message = input()
                    if message.lower() == 'exit':
                        break
                    server.broadcast_message(room_id, message, username)
                
                server.stop()
                break
            
            elif option == "2":
                room_id = input("Código de la sala: ").strip()
                if not room_id:
                    print("El código no puede estar vacío")
                    continue
                
                username = input("Tu nombre: ").strip()
                if not username:
                    print("El nombre no puede estar vacío")
                    continue
                
                # Intentar conectarse a diferentes puertos comunes
                ports = [5000, 5001, 5002, 5003, 5004]
                connected = False
                
                for port in ports:
                    try:
                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client_socket.settimeout(1)  # 1 segundo de timeout
                        client_socket.connect(('127.0.0.1', port))
                        
                        # Enviar solicitud de unión
                        join_message = {
                            'type': 'join',
                            'room_id': room_id,
                            'username': username
                        }
                        client_socket.send(json.dumps(join_message).encode())
                        
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
                                        print(f"\n[{timestamp}] {sender}: {content}")
                                except:
                                    break
                            print("\nDesconectado del servidor")
                        
                        listen_thread = threading.Thread(target=listen_for_messages)
                        listen_thread.daemon = True
                        listen_thread.start()
                        
                        # Enviar mensajes
                        while True:
                            message = input()
                            if message.lower() == 'exit':
                                break
                            
                            message_data = {
                                'type': 'message',
                                'content': message
                            }
                            client_socket.send(json.dumps(message_data).encode())
                        
                        connected = True
                        break
                        
                    except:
                        continue
                    finally:
                        if not connected:
                            client_socket.close()
                
                if not connected:
                    print("No se pudo encontrar la sala. Asegúrate de que el código sea correcto.")
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