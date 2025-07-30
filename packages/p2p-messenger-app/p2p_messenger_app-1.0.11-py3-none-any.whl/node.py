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
        
        self.peers = {}  # {node_id: (host, port, name, birth_date)}
        self.server_socket = None
        self.running = False
        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.known_nodes = {}
        self.verifying_id = False
        self.friend_manager = FriendManager()
        self.contacts = {}
        
        # Iniciar el descubrimiento de nodos
        self.discovery_thread = None
        self.broadcast_port = 5000  # Puerto para broadcast

    def add_contact(self, contact_name, contact_birth_date):
        """Añade un contacto a la lista de contactos"""
        contact_id = self.user_manager._generate_user_id(contact_name, contact_birth_date)
        self.contacts[contact_id] = (contact_name, contact_birth_date)
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
            peer_name = message_data.get('name')
            peer_birth_date = message_data.get('birth_date')
            self.peers[peer_id] = (address[0], message_data.get('port'), peer_name, peer_birth_date)
            self.known_nodes[peer_id] = (address[0], message_data.get('port'))
            self.user_manager.add_known_node(peer_id, address[0], message_data.get('port'))
            print(f"Nuevo usuario conectado: {peer_name} (Año de nacimiento: {peer_birth_date})")
            
        elif message_type == 'message':
            content = message_data.get('content')
            from_name = message_data.get('from_name')
            if message_data.get('has_file'):
                file_data = base64.b64decode(message_data.get('file_data'))
                file_name = message_data.get('file_name')
                with open(file_name, 'wb') as f:
                    f.write(file_data)
                content += f"\n[Archivo adjunto: {file_name}]"
            print(f"\nMensaje de {from_name}: {content}")

        elif message_type == 'friend_request':
            from_id = message_data.get('from')
            print(f"\nSolicitud de amistad de {from_id}")
            print("Comandos disponibles:")
            print("accept <nombre> <año_nacimiento> - Aceptar solicitud")
            print("reject <nombre> <año_nacimiento> - Rechazar solicitud")
            
        elif message_type == 'friend_response':
            response = message_data.get('response')
            from_id = message_data.get('from')
            if response == 'accepted':
                print(f"\n{from_id} ha aceptado tu solicitud de amistad")
                self.friend_manager.add_friend(from_id)
            else:
                print(f"\n{from_id} ha rechazado tu solicitud de amistad")

    def start_discovery(self):
        """Inicia el proceso de descubrimiento de nodos en la red"""
        self.discovery_thread = threading.Thread(target=self._discovery_loop)
        self.discovery_thread.daemon = True
        self.discovery_thread.start()

    def _discovery_loop(self):
        """Loop principal para descubrir nodos en la red"""
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        broadcast_socket.bind(('', self.broadcast_port))
        
        # Conjunto para mantener registro de nodos ya descubiertos
        discovered_nodes = set()
        last_broadcast_time = 0
        
        while self.running:
            try:
                current_time = time.time()
                
                # Enviar broadcast cada 30 segundos
                if current_time - last_broadcast_time >= 30:
                    broadcast_message = {
                        'type': 'discovery',
                        'node_id': self.node_id,
                        'name': self.name,
                        'birth_date': self.birth_date,
                        'port': self.port
                    }
                    broadcast_socket.sendto(
                        json.dumps(broadcast_message).encode(),
                        ('<broadcast>', self.broadcast_port)
                    )
                    last_broadcast_time = current_time

                # Escuchar respuestas por 5 segundos
                broadcast_socket.settimeout(5)
                try:
                    while True:
                        data, addr = broadcast_socket.recvfrom(1024)
                        message = json.loads(data.decode())
                        
                        if (message['type'] == 'discovery' and 
                            message['node_id'] != self.node_id and 
                            message['node_id'] not in discovered_nodes):
                            
                            discovered_nodes.add(message['node_id'])
                            # Intentar conectar con el nodo descubierto
                            if self.connect_to_peer(addr[0], message['port']):
                                print(f"Nodo descubierto: {message['name']} ({addr[0]}:{message['port']})")
                except socket.timeout:
                    pass
                
            except Exception as e:
                if not isinstance(e, (ConnectionResetError, socket.timeout)):
                    print(f"Error en descubrimiento: {str(e)}")
                time.sleep(5)  # Esperar antes de reintentar

    def start(self):
        """Inicia el nodo y comienza a escuchar conexiones entrantes"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Usar un puerto aleatorio entre 1024 y 65535
        while True:
            try:
                port = random.randint(1024, 65535)
                self.server_socket.bind((self.host, port))
                self.port = port
                break
            except OSError:
                continue

        self.server_socket.listen(5)
        self.running = True
        
        # Verificar que el ID no esté en uso
        self.verify_node_id()
        
        # Iniciar el descubrimiento de nodos
        self.start_discovery()
        
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
                response = self._process_message(message_data, address)
                if response:
                    client_socket.send(response)
        except Exception as e:
            # Solo mostrar errores específicos que sean útiles para el usuario
            if not isinstance(e, (ConnectionResetError, socket.timeout)):
                print(f"Error en la conexión: {str(e)}")
        finally:
            client_socket.close()

    def connect_to_peer(self, host, port):
        """Conecta con otro nodo"""
        try:
            # Verificar si ya estamos conectados a este nodo
            for node_id, (existing_host, existing_port, _, _) in self.peers.items():
                if existing_host == host and existing_port == port:
                    return True

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(2)  # Timeout de 2 segundos
            client_socket.connect((host, port))
            
            # Enviar mensaje de conexión
            connect_message = {
                'type': 'connect',
                'node_id': self.node_id,
                'port': self.port,
                'name': self.name,
                'birth_date': self.birth_date
            }
            
            encrypted_message = self.cipher_suite.encrypt(json.dumps(connect_message).encode())
            client_socket.send(encrypted_message)
            client_socket.close()
            
            return True
        except socket.timeout:
            return False
        except ConnectionRefusedError:
            return False
        except Exception as e:
            return False

    def send_message(self, target_name, target_birth_date, message, file_path=None):
        """Envía un mensaje a un usuario específico"""
        target_id = self.user_manager._generate_user_id(target_name, target_birth_date)
        host = "127.0.0.1"  # Por defecto, intentar en localhost
        
        # Intentar puertos aleatorios
        tried_ports = set()
        while len(tried_ports) < 100:  # Intentar máximo 100 puertos diferentes
            port = random.randint(1024, 65535)
            if port in tried_ports:
                continue
            tried_ports.add(port)
            
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(0.1)  # Timeout más corto
                client_socket.connect((host, port))
                
                message_data = {
                    'type': 'message',
                    'from': self.node_id,
                    'from_name': self.name,
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
                
                print(f"Mensaje enviado exitosamente a {target_name}")
                return True
            except:
                continue
        
        print(f"Error: No se pudo conectar con el usuario {target_name}")
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

    def list_connected_nodes(self):
        """Lista todos los usuarios conectados en este momento"""
        print("\nUsuarios en línea:")
        if not self.peers:
            print("No hay usuarios conectados")
            print("\nPara conectar con otros usuarios:")
            print("1. Asegúrate de que ambos estén en la misma red")
            print("2. Usa el comando 'add <nombre> <año_nacimiento>' con la IP del otro usuario")
            print("3. Si estás en redes diferentes, necesitarás la IP pública del otro usuario")
            return
        
        for node_id, (host, port, name, birth_date) in self.peers.items():
            print(f"- {name} (Año de nacimiento: {birth_date}) | IP: {host} | Puerto: {port}")

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
    print("send <nombre> <año_nacimiento> <mensaje> - Enviar mensaje a un usuario")
    print("sendfile <nombre> <año_nacimiento> <ruta_archivo> - Enviar archivo a un usuario")
    print("add <nombre> <año_nacimiento> - Añadir contacto")
    print("contacts - Ver lista de contactos")
    print("nodes - Ver usuarios en línea")
    print("friend <nombre> <año_nacimiento> - Enviar solicitud de amistad")
    print("accept <nombre> <año_nacimiento> - Aceptar solicitud de amistad")
    print("reject <nombre> <año_nacimiento> - Rechazar solicitud de amistad")
    print("friends - Ver lista de amigos en línea")
    print("exit - Salir")
    
    while True:
        try:
            command = input("\n> ").strip()
            if not command:
                continue

            if command.startswith("add "):
                try:
                    # Extraer el contenido después de "add "
                    content = command[4:].strip()
                    
                    # Verificar que tenga el formato correcto
                    if not (content.startswith("<") and content.endswith(">")):
                        print("Error: Formato incorrecto. Uso: add <nombre> <año_nacimiento>")
                        continue
                    
                    # Dividir en nombre y año
                    parts = content.split("> <")
                    if len(parts) != 2:
                        print("Error: Formato incorrecto. Uso: add <nombre> <año_nacimiento>")
                        continue
                    
                    # Extraer nombre y año (quitando los < y >)
                    contact_name = parts[0][1:]  # Quitar el primer <
                    contact_birth_year = parts[1][:-1]  # Quitar el último >
                    
                    # Validar año de nacimiento
                    try:
                        year = int(contact_birth_year)
                        if year < 1900 or year > datetime.now().year:
                            print(f"Error: El año debe estar entre 1900 y {datetime.now().year}")
                            continue
                    except ValueError:
                        print("Error: Debes ingresar un año válido (ejemplo: 1990)")
                        continue
                    
                    node.add_contact(contact_name, contact_birth_year)
                    print(f"Contacto añadido: {contact_name} (Año de nacimiento: {contact_birth_year})")
                except Exception as e:
                    print("Error en el formato. Uso: add <nombre> <año_nacimiento>")

            elif command == "contacts":
                contacts = node.get_contacts()
                if not contacts:
                    print("No tienes contactos")
                else:
                    print("\nContactos:")
                    for contact_id, (contact_name, contact_birth_year) in contacts.items():
                        print(f"- {contact_name} (Año de nacimiento: {contact_birth_year})")

            elif command == "nodes":
                node.list_connected_nodes()

            elif command.startswith("send "):
                try:
                    parts = command[5:].split("<", 3)
                    if len(parts) != 4:
                        print("Error: Formato incorrecto. Uso: send <nombre> <año_nacimiento> <mensaje>")
                        continue
                    
                    target_name = parts[1].split(">")[0].strip()
                    target_birth_year = parts[2].split(">")[0].strip()
                    message = parts[3].rstrip(">")
                    
                    # Validar año de nacimiento
                    try:
                        year = int(target_birth_year)
                        if year < 1900 or year > datetime.now().year:
                            print(f"Error: El año debe estar entre 1900 y {datetime.now().year}")
                            continue
                    except ValueError:
                        print("Error: Debes ingresar un año válido (ejemplo: 1990)")
                        continue
                    
                    node.send_message(target_name, target_birth_year, message)
                except Exception as e:
                    print("Error en el formato. Uso: send <nombre> <año_nacimiento> <mensaje>")
            
            elif command.startswith("sendfile "):
                try:
                    parts = command[9:].split("<", 3)
                    if len(parts) != 4:
                        print("Error: Formato incorrecto. Uso: sendfile <nombre> <año_nacimiento> <ruta_archivo>")
                        continue
                    
                    target_name = parts[1].split(">")[0].strip()
                    target_birth_year = parts[2].split(">")[0].strip()
                    file_path = parts[3].rstrip(">")
                    
                    # Validar año de nacimiento
                    try:
                        year = int(target_birth_year)
                        if year < 1900 or year > datetime.now().year:
                            print(f"Error: El año debe estar entre 1900 y {datetime.now().year}")
                            continue
                    except ValueError:
                        print("Error: Debes ingresar un año válido (ejemplo: 1990)")
                        continue
                    
                    if os.path.exists(file_path):
                        node.send_message(target_name, target_birth_year, f"Archivo: {os.path.basename(file_path)}", file_path)
                    else:
                        print(f"Error: El archivo {file_path} no existe")
                except Exception as e:
                    print("Error en el formato. Uso: sendfile <nombre> <año_nacimiento> <ruta_archivo>")
            
            elif command.startswith("friend "):
                try:
                    parts = command[7:].split("<", 2)
                    if len(parts) != 3:
                        print("Error: Formato incorrecto. Uso: friend <nombre> <año_nacimiento>")
                        continue
                    
                    target_name = parts[1].split(">")[0].strip()
                    target_birth_year = parts[2].rstrip(">").strip()
                    
                    # Validar año de nacimiento
                    try:
                        year = int(target_birth_year)
                        if year < 1900 or year > datetime.now().year:
                            print(f"Error: El año debe estar entre 1900 y {datetime.now().year}")
                            continue
                    except ValueError:
                        print("Error: Debes ingresar un año válido (ejemplo: 1990)")
                        continue
                    
                    target_id = node.user_manager._generate_user_id(target_name, target_birth_year)
                    node.send_friend_request(target_id)
                except Exception as e:
                    print("Error en el formato. Uso: friend <nombre> <año_nacimiento>")
            
            elif command.startswith("accept "):
                try:
                    parts = command[7:].split("<", 2)
                    if len(parts) != 3:
                        print("Error: Formato incorrecto. Uso: accept <nombre> <año_nacimiento>")
                        continue
                    
                    from_name = parts[1].split(">")[0].strip()
                    from_birth_year = parts[2].rstrip(">").strip()
                    
                    # Validar año de nacimiento
                    try:
                        year = int(from_birth_year)
                        if year < 1900 or year > datetime.now().year:
                            print(f"Error: El año debe estar entre 1900 y {datetime.now().year}")
                            continue
                    except ValueError:
                        print("Error: Debes ingresar un año válido (ejemplo: 1990)")
                        continue
                    
                    from_id = node.user_manager._generate_user_id(from_name, from_birth_year)
                    node.accept_friend_request(from_id)
                except Exception as e:
                    print("Error en el formato. Uso: accept <nombre> <año_nacimiento>")
            
            elif command.startswith("reject "):
                try:
                    parts = command[7:].split("<", 2)
                    if len(parts) != 3:
                        print("Error: Formato incorrecto. Uso: reject <nombre> <año_nacimiento>")
                        continue
                    
                    from_name = parts[1].split(">")[0].strip()
                    from_birth_year = parts[2].rstrip(">").strip()
                    
                    # Validar año de nacimiento
                    try:
                        year = int(from_birth_year)
                        if year < 1900 or year > datetime.now().year:
                            print(f"Error: El año debe estar entre 1900 y {datetime.now().year}")
                            continue
                    except ValueError:
                        print("Error: Debes ingresar un año válido (ejemplo: 1990)")
                        continue
                    
                    from_id = node.user_manager._generate_user_id(from_name, from_birth_year)
                    node.reject_friend_request(from_id)
                except Exception as e:
                    print("Error en el formato. Uso: reject <nombre> <año_nacimiento>")
            
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