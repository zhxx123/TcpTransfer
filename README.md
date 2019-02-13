## python designer to *.py file
pyuic5 tcp/tcp.ui -o tcp/tcp.py
## generate executable file
#### linux
pyinstaller -w -F main.py -i config/py1.ico
#### windows
pyinstaller -w -F main.py -i config/py1.ico