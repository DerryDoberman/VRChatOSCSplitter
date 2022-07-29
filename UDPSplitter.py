import socket
import sys
import time
import threading
from queue import Queue

UDP_IP = "127.0.0.1"

message_queue = Queue()

# generate work
def receiver(queue, port):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, # Internet
                                socket.SOCK_DGRAM) # UDP
            print(f"Binding to {UDP_IP} on {port}...")
            sock.bind((UDP_IP, port))
            print(f"BOUND TO {UDP_IP} on {port}!")
            
            while True:
                data, _ = sock.recvfrom(1024) # buffer size is 1024 bytes
                queue.put(data)
        except:
            raise
        finally:
            try:
                sock.close()
            except:
                pass

 
# consume work
def rebroadcast(queue, *ports):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, # Internet
                                    socket.SOCK_DGRAM) # UDP
            while True:
                while queue.qsize() > 0:
                    item = queue.get()
                    print(f"Received {item}")
                    for port in ports:
                        print(f"Sent on {item} on {port}")
                        sock.sendto(item, (UDP_IP, port))
                else:
                    time.sleep(0.1)
        except:
            raise
        finally:
            try:
                sock.close()
            except:
                pass

if __name__ == "__main__":
    print(sys.argv)
    port = int(sys.argv[1])
    ports = [int(s) for s in sys.argv[2:]]
    print(f"{port} {ports}")

    receiverThread = threading.Thread(target=receiver, args=[message_queue, port])  # <- 1 element list
    receiverThread.start()

    senderThread = threading.Thread(target=rebroadcast, args=[message_queue, *ports])  # <- 1 element list
    senderThread.start()

    receiverThread.join()
    senderThread.join()

    """
    UDP_IP = "127.0.0.1"
    UDP_PORT = 9000
    MESSAGE = "Hello, World!"

    print("UDP target IP: %s" % UDP_IP)
    print("UDP target port: %s" % UDP_PORT)
    print("message: %s" % MESSAGE)

    receive_socks = {}
    for port in ports:
        testsock = socket.socket(socket.AF_INET,
                                socket.SOCK_DGRAM)
        testsock.bind((UDP_IP, port))
        receive_socks[port] = testsock

    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
    
    for port, sock in receive_socks.items():
        print(f"{port} - {sock.recvfrom(1024)}")
    """
