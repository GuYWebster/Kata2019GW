#*************************************************************************************
#
# FILENAME                : Tennis_Controller.py
#
# SOURCE                  : Kata Task
#
# COPYRIGHT               :(C) GW
#
#************************************************************************************
#
# DESCRIPTION:
# 
#	Tennis_Controller.py is the entry point to the application.
#   The class Tennis_Application_Controller controls program flow taking requests from view classes, 
#   populating models, and utilising service classes where applicable
#	
#*************************************************************************************


# Imports : 
from Tennis_View import View_Capability_Handler
from Tennis_Model import Tennis_Player_Model
from Tennis_Services import Tennis_Model_Services

# Class controlling program flow
class Tennis_Application_Controller():
	
	def __init__(self):
	
		# Init views
		self.view_capability_handler_instance = View_Capability_Handler(self)
		# Activate views
		self.view_capability_handler_instance.start_view()
		# Init services capabilities
		self.tennis_model_services_instance = Tennis_Model_Services()
		# Attribute to store all models created
		self.player_models_dictionary = {}
		
	# Method which acceses all views from handler and displays the requested view
	def request_frame(self, cont):
		# Set attribute to new current view
		self.active_view = cont
		# Get requested view from handler
		frame = self.view_capability_handler_instance.get_all_views()[cont]
		# Make view "active"
		frame.tkraise()
	
	# Method which kills root object and thus all views
	def request_view_termination(self):
		self.view_capability_handler_instance.get_view_root_object().quit()
	
	# Method which calls view to provide its data payload and populates the player models
	def request_player_model_population(self, cont, main_tennis_view):
		# Get data payload
		pay_load = self.view_capability_handler_instance.get_all_views()[cont].get_view_payload()
		# For each player...
		for index, player_name in enumerate(pay_load["player_name"]):
			# Create and populate model
			tennis_player_model_instance = Tennis_Player_Model()
			tennis_player_model_instance.set_player_name(pay_load["player_name"][index])
			tennis_player_model_instance.set_up_movement_key(pay_load["up_movement_key"][index])
			tennis_player_model_instance.set_down_movement_key(pay_load["down_movement_key"][index])
			tennis_player_model_instance.set_left_movement_key(pay_load["left_movement_key"][index])
			tennis_player_model_instance.set_right_movement_key(pay_load["right_movement_key"][index])
			tennis_player_model_instance.set_player_id(index)
			tennis_player_model_instance.set_player_color(pay_load["player_color"][index])
			# Use service to check if model is indeed valid
			if(self.tennis_model_services_instance.validate_player_model(tennis_player_model_instance) == True):
				# Model valid assign to member attribute
				player_model_dictionary_element = {pay_load["player_name"][index] : tennis_player_model_instance}
				self.player_models_dictionary.update(player_model_dictionary_element)
			else:
				# Model invalid display error to user and exit method
				self.view_capability_handler_instance.ammend_error_to_frame(cont, self.tennis_model_services_instance.return_error_message())
				return
		# Valid model show next frame
		self.request_frame(main_tennis_view)
		# Create player on next frame
		self.player_creation(cont, main_tennis_view)
	
	# Method which creates player on canvas
	def player_creation(self, cont, main_tennis_view):
		for index, player_model in enumerate(self.player_models_dictionary.keys()):
			self.player_models_dictionary[player_model].set_player_view_object(self.view_capability_handler_instance.get_all_views()[main_tennis_view].create_player(\
			self.player_models_dictionary[player_model].get_player_name(), index, \
			self.player_models_dictionary[player_model].get_player_color()))
			self.view_capability_handler_instance.get_all_views()[main_tennis_view].set_player_starting_positions(index)
	
	# Method which returns the view player object identified by key press	
	def request_player_object(self, pressed_key):
		for player_name in self.player_models_dictionary.keys():
			player_model_object = self.player_models_dictionary[player_name]
			player_movement_keys = player_model_object.get_player_keys_string()
			if pressed_key in player_movement_keys:
				return player_model_object
		return None
	
	# Method called when a player scores a point - steps through tennis point scoring logic  
	def request_player_score(self, player_id):
		scoring_player_score = 0
		conceeding_player_score = 0
		scoring_player_object = None
		# For each player
		for player_name in self.player_models_dictionary.keys():
			player_model_object = self.player_models_dictionary[player_name]
			player_model_id = player_model_object.get_player_id()
			# If the id is the same as the id of the scoring player
			if player_id == player_model_id:
				# assign player score and object
				scoring_player_score = player_model_object.get_player_score()
				scoring_player_object = player_model_object
			else:
				# Else id is of the conceeding player assing their value
				conceeding_player_score = player_model_object.get_player_score()
		# Call service method to apply tennis scoring logic 
		player_score = self.tennis_model_services_instance.determine_score_value(scoring_player_score, conceeding_player_score)
		# Player score is within bounds there is no "winner" yet so set scoring players ammended score
		if player_score is not None:
			scoring_player_object.set_player_score(player_score)
		else:
			# Kill screen game end
			self.request_view_termination()
		
			
# Start application		
Tennis_Application_Controller()