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