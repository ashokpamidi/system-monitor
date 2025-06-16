class Node:
    def __init__(self):
        self.data = None
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
    
    def isEmpty(self):
        return self.size == 0
    
    def enqueue(self, item):
        new_node = Node(item)
        if self.isEmpty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1  

    def dequeue(self):
        if self.isEmpty():
            return None
        else:
            self.front = self.front.next
            self.size -= 1
        
        if self.isEmpty():
            self.rear = None
    
