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
        socketstuff.server.server_running = True
        
        #begin the server listener
        try:
            socketstuff.server.begin_listen()
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
        socketstuff.server.server_running = False
        sys.exit()

    def UpdateScreen(self):
        if waiting:
            wx.CallLater(500, self.UpdateScreen)
        count = len(socketstuff.server.connected)
        if count<2:
            self.StartGameButton.Enabled = False
        else:
            self.StartGameButton.Enabled = True
        self.PlayerCountLabel.SetLabel(str(count))
        decks = 1+count//10
        self.DecksUsedLabel.SetLabel(str(decks))
        already = self.PlayerListBox.GetCount()
        #print(count, already)
        names = []
        for item in socketstuff.server.info[already:]:
            self.PlayerListBox.Append(item[0])
        pass

class JoinGameFrame(Frames.JoinGameFrame):
    def __init__(self,parent):
        Frames.JoinGameFrame.__init__(self,parent)
    def JoinGame(self, event):
        global server_ip
        self.Show(False)
        server_ip = self.IPTextBox.Value
        WaitForStart.Show(True)
        #print(server_ip)

    def Cancel(self,event):
        self.Show(False)
        Opening.Show(True)

class WaitForStartFrame(Frames.WaitForStartFrame):
    def __init__(self, parent):
        Frames.WaitForStartFrame.__init__(self, parent)

    def OnShow(self, event):
        if not socketstuff.client.connected:
            wx.CallLater(500, socketstuff.client.connect, server_ip)
            wx.CallLater(500, self.Update)

    def Update(self):
        if socketstuff.client.started:
            InGame.Show(True)
            self.Show(False)
            return
        wx.CallLater(500, self.Update)

class InGameFrame(Frames.JoinGameFrame):
    def __init__(self,parent):
        global running
        Frames.InGameFrame.__init__(self,parent)
        self.InfoListCtrl.AppendColumn("Name")
        self.InfoListCtrl.AppendColumn("Money")
        self.InfoListCtrl.AppendColumn("Status")
        self.InfoListCtrl.AppendColumn("Turn")
        self.InfoListCtrl.Append(["Placeholder Name", "Money", "-", ""])
        running = True
        self.Folded = False
        self.Matched = False
        self.Raised = False
        self.AllIned = False
    def OnShow(self,event):
        global server_ip
        Chat.Show(True)
        Cards.Show(True)
        TableCards.Show(True)
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
        socketstuff.server.server_running = False
        sys.exit()
        
    def Fold(self,event):
        self.TurnOffAll()
        socketstuff.client.send_fold()
        self.Folded = True
        self.RaiseTextBox.Enabled=False
    def Match(self,event):
        socketstuff.client.send_match()
        self.TurnOffAll()
        self.Matched = True
    def Raise(self,event):
        socketstuff.client.send_raise(self.RaiseTextBox.Value)
        self.TurnOffAll()
        self.Raised = True
    def AllIn(self,event):
        self.TurnOffAll()
        socketstuff.client.send_all_in()
        self.AllIned = True
        self.RaiseTextBox.Enabled=False

    def TurnOffAll(self):
        self.FoldButton.Enabled=False
        self.MatchButton.Enabled=False
        self.RaiseButton.Enabled=False
        
        #self.RaiseTextBox.Enabled=False
        self.AllInButton.Enabled=False
    
    def OnText(self,event):
        #check if the number put in is valid
        self.SetButtons()

    def SetButtons(self):
        self.TurnOffAll()
        if not (self.AllIned or self.Folded):
            self.FoldButton.Enabled = True
            self.RaiseButton.Enabled = True
            self.MatchButton.Enabled = True
            self.RaiseTextBox.Enabled = True
            self.AllInButton.Enabled = True
            
        else: #folded or went all in
            return
        
        try:
            proposed = int(self.RaiseTextBox.Value)
        except:
            self.RaiseButton.Enabled=False
            proposed = float("inf")
        
        money = int(self.FundsLabel.Label)
        current_raise = int(self.CurrentRaiseTextBox.Value)
        self.AllInButton.Enabled = True
        if proposed>money:
            self.RaiseButton.Enabled=False
            
        if proposed <1:
            self.RaiseButton.Enabled=False

        if proposed <= current_raise:
            self.RaiseButton.Enabled=False

        if current_raise>=money:
            self.MatchButton.Enabled=False


    def Update(self):
        global running
        #updates the list ctrl
        if running:
            wx.CallLater(500, self.Update)
        else:
            return
        if not socketstuff.client.anything_changed:
            return
        self.InfoListCtrl.DeleteAllItems()
        for player in socketstuff.client.player_info:
            self.InfoListCtrl.Append(player)
            
        self.FundsLabel.Label = str(socketstuff.client.player_info[socketstuff.client.player_number][1])
        self.CurrentRaiseTextBox.Value = str(socketstuff.client.raise_by)
        self.CurrentPotTextBox.Value = str(socketstuff.client.pot)
        
        self.TurnOffAll()
        
        if socketstuff.client.player_number==socketstuff.client.turn:#our turn
            
            status = socketstuff.client.player_info[socketstuff.client.player_number][2]
            if status=="ALLIN" or status == "FOLD":
                return
            self.SetButtons()
            
        socketstuff.client.anything_changed = False

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
        #self.ChatLogTextBox.Value = socketstuff.client.chat_log
        self.ChatLogTextBox.write(socketstuff.client.chat_log)
        socketstuff.client.chat_log = ""

