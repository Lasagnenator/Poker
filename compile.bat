pyinstaller main.py --name=Poker -y

robocopy "." "dist/Poker" database.json
robocopy "." "dist/Poker" config.ini
robocopy "." "dist/Poker" "Blocks-1s-200px.gif"

robocopy "Cards" "dist/Poker/Cards" 

7z a -r "dist/Poker.zip" "dist/Poker/*.*"

pause