#*************************************************************************************
#
# FILENAME                : Tennis_View.py
#
# SOURCE                  : Kata Task
#
# COPYRIGHT               :(C) GW
#
#************************************************************************************
#
# DESCRIPTION:
#	Tennis_View.py contains all capability which interacts with the user
#	
#*************************************************************************************

from Tkinter import *
from ttk import *
import threading
import Tkinter as tk

# Class which manages all other view objects takes action from the controller
class View_Capability_Handler(threading.Thread):
	
	def __init__(self, controller):
		
		# Dictionary holding all views
		self.frames = {}
		
		# Attribute to hold controller class instance
		self.controller_instance = controller
		
		# Setup tkinter root object
		self.root = Tk()
		self.root.title("Tennis Game")
		self.root.protocol("WM_DELETE_WINDOW", self.controller_instance.request_view_termination)
		self.root.geometry("500x675")
		self.root.resizable(width=False, height=False)
		self.root.grid_rowconfigure(0, weight=1)
		self.root.grid_columnconfigure(0, weight=1)
	
	# Controller to call to run up view
	def start_view(self):
		threading.Thread.__init__(self)
		self.start()
	
	def run(self):
		
		self.main_frame = Frame(self.root).grid(row=1, sticky="nsew")
		
		# For each view init instance and assign to attribute dict container
		for view in (Co_Op_Setup_View, Single_Player_Setup_View, Title_Screen_View, Main_Tennis_View):

			frame = view(self.main_frame, self.controller_instance)

			self.frames[view] = frame
			
			frame.grid(column=0,row=0, sticky=(N,W,E,S) )
		
		# Load initial frame
		self.controller_instance.request_frame(Title_Screen_View)
		
		# On any key press call move_player method
		self.root.bind("<Key>", self.frames[Main_Tennis_View].move_player)
		
		self.root.mainloop()
	
	# Method for handler to return all views to controller
	def get_all_views(self):
		return self.frames

	def get_view_root_object(self):
		return self.root

	# Method which adds label with error message to view
	def ammend_error_to_frame(self, cont, error_message):
		self.frames[cont].ammend_error(error_message)


class Main_Tennis_View(Frame):

	def move_player(self, event):
		# Get key press
		key = event.keysym
		# Key has been pressed move ball
		self.move_Ball()
		# Get player object from controller
		player_object = self.view_controller.request_player_object(key)
		# Check if player_object is None - This occurs if pressed key is not assoicated with a player
		if player_object is not None:
			# Get overlap of player
			overlap_player = self.tennis_lawn_canvas.find_overlapping(*self.tennis_lawn_canvas.coords(player_object.get_player_view_object()))
			# Get overlap of ball
			overlap_tennis_ball = self.tennis_lawn_canvas.find_overlapping(*self.tennis_lawn_canvas.coords(self.tennis_ball))
			# Get line overlap
			goal_1_overlap = self.tennis_lawn_canvas.find_overlapping(*self.tennis_lawn_canvas.coords(self.goal_2))
			# Get line overlap
			goal_2_overlap = self.tennis_lawn_canvas.find_overlapping(*self.tennis_lawn_canvas.coords(self.goal_1))
			# Check if ball on either line
			if(overlap_tennis_ball == goal_1_overlap or overlap_tennis_ball == goal_2_overlap):
				# Check if player has hit ball
				if(self.last_contact_id is not None):
					# Player has scored request controller process and update model
					self.view_controller.request_player_score(self.last_contact_id)
					# Move ball to original position
					self.reset_ball()
				else:
					self.reset_ball()
			# Check if player hit ball
			if(overlap_player == overlap_tennis_ball):
				# Assign hit player and invert ball projectory
				self.last_contact_id = player_object.get_player_id
				self.ball_y = self.ball_y * -1
				self.ball_x = self.ball_x * -1
			# Get player view object
			player_view_object = player_object.get_player_view_object()
			# Move player according to key press
			if key == player_object.get_left_movement_key():
				self.tennis_lawn_canvas.move(player_view_object, -20, 0)        
			elif key == player_object.get_right_movement_key():
				self.tennis_lawn_canvas.move(player_view_object, 20, 0)    
			elif key == player_object.get_up_movement_key():
				self.tennis_lawn_canvas.move(player_view_object, 0, -20)        
			elif key == player_object.get_down_movement_key():
				self.tennis_lawn_canvas.move(player_view_object, 0, 20) 
	
	
	def get_object_coordinates(self, object):
		return self.tennis_lawn_canvas.coords(object)
	
	def move_Ball(self):
		self.tennis_lawn_canvas.move('tennis_ball', self.ball_x, self.ball_y)
	
	def reset_ball(self):
		self.tennis_lawn_canvas.delete(self.tennis_ball)
		self.tennis_ball = self.tennis_lawn_canvas.create_oval(10,10,20,20, fill="blue", tag=('tennis_ball'))
		self.tennis_lawn_canvas.move('tennis_ball', 240, 240)
	
	def draw_pitch(self):
		self.tennis_lawn_canvas = Canvas(self, bg='green', width=500, height=500)
		self.tennis_lawn_canvas.grid(row=1, column=0, pady=(0, 20))
		self.tennis_lawn_canvas.create_rectangle(50, 50, 440, 440, outline='white', width=7)
		self.tennis_lawn_canvas.create_rectangle(50, 50, 440, 245, outline='white', width=7)
		self.tennis_lawn_canvas.create_rectangle(50, 50, 440, 160, outline='white', width=7)
		self.tennis_lawn_canvas.create_rectangle(50, 330, 440, 160, outline='white', width=7)
		self.tennis_lawn_canvas.create_rectangle(245, 245, 440, 160, outline='white', width=7)
		self.tennis_lawn_canvas.create_rectangle(245, 330, 440, 160, outline='white', width=7)
		self.tennis_lawn_canvas.create_rectangle(0, 0, 380, 7, fill='black', tags=('net'))
		self.goal_1 = self.tennis_lawn_canvas.create_rectangle(0, 0, 400, 7, fill='white', tags=('goal_1'))
		self.goal_2 = self.tennis_lawn_canvas.create_rectangle(0, 0, 400, 7, fill='white', tags=('goal_2'))
		self.tennis_lawn_canvas.move('net', 55, 240)
		self.tennis_lawn_canvas.move('goal_1', 55, 50)
		self.tennis_lawn_canvas.move('goal_2', 55, 440)
	
	def create_player(self, player_name, player_index, color="red"):
		if player_index == 0:
			return self.tennis_lawn_canvas.create_oval(50,50,70,70, fill=color, tags=('player_one'))
		else:
			return self.tennis_lawn_canvas.create_oval(50,50,70,70, fill=color, tag=('player_two'))
	
	def set_player_starting_positions(self, player_index):
		if player_index == 0:
			self.tennis_lawn_canvas.move('player_one', 20, 20)
		else:
			self.tennis_lawn_canvas.move('player_two', 350, 350)
	
	def __init__(self, parent, controller):
		self.ball_x = 2
		self.ball_y = 2
		self.last_contact_id = None
		self.game_on_flag = True
		Frame.__init__(self, parent)
		self.view_controller = controller
		self.draw_pitch()
		self.tennis_ball = self.tennis_lawn_canvas.create_oval(10,10,20,20, fill="blue", tag=('tennis_ball'))
		self.tennis_lawn_canvas.move('tennis_ball', 240, 240)
		
	
