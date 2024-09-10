#include <iostream>
#include <string>
#include<windows.h>

using namespace std;

int main()
{
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);

	string a = ".- -. - .. -.-", b = "{ . .-. . ...- .- -. ", c = " .--. -.- .---- ", d = "..--.- --. .- -. --. ..--.- ", e = ".-- .. .-.. .-.. ", f = "..--.- - .- -.- . " g = "..--.- --- ...- . .-. ", h = "..--.- - .... . " i = "..--.- .-- --- ", j = ".-. .-.. -.. }", pa = "bo", ro = "mb", l = "a"
	string aa = a + c + b;
	string bb = d + e + f + g;
	string cc = h + i + j;
	string parol;
	cout << "Введите пароль: ";
	getline(cin, parol);
	if (parol == pa + ro + l)
		string flag = aa + bb + cc;
		cout << flag;

	
}
