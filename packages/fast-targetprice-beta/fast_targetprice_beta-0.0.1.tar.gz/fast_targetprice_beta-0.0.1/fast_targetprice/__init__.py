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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.send_lock = threading.Lock()
        self.pending_requests = collections.deque()  # FIFO queue of (Future, Event)
        self.running = True
        self.recv_thread = threading.Thread(target=self._recv_loop, daemon=True)
        self.recv_thread.start()

    def query(self, keys: List[int], timeout: float = 10.0) -> Dict[int, int]:
        """
        Gửi truy vấn key list (list 32-bit int). Trả về dict[key] = value.
        Timeout mặc định 10s.
        """
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

        with self.send_lock:
            self.sock.sendall(packet)

        try:
            return fut.result(timeout=timeout)
        except Exception as e:
            flag.clear()
            raise

    def _recv_loop(self):
        while self.running:
            try:
                raw_len = self._recv_n_bytes(4)
                if not raw_len:
                    break
                (length,) = struct.unpack(">I", raw_len)
                body = self._recv_n_bytes(length)
                if not body:
                    break

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
                break

    def _recv_n_bytes(self, n: int) -> bytes:
        data = b""
        while len(data) < n:
            chunk = self.sock.recv(n - len(data))
            if not chunk:
                return None
            data += chunk
        return data

    def close(self):
        self.running = False
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.sock.close()
    def __hash32(self, s: str, seed=0) -> int:
        return xxhash.xxh32(s, seed=seed).intdigest()
    
    def gets(self, site: SITE, market_hash_names):
        if not isinstance(market_hash_names, list):
            raise TypeError("market_hash_names must be a list")
        query = {self.__hash32(f"{site}_{name}"): name for name in market_hash_names}
        resultQuery = self.query(query.keys(), timeout=5)
        return {query[key]: value for key, value in resultQuery.items()}

    def get(self, site:SITE, market_hash_name):
        query = [self.__hash32(f"{site}_{market_hash_name}")]
        resultQuery = self.query(query, timeout=5)
        return resultQuery[query[0]]

if __name__ == "__main__":
    client = FAST_TARGETPRICE()
    print(client.get(SITE.buff163,"M4A4 | Griffin (Minimal Wear)"))
    print(client.gets(SITE.youpin898,["M4A4 | Griffin (Minimal Wear)","P90 | Verdant Growth (Factory New)"]))
