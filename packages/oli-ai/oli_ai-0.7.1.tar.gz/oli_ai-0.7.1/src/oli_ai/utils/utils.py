class Node:
    def __init__(self, value, next):
        self.value = value
        self.next = next


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        

    def put(self, value):
        if self.head is None:
            self.head = Node(value, None)
            self.tail = self.head
        else:
            self.tail.next = Node(value, None)
            self.tail = self.tail.next

    def pop(self):
        value = self.head.value
        self.head = self.head.next
        return value


    def __contains__(self, value):
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False

    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next





class Stack:
    def __init__(self):
        self.head = None

    def put(self, value):
        self.head = Node(value, self.head)

    def pop(self):
        value = self.head.value
        self.head = self.head.next
        return value

    def __contains__(self, value):
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False

    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next



