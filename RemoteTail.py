#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
import select
import signal
import sys
from functools import partial
import logging
import paramiko

class RemoteTailer(object):
    def __init__(self, host, username, file_name, password='1', command='tail -f -n+1 ', port=22):
        self.host = host
        self.command = command + file_name
        self.username = username
        self.port = port
        self.password = password
        self.client = None
    
    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, username=self.username, password=self.password, port=self.port)
    
    def _channel(self):
        if not self.client:
            self.connect()
        channel = self.client.get_transport().open_session()
        channel.exec_command(self.command)
        return channel

    def tail(self, dilemeter='\n'):
        channel = self._channel()
        while not channel.closed or channel.recv_ready() or channel.recv_stderr_ready():
            rl, wl, xl = select.select([channel], [], [], 0.0)
            for c in rl:
                if c.recv_ready(): 
                    for line in channel.recv(len(c.in_buffer)).split(dilemeter):
                        if line.strip():
                            yield line

    def clean(self):
        if not self.client:
            self.connect()
        stdin, stdout, stderr = self.client.exec_command("ps aux|grep '%s' |awk '{print $2}'|xargs kill -9"%self.command)
        logging.info('clean remote %s, command: %s'%(self.host, self.command))
        logging.info('%s %s'%(stdout.read(), stderr.read()))
        stdin.flush()
    
    @classmethod
    def multi_tail(cls, connections, dilemeter='\n'):
        channels = map(lambda connection: connection._channel(), connections)
        to_query = filter(lambda channel: not channel.closed or channel.recv_ready() or channel.recv_stderr_ready(), channels)
        while len(to_query) > 0:
            to_query = filter(lambda channel: not channel.closed or channel.recv_ready() or channel.recv_stderr_ready(), channels)
            rl, wl, xl = select.select(to_query, [], [], 0.0)
            for c in rl:
                if c.recv_ready(): 
                    for line in channel.recv(len(c.in_buffer)).split(dilemeter):
                        if line.strip():
                            yield line
        
    @classmethod
    def multi_clean(cls, connections):
        for connection in connections:
            connection.clean()

def multi_signal_hander(remote_tailers, signal, frame):
    logging.warn('you pressed ctrl+c')
    for remote_tailer in remote_tailers:
        remote_tailer.clean()
    sys.exit(0)

def signal_handler(remote_tailer, signal, frame):
    logging.warn('you pressed ctrl+c')
    remote_tailer.clean()
    sys.exit(0)