class TableCardsFrame(Frames.TableCardsFrame):
    def __init__(self, parent):
        Frames.TableCardsFrame.__init__(self, parent)

    def OnShow(self, event):
        wx.CallLater(500, self.Update)
        self.done = False

    def Update(self):
        global running
        if self.done:
            return
        if running:
            wx.CallLater(500, self.Update)
        else:
            return
        cards_on_table = len(socketstuff.client.table)
        if cards_on_table==3:
            c1,c2,c3 = socketstuff.client.table
            self.Card1Bitmap.SetBitmap(wx.Bitmap(c1, type=wx.BITMAP_TYPE_ANY))
            self.Card2Bitmap.SetBitmap(wx.Bitmap(c2, type=wx.BITMAP_TYPE_ANY))
            self.Card3Bitmap.SetBitmap(wx.Bitmap(c3, type=wx.BITMAP_TYPE_ANY))
        elif cards_on_table==4:
            c1,c2,c3,c4 = socketstuff.client.table
            self.Card1Bitmap.SetBitmap(wx.Bitmap(c1, type=wx.BITMAP_TYPE_ANY))
            self.Card2Bitmap.SetBitmap(wx.Bitmap(c2, type=wx.BITMAP_TYPE_ANY))
            self.Card3Bitmap.SetBitmap(wx.Bitmap(c3, type=wx.BITMAP_TYPE_ANY))
            self.Card4Bitmap.SetBitmap(wx.Bitmap(c4, type=wx.BITMAP_TYPE_ANY))
        elif cards_on_table==5:
            c1,c2,c3,c4,c5 = socketstuff.client.table
            self.Card1Bitmap.SetBitmap(wx.Bitmap(c1, type=wx.BITMAP_TYPE_ANY))
            self.Card2Bitmap.SetBitmap(wx.Bitmap(c2, type=wx.BITMAP_TYPE_ANY))
            self.Card3Bitmap.SetBitmap(wx.Bitmap(c3, type=wx.BITMAP_TYPE_ANY))
            self.Card4Bitmap.SetBitmap(wx.Bitmap(c4, type=wx.BITMAP_TYPE_ANY))
            self.Card5Bitmap.SetBitmap(wx.Bitmap(c5, type=wx.BITMAP_TYPE_ANY))
            self.done = True

        self.Layout()
        

app = wx.App()

Opening = OpeningFrame(None)
JoinGame = JoinGameFrame(None)
CreateGame = CreateGameFrame(None)
WaitForStart = WaitForStartFrame(None)
InGame = InGameFrame(None)
Cards = CardsFrame(InGame)
Chat = ChatFrame(InGame)
TableCards = TableCardsFrame(InGame)

Opening.Show(True)
try:
    app.MainLoop()
finally:
    socketstuff.server.money.save_table()
