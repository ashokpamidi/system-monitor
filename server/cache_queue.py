import threading
import asyncio

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CacheQueue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
        self.lock = threading.Lock()
    
    def isEmpty(self):
        return self.size == 0
    
    def enqueue(self, item):
        new_node = Node(item)
        with self.lock:
            if self.isEmpty():
                self.front = new_node
                self.rear = new_node
            else:
                self.rear.next = new_node
                self.rear = new_node
            self.size += 1  

    def dequeue(self):
        with self.lock:
            if self.isEmpty():
                return None
            else:
                dequeued = self.front.data
                self.front = self.front.next
                self.size -= 1
            
            if self.isEmpty():
                self.rear = None
            return dequeued
    
    def peek(self):
        return self.rear