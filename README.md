On Linux and MacOS, you need to follow these steps:
  1. Install Python
  2. Place the file in whatever folder you want
  3. Navigate to that directory with the terminal
  4. Execute these commands
     > chmod +x spkg.py
     > 
     > sudo mv spkg.py /usr/local/bin/spkg
     >
     > sudo chmod +x /usr/local/bin/spkg
  5. Test it with this command
     > spkg version


On Windows:
  1. Install Python
  2. Add the main.py file to whatever directory you want
  3. Make an spkg.bat file and add these contents to it:
     > @echo off
     >
     > 
     > python "C:\path\to\spkg.py" %*
  4. Move the spkg.bat file to a Windows directory (like C:\windows or C:\windows\system32)
