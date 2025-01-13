On Linux and MacOS, you need to follow these steps:
  1. Place the file in whatever folder you want
  2. Navigate to that directory with the terminal
  3. Execute these commands
     > chmod +x main.py
     > sudo mv spkg.py /usr/local/bin/spkg
  4. Test it with this command
     > spkg version


On Windows:
  1. Add the main.py file to whatever directory you want
  2. Make an spkg.bat file and add these contents to it:
       @echo off
       python "C:\path\to\main.py" %*
  3. Move the spkg.bat file to a Windows directory (like C:\windows or C:\windows\system32)
