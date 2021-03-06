# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 23:33:01 2020

@author: burak-kara
"""

from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime


def local_time(counter):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter, datetime.now())


def calc_recv_timestamp(recv_time_stamp, counter):
    return max(recv_time_stamp, counter) + 1


def event(pid, counter):
    counter += 1
    print('Something happened in {} !'.format(pid) + local_time(counter))
    return counter


def send_message(pipe, pid, counter):
    counter += 1
    pipe.send(('Empty shell', counter))
    print('Message sent from ' + str(pid) + local_time(counter))
    return counter


def recv_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    print('Message received at ' + str(pid) + local_time(counter))
    return counter


def process_zero(pipe01, pipe02):
    pid = getpid()
    counter = 0
    counter = event(pid, counter)  # 1
    counter = send_message(pipe01, pid, counter)  # 2
    counter = recv_message(pipe01, pid, counter)  # 3
    counter = send_message(pipe02, pid, counter)  # 4
    counter = recv_message(pipe02, pid, counter)  # 5
    counter = send_message(pipe01, pid, counter)  # 6
    counter = event(pid, counter)  # 7


def process_one(pipe10):
    pid = getpid()
    counter = 0
    counter = send_message(pipe10, pid, counter)  # 1
    counter = recv_message(pipe10, pid, counter)  # 3
    counter = recv_message(pipe10, pid, counter)  # 7


def process_two(pipe20):
    pid = getpid()
    counter = 0
    counter = event(pid, counter)  # 1
    counter = send_message(pipe20, pid, counter)  # 2
    counter = recv_message(pipe20, pid, counter)  # 5


if __name__ == '__main__':
    zeroandone, oneandzero = Pipe()
    zeroandtwo, twoandzero = Pipe()

    process0 = Process(target=process_zero, args=(zeroandone, zeroandtwo))
    process1 = Process(target=process_one, args=(oneandzero,))
    process2 = Process(target=process_two, args=(twoandzero,))

    process0.start()
    process1.start()
    process2.start()

    process0.join()
    process1.join()
    process2.join()
