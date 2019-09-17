# Dependecies

wxPython >= 4.0.3 (made with 4.0.3, untested in higher versions)
pyinstaller >= 3.4 (only needed for distributing binaries)

# Usage

1. Edit the config.ini file with your username and password

2. Run main.py (or poker.exe if from release)

3. Keep an eye on the black terminal window

4. Follow on-screen prompts. After hiting join game, when there is a waiting screen, it means that the server starter needs to press the `start game` button. When this button is hit, the game starts and everyone is shown their windows.

5. During the game, you cannot leave as leaving will surrender your current bet and the game will continue without you. (a disconnect counts as a fold)

# Important notes

* This version of poker is one I made for my friends as we play a variation on the types out there. From what I can tell, this version creates higher stakes, better odds, and encourages more betting than Texas Hold'em No limit poker.

* There are only 4 possible choices per turn: `Fold`, `Match`, `Raise`, `All In`.

* The rules around the community cards are changed

* To reveal cards on the table, at least one raise must happen and all other players need to fold, go all-in or match the raise.

#### Fold

When this is pressed, you are telling the server that you surrender your bet and you will not be able to participate for the rest of the round (you can still watch though). 

This buton gets disabled when you go all in. Disables all buttons when pressed.

#### Match

This is where you put in the same bet as the highest raise so far (starts a 1 and does not reset between rounds of betting). When all players have matched the highest raise, cards on the table are revealed (first time 3 cards revealed, second and third time only one card revealed). 

This button gets disabled if you are unable to match the current highest raise.

#### Raise

Input the amount you want to raise by in the box and then hit the button. For the round to end, all other players must fold, all-in or match the raise. You can only raise by an amount higher than the current raise.

This button gets disabled if the input is invalid or if you cannot raise by that amount. 

#### All in

This puts all of your funds into the pot and forces you to play out the rest of the game with no input. All-in can match any raise and if it is higher, it will set the new highest raise otherwise not. 

This button is only disabled when you fold.

#### Cards and winners

Standard poker rankings apply. However, these hands can be formed from **ALL** of the community cards where as in Texas Hold'em, only the top 3 cards are used for making hands. This means that there are 7 cards to make a hand from, increasing chances of getting high plays. In the event of a tie, the pot is shared equally amongst winners with fractional part rounded up.

# Building

To disribute a binary after edits, run compile.bat (or compile.sh depending on platform). This will create a binary in the folder dist/Poker. It also creates a zip of the Poker folder (requires 7-zip) ready for distribution.
