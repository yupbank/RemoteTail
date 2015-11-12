#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
from RemoteTail import RemoteTailer, signal_handler
import signal
from functools import partial


def singal_machine():
    remote_tailer = RemoteTailer(host='localhost', username='pengyu', file_name='/Users/pengyu/projects/RemoteTail/README.md')
    signal.signal(signal.SIGINT, partial(signal_handler, remote_tailer))

    remote_tailer.clean()
    for line in remote_tailer.tail():
        print line


def multi_machine():
    machine_hosts = ['localhost1', 'localhost2']
    remote_tailers = map(lambda host: RemoteTailer(host=host, username='root', file_name='/root/hello_word.some_date'), machine_hosts)
    signal.signal(signal.SIGINT, partial(signal_handler, remote_tailers))

    map(lambda remote_tailer:remote_tailer.clean(), remote_tailers)
    for line in RemoteTailer.multi_tail(remote_tailers):
        print line

def main():
    singal_machine()

if __name__ == "__main__":
    main()
