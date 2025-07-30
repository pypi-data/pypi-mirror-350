import socket
import threading
import json
import sys

class ChatClient:
    def __init__(self, host='127.0.0.1', port=0):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        self.current_room = None
        self.username = None

    def connect(self, host, port):
        """Conecta al servidor"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.running = True
            
            # Iniciar thread para escuchar mensajes
            listen_thread = threading.Thread(target=self._listen_for_messages)
            listen_thread.daemon = True
            listen_thread.start()
            
            return True
        except Exception as e:
            print(f"Error al conectar: {e}")
            return False

    def create_room(self, username):
        """Crea una nueva sala"""
        self.username = username
        message = {
            'type': 'create',
            'username': username
        }
        self.socket.send(json.dumps(message).encode())
        
        # Esperar respuesta
        data = self.socket.recv(4096)
        response = json.loads(data.decode())
        
        if response['type'] == 'room_created':
            self.current_room = response['room_id']
            print(f"\nSala creada: {self.current_room}")
            print("Comparte este ID para que otros se unan a tu sala")
            return True
        return False

    def join_room(self, room_id, username):
        """Se une a una sala existente"""
        self.username = username
        message = {
            'type': 'join',
            'room_id': room_id,
            'username': username
        }
        self.socket.send(json.dumps(message).encode())
        
        # Esperar respuesta
        data = self.socket.recv(4096)
        response = json.loads(data.decode())
        
        if response['type'] == 'error':
            print(f"\nError: {response['message']}")
            return False
        
        self.current_room = room_id
        print(f"\nUnido a la sala: {room_id}")
        return True

    def send_message(self, message):
        """Envía un mensaje a la sala actual"""
        if not self.current_room:
            print("No estás en ninguna sala")
            return False
        
        message_data = {
            'type': 'message',
            'content': message
        }
        self.socket.send(json.dumps(message_data).encode())
        return True

    def _listen_for_messages(self):
        """Escucha mensajes del servidor"""
        while self.running:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break
                
                message = json.loads(data.decode())
                if message['type'] == 'message':
                    timestamp = message.get('timestamp', '')
                    username = message.get('username', 'Sistema')
                    content = message.get('content', '')
                    print(f"\n[{timestamp}] {username}: {content}")
            except:
                break
        
        print("\nDesconectado del servidor")
        self.running = False

    def disconnect(self):
        """Desconecta del servidor"""
        self.running = False
        if self.socket:
            self.socket.close()

def main():
    if len(sys.argv) < 3:
        print("Uso:")
        print("Para crear una sala:")
        print("python client.py create <nombre>")
        print("\nPara unirse a una sala:")
        print("python client.py join <room_id> <nombre>")
        return

    command = sys.argv[1]
    client = ChatClient()
    
    if command == "create":
        if len(sys.argv) != 3:
            print("Uso: python client.py create <nombre>")
            return
        
        username = sys.argv[2]
        if client.connect('127.0.0.1', 5000):
            if client.create_room(username):
                print("\nEscribe tus mensajes (escribe 'exit' para salir):")
                while client.running:
                    message = input()
                    if message.lower() == 'exit':
                        break
                    client.send_message(message)
    
    elif command == "join":
        if len(sys.argv) != 4:
            print("Uso: python client.py join <room_id> <nombre>")
            return
        
        room_id = sys.argv[2]
        username = sys.argv[3]
        if client.connect('127.0.0.1', 5000):
            if client.join_room(room_id, username):
                print("\nEscribe tus mensajes (escribe 'exit' para salir):")
                while client.running:
                    message = input()
                    if message.lower() == 'exit':
                        break
                    client.send_message(message)
    
    else:
        print("Comando no válido")
    
    client.disconnect()

if __name__ == "__main__":
    main() 