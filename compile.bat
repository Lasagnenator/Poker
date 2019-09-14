pyinstaller main.py --name=Poker -y

robocopy "." "dist/Poker" database.json
robocopy "." "dist/Poker" config.ini

robocopy "Cards" "dist/Poker/Cards" 

pause