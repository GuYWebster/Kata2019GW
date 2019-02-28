#*************************************************************************************
#
# FILENAME                : Tennis_Services.py
#
# SOURCE                  : Kata Task
#
# COPYRIGHT               :(C) GW
#
#************************************************************************************
#
# DESCRIPTION:
#
#	Tennis_Services.py contains logical capability for validation of model values and player scoring	
#
#*************************************************************************************

class Tennis_Model_Services():
	
	def __init__(self):
		self.error_message = ""
		self.color_list = ["red", "yellow", "green"]
		self.advantage_flag = False
	
	# Return attribute error message set if model information is incorrect
	def return_error_message(self):
		return self.error_message
	
	# Method to check movement key input is valid aka - its of 1 length of a arrow key 	
	def validate_movement_key(self, key):
		if key == "Left":
			return True       
		elif key == "Right":
			return True   
		elif key == "Up":
			return True      
		elif key == "Down":
			return True
		elif len(key)== 1:
			return True
		else:
			self.error_message = "Movement Keys entered are not valid! \nKeys are either 1 character long! \nOr 'Left|Right|Up|Down'"
			return False
	
	# Method to see if color entered is applicable
	def validate_color(self, color):
		if color not in self.color_list:
			self.error_message = self.error_message + "\n Color entred incorrect either 'yellow|red|green'"
			return False
		else:
			return True
	
	# Method which returns false if model data is incorrect and true if it is correct
	def validate_player_model(self, player_model_instance):	
		valid_flag = True
		if(self.validate_movement_key(player_model_instance.get_up_movement_key()) != True):
			valid_flag = False
		
		if(self.validate_movement_key(player_model_instance.get_down_movement_key()) != True):
			valid_flag = False
		
		if(self.validate_movement_key(player_model_instance.get_left_movement_key()) != True):
			valid_flag = False
			
		if(self.validate_movement_key(player_model_instance.get_left_movement_key()) != True):
			valid_flag = False
		
		if(self.validate_movement_key(player_model_instance.get_right_movement_key()) != True):
			valid_flag = False
			
		if(self.validate_color(player_model_instance.get_player_color()) != True):
			valid_flag = False
		
		return valid_flag
	
	# Method which applies tennis scoring rules
	def determine_score_value(self, scoring_player_score, conceeding_player_score):
		# Check if players are even apply advntage rules ect
		if(scoring_player_score != conceeding_player_score or (scoring_player_score == 0 and conceeding_player_score == 0)):
			# Had player won
			if(scoring_player_score < 40):
				# No increment by 15
				scoring_player_score = scoring_player_score + 15
			else:
				# Yes None value
				scoring_player_score = None
		else:
			# Players in advantage ?
			if (self.advantage_flag == True):
				# Yes None value
				scoring_player_score = None
			else:
				# They have now reached advnatage set flag
				self.advantage_flag = True
		return scoring_player_score
				
		
		
		
		