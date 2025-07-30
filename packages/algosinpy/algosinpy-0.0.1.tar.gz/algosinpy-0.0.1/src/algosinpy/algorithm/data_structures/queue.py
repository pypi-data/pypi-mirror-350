class Queue:

    # Constructor to initiate queue
    def __init__(self, queue=None):
        if queue is None:
            queue = []
        self.queue = queue

    # push to append an item into queue
    def push(self, value):
        self.queue.append(value)

    # front to return starting element from queue
    def front(self):
        if Queue.empty(self) is False:
            return self.queue[0]
        else:
            raise IndexError("You are trying to front in an empty queue.")

    # pop to remove front element from queue
    def pop(self):
        if Queue.empty(self) is False:
            self.queue.pop(0)
        else:
            raise IndexError("You are trying to pop in an empty queue.")

    # to check queue size
    def size(self):
        return len(self.queue)

    # to check queue is empty or not
    def empty(self):
        if self.size() > 0:
            return False
        else:
            return True

    # to see elements of queue
    def display(self):
        return self.queue