class Setup_View_Base_View():
	
	def __init__(self):
		self.entry_widget_dict =  {"player_name" : [], "up_movement_key" : [], "down_movement_key" : [], "left_movement_key" : [], "right_movement_key" : [], "player_color" : []}
	
	def setup_player_information_view_elements(self, player_numeric):
		if player_numeric == 1:
			player_string = "One"
			additional_elements = 7
		else:
			player_string = ""
			additional_elements = 0
			
		Label(self, text="Player " + player_string, font=("Verdana", 15)).grid(row = 1 + additional_elements, column = 0)
		Label(self, text="Player " + player_string + " Name : ", font=("Verdana", 10)).grid(row = 2 + additional_elements, column = 0)
		Label(self, text="Up Key : ", font=("Verdana", 10)).grid(row = 3 + additional_elements, column = 0)
		Label(self, text="Left Key : ", font=("Verdana", 10)).grid(row = 4 + additional_elements, column = 0)
		Label(self, text="Right Key : ", font=("Verdana", 10)).grid(row = 5 + additional_elements, column = 0)
		Label(self, text="Down Key : ", font=("Verdana", 10)).grid(row = 6 + additional_elements, column = 0)
		Label(self, text="Player Color : ", font=("Verdana", 10)).grid(row = 7 + additional_elements, column = 0)
		
		player_color_entry = Entry(self)
		player_color_entry.grid(row = 7 + additional_elements, column = 1)
		self.entry_widget_dict["player_color"].append(player_color_entry)
		
		player_name_entry = Entry(self)
		player_name_entry.grid(row = 2 + additional_elements, column = 1)
		self.entry_widget_dict["player_name"].append(player_name_entry)
		
		up_movement_key_entry = Entry(self)
		up_movement_key_entry.grid(row = 3 + additional_elements, column = 1)
		self.entry_widget_dict["up_movement_key"].append(up_movement_key_entry)
		
		left_movement_key_entry = Entry(self)
		left_movement_key_entry.grid(row = 4 + additional_elements, column = 1)
		self.entry_widget_dict["left_movement_key"].append(left_movement_key_entry)
		
		right_movement_key_entry = Entry(self)
		right_movement_key_entry.grid(row = 5 + additional_elements, column = 1)
		self.entry_widget_dict["right_movement_key"].append(right_movement_key_entry)
		
		down_movement_key_entry = Entry(self)
		down_movement_key_entry.grid(row = 6 + additional_elements, column = 1)
		self.entry_widget_dict["down_movement_key"].append(down_movement_key_entry)
		
	# Method called by handler class to update error message from controller
	def ammend_error(self, error_message):
		self.error_label = Label(self, text=error_message, font=("Verdana", 8)).grid(row = 15, column = 0, pady=(10))	
		
	
