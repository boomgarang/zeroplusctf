#Что сделать чтобы залутать флаг
#python2 vol.py -f /media/sf_Kali/Snapshot19.vmem --profile=Win7SP1x64 hivelist
#->
#0xfffff8a0016dc410 0x0000000010426410 \SystemRoot\System32\Config\SAM




task 4 - Мёд
Использовать дамп из таска 1 - Добро пожаловать
Задача 4 - Найти в данном кусте ключ Names и его значение его четвертого подключа
Формат флага: KpkCTF{XXXX}

#ФЛАГ
#KpkCTF{John}
#Что сделать чтобы залутать флаг
#python2 vol.py -f /media/sf_Kali/Snapshot19.vmem --profile=Win7SP1x64 printkey -o 0xfffff8a0016dc410 -K "SAM\Domains\Account\Users\Names"
#->
#Volatility Foundation Volatility Framework 2.6.1
#Legend: (S) = Stable   (V) = Volatile
#----------------------------
#Registry: \SystemRoot\System32\Config\SAM
#Key name: Names (S)
#Last updated: 2020-12-27 01:20:51 UTC+0000
#
#Subkeys:
#  (S) Administrator
#  (S) Guest
#  (S) HomeGroupUser$
#  (S) John
#
#Values:
#REG_NONE                      : (S) 