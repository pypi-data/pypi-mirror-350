import socket
import struct
import threading
from concurrent.futures import Future
import time
from typing import List, Dict
import collections

import xxhash

class SITE:
    buff163 = "BUFF"
    youpin898 = "YOUPIN"

class FAST_TARGETPRICE:
    def __init__(self, host="103.82.133.78", port=9000):
        self.host = host
        self.port = port
        self.sock = None
        self.send_lock = threading.Lock()
        self.pending_requests = collections.deque()  # FIFO queue of (Future, Event)
        self.running = True
        self.connected_event = threading.Event()
        self._connect_thread = threading.Thread(target=self._connect_loop, daemon=True)
        self._connect_thread.start()

    def _connect_loop(self):
        """Tự động reconnect khi mất kết nối."""
        while self.running:
            if not self.connected_event.is_set():
                try:
                    self._connect()
                    self.connected_event.set()
                except Exception as e:
                    print("[!] Failed to connect, retrying in 3 seconds:", e)
                    time.sleep(3)
            else:
                time.sleep(1)

    def _connect(self):
        """Thực hiện kết nối socket và khởi động recv loop."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        self.sock = sock
        self.recv_thread = threading.Thread(target=self._recv_loop, daemon=True)
        self.recv_thread.start()
        print("[+] Connected to server")

    def query(self, keys: List[int], timeout: float = 10.0) -> Dict[int, int]:
        fut = Future()
        flag = threading.Event()
        flag.set()
        self.pending_requests.append((fut, flag))

        # Build packet: [length:4][count:4][keys...]
        length = 4 + 4 * len(keys)
        packet = struct.pack(">I", length)
        packet += struct.pack(">I", len(keys))
        for k in keys:
            packet += struct.pack(">I", k)

        if not self.connected_event.wait(timeout=timeout):
            raise TimeoutError("Connection timeout before sending query")

        with self.send_lock:
            try:
                self.sock.sendall(packet)
            except Exception as e:
                flag.clear()
                self.connected_event.clear()
                raise ConnectionError("Send failed, connection dropped") from e

        try:
            return fut.result(timeout=timeout)
        except Exception as e:
            flag.clear()
            raise

    def _recv_loop(self):
        try:
            while self.running:
                raw_len = self._recv_n_bytes(4)
                if not raw_len:
                    raise ConnectionError("Socket closed")

                (length,) = struct.unpack(">I", raw_len)
                body = self._recv_n_bytes(length)
                if not body:
                    raise ConnectionError("Socket closed during body recv")

                (count,) = struct.unpack(">I", body[:4])
                results = {}
                offset = 4
                for _ in range(count):
                    k, v = struct.unpack(">II", body[offset:offset+8])
                    offset += 8
                    results[k] = v

                # Lấy request hợp lệ đầu tiên
                while self.pending_requests:
                    fut, flag = self.pending_requests.popleft()
                    if flag.is_set():
                        fut.set_result(results)
                        break
        except Exception as e:
            print("[-] Recv loop error:", e)
            self.connected_event.clear()
            if self.sock:
                try:
                    self.sock.close()
                except:
                    pass

    def _recv_n_bytes(self, n: int) -> bytes:
        data = b""
        while len(data) < n:
            try:
                chunk = self.sock.recv(n - len(data))
                if not chunk:
                    return None
                data += chunk
            except Exception:
                return None
        return data

    def close(self):
        self.running = False
        self.connected_event.clear()
        try:
            if self.sock:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
        except:
            pass

    def __hash32(self, s: str, seed=0) -> int:
        return xxhash.xxh32(s, seed=seed).intdigest()

    def gets(self, site: SITE, market_hash_names):
        if not isinstance(market_hash_names, list):
            raise TypeError("market_hash_names must be a list")
        query = {self.__hash32(f"{site}_{name}"): name for name in market_hash_names}
        resultQuery = self.query(list(query.keys()), timeout=5)
        return {query[key]: value for key, value in resultQuery.items()}

    def get(self, site: SITE, market_hash_name):
        query = [self.__hash32(f"{site}_{market_hash_name}")]
        resultQuery = self.query(query, timeout=5)
        return resultQuery[query[0]]

if __name__ == "__main__":
    client = FAST_TARGETPRICE()
    try:
        print(client.get(SITE.buff163, "M4A4 | Griffin (Minimal Wear)"))
        print(client.gets(SITE.youpin898, ["M4A4 | Griffin (Minimal Wear)", "P90 | Verdant Growth (Factory New)"]))
    finally:
        client.close()
