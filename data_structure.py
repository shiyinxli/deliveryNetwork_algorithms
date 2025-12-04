class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    def find(self, key):
        current = self.head
        while current:
            if current.data[0] == key:
                return current
            current = current.next
        return None
    def remove(self, key):
        current = self.head
        prev = None
        while current:
            if current.data[0] == key:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False
    def iter(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

def custom_hash(name):
    code = 0
    for i, c in enumerate(str(name)):
        code+= ord(c)*(31**i)
    return code

class CustomHashMap:
    def __init__(self, bucket_count = 73):
        self.bucket_count = bucket_count
        self.table = [LinkedList() for _ in range(bucket_count)]
    def _bucket_index(self, key):
        return custom_hash(key) % self.bucket_count
    def insert(self, key, value):
        idx = self._bucket_index(key)
        bucket = self.table[idx]
        node = bucket.find(key)
        if node:
            node.data[1] = value
        else:
            bucket.append([key, value])
    def search(self, key):
        idx = self._bucket_index(key)
        bucket = self.table[idx]
        node = bucket.find(key)
        if node:
            return node.data[1]
        else:
            return None
    def remove(self, key):
        idx = self._bucket_index(key)
        bucket = self.table[idx]
        return bucket.remove(key)
    def values(self):
        for bucket in self.table:
            for pair in bucket.iter():
                yield pair[1]
    def items(self):
        for bucket in self.table:
            for pair in bucket.iter():
                yield (pair[0], pair[1])

class CustomArray:
    def __init__(self, capacity=50):
        self.capacity = capacity
        self.size = 0
        self.buffer = [None] * capacity
    
    def get(self, index):
        return self.buffer[index]
    
    def set(self, index, value):
        self.buffer[index] = value
    
    def append(self, value):
        if self.size == self.capacity:
            self._resize()
        self.buffer[self.size] = value
        self.size += 1
    
    def pop(self):
        if self.size == 0:
            return None
        self.size -= 1
        value = self.buffer[self.size]
        self.buffer[self.size] = None
        return value
    
    def _resize(self):
        new_cap = self.capacity * 2
        new_buf = [None] * new_cap
        for i in range(self.size):
            new_buf[i] = self.buffer[i]
        self.buffer = new_buf
        self.capacity = new_cap

    def __len__(self):
        return self.size
    def __getitem__(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        return self.buffer[index]
    
    def __setitem__(self, index, value):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        self.buffer[index] = value


class CustomMinHeap:
    def __init__(self):
        self.data = CustomArray()

    def is_empty(self):
        return len(self.data) == 0

    def push(self, priority, value):
        self.data.append((priority, value))
        self._bubble_up(len(self.data) - 1)

    def pop(self):
        if self.is_empty():
            return None

        self._swap(0, len(self.data) - 1)
        min_item = self.data.pop()
        self._bubble_down(0)
        return min_item

    def peek(self):
        return self.data[0] if not self.is_empty() else None


    def _bubble_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.data[index][0] < self.data[parent][0]:
            self._swap(index, parent)
            index = parent
            parent = (index - 1) // 2

    def _bubble_down(self, index):
        size = len(self.data)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < size and self.data[left][0] < self.data[smallest][0]:
                smallest = left
            if right < size and self.data[right][0] < self.data[smallest][0]:
                smallest = right

            if smallest == index:
                break
            
            self._swap(index, smallest)
            index = smallest

    def _swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]
