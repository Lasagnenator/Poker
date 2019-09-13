# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class OpeningFrame
###########################################################################

class OpeningFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Landing", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText10 = wx.StaticText( self, wx.ID_ANY, u"Join or create a game?", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )

		bSizer10.Add( self.m_staticText10, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button3 = wx.Button( self, wx.ID_ANY, u"Join Game", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.m_button3, 0, wx.ALL, 5 )

		self.m_button4 = wx.Button( self, wx.ID_ANY, u"Create Game", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.m_button4, 0, wx.ALL, 5 )


		bSizer10.Add( bSizer9, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer10 )
		self.Layout()
		bSizer10.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button3.Bind( wx.EVT_BUTTON, self.JoinGame )
		self.m_button4.Bind( wx.EVT_BUTTON, self.CreateGame )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def JoinGame( self, event ):
		event.Skip()

	def CreateGame( self, event ):
		event.Skip()


###########################################################################
## Class CreateGameFrame
###########################################################################

class CreateGameFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Create Game", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Player list:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer8.Add( self.m_staticText7, 0, wx.ALL, 5 )

		PlayerListBoxChoices = [ u"Player 1", u"Player 2", u"Player 3" ]
		self.PlayerListBox = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, PlayerListBoxChoices, wx.LB_ALWAYS_SB|wx.LB_SINGLE|wx.LB_SORT )
		bSizer8.Add( self.PlayerListBox, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Player count:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		bSizer13.Add( self.m_staticText8, 0, wx.ALL, 5 )

		self.PlayerCountLabel = wx.StaticText( self, wx.ID_ANY, u"3", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.PlayerCountLabel.Wrap( -1 )

		bSizer13.Add( self.PlayerCountLabel, 0, wx.ALL, 5 )


		bSizer8.Add( bSizer13, 0, 0, 5 )

		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"Decks to be used:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		bSizer14.Add( self.m_staticText11, 0, wx.ALL, 5 )

		self.DecksUsedLabel = wx.StaticText( self, wx.ID_ANY, u"2", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.DecksUsedLabel.Wrap( -1 )

		bSizer14.Add( self.DecksUsedLabel, 0, wx.ALL, 5 )


		bSizer8.Add( bSizer14, 0, wx.EXPAND, 5 )


		bSizer10.Add( bSizer8, 1, wx.EXPAND, 5 )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText9 = wx.StaticText( self, wx.ID_ANY, u"Server IP:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )

		bSizer12.Add( self.m_staticText9, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.IPLabel = wx.StaticText( self, wx.ID_ANY, u"TBA", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.IPLabel.Wrap( -1 )

		bSizer12.Add( self.IPLabel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

		self.m_button5 = wx.Button( self, wx.ID_ANY, u"Start Game", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_button5, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer10.Add( bSizer12, 1, wx.ALIGN_CENTER_VERTICAL, 5 )


		self.SetSizer( bSizer10 )
		self.Layout()
		bSizer10.Fit( self )

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.Cancel )
		self.Bind( wx.EVT_SHOW, self.OnShow )
		self.m_button5.Bind( wx.EVT_BUTTON, self.StartGame )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def Cancel( self, event ):
		event.Skip()

	def OnShow( self, event ):
		event.Skip()

	def StartGame( self, event ):
		event.Skip()


###########################################################################
## Class JoinGameFrame
###########################################################################

class JoinGameFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Join Game", pos = wx.DefaultPosition, size = wx.Size( 300,144 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer15 = wx.BoxSizer( wx.VERTICAL )

		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"Server IP:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		bSizer16.Add( self.m_staticText14, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.IPTextBox = wx.TextCtrl( self, wx.ID_ANY, u"192.168.2.99", wx.DefaultPosition, wx.DefaultSize, wx.TE_CENTER )
		bSizer16.Add( self.IPTextBox, 1, wx.ALL, 5 )


		bSizer15.Add( bSizer16, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )

		self.m_button7 = wx.Button( self, wx.ID_ANY, u"Join Game", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer15.Add( self.m_button7, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


		self.SetSizer( bSizer15 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.Cancel )
		self.m_button7.Bind( wx.EVT_BUTTON, self.JoinGame )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def Cancel( self, event ):
		event.Skip()

	def JoinGame( self, event ):
		event.Skip()


###########################################################################
## Class WaitForStartFrame
###########################################################################

class WaitForStartFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Waiting for start", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer17 = wx.BoxSizer( wx.VERTICAL )


		self.SetSizer( bSizer17 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


###########################################################################
## Class InGameFrame
###########################################################################

class InGameFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Poker!", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer21 = wx.BoxSizer( wx.VERTICAL )

		bSizer22 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, u"Current pot:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )

		bSizer22.Add( self.m_staticText16, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.CurrentPotTextBox = wx.TextCtrl( self, wx.ID_ANY, u"200", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizer22.Add( self.CurrentPotTextBox, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText17 = wx.StaticText( self, wx.ID_ANY, u"Current Raise", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )

		bSizer22.Add( self.m_staticText17, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.CurrentRaiseTextBox = wx.TextCtrl( self, wx.ID_ANY, u"10", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		bSizer22.Add( self.CurrentRaiseTextBox, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer21.Add( bSizer22, 0, wx.EXPAND, 5 )

		self.InfoListCtrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_HRULES|wx.LC_REPORT|wx.LC_VRULES )
		bSizer21.Add( self.InfoListCtrl, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer24 = wx.BoxSizer( wx.HORIZONTAL )

		self.FoldButton = wx.Button( self, wx.ID_ANY, u"Fold", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer24.Add( self.FoldButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.MatchButton = wx.Button( self, wx.ID_ANY, u"Match", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer24.Add( self.MatchButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.RaiseButton = wx.Button( self, wx.ID_ANY, u"Raise by", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		self.RaiseButton.Enable( False )

		bSizer24.Add( self.RaiseButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.RaiseTextBox = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer24.Add( self.RaiseTextBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer21.Add( bSizer24, 0, 0, 5 )

		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText19 = wx.StaticText( self, wx.ID_ANY, u"Your funds:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )

		bSizer26.Add( self.m_staticText19, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.FundsLabel = wx.StaticText( self, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.FundsLabel.Wrap( -1 )

		bSizer26.Add( self.FundsLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer21.Add( bSizer26, 0, 0, 5 )


		self.SetSizer( bSizer21 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_SHOW, self.OnShow )
		self.FoldButton.Bind( wx.EVT_BUTTON, self.Fold )
		self.MatchButton.Bind( wx.EVT_BUTTON, self.Match )
		self.RaiseButton.Bind( wx.EVT_BUTTON, self.Raise )
		self.RaiseTextBox.Bind( wx.EVT_TEXT, self.OnText )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnShow( self, event ):
		event.Skip()

	def Fold( self, event ):
		event.Skip()

	def Match( self, event ):
		event.Skip()

	def Raise( self, event ):
		event.Skip()

	def OnText( self, event ):
		event.Skip()


###########################################################################
## Class CardsFrame
###########################################################################

class CardsFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Your cards", pos = wx.DefaultPosition, size = wx.Size( 290,240 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer28 = wx.BoxSizer( wx.HORIZONTAL )

		self.Card1Bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer28.Add( self.Card1Bitmap, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

		self.Card2Bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer28.Add( self.Card2Bitmap, 0, wx.ALIGN_CENTER_VERTICAL, 5 )


		self.SetSizer( bSizer28 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_SHOW, self.OnShow )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnShow( self, event ):
		event.Skip()


###########################################################################
## Class ChatFrame
###########################################################################

class ChatFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Chat", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer18 = wx.BoxSizer( wx.VERTICAL )

		self.ChatLogTextBox = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_BESTWRAP|wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer18.Add( self.ChatLogTextBox, 1, wx.ALL|wx.EXPAND, 5 )

		bSizer19 = wx.BoxSizer( wx.HORIZONTAL )

		self.TextInputBox = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
		self.TextInputBox.SetMaxLength( 0 )
		bSizer19.Add( self.TextInputBox, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_button8 = wx.Button( self, wx.ID_ANY, u"Enter", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer19.Add( self.m_button8, 0, wx.ALL, 5 )


		bSizer18.Add( bSizer19, 0, wx.EXPAND, 5 )


		self.SetSizer( bSizer18 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.Bind( wx.EVT_SHOW, self.OnShow )
		self.TextInputBox.Bind( wx.EVT_TEXT_ENTER, self.Enter )
		self.m_button8.Bind( wx.EVT_BUTTON, self.Enter )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):
		event.Skip()

	def OnShow( self, event ):
		event.Skip()

	def Enter( self, event ):
		event.Skip()



###########################################################################
## Class TableCardsFrame
###########################################################################

class TableCardsFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Cards on table", pos = wx.DefaultPosition, size = wx.Size( 710,240 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer18 = wx.BoxSizer( wx.HORIZONTAL )

		self.Card1Bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.Card1Bitmap, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

		self.Card2Bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.Card2Bitmap, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

		self.Card3Bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.Card3Bitmap, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

		self.Card4Bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.Card4Bitmap, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

		self.Card5Bitmap = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer18.Add( self.Card5Bitmap, 0, wx.ALIGN_CENTER_VERTICAL, 5 )


		self.SetSizer( bSizer18 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


