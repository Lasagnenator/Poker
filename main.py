import wx
import Frames
import socketstuff
import time
import sys

server_ip = ""
running = False #game running
waiting = False #waiting for players to join
chat_open = False

class OpeningFrame(Frames.OpeningFrame):
    def __init__(self, parent):
        Frames.OpeningFrame.__init__(self, parent)
    def JoinGame(self,event):
        self.Show(False)
        JoinGame.Show(True)
    def CreateGame(self,event):
        self.Show(False)
        CreateGame.Show(True)

class CreateGameFrame(Frames.CreateGameFrame):
    def __init__(self, parent):
        global waiting
        Frames.CreateGameFrame.__init__(self,parent)
        waiting = True
        wx.CallLater(1000, self.UpdateScreen)
    def OnShow(self, event):
        global server_ip
        #display the ip
        server_ip = socketstuff.get_ip()
        self.IPLabel.SetLabel(server_ip)
        
        #begin the server listener
        socketstuff.server.begin_listen()
        try:
            socketstuff.client.connect(server_ip)
        except:
            pass
    def StartGame(self,event):
        global waiting
        #prevent server from accepting new connections
        self.Show(False)
        InGame.Show(True)
        socketstuff.server.end_listen()
        print("Starting game")
        waiting = False
    def Cancel(self, event):
        self.Show(False)
        socketstuff.server.end_listen()
        sys.exit()

    def UpdateScreen(self):
        socketstuff.server.connected
        pass

class JoinGameFrame(Frames.JoinGameFrame):
    def __init__(self,parent):
        Frames.JoinGameFrame.__init__(self,parent)
    def JoinGame(self, event):
        global server_ip
        self.Show(False)
        InGame.Show(True)
        server_ip = self.IPTextBox.Value
        print(server_ip)

    def Cancel(self,event):
        self.Show(False)
        Opening.Show(True)

class InGameFrame(Frames.JoinGameFrame):
    def __init__(self,parent):
        global running
        Frames.InGameFrame.__init__(self,parent)
        self.InfoListCtrl.AppendColumn("Name")
        self.InfoListCtrl.AppendColumn("Money")
        self.InfoListCtrl.AppendColumn("Status")
        self.InfoListCtrl.Append(["Player 1", "5000", "Match"])
        running = True
    def OnShow(self,event):
        global server_ip
        Chat.Show(True)
        Cards.Show(True)
        try:
            socketstuff.client.connect(server_ip)
        except:
            pass #as in already connected
        
        #rarely, but can cause issues due to coordination of threads
        #time.sleep(1)
        wx.CallLater(1000, socketstuff.client.send_match)
        wx.CallLater(500, self.Update)

    def OnClose(self, event):
        global running, waiting, chat_open
        Cards.Show(False)
        self.Show(False)
        running = False
        waiting = False
        chat_open = False
        sys.exit()
        
    def Fold(self,event):
        self.FoldButton.Enabled=False
        self.MatchButton.Enabled=False
        self.RaiseButton.Enabled=False
        self.RaiseTextBox.Value = ""
        self.RaiseTextBox.Enabled=False
        socketstuff.client.send_fold()
    def Match(self,event):
        socketstuff.client.send_match()
        self.OnText(None)
    def Raise(self,event):
        socketstuff.client.send_raise(self.RaiseTextBox.Value)
        self.OnText(None)
    def OnText(self,event):
        #check if the number put in is valid
        self.RaiseButton.Enabled = True
        try:
            proposed = int(self.RaiseTextBox.Value)
        except:
            self.RaiseButton.Enabled=False
            return
        money = int(self.FundsLabel.Label)
        if proposed>money:
            self.RaiseButton.Enabled=False
            return
        if proposed <1:
            self.RaiseButton.Enabled=False
            return
        if proposed <= int(self.CurrentRaiseTextBox.Value):
            self.RaiseButton.Enabled=False
            return

    def Update(self):
        global running
        #updates the table
        if running:
            wx.CallLater(500, self.Update)
        else:
            return
        self.InfoListCtrl.DeleteAllItems()
        for player in socketstuff.client.player_info:
            self.InfoListCtrl.Append(player)
            
        self.FundsLabel.Label = str(socketstuff.client.player_info[socketstuff.client.number][1])
        self.CurrentRaiseTextBox.Value = str(socketstuff.client.raise_by)
        self.CurrentPotTextBox.Value = str(socketstuff.client.pot)

class CardsFrame(Frames.CardsFrame):
    def __init__(self, parent):
        Frames.CardsFrame.__init__(self, parent)

    def OnShow(self,event):
        wx.CallLater(500,self.UpdateCards)

    def UpdateCards(self):
        try:
            c1, c2 = socketstuff.client.cards
            #print(c1, c2)
            self.Card1Bitmap.SetBitmap(wx.Bitmap(c1, type=wx.BITMAP_TYPE_ANY))
            self.Card2Bitmap.SetBitmap(wx.Bitmap(c2, type=wx.BITMAP_TYPE_ANY))
            self.Layout()
        except BaseException as e:
            #print(e.args)
            wx.CallLater(500, self.UpdateCards)

class ChatFrame(Frames.ChatFrame):
    def __init__(self,parent):
        Frames.ChatFrame.__init__(self,parent)
        
    def Enter(self,event):
        message = self.TextInputBox.Value
        socketstuff.client.chat(message)
        self.TextInputBox.Value = ""
    def OnShow(self, event):
        global chat_open
        chat_open = True
        wx.CallLater(500, self.Update)

    def OnClose(self, event):
        global chat_open
        self.Show(False)
        chat_open = False
        

    def Update(self):
        global chat_open
        if chat_open:
            wx.CallLater(500, self.Update)
        else:
            return
        self.ChatLogTextBox.Value = socketstuff.client.chat_log

class TableCardsFrame(Frames.TableCardsFrame):
    def __init__(self, parent):
        Frames.TableCardsFrame.__init__(self, parent)
    
        

app = wx.App()

Opening = OpeningFrame(None)
JoinGame = JoinGameFrame(None)
CreateGame = CreateGameFrame(Opening)
InGame = InGameFrame(None)
Cards = CardsFrame(InGame)
Chat = ChatFrame(InGame)

Opening.Show(True)
try:
    app.MainLoop()
finally:
    socketstuff.server.money.save_table()
