import socket
import threading
import json
import time
import random
import os
import base64
from cryptography.fernet import Fernet
import uuid
import sqlite3
from datetime import datetime
import hashlib
import psutil

class UserManager:
    def __init__(self):
        self.db_path = 'users.db'
        self._init_db()

    def _init_db(self):
        """Inicializa la base de datos de usuarios"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (user_id TEXT PRIMARY KEY,
                     name TEXT,
                     birth_date TEXT,
                     created_at TIMESTAMP)''')
        c.execute('''CREATE TABLE IF NOT EXISTS known_nodes
                    (node_id TEXT PRIMARY KEY,
                     host TEXT,
                     port INTEGER,
                     last_seen TIMESTAMP)''')
        conn.commit()
        conn.close()

    def get_or_create_user(self, name, birth_date):
        """Obtiene el ID de usuario existente o crea uno nuevo"""
        config_path = 'user_config.json'
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    user_id = config.get('user_id')
                    if user_id:
                        return user_id
            except:
                pass

        # Generar ID único basado en nombre y fecha de nacimiento
        user_id = self._generate_user_id(name, birth_date)
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT INTO users (user_id, name, birth_date, created_at) VALUES (?, ?, ?, ?)',
                 (user_id, name, birth_date, datetime.now()))
        conn.commit()
        conn.close()

        with open(config_path, 'w') as f:
            json.dump({'user_id': user_id}, f)

        return user_id

    def _generate_user_id(self, name, birth_date):
        """Genera un ID único basado en el nombre y fecha de nacimiento"""
        # Combinar nombre y fecha de nacimiento
        combined = f"{name.lower()}{birth_date}"
        # Generar hash
        hash_object = hashlib.sha256(combined.encode())
        # Tomar los primeros 8 caracteres del hash
        return hash_object.hexdigest()[:8]

    def assign_node_id(self, user_id, node_id):
        """Asigna un ID de nodo a un usuario"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('UPDATE users SET node_id = ? WHERE user_id = ?',
                 (node_id, user_id))
        conn.commit()
        conn.close()

    def get_node_id(self, user_id):
        """Obtiene el ID de nodo asignado a un usuario"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT node_id FROM users WHERE user_id = ?', (user_id,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

    def add_known_node(self, node_id, host, port):
        """Añade o actualiza un nodo conocido"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO known_nodes 
                    (node_id, host, port, last_seen) 
                    VALUES (?, ?, ?, ?)''',
                 (node_id, host, port, datetime.now()))
        conn.commit()
        conn.close()

    def get_known_nodes(self):
        """Obtiene la lista de nodos conocidos"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT node_id, host, port FROM known_nodes')
        nodes = c.fetchall()
        conn.close()
        return [(node_id, host, port) for node_id, host, port in nodes]

class FriendManager:
    def __init__(self):
        self.db_path = 'friends.db'
        self._init_db()

    def _init_db(self):
        """Inicializa la base de datos de amigos"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS friends
                    (node_id TEXT PRIMARY KEY,
                     status TEXT,
                     last_seen TIMESTAMP)''')
        c.execute('''CREATE TABLE IF NOT EXISTS friend_requests
                    (from_id TEXT,
                     to_id TEXT,
                     status TEXT,
                     created_at TIMESTAMP,
                     PRIMARY KEY (from_id, to_id))''')
        conn.commit()
        conn.close()

    def add_friend(self, node_id):
        """Añade un amigo"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO friends (node_id, status, last_seen) VALUES (?, ?, ?)',
                 (node_id, 'online', datetime.now()))
        conn.commit()
        conn.close()

    def remove_friend(self, node_id):
        """Elimina un amigo"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM friends WHERE node_id = ?', (node_id,))
        conn.commit()
        conn.close()

    def get_friends(self):
        """Obtiene la lista de amigos"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT node_id, status, last_seen FROM friends')
        friends = c.fetchall()
        conn.close()
        return friends

    def add_friend_request(self, from_id, to_id):
        """Añade una solicitud de amistad"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO friend_requests (from_id, to_id, status, created_at) VALUES (?, ?, ?, ?)',
                 (from_id, to_id, 'pending', datetime.now()))
        conn.commit()
        conn.close()

    def get_friend_requests(self):
        """Obtiene las solicitudes de amistad pendientes"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT from_id, created_at FROM friend_requests WHERE status = ?', ('pending',))
        requests = c.fetchall()
        conn.close()
        return requests

    def accept_friend_request(self, from_id):
        """Acepta una solicitud de amistad"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('UPDATE friend_requests SET status = ? WHERE from_id = ? AND status = ?',
                 ('accepted', from_id, 'pending'))
        c.execute('INSERT OR REPLACE INTO friends (node_id, status, last_seen) VALUES (?, ?, ?)',
                 (from_id, 'online', datetime.now()))
        conn.commit()
        conn.close()

    def reject_friend_request(self, from_id):
        """Rechaza una solicitud de amistad"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('DELETE FROM friend_requests WHERE from_id = ? AND status = ?',
                 (from_id, 'pending'))
        conn.commit()
        conn.close()

class P2PNode:
    def __init__(self, name, birth_date, host='0.0.0.0', port=0):
        self.host = host
        self.port = port
        self.user_manager = UserManager()
        self.name = name
        self.birth_date = birth_date
        
        # Obtener la IP local usando psutil
        try:
            interfaces = psutil.net_if_addrs()
            for interface_name, addrs in interfaces.items():
                for addr in addrs:
                    if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                        self.local_ip = addr.address
                        break
                if hasattr(self, 'local_ip'):
                    break
            else:
                self.local_ip = '127.0.0.1'
        except:
            self.local_ip = '127.0.0.1'
        
        # Generar ID único basado en nombre y fecha de nacimiento
        self.node_id = self.user_manager._generate_user_id(name, birth_date)
        
        self.peers = {}
        self.server_socket = None
        self.running = False
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.known_nodes = {}
        self.verifying_id = False
        self.friend_manager = FriendManager()
        self.contacts = {}

    def add_contact(self, contact_id, contact_name):
        """Añade un contacto a la lista de contactos"""
        self.contacts[contact_id] = contact_name
        self.user_manager.add_known_node(contact_id, contact_name)

    def get_contacts(self):
        """Obtiene la lista de contactos"""
        return self.contacts

    def verify_node_id(self):
        """Verifica que el ID del nodo no esté en uso"""
        self.verifying_id = True
        known_nodes = self.user_manager.get_known_nodes()
        
        for node_id, host, port in known_nodes:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(2)
                client_socket.connect((host, port))
                
                # Enviar mensaje de verificación
                verify_message = {
                    'type': 'verify_id',
                    'node_id': self.node_id
                }
                
                encrypted_message = self.cipher_suite.encrypt(json.dumps(verify_message).encode())
                client_socket.send(encrypted_message)
                
                # Esperar respuesta
                data = client_socket.recv(4096)
                if data:
                    response = json.loads(self.cipher_suite.decrypt(data).decode())
                    if response.get('type') == 'id_in_use':
                        print(f"ID {self.node_id} ya está en uso. Generando nuevo ID...")
                        self.node_id = f"{random.randint(1000, 9999)}-{hashlib.sha256(self.local_ip.encode()).hexdigest()[:4]}"
                        self.user_manager.assign_node_id(self.name, self.node_id)
                        client_socket.close()
                        return self.verify_node_id()  # Verificar el nuevo ID
                
                client_socket.close()
            except:
                continue
        
        self.verifying_id = False
        return True

    def _process_message(self, message_data, address):
        """Procesa un mensaje recibido"""
        message_type = message_data.get('type')
        
        if message_type == 'verify_id':
            # Si recibimos una verificación de ID y es el nuestro, responder que está en uso
            if message_data.get('node_id') == self.node_id:
                response = {
                    'type': 'id_in_use'
                }
                return self.cipher_suite.encrypt(json.dumps(response).encode())
            return None
            
        elif message_type == 'connect':
            peer_id = message_data.get('node_id')
            self.peers[peer_id] = (address[0], message_data.get('port'))
            self.known_nodes[peer_id] = (address[0], message_data.get('port'))
            self.user_manager.add_known_node(peer_id, address[0], message_data.get('port'))
            print(f"Nuevo peer conectado: {peer_id} desde {address[0]}:{message_data.get('port')}")
            
        elif message_type == 'message':
            content = message_data.get('content')
            if message_data.get('has_file'):
                file_data = base64.b64decode(message_data.get('file_data'))
                file_name = message_data.get('file_name')
                with open(file_name, 'wb') as f:
                    f.write(file_data)
                content += f"\n[Archivo adjunto: {file_name}]"
            print(f"\nMensaje de {message_data.get('from')}: {content}")

        elif message_type == 'friend_request':
            from_id = message_data.get('from')
            print(f"\nSolicitud de amistad de {from_id}")
            print("Comandos disponibles:")
            print("accept <id> - Aceptar solicitud")
            print("reject <id> - Rechazar solicitud")
            
        elif message_type == 'friend_response':
            response = message_data.get('response')
            from_id = message_data.get('from')
            if response == 'accepted':
                print(f"\n{from_id} ha aceptado tu solicitud de amistad")
                self.friend_manager.add_friend(from_id)
            else:
                print(f"\n{from_id} ha rechazado tu solicitud de amistad")

    def start(self):
        """Inicia el nodo y comienza a escuchar conexiones entrantes"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Intentar puertos hasta encontrar uno disponible
        for port in range(5000, 5100):
            try:
                self.server_socket.bind((self.host, port))
                self.port = port
                break
            except OSError:
                continue
        else:
            print("Error: No se pudo encontrar un puerto disponible")
            return

        self.server_socket.listen(5)
        self.running = True
        
        # Verificar que el ID no esté en uso
        self.verify_node_id()
        
        print(f"Nodo iniciado en {self.host}:{self.port}")
        print(f"ID de usuario: {self.name}")
        print(f"ID del nodo: {self.node_id}")
        print(f"IP local: {self.local_ip}")
        
        # Iniciar thread para escuchar conexiones
        listen_thread = threading.Thread(target=self._listen_for_connections)
        listen_thread.daemon = True
        listen_thread.start()

    def _listen_for_connections(self):
        """Escucha conexiones entrantes de otros nodos"""
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self._handle_connection,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                if self.running:
                    print(f"Error al aceptar conexión: {e}")

    def _handle_connection(self, client_socket, address):
        """Maneja una conexión entrante"""
        try:
            data = client_socket.recv(4096)
            if data:
                message = self.cipher_suite.decrypt(data).decode()
                message_data = json.loads(message)
                self._process_message(message_data, address)
        except Exception as e:
            print(f"Error al manejar conexión: {e}")
        finally:
            client_socket.close()

    def connect_to_peer(self, host, port):
        """Conecta con otro nodo"""
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            
            # Enviar mensaje de conexión
            connect_message = {
                'type': 'connect',
                'node_id': self.node_id,
                'port': self.port
            }
            
            encrypted_message = self.cipher_suite.encrypt(json.dumps(connect_message).encode())
            client_socket.send(encrypted_message)
            client_socket.close()
            
            print(f"Conectado exitosamente a {host}:{port}")
            return True
        except Exception as e:
            print(f"Error al conectar con peer: {e}")
            return False

    def send_message(self, target_id, message, file_path=None):
        """Envía un mensaje a un nodo específico"""
        # Intentar puertos hasta encontrar el nodo
        host = "127.0.0.1"  # Por defecto, intentar en localhost
        
        for port in range(5000, 5100):
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(1)  # Timeout de 1 segundo
                client_socket.connect((host, port))
                
                message_data = {
                    'type': 'message',
                    'from': self.node_id,
                    'content': message,
                    'has_file': False
                }
                
                if file_path and os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        file_data = f.read()
                    message_data['has_file'] = True
                    message_data['file_name'] = os.path.basename(file_path)
                    message_data['file_data'] = base64.b64encode(file_data).decode()
                
                encrypted_message = self.cipher_suite.encrypt(json.dumps(message_data).encode())
                client_socket.send(encrypted_message)
                client_socket.close()
                
                print(f"Mensaje enviado exitosamente a {target_id}")
                return True
            except:
                continue
        
        print(f"Error: No se pudo conectar con el nodo {target_id}")
        return False

    def stop(self):
        """Detiene el nodo"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("Nodo detenido")

    def send_friend_request(self, target_id):
        """Envía una solicitud de amistad"""
        try:
            port = int(target_id.split('-')[0])
            host = "127.0.0.1"
            
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            
            message_data = {
                'type': 'friend_request',
                'from': self.node_id
            }
            
            encrypted_message = self.cipher_suite.encrypt(json.dumps(message_data).encode())
            client_socket.send(encrypted_message)
            client_socket.close()
            
            self.friend_manager.add_friend_request(self.node_id, target_id)
            print(f"Solicitud de amistad enviada a {target_id}")
            return True
        except Exception as e:
            print(f"Error al enviar solicitud de amistad: {e}")
            return False

    def accept_friend_request(self, from_id):
        """Acepta una solicitud de amistad"""
        self.friend_manager.accept_friend_request(from_id)
        
        try:
            port = int(from_id.split('-')[0])
            host = "127.0.0.1"
            
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            
            message_data = {
                'type': 'friend_response',
                'from': self.node_id,
                'response': 'accepted'
            }
            
            encrypted_message = self.cipher_suite.encrypt(json.dumps(message_data).encode())
            client_socket.send(encrypted_message)
            client_socket.close()
            
            print(f"Solicitud de amistad aceptada de {from_id}")
            return True
        except Exception as e:
            print(f"Error al aceptar solicitud de amistad: {e}")
            return False

    def reject_friend_request(self, from_id):
        """Rechaza una solicitud de amistad"""
        self.friend_manager.reject_friend_request(from_id)
        
        try:
            port = int(from_id.split('-')[0])
            host = "127.0.0.1"
            
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            
            message_data = {
                'type': 'friend_response',
                'from': self.node_id,
                'response': 'rejected'
            }
            
            encrypted_message = self.cipher_suite.encrypt(json.dumps(message_data).encode())
            client_socket.send(encrypted_message)
            client_socket.close()
            
            print(f"Solicitud de amistad rechazada de {from_id}")
            return True
        except Exception as e:
            print(f"Error al rechazar solicitud de amistad: {e}")
            return False

    def list_friends(self):
        """Lista los amigos en línea"""
        friends = self.friend_manager.get_friends()
        if not friends:
            print("No tienes amigos en línea")
            return
        
        print("\nAmigos en línea:")
        for node_id, status, last_seen in friends:
            print(f"- {node_id} ({status})")

def main():
    # Solicitar nombre y año de nacimiento al iniciar
    name = input("Ingresa tu nombre completo: ").strip()
    birth_year = input("Ingresa tu año de nacimiento (ejemplo: 1990): ").strip()
    
    # Validar formato del año
    try:
        year = int(birth_year)
        if year < 1900 or year > datetime.now().year:
            print(f"Error: El año debe estar entre 1900 y {datetime.now().year}")
            return
    except ValueError:
        print("Error: Debes ingresar un año válido (ejemplo: 1990)")
        return
    
    node = P2PNode(name, birth_year)
    node.start()
    
    print("\nComandos disponibles:")
    print("send <id> <mensaje> - Enviar mensaje a un contacto")
    print("sendfile <id> <ruta_archivo> - Enviar archivo a un contacto")
    print("add <id> <nombre> - Añadir contacto")
    print("contacts - Ver lista de contactos")
    print("friend <id> - Enviar solicitud de amistad")
    print("accept <id> - Aceptar solicitud de amistad")
    print("reject <id> - Rechazar solicitud de amistad")
    print("friends - Ver lista de amigos en línea")
    print("exit - Salir")
    
    while True:
        try:
            command = input("\n> ").strip()
            if not command:
                continue

            if command.startswith("add "):
                try:
                    parts = command[4:].split("<", 2)
                    if len(parts) != 3:
                        print("Error: Formato incorrecto. Uso: add <id> <nombre>")
                        continue
                    
                    contact_id = parts[1].split(">")[0].strip()
                    contact_name = parts[2].rstrip(">")
                    
                    node.add_contact(contact_id, contact_name)
                    print(f"Contacto añadido: {contact_name} ({contact_id})")
                except Exception as e:
                    print("Error en el formato. Uso: add <id> <nombre>")

            elif command == "contacts":
                contacts = node.get_contacts()
                if not contacts:
                    print("No tienes contactos")
                else:
                    print("\nContactos:")
                    for contact_id, contact_name in contacts.items():
                        print(f"- {contact_name} ({contact_id})")

            elif command.startswith("send "):
                try:
                    parts = command[5:].split("<", 2)
                    if len(parts) != 3:
                        print("Error: Formato incorrecto. Uso: send <id> <mensaje>")
                        continue
                    
                    target_id = parts[1].split(">")[0].strip()
                    message = parts[2].rstrip(">")
                    
                    node.send_message(target_id, message)
                except Exception as e:
                    print("Error en el formato. Uso: send <id> <mensaje>")
            
            elif command.startswith("sendfile "):
                try:
                    parts = command[9:].split("<", 2)
                    if len(parts) != 3:
                        print("Error: Formato incorrecto. Uso: sendfile <id> <ruta_archivo>")
                        continue
                    
                    target_id = parts[1].split(">")[0].strip()
                    file_path = parts[2].rstrip(">")
                    
                    if os.path.exists(file_path):
                        node.send_message(target_id, f"Archivo: {os.path.basename(file_path)}", file_path)
                    else:
                        print(f"Error: El archivo {file_path} no existe")
                except Exception as e:
                    print("Error en el formato. Uso: sendfile <id> <ruta_archivo>")
            
            elif command.startswith("friend "):
                try:
                    target_id = command[7:].strip()
                    if not target_id.startswith("<") or not target_id.endswith(">"):
                        print("Error: Formato incorrecto. Uso: friend <id>")
                        continue
                    target_id = target_id[1:-1]
                    node.send_friend_request(target_id)
                except Exception as e:
                    print("Error en el formato. Uso: friend <id>")
            
            elif command.startswith("accept "):
                try:
                    from_id = command[7:].strip()
                    if not from_id.startswith("<") or not from_id.endswith(">"):
                        print("Error: Formato incorrecto. Uso: accept <id>")
                        continue
                    from_id = from_id[1:-1]
                    node.accept_friend_request(from_id)
                except Exception as e:
                    print("Error en el formato. Uso: accept <id>")
            
            elif command.startswith("reject "):
                try:
                    from_id = command[7:].strip()
                    if not from_id.startswith("<") or not from_id.endswith(">"):
                        print("Error: Formato incorrecto. Uso: reject <id>")
                        continue
                    from_id = from_id[1:-1]
                    node.reject_friend_request(from_id)
                except Exception as e:
                    print("Error en el formato. Uso: reject <id>")
            
            elif command == "friends":
                node.list_friends()
            
            elif command == "exit":
                node.stop()
                break
            else:
                print("Comando no válido")
        except KeyboardInterrupt:
            node.stop()
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main() 