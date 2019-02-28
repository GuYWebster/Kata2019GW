#*************************************************************************************
#
# FILENAME                : Tennis_Model.py
#
# SOURCE                  : Kata Task
#
# COPYRIGHT               :(C) GW
#
#************************************************************************************
#
# DESCRIPTION:
#
#	Tennis_Model.py	 contains the data structure for the players - the class is a skeleton with only getters and setter with any logical capacity seperated into Tennis_Services.py
#
#*************************************************************************************

# Player model skeleton class
class Tennis_Player_Model():

	def __init__(self):
		# init all data structure attributes to default values
		self.player_name = None
		self.up_movement_key = None
		self.down_movement_key = None
		self.left_movement_key = None
		self.right_movement_key = None
		self.player_color = None
		self.player_view_object = None
		self.player_id = None
		self.player_score = 0
	
	# all getters and setters for the above attributes	
	def set_player_name(self, name):
		self.player_name = name
		
	def get_player_name(self):
		return self.player_name
	
	def set_up_movement_key(self, key):
		self.up_movement_key = key

	def get_up_movement_key(self):
		return self.up_movement_key	
	
	def set_down_movement_key(self, key):
		self.down_movement_key = key
	
	def get_down_movement_key(self):
		return self.down_movement_key
	
	def set_left_movement_key(self, key):
		self.left_movement_key = key
	
	def get_left_movement_key(self):
		return self.left_movement_key
	
	def set_right_movement_key(self, key):
		self.right_movement_key = key
		
	def get_right_movement_key(self):
		return self.right_movement_key
		
	def set_player_color(self, color):
		self.player_color = color
		
	def get_player_color(self):
		return self.player_color
	
	# Special getter which returns all movement key characters as one string
	# This is so the application can check if key pressed is within the model
	def get_player_keys_string(self):
		return self.up_movement_key + self.down_movement_key + self.left_movement_key + self.right_movement_key
		
	def set_player_view_object(self, view_object):
		self.player_view_object = view_object
		
	def get_player_view_object(self):
		return self.player_view_object
		
	def set_player_id(self, id):
		self.player_id = id
		
	def get_player_id(self):
		return self.player_id
		
	def set_player_score(self, score):
		self.player_score = score
		
	def get_player_score(self):
		return self.player_score
	


	
	
	
