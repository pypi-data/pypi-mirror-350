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
        room_id = f"room_{random.randint(1000, 9999)}"
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
                
                elif message_type == 'create':
                    username = message.get('username')
                    room_id = self.create_room(username)
                    if self.join_room(room_id, username, client_socket):
                        current_room = room_id
                        print(f"Sala {room_id} creada por {username}")
                        client_socket.send(json.dumps({
                            'type': 'room_created',
                            'room_id': room_id
                        }).encode())
        
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
    server = ChatServer()
    server.start()
    
    print("\nComandos disponibles:")
    print("create <nombre> - Crear una nueva sala")
    print("join <room_id> <nombre> - Unirse a una sala existente")
    print("exit - Salir")
    
    while True:
        try:
            command = input("\n> ").strip()
            if not command:
                continue

            if command == "exit":
                server.stop()
                break
            else:
                print("Comando no válido")
        except KeyboardInterrupt:
            server.stop()
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main() 