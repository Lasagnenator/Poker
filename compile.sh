pyinstaller main.py --name=Poker -y

cp "./database.json" "./dist/Poker"
cp "./config.ini" "./dist/Poker"
cp "./Blocks-1s-200px.gif" "./dist/Poker"

cp -R "./Cards" "./dist/Poker/Cards"

7z a -r "dist/Poker.zip" "dist/Poker/*.*"

pause
