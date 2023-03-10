# coding=utf-8

# Author: Diego Gonzalez Chavez
# email : diegogch@cbpf.br / diego.gonzalez.chavez@gmail.com

import threading
import types

__all__ = ['Threaded_Function', 'as_thread', 'check_stop']

class _Exception_StopThread(Exception):
    pass


class Threaded_Function(object):

    def __init__(self, target):
        self._target = target
        self.thread = None

    def stop(self):
        if self.thread is not None:
            self.thread._TD_stop = True

    def __get__(self, instance, owner):
        # Allows the use of the decorator inside classes
        return types.MethodType(self, instance)

    def __call__(self, *args, **kwargs):
        def stoppable_target():
            try:
                self._target(*args, **kwargs)
            except _Exception_StopThread:
                pass

        self.thread = threading.Thread(target=stoppable_target)
        self.thread._TD_stop = False
        self.thread.start()


def as_thread(target):
    '''Executes traget as a thread'''
    return Threaded_Function(target)


def check_stop():
    if threading.current_thread()._TD_stop:
        raise _Exception_StopThread()
