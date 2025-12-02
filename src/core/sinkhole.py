import socket
import threading
import struct
import time
from datetime import datetime

class SinkholeServer:
    def __init__(self):
        self.running = False
        self.stats = {
            "total_blocked": 0,
            "domains": {}
        }
        self.lock = threading.Lock()
        self.threads = []

    def start(self):
        if self.running:
            return
        self.running = True
        
        # Start listeners for HTTP (80) and HTTPS (443) on both IPv4 and IPv6
        for port in [80, 443]:
            self.start_listener(port, "HTTP" if port == 80 else "HTTPS", socket.AF_INET)
            self.start_listener(port, "HTTP" if port == 80 else "HTTPS", socket.AF_INET6)

    def stop(self):
        self.running = False
        # Connect to self to unblock accept() calls
        for port in [80, 443]:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.1) # Short timeout to avoid hanging
                    s.connect(('127.0.0.1', port))
            except:
                pass
            try:
                with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
                    s.settimeout(0.1) # Short timeout to avoid hanging
                    s.connect(('::1', port))
            except:
                pass

    def start_listener(self, port, protocol, family):
        t = threading.Thread(target=self._listen_loop, args=(port, protocol, family), daemon=True)
        t.start()
        self.threads.append(t)

    def _listen_loop(self, port, protocol, family):
        try:
            sock = socket.socket(family, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            bind_addr = '127.0.0.1' if family == socket.AF_INET else '::1'
            sock.bind((bind_addr, port))
            sock.listen(5)
        except Exception as e:
            # IPv6 might not be available, just ignore
            if family == socket.AF_INET6:
                return
            print(f"Error binding to port {port} ({family}): {e}")
            return

        print(f"Sinkhole listening on {bind_addr}:{port} ({protocol})")

        while self.running:
            try:
                client_sock, addr = sock.accept()
                if not self.running:
                    client_sock.close()
                    break
                
                # Handle connection in a separate thread to not block the listener
                threading.Thread(target=self._handle_connection, args=(client_sock, protocol), daemon=True).start()
            except Exception as e:
                print(f"Error in accept loop: {e}")
        
        sock.close()

    def _handle_connection(self, sock, protocol):
        domain = "Unknown"
        try:
            sock.settimeout(1.0)
            data = sock.recv(4096)
            
            if protocol == "HTTPS":
                domain = self._parse_sni(data) or "Encrypted AI Service"
            elif protocol == "HTTP":
                domain = self._parse_host_header(data) or "Unencrypted AI Service"
            
            self._record_hit(domain)
            
            # Send a polite refusal
            if protocol == "HTTP":
                response = b"HTTP/1.1 403 Forbidden\r\nContent-Type: text/plain\r\n\r\nAccess Denied by IfNoAI Protocol."
                sock.sendall(response)
            
        except Exception:
            pass
        finally:
            sock.close()

    def _record_hit(self, domain):
        with self.lock:
            self.stats["total_blocked"] += 1
            self.stats["domains"][domain] = self.stats["domains"].get(domain, 0) + 1
            # print(f"Blocked request to: {domain}") # Debug log

    def _parse_sni(self, data):
        """
        Basic parser for TLS Client Hello to extract SNI (Server Name Indication).
        """
        try:
            # TLS Record Header (5 bytes)
            # Content Type (1) | Version (2) | Length (2)
            if len(data) < 5: return None
            content_type, version, length = struct.unpack("!BHH", data[:5])
            
            if content_type != 22: # 22 is Handshake
                return None
            
            # Handshake Header
            # Msg Type (1) | Length (3)
            if len(data) < 9: return None
            msg_type = data[5]
            if msg_type != 1: # 1 is Client Hello
                return None
            
            # Skip fixed length fields to get to Extensions
            # Session ID Length is at offset 43 (approx, depends on Random)
            # Actually let's do dynamic parsing pointer
            p = 5 + 4 # Skip Record+Handshake headers
            p += 2 # Version
            p += 32 # Random
            
            # Session ID
            if p >= len(data): return None
            sess_id_len = data[p]
            p += 1 + sess_id_len
            
            # Cipher Suites
            if p + 2 >= len(data): return None
            cipher_len = struct.unpack("!H", data[p:p+2])[0]
            p += 2 + cipher_len
            
            # Compression Methods
            if p >= len(data): return None
            comp_len = data[p]
            p += 1 + comp_len
            
            # Extensions
            if p + 2 >= len(data): return None
            ext_len = struct.unpack("!H", data[p:p+2])[0]
            p += 2
            
            end_ext = p + ext_len
            while p < end_ext:
                if p + 4 > len(data): break
                ext_type, ext_data_len = struct.unpack("!HH", data[p:p+4])
                p += 4
                
                if ext_type == 0: # 0 is Server Name
                    # Server Name List Length (2)
                    p += 2 
                    # Server Name Type (1)
                    sn_type = data[p]
                    p += 1
                    if sn_type == 0: # Hostname
                        sn_len = struct.unpack("!H", data[p:p+2])[0]
                        p += 2
                        return data[p:p+sn_len].decode('utf-8')
                else:
                    p += ext_data_len
                    
        except Exception:
            return None
        return None

    def _parse_host_header(self, data):
        try:
            text = data.decode('utf-8', errors='ignore')
            for line in text.split('\r\n'):
                if line.lower().startswith('host:'):
                    return line.split(':', 1)[1].strip()
        except:
            pass
        return None

    def get_stats(self):
        with self.lock:
            return self.stats.copy()
