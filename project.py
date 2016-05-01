import wx
import random
import copy
import score

class Game(wx.Frame):
	def __init__(self, title):
		super(Game, self).__init__(None, -1, title=title, style=wx.DEFAULT_FRAME_STYLE)

		self.judge = 0
		self.InitUI()

	'''This Function is used to Initial the User Interface.
	self.data : store all the value
	self.mode : the user can choose the game mode (4*4 or 6*6) in MenuBar
	self.Bind(event, event handler) : bind a method to an event'''
	def InitUI(self):

		self.old_data = None

		self.setMenu()
		self.setIcon()

		self.getKeyboard()
		self.GetName()
		
		self.initStat()
		self.initBuffer()
		
		#The EVT_SIZE will be activated when changing size
		self.Bind(wx.EVT_SIZE, self.OnSize)
		#The EVT_PAINT will be activated when painting
		self.Bind(wx.EVT_PAINT, self.OnPaint)
		#THe EVT_CLOSE will be activated when closing the window
		self.Bind(wx.EVT_CLOSE, self.OnClose)

		if self.mode == 4:
			self.SetClientSize((550,800))
		elif self.mode == 6:
			self.SetClientSize((800,1000))
		print(self.GetClientSize())

		self.Centre()
		self.Show(True) # Show the Window
	
	'''Initial all data, first initial the self.data,
		then add two none-zero values into self.data '''
	def initStat(self):
		self.curr_score = 0
		self.GetScore(self.name) # Get best score from stroe.txt
		
		# The default mode is 4*4
		if self.judge == 0:
			self.mode = 4

		if self.mode == 4:
			self.data = [[0 for x in range(4)] for x in range(4)]

		elif self.mode == 6:
			self.data = [[0 for x in range(6)] for x in range(6)]

		count = 2
		while(count != 0):
			row = random.randint(0, len(self.data)-1)
			col = random.randint(0, len(self.data)-1)
			if self.data[row][col] == 0:
				self.data[row][col] = random.choice((2,4))
				count -= 1
		print(self.data)
		
	'''The function to get your name or usename by TextEntryDialog'''
	def GetName(self):
		dlg = wx.TextEntryDialog(None, "What's your name?", "A question")
		if dlg.ShowModal() == wx.ID_OK:
			self.name = dlg.GetValue()
		dlg.Destroy()

	'''The Function to get score from stroe.txt
		the details of ReadScore() please see the file "score.py" '''
	def GetScore(self, name):
		self.score_bst = score.ReadScore(self.name)

	'''The function to write your current best score into store.txt
		the details of WriteScore() please see the file "score.py" '''
	def WriteScore(self):
		score.WriteScore(self.name, self.score_bst)

	'''The buffer is used to avoid flicker.
		More details are on "www.wxpython.org/docs/api/wx.BufferedDC-class.html" ''' 
	def initBuffer(self):
		size = self.GetClientSize()
		self.buffer = wx.EmptyBitmap(size.width, size.height)
	
	'''The event handler of Size_event '''
	def OnSize(self, event):
		self.initBuffer()
		self.draw()

	'''The event handler of Paint_event'''
	def OnPaint(self, event):
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)

	'''Function: Add the menu to the app
	Menu bar:| File : Quit()
			 | Edit : | Mode()
			 		  | Undo()
			 		  | Restart() '''
	def setMenu(self):
		menubar = wx.MenuBar() # get the menu bar
		fileMenu = wx.Menu()   # file menu
		editMenu = wx.Menu()   # edit menu
		exitItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
		ModeItem = editMenu.Append(wx.ID_ANY, 'Mode', 'Select the mode')
		UndoItem = editMenu.Append(wx.ID_ANY, 'Undo', 'Return last step')
		ReItem   = editMenu.Append(wx.ID_ANY, 'Restart', 'Restart the game')
		menubar.Append(fileMenu, 'File')
		menubar.Append(editMenu, 'Edit')
		self.SetMenuBar(menubar)

		self.Bind(wx.EVT_MENU, self.OnClose, exitItem)
		self.Bind(wx.EVT_MENU, self.Mode, ModeItem)
		self.Bind(wx.EVT_MENU, self.Undo, UndoItem)
		self.Bind(wx.EVT_MENU, self.Restart, ReItem)

	'''Idea: Firstly, store your score_bst into store.txt. Then, Destroy the window.
		The function will be executed when click "Quit" in menu'''
	def OnClose(self,event):
		self.WriteScore()
		self.Destroy()

	'''To choose your game mode, when change mode, we should store your bestscore.
	   The function will be executed when click "Mode" in menu'''
	def Mode(self, event):
		old_mode = self.mode
		dlg = wx.SingleChoiceDialog(None, "Please choose the mode of game!",\
						"Mode", ['4*4','6*6'])
		if dlg.ShowModal() == wx.ID_OK:
			result = dlg.GetStringSelection()
			choice = int(result[0])
			self.mode = choice
			self.judge = 1
		dlg.Destroy()

		if old_mode != self.mode:
			self.WriteScore()
			self.InitUI()

	'''Undo your current step. And your can't undo continuously
		The function will be executed when click "Undo" in menu'''
	def Undo(self, event):
		print(self.old_data)
		if self.data == self.old_data:
			Box = wx.MessageBox('You can not press Undo continuously', 'Info', wx.OK)
		
		elif self.old_data == None:
			Box = wx.MessageBox('It is first step', 'Info', wx.OK)


		else:
			self.data = copy.deepcopy(self.old_data)
			self.curr_score -= self.old_score
			self.change_score(self.curr_score)

	'''Set the Icon of app'''
	def setIcon(self):
		icon = wx.Icon("image.png", wx.BITMAP_TYPE_PNG)
		self.SetIcon(icon)

	'''Restart the game. Before restart,it will store bestscore
		The function will be executed when click "Restart" in menu'''
	def Restart(self, event):
		self.WriteScore()
		self.InitUI()

	'''Get the information when you use the KeyBoard'''
	def getKeyboard(self):
		panel = wx.Panel(self, -1)
		panel.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
		panel.SetFocus()

	'''The function is to activate other related funtions 
			when you press up/down/left/right in your KeyBoard'''
	def OnKeyDown(self,event):
		KeyCode = event.GetKeyCode()
		self.old_data = copy.deepcopy(self.data)

		# the condition of pressing up
		if KeyCode == 315:
			flag, add_score = self.Slide(1)
			self.Move(flag, add_score)
		# the condition of pressing down
		elif KeyCode == 317:
			flag, add_score = self.Slide(2)
			self.Move(flag, add_score)
		# the condition of pressing left
		elif KeyCode == 314:
			flag, add_score = self.Slide(3)
			self.Move(flag, add_score)
		# the condition of pressing right:
		elif KeyCode == 316:
			flag, add_score = self.Slide(4)
			self.Move(flag, add_score)

	'''Idea:
	When two adjacent tiles have same value, they will merge into a bigger value.
			And use flag to skip the tile which has been used to merge.
	When it appears 2048, the game will end by "win" MessageBox
	Return: first, merge result. Then, the add_score'''
	def merge(self, non_zero):
		flag = False
		result = []
		add_score = 0
		
		while len(non_zero) != len(self.data):
			non_zero.append(0)

		for i in range(0, len(non_zero) -1):
			if non_zero[i] == non_zero[i+1] and not flag:
				if non_zero[i]*2 == 2048:
					self.win()
				result.append(non_zero[i]*2)
				add_score += non_zero[i]*2
				flag = True

			elif non_zero[i] != non_zero[i+1] and not flag:
				result.append(non_zero[i])

			elif flag == True:
				flag = False

		if non_zero[-1] != 0 and flag == False:
			result.append(non_zero[-1])

		while len(result) != len(non_zero):
			result.append(0)
		return result,add_score

	'''Idea:
	Fristly, get the column/row, then remove "0" from object.
		Then, use merge() function to get merge result.
	
	If the Input is Up/Down, we will merge column by column.
		What's more, when Input is Down, we should reverse the non_zero list firstly.

	If the Input is left/right, we will merge row by row.
		What's more, when Input is rightm we should reverse the non_zero list firstly.
	'''
	def Slide(self, control):
		''' If Up, control = 1  & If Down, control = 2
			If Left, control = 3 & If Right, control = 4
		'''
		pre_data = copy.deepcopy(self.data)
		add_score = 0
		
		# condition of up or down
		if control in (1,2):
			for col in range(len(self.data)):
				non_zero = []
				for row in range(len(self.data)):
					if self.data[row][col] != 0:
						non_zero.append(self.data[row][col])
				if control == 1:
					result,score = self.merge(non_zero)
				else:
					non_zero.reverse()
					result,score = self.merge(non_zero)
					result.reverse()
				
				add_score += score
				for row in range(len(self.data)):
					self.data[row][col] = result[row]

		elif control in (3,4):
			for row in range(len(self.data)):
				non_zero = []
				for col in range(len(self.data)):
					if self.data[row][col] != 0:
						non_zero.append(self.data[row][col])
				if control == 3:
					result,score = self.merge(non_zero)
				else:
					non_zero.reverse()
					result,score = self.merge(non_zero)
					result.reverse()

				add_score += score
				for col in range(len(self.data)):
					self.data[row][col] = result[col]


		return self.data != pre_data, add_score 
	
	'''Everytime we move tiles, it will add a new non_zero tile into self.data'''
	def new_tile(self):
		count = 1
		while(count != 0):
			row = random.randint(0, len(self.data)-1)
			col = random.randint(0, len(self.data)-1)
			if self.data[row][col] == 0:
				self.data[row][col] = random.choice((2,4))
				count -= 1

	'''Use this function to judge whether Game is over
	When after all actions of Up/Down/Left/Right, the self.data does not change,
		 the game is judged over'''
	def judge_GameOver(self):
		pre_data = copy.deepcopy(self.data)
		judge = list()

		for i in range(1,5):
			# self.Slide(i)[0] is to judge whether self.data has changed
			if self.Slide(i)[0] == False: 
				judge.append(1) # can't move
			else:
				self.data = copy.deepcopy(pre_data)
				return False
		
		if judge == [1,1,1,1]:
			return True

	'''When you get 2048 value, it will appear to tell you that you win the game'''
	def win(self):
		wx.MessageBox('YOU WIN!!!', 'Info', wx.OK|wx.ICON_INFORMATION)
		self.WriteScore()
		self.InitUI()
	
	'''when self.data has changed, the argument judge will be True, vice versa.
	If True, we will get the new current_score, and add new tile into game.
	'''
	def Move(self, judge, score):
		if judge:
			self.old_score = score
			self.curr_score += score
			self.new_tile()
			self.change_score(self.curr_score)

			dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
			self.drawTiles(dc)
			
			if self.judge_GameOver():
				dlg = wx.SingleChoiceDialog(None, "Retart?",\
							"Choose", ['Yes','No'])
				if dlg.ShowModal() == wx.ID_OK:
					result = dlg.GetStringSelection()
					dlg.Destroy()
			
				if result == 'Yes':
					self.WriteScore()
					self.InitUI()

	'''Draw new current score, if bestscore has changed, we also should draw bestscore.
	Then, draw tiles to cover the old one '''
	def change_score(self,curr_score):
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		if self.score_bst < curr_score:
			self.score_bst = curr_score
		self.drawcurr_score(dc)
		self.drawbst_score(dc)
		self.drawTiles(dc)

	'''The function of drawing background.
		Different mode should draw different size's background '''
	def drawBack(self, dc):
		dc.SetBackground(wx.Brush((255,255,255)))
		dc.Clear()
		dc.SetBrush(wx.Brush((187,173,160)))
		dc.SetPen(wx.Pen((187,173,160)))
		if self.mode == 4:
			dc.DrawRoundedRectangle(15,120,475,475,7)
		else:
			dc.DrawRoundedRectangle(15,120,705,705,7)

	'''The function of drawing Headline.
		we put an image as the Headline'''
	def drawHeadline(self, dc):
		bmp = wx.Bitmap("Headline.png")
		dc.DrawBitmap(bmp, 15,25)

	'''The function of drawing Instruction which lies below the Headline or tiles'''
	def drawInstruction(self, dc):
		dc.SetTextForeground((0,0,0))
		dc.DrawText("Join the numbers and get to the 2048 tile!", 15,90)
		if self.mode == 4:
			dc.DrawText("HOW TO PLAY: Use your arrow keys to move the tiles.When",15,620)
			dc.DrawText("two tiles with the smaenumber touch, they merge into one!",15, 645)

	'''The function of drawing current score which shows on right of Headline'''
	def drawcurr_score(self, dc):
		dc.SetBrush(wx.Brush((187,173,160)))
		dc.SetPen(wx.Pen((187,173,160)))
		dc.DrawRoundedRectangle(250,5,100,80,7)
		dc.SetFont(wx.Font(10,wx.SWISS,wx.NORMAL,wx.BOLD))
		dc.SetTextForeground((236,224,202))
		dc.DrawText("SCORE",275,15)
		dc.SetFont(wx.Font(15,wx.SWISS,wx.NORMAL,wx.BOLD))
		dc.SetTextForeground((255,255,255))
		dc.DrawText(str(self.curr_score),270,45)

	'''The function of drawing best score which shows on right of current score'''
	def drawbst_score(self, dc):
		dc.SetBrush(wx.Brush((187,173,160)))
		dc.SetPen(wx.Pen((187,173,160)))
		dc.DrawRoundedRectangle(365,5,100,80,7)
		dc.SetFont(wx.Font(10,wx.SCRIPT,wx.NORMAL,wx.BOLD))
		dc.SetTextForeground((236,224,202))
		dc.DrawText("BEST",395,15)
		dc.SetFont(wx.Font(15,wx.SCRIPT,wx.NORMAL,wx.BOLD))
		dc.SetTextForeground((255,255,255))
		dc.DrawText(str(self.score_bst),385,45)

	'''Idea:
	Firstly, we should store colors in RGB mode. The RGB data you can find online
	Then, write tile one by one.
		Because the tiles of different value have different size, 
				we should set different begin position.
	'''
	def drawTiles(self, dc):
		colors = {0:(205,193,180),2:(239, 229, 219),4:(238, 225, 201),\
				8:(243, 178, 122),16:(246, 150, 100),32:(247, 125, 96),\
				64:(247, 95, 60),128:(238, 206, 114),256:(238, 204, 100),\
				512:(222, 168, 59),1024:(223, 165, 49),2048:(238, 193, 47)}

		size = len(self.data)
		for row in range(size):
			for col in range(size):
				value = self.data[row][col]
				color = colors[value]
				
				dc.SetBrush(wx.Brush(color))
				dc.SetPen(wx.Pen(color))
				dc.DrawRoundedRectangle(30+col*115, 135+row*115, 100, 100, 7)
				dc.SetFont(wx.Font(30,wx.SCRIPT,wx.NORMAL,wx.BOLD))

				if value != 0:
					if value == 2 or value == 4:
						dc.SetTextForeground((114,104,94))
						dc.DrawText(str(value), 50+col*115, 153+row*115)
					elif value < 100:
						dc.SetTextForeground((243,243,239))
						dc.DrawText(str(value), 50+col*115, 153+row*115)
					elif value < 1000:
						dc.SetTextForeground((243,243,239))
						dc.DrawText(str(value), 42+col*115, 153+row*115)
					else:
						dc.SetTextForeground((243,243,239))
						dc.DrawText(str(value), 34+col*115, 153+row*115)

	'''The function of drawing everything you need in User Interface'''
	def draw(self):
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.drawBack(dc)
		self.drawHeadline(dc)
		self.drawInstruction(dc)
		self.drawcurr_score(dc)
		self.drawbst_score(dc)
		self.drawTiles(dc)

if __name__ == '__main__':
	app = wx.App()
	Game(title='2048')
	app.MainLoop()

