from typing import Any, NewType, Iterator

import heapq


class PriorityQueue(Iterator):
    """
    > 说明
        优先级队列.
    > 用法
        >>> pq = PriorityQueue()
        >>> pq.join(lambda: task_first(), 1)
        >>> pq.join(lambda: task_second(), 2)
        >>> pq.join(lambda: task_third(), 3)
        >>> ...
        >>> for task in range(len(pq)):
        ...     pq.first()
        ...
    """

    T = NewType('T', Any)

    def __init__(self):
        self.queue = []
        self.items = []
        self.priorities = []
        self.index = 0

    def join(self, item: T, priority: int) -> None:
        heapq.heappush(self.queue, (priority, self.index, item))
        self.index += 1
        self.items.append(item)
        self.priorities.append(priority)

    def rejoin(self) -> None:
        self.index = 0
        for item in self.items:
            heapq.heappush(self.queue, (self.priorities[self.items.index(item)], self.index, item))
            self.index += 1

    def __next__(self) -> T:
        if self.queue:
            return heapq.heappop(self.queue)[-1]
        else:
            raise StopIteration
