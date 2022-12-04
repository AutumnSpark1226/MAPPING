import threading


class AnalysisThread0(threading.Thread):
    keep_alive = True
    current_id = 0

    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = 'AnalysisThread0'
        print('[server/analysis_algorithms.py] ' + self.thread_name + ' initialized')

    def run(self):
        while self.keep_alive:
            print("WIP")
            break  # temporary solution to prevent an endless loop


thread0 = AnalysisThread0()


def complete_analysis():
    print("WIP")


def start():
    thread0.start()


def stop():
    thread0.keep_alive = False
