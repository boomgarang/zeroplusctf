#Что сделать чтобы залутать флаг
python2 vol.py -f /media/sf_Kali/Snapshot19.vmem --profile=Win7SP1x64 pstree | grep 'dllhost' 
#->
#.. 0xfffffa800515d890:dllhost.exe                    1932    508     13    189 2020-12-27 22:50:53 UTC+0000
#Значение поля PPID - 508