class Co_Op_Setup_View(Frame, Setup_View_Base_View):
	
	# Method to init all Tkinter Objects
	def setup_view_elements(self):
		Label(self, text="Co-oP", font=("Verdana", 20)).grid(row = 0, column = 0)
		self.setup_player_information_view_elements(0)
		self.setup_player_information_view_elements(1)		
		Button(self, text="Face Off!", command=lambda: self.view_controller.request_player_model_population(Co_Op_Setup_View, Main_Tennis_View)).grid(row=15, column =1)
		
	# Method for controller to get all user input from this view
	def get_view_payload(self):
		view_pay_load = {"player_name" : [], "up_movement_key" : [], "down_movement_key" : [], "left_movement_key" : [], "right_movement_key" : [], "player_color" : []}
		for data_key in self.entry_widget_dict.keys():
			for entry_widget in self.entry_widget_dict[data_key]:
				view_pay_load[data_key].append(entry_widget.get())				
		return view_pay_load 
			
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		Setup_View_Base_View.__init__(self)
		
		self.view_controller = controller
		
		self.setup_view_elements()
		
		
		
class Single_Player_Setup_View(Frame, Setup_View_Base_View):

	# Method to init all Tkinter Objects
	def setup_view_elements(self):
		single_player_label = Label(self, text="Single Player", font=("Verdana", 20)).grid(row = 0, column = 0)		
		self.setup_player_information_view_elements(0)
		Button(self, text="Lets Play!", command=lambda: self.view_controller.request_player_model_population(Single_Player_Setup_View, Main_Tennis_View)).grid(row=10, column =1)
		
	# Method for controller to get all user input from this view
	def get_view_payload(self):
		view_pay_load = {"player_name" : [], "up_movement_key" : [], "down_movement_key" : [], "left_movement_key" : [], "right_movement_key" : [], "player_color" : []}
		# For each entry box widget
		for data_key in self.entry_widget_dict.keys():
			for entry_widget in self.entry_widget_dict[data_key]:
				# Update data with key
				view_pay_load[data_key].append(entry_widget.get())				
		return view_pay_load 
	
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		Setup_View_Base_View.__init__(self)
				
		self.view_controller = controller
		
		self.setup_view_elements()
		
		
	
class Title_Screen_View(Frame):
		
	# Method to init all Tkinter objects
	def setup_view_elements(self):
		title_label = Label(self, text="Grand Slam Tennis", font=("Verdana", 20)).grid(row = 0, column = 0)		
		tennis_lawn_canvas = Canvas(self, bg='green', width=500, height=500)
		tennis_lawn_canvas.grid(row=1, column=0, pady=(0, 20))
		tennis_lawn_canvas.create_rectangle(50, 50, 440, 440, outline='white', width=7)
		tennis_lawn_canvas.create_rectangle(50, 50, 440, 245, outline='white', width=7)
		tennis_lawn_canvas.create_rectangle(50, 50, 440, 160, outline='white', width=7)
		tennis_lawn_canvas.create_rectangle(50, 330, 440, 160, outline='white', width=7)
		tennis_lawn_canvas.create_rectangle(245, 245, 440, 160, outline='white', width=7)
		tennis_lawn_canvas.create_rectangle(245, 330, 440, 160, outline='white', width=7)
		tennis_lawn_canvas.create_rectangle(0, 0, 380, 7, fill='black', tags=('net'))
		tennis_lawn_canvas.move('net', 55, 240)
		
		Button(self, text="Quit", command=lambda: self.view_controller.request_view_termination()).grid(row=4, column =0)	
		Button(self, text="Single Player", command=lambda: self.view_controller.request_frame(Single_Player_Setup_View)).grid(row=2, column =0)	
		Button(self, text="Co-Op", command=lambda: self.view_controller.request_frame(Co_Op_Setup_View)).grid(row=3, column =0)	
	
	# Method called by handler class to update error message from controller
	def ammend_error(self, error_message):
		self.error_label = Label(self, text=error_message, font=("Verdana", 12)).grid(row = 20, column = 0)	
	
	def __init__(self, parent, controller):

		Frame.__init__(self, parent)
		
		self.view_controller = controller
		
		self.setup_view_elements()
		
		
		
		
		