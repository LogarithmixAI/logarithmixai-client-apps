import threading

class WorkerPool:

    def __init__(self, worker_count, target):

        self.worker_count = worker_count
        self.target = target
        self.threads = []

    def start(self):
        if self.worker_count > 0:
            for idx in range(self.worker_count):
                t = threading.Thread(target=self.target, args=(idx,))
                t.daemon = True
                t.start()

                self.threads.append(t)

    def join(self):
        if self.worker_count > 0:
            for t in self.threads:
                t.join()
