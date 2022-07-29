"""
Simple script to listen to one udp port and relay messages to multiple other
ports. Made primarily for splitting VRChat OSC message streams.
"""
import socket
import sys
import time
import threading
from queue import Queue

UDP_IP = "127.0.0.1"


def receiver(queue, port):
    """
    Receiver thread. Receives messages on the specified port and adds them to
    the message queue.

    Args:
        queue (queue.Queue):
            A queue of byte arrays read from receiver
        port (int):
            Port to listen to for messages to rebroadcast
    """
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
            pass
        finally:
            try:
                sock.close()
            except:
                pass


def rebroadcast(queue, *ports):
    """
    Rebroadcast thread. Consumes messages from the thread and rebroadcasts them
    on the specified ports.

    Args:
        queue (queue.Queue):
            A queue of byte arrays read from receiver
        ports (Iterable of int):
            A list of ports
    """
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
            pass
        finally:
            try:
                sock.close()
            except:
                pass

if __name__ == "__main__":
    port = int(sys.argv[1])
    ports = [int(s) for s in sys.argv[2:]]
    message_queue = Queue()

    receiverThread = threading.Thread(target=receiver, args=[message_queue, port])  # <- 1 element list
    receiverThread.start()

    senderThread = threading.Thread(target=rebroadcast, args=[message_queue, *ports])  # <- 1 element list
    senderThread.start()

    receiverThread.join()
    senderThread.join()
