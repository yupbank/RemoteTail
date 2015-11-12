# RemoteTail

remote tail log utils

---

example usage are in the example.py

```
from RemoteTail import RemoteTailer, signal_handler
    
def singal_machine():
    remote_tailer = RemoteTailer(host='localhost', username='pengyu', file_name='/Users/pengyu/projects/RemoteTail/README.md')
    for line in remote_tailer.tail():
        print line

def multi_machine():
    remote_tailer_one = RemoteTailer(host='app_server_1', username='pengyu', file_name='/var/log/nginx/access.log')
    remote_tailer_two = RemoteTailer(host='app_server_2', username='pengyu', file_name='/var/log/nginx/access.log')
    for line in RemoteTailer.multi_tail([remote_tailer_one, remote_tailer_two]):
        print line

```

----

logs are being pulled back asynchronously

