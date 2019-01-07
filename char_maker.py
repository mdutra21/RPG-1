import time
from tqdm import tqdm
import random, json, pprint, itertools
from math import floor

class Character(object):
	def __init__(self):
		self.name = 'Name'
		self.title = False
		self.age = 'Age'
		self.stats = 'Stats'
		self.money = 'Money'
		self.social = 'Social'
		self.profession = 'Profession'
		self.skills = 'Skills'
		self.items = 'Items'
		self.urban = 'Urban Skill'
		self.gravity = 'Gravity Skills'

	def __repr__(self):
		return json.dumps(self.__dict__, indent=2)

	def create_name(self):
		self.name=raw_input("Enter your character's full name: ")

	def determine_multipliers(self):
		m=[0, 0, 0, 0]
		for num in range(0,4):
			d10 = random.randint(1,10)
			if d10 == 1:
				m[num] = 0.5
			elif d10 == 2 or d10 == 3:
				m[num] = 1
			elif 4 <= d10 <= 6:
				m[num] = 2
			elif 7 <= d10 <= 9:
				m[num] = 3
			else:
				m[num] = 4
		mult_tot = sum(m)
		if mult_tot <= 4:
			study_points = 6
		elif 4.5 <= mult_tot <= 6.5:
			study_points = 5
		elif 7 <= mult_tot <= 9.5:
			study_points = 4
		elif 10 <= mult_tot <= 11.5:
			study_points = 3
		else:
			study_points = 2

		mults = {'phys_mult':m[0], 'coord_mult':m[1], 'int_mult':m[2], 'social_mult':m[3]}

		print ""
		print "Determining potential multipliers:"
		status_bar()
		print ""

		print "Your potential multipliers are (0.5 - 4): "
		print "Physical Multiplier: ", + mults['phys_mult']
		print "Coordination Multiplier: ", + mults['coord_mult']
		print "Intelligence Multiplier: ", + mults['int_mult']
		print "Social Multiplier: ", + mults['social_mult']
		print ""

		return (mults, study_points)

	def create_grav_skills(self, home_environ, environ_skill, urban_skill):
		if home_environ.gravity == 'NW':
			grav_skills = [1,-1,-3,-5]
		elif home_environ.gravity == 'LT':
			grav_skills = [-1,1,-1,-3]
		elif home_environ.gravity == 'HY':
			grav_skills = [-3,-1,1,-1]
		elif home_environ.gravity == 'EX':
			grav_skills = [-5,-3,-1,1]
		else:
			print "Unrecognized gravity type in create_grav_skills()"

		print "Determining gravity tolerances:"
		status_bar()

		print ""
		print "Your current gravity tolerances are: "
		print "Nearly Weightless (NW, 0.0 - 0.4 G): " + str(grav_skills[0])
		print "Light Gravity (LT, 0.7 - 1.0 G): " + str(grav_skills[1])
		print "Heavy Gravity (HY, 1.3 - 1.7 G): " + str(grav_skills[2])
		print "Extreme Gravity (EX, 2.0 - 2.5 G): " + str(grav_skills[3])
		print ""
		print "You may expend environ skill points (current: " + str(environ_skill) + ") to upgrade all gravity tolerences."
		print "Would you like to do this? (Y/N)"

		response = y_n_response()

		if response == 'Y':
			print "Enter a number of environ skill points to spend (0-" + str(environ_skill-1) +"): "
			modifier = int(raw_input())
			if modifier < 0:
				print "Cannot spend fewer than 0 points. Adjusting to spend 0..."
				modifier = 0
			elif modifier > environ_skill-1:
				print "Cannot reduce environ skill below 1. Adjusting to spend maximum allowed value..."
				modifier = environ_skill-1
			else:
				modifier = modifier

			print ""
			print "New gravity tolerances will be: "
			print "Nearly Weightless (NW, 0.0 - 0.4 G): " + str(grav_skills[0]+modifier)
			print "Light Gravity (LT, 0.7 - 1.0 G): " + str(grav_skills[1]+modifier)
			print "Heavy Gravity (HY, 1.3 - 1.7 G): " + str(grav_skills[2]+modifier)
			print "Extreme Gravity (EX, 2.0 - 2.5 G): " + str(grav_skills[3]+modifier)
			print "Proceed? (Y/N)"

			response = y_n_response()
			if response == 'Y':
				for i in range(0,4):
					grav_skills[i] = grav_skills[i] + modifier
				environ_skill = environ_skill - modifier
			else:
				print "Keeping old tolerance values..."
				print ""
		else:
			print "Keeping old tolerance values..."
			print ""
			modifier = 0

		self.gravity = {'NW':grav_skills[0], 'LT':grav_skills[1], 'HY':grav_skills[2], 'EX':grav_skills[3]}
		return(modifier)

	def create_social_standing(self, mults, environ_skill, urban_skill):
		d10 = random.randint(1,10)
		row = int(d10 + 2*mults['social_mult'] + urban_skill - environ_skill + 1)
		if row < 0:
			row = 0
		file = open('social_standings.txt')
		i=0
		for line in file:
			self.social, self.money, init_skill_mod = line.strip().split('\t')
			i+=1
			if i > row:
				break

		value, unit = self.money.split(' ')
		value = int(value)*random.randint(1,10)
		if unit == 'Mils' or unit == 'Mil':
#	Fix conversion from Mils to Trans
#			if value >= 1000:
#				value = round(float(value)/1000.0,1)
#				self.money = str(value)+' Trans'
#			else:
			self.money = str(value) + ' Mils'
		else:
			self.money = str(value) + ' Trans'

		print "Establishing social standing:"
		status_bar()

		print "Your social standing is: " + self.social
		print "Initial Wealth: " + self.money
		print ""
		return(init_skill_mod)

	def create_skill_points(self, init_skill_mod):
		check = random.randint(1,10) + int(init_skill_mod)
		if check <= 0:
			num_skill_points = 1
		elif 1 <= check <= 3:
			num_skill_points = 2
		elif 4 <= check <= 6:
			num_skill_points = 3
		elif 7 <= check <= 9:
			num_skill_points = 4
		else:
			num_skill_points = 5

		print "Generating skill points:"
		status_bar()
		return(num_skill_points)

	def choose_fields_of_study(self, study_points):
		study_dict = {'1':'Theoretical Science', '2':'Applied Science', '3':'Business', '4':'Humanities', '5':'The Mind', '6':'The Body', '7':'Military'}
		i = 0

		print ""
		print "You have " + str(study_points) + " study points to allocate to fields of study. Most fields require 1 study point; The Mind requires 2."
		print "You may study a particular field twice by spending 2 study points instead of 1. The Mind requires 4 study points to be studied twice."
		print "The available fields of study are listed below. Make your selection(s) by entering the number(s) associated with the appropriate field(s)."
		print ""

		for number, field in sorted(study_dict.iteritems()):
			print number, field

		print ""
		print "Your selections (one entry at a time):"

		study_choices = []
		while study_points > 0:
			choice = raw_input()
			if choice in study_dict.keys():
				if study_choices.count(study_dict[choice]) < 2:
					study_choices.append(study_dict[choice])
					if study_dict[choice] != 'The Mind':
						study_points += -1
					else:
						study_points += -2
					if study_points < 0:
						print "You do not have enough points remaining to study 'The Mind', please try again:"
						study_choices.remove('The Mind')
						study_points += 2
				else:
					print "You have studied that field twice already, please try again:"
			else:
				print "Invalid selection, please try again:"

		print ""
		print "Your chosen fields of study are: "
		for field in set(study_choices):
			if study_choices.count(field) < 2:
				print field
			else:
				print field, "(x"+str(study_choices.count(field))+")"
		print ""
		return(study_choices)

	def choose_initial_skills(self, study_choices, num_skill_points, urban_skill):
		print "Creating skill options from chosen fields of study: "
		status_bar()

		study_choices.append('General')
		skill_dict = {'Theoretical Science':['Chemistry', 'Physics', 'Programming', 'Biology', 'Geology', 'Astronomy'],
		              'Applied Science':['Suit Tech', 'Electro Tech', 'Construction', 'Vehicle Tech', 'Programming'],
		              'Business':['Programming', 'Recruiting', 'Law', 'Economics', 'Trading'],
		              'Humanities':['Linguistics', 'Diplomacy', 'Law', 'Teaching'],
		              'The Mind':['Psionic Boost', 'Psionic Communication', 'Life Sense'],
		              'The Body':['Unarmed Combat', 'Ambush', 'EVA', 'Home Gravity', 'Jetpacks', 'Survival'],
		              'Military':['Battlefield', 'Longarms', 'Handguns', 'Demolitions', 'Grenades'],
		              'General':['Streetwise', 'Stun Gun', 'Gambling', 'Blades', 'Ground Vehicles', 'Urban', 'Home Environ']}

		print ""
		print "You have " + str(num_skill_points) + " skill points to assign to skills appropriate to your chosen fields of study. Each skill costs 1 point and may only be chosen once."
		print "The skills available to you are listed below. Make your selection(s) by entering the number(s) associated with the appropriate field(s)."
		print ""

		skill_subset = []
		for field in set(study_choices):
			if field in skill_dict.keys():
				for skill in skill_dict[field]:
					skill_subset.append(skill)
		if urban_skill < 1:
			skill_subset.remove('Urban')
		
		i = 1
		skill_subset_dict = {}
		for skill in set(skill_subset):
			skill_subset_dict[i] = skill
			i += 1

		for number, field in sorted(skill_subset_dict.iteritems()):
			print number, '\t', field

		print ""
		print "Your selections (one entry at a time):"

		skill_choices = []
		while num_skill_points > 0:
			choice = raw_input()
			if choice.isdigit():
				choice = int(choice)
				if choice in skill_subset_dict.keys():
					if skill_choices.count(skill_subset_dict[choice]) < 1:
						skill_choices.append(skill_subset_dict[choice])
						num_skill_points += -1
					else:
						print "You have chosen that skill already, please try again:"
				else:
					print "Invalid selection, please try again:"
			else:
				print "Invalid selection, please try again:"
		return (skill_choices)

	def create_stats(self, study_chocies, mults):
		strength, endurance, dexterity, agility, intelligence = 0, 0, 0, 0, 0
		mental_power, leadership, empathy, aggression = 0, 0, 0, 0
		file = open('char_mod_chart.txt')
		for line in file:
			stat_mods = line.strip().split('\t')
			for field in set(study_choices):
				if stat_mods[0] == field:
					mult1 = study_choices.count(field)
					strength += mult1*int(stat_mods[1])
					endurance += mult1*int(stat_mods[2])
					dexterity += mult1*int(stat_mods[3])
					agility += mult1*int(stat_mods[4])
					intelligence += mult1*int(stat_mods[5])
					mental_power += mult1*int(stat_mods[6])
					leadership += mult1*int(stat_mods[7])
					empathy += mult1*int(stat_mods[8])
					aggression += mult1*int(stat_mods[9])

		strength = int(strength*mults['phys_mult']*mults['coord_mult']+random.randint(1,100))
		endurance = int(endurance*mults['phys_mult']+random.randint(1,100))
		dexterity = int(dexterity*mults['coord_mult']*mults['int_mult']+random.randint(1,100))
		agility = int(agility*mults['phys_mult']*mults['coord_mult']+random.randint(1,100))
		intelligence = int(intelligence*mults['int_mult']+random.randint(1,100))
		mental_power = int(mental_power*mults['int_mult']+random.randint(1,100))
		leadership = int(leadership*mults['int_mult']*mults['social_mult']+random.randint(1,100))
		empathy = int(empathy*mults['int_mult']+random.randint(1,100))
		aggression = int(aggression+random.randint(1,100))

		stats_dict = {'Strength':strength,
		              'Endurance':endurance,
		              'Dexterity':dexterity,
		              'Agility':agility,
		              'Intelligence':intelligence,
		              'Mental Power':mental_power,
		              'Leadership':leadership,
		              'Empathy':empathy,
		              'Aggression':aggression}

		cgen_list = [(-1000,7,1),(8,15,2),(16,24,3),(25,34,4),(35,57,5),(58,83,6),(84,96,7),(97,108,8),(109,119,9),(120,129,10),(130,139,11),(140,1000,12)]

		for stat in stats_dict.keys():
			for stat_range in cgen_list:
				if stat_range[0] <= stats_dict[stat] <= stat_range[1]:
					stats_dict[stat] = stat_range[2]

		if stats_dict['Agility'] < 5:
			stats_dict['Agility'] = 5
		stats_dict['Mental Power'] = int(stats_dict['Mental Power']/2.0)
		
		self.stats = stats_dict

		print "Calculating characteristic ratings based on chosen fields of study: "
		status_bar()
		print ""

		print "Your characteristic ratings are: "
		print stats_dict

	def create_profession_options(self, study_choices, home_environ, urban_skill):
		value, unit = self.money.split(' ')
		profession_options = {}

		astroguard = True
		if 'Military' not in study_choices:
			astroguard = False
		if int(character.stats['Aggression']) < 5:
			astroguard = False
		if astroguard:
			profession_options['Astroguard'] = {'Name':'Astroguard',
												'Personnel Type':'Military', 
												'Description':'',
												'Prerequisites':'Study of the military; Aggression Rating of at least 5.',
												'Skill Point Mod':1,
												'Extra Skill Options':['Gunnery','Missile Guidance', 'Space Tactics', 'Pilot', 'Air Vehicles', 'EVA', 'Spaceship Tech'],
												'Benefits':{'A':['Corporal, 300 Mils Cash'],
		                 									'B':['Flight Sergeant', '1 Tran Cash'],
		                 									'C':['Flight Lieutenant', '3 Trans Cash', 'Internal Gravity Web'],
		                 									'D':['Squadron Leader', '10 Trans Cash', '250 Mils/Year Pension', 'Internal Gravity Web'],
		                 									'E':['Wing Commander', '25 Trans Cash', '750 Mils/Year Pension', 'Internal Gravity Web'],
		                 									'F':['Group Captain', '60 Trans Cash', '2.5 Trans/Year Pension', 'Internal Gravity Web']}}

		civil_inspector = True
		if 'Humanities' not in study_choices or 'Business' not in study_choices:
			civil_inspector = False
		if int(character.stats['Intelligence']) < 6:
			civil_inspector = False
		if int(character.stats['Leadership']) < 4:
			civil_inspector = False
		if int(character.stats['Empathy']) < 6:
			civil_inspector = False
		if int(character.stats['Mental Power']) < 2:
			civil_inspector = False
		if civil_inspector:
			profession_options['Civil Inspector'] = {'Name':'Civil Inspector',
													 'Personnel Type':'Government', 
													 'Description':'',
													 'Prerequisites':'Study of the humanities and business; Characteristic Ratings of at least Intelligence 6, Leadership 4, Empathy 6, and Mental Power 2.',
													 'Skill Point Mod':4,
													 'Extra Skill Options':['Handguns','Unarmed Combat', 'Agriculture', 'Biology', 'Planetology', 'Urban'],
													 'Benefits':{'A':['250 Mils Cash'],
		                 									     'B':['1 Tran Cash', 'Translator'],
		                 										 'C':['2 Trans Cash', 'Translator or Interstellar Comlink'],
		                 										 'D':['7 Trans Cash', 'Translator and Interstellar Comlink'],
		                 										 'E':['20 Trans Cash', 'Frazette Blue Robot w/ Information & Recorder Systems'],
		                 										 'F':['40 Trans Cash', '36sd Robot w/ Information, Weapon Targeting, Laser Pistol, & Recorder Systems']}}

		colonist = True
		if colonist:
			profession_options['Colonist'] = {'Name':'Colonist',
											  'Personnel Type':'Civilian', 
											  'Description':'',
											  'Prerequisites':'None',
											  'Skill Point Mod':0,
											  'Extra Skill Options':['Trading','Air Vehicles', 'Marine Vehicles', 'Agriculture', 'Mining'],
											  'Benefits':{'A':['Nothing'],
		                 								  'B':['1 Tran Cash'],
		                 								  'C':['2 Trans Cash', 'Civ Level 6 Laser Pistol'],
		                 								  'D':['4 Trans Cash', 'Civ Level 6 Laser Pistol'],
		                 								  'E':['8 Trans Cash', 'Car'],
		                								  'F':['15 Trans Cash', 'Civ Level 5 Automobile', 'Civ Level 6 Laser Pistol']}}

		diplomat = True
		if 'Humanities' not in study_choices or 'The Mind' not in study_choices:
			civil_inspector = False
		if int(character.stats['Intelligence']) < 7:
			civil_inspector = False
		if int(character.stats['Empathy']) < 7:
			civil_inspector = False
		if int(character.stats['Mental Power']) < 2:
			civil_inspector = False
		if self.money != '1 Tran' and unit != 'Trans':
			civil_inspector = False
		if civil_inspector:
			profession_options['Diplomat'] = {'Name':'Diplomat',
											  'Personnel Type':'Government', 
											  'Description':'',
											  'Prerequisites':'Study of the humanities and the mind, Characteristic Ratings of at least Intelligence 7, Empathy 7, Mental Power 2. Aggression Rating may not exceed 6. Initial wealth must be at least 1 Tran.',
											  'Skill Point Mod':8,
											  'Extra Skill Options':['Recruitment','Programming', 'Computer/Robot Tech', 'Urban'],
											  'Benefits':{'A':['300 Mils Cash'],
		                 					  'B':['1 Tran Cash', 'Audio-Sealed Case'],
		                 					  'C':['3 Trans Cash', 'Audio-Sealed Case', 'Translator'],
		                 					  'D':['10 Trans Cash', 'Audio-Sealed Case', 'Translator', 'Interstellar Comlink'],
		                					  'E':['25 Trans Cash', 'Manner 38sdf Robot w/ Holographer & Language Systems'],
		               					      'F':['60 Trans Cash', 'Soidistant V-201 w/ Creative Thought & Holographer Systems']}}

		doctor = True
		if 'Theoretical Science' not in study_choices or 'Applied Science' not in study_choices:
			doctor = False
		if int(character.stats['Dexterity']) < 7:
			doctor = False
		if int(character.stats['Intelligence']) < 8:
			doctor = False
		if int(character.stats['Mental Power']) < 2:
			doctor = False
		if int(character.stats['Empathy']) < 6:
			doctor = False
		if doctor:
			profession_options['Doctor'] = {'Name':'Doctor',
											'Personnel Type':'Civilian', 
											'Description':'',
											'Prerequisites':'Study of theoretical and applied science, Characteristic Ratings of at least Dexterity 7, Intelligence 8, Mental Power 2, and Empathy 6.',
											'Skill Point Mod':10,
											'Extra Skill Options':['Teaching','Diagnosis', 'Treatment'],
											'Benefits':{'A':['First Aid Kit'],
		                					'B':['3 Trans Cash', 'First Aid Kit'],
		                 					'C':['1 Tran x Int. Rating Cash', 'Civ Level 6 Mediscanner'],
		                 					'D':['4 Trans x Int. Rating Cash', 'Civ Level 6 Mediscanner'],
		                 					'E':['10 Trans x Int. Rating Cash', 'Civ Level 8 Mediscanner'],
		                 					'F':['20 Trans x Int. Rating Cash', 'Manner 38sdf Robot w/ Medical System']}}	

		enforcer = True
		if 'The Mind' not in study_choices or 'The Body' not in study_choices:
			enforcer = False
		if int(character.stats['Strength']) < 4:
			enforcer = False
		if int(character.stats['Endurance']) < 4:
			enforcer = False
		if int(character.stats['Dexterity']) < 4:
			enforcer = False
		if int(character.stats['Agility']) < 4:
			enforcer = False	
		if int(character.stats['Intelligence']) < 5:
			enforcer = False
		if int(character.stats['Leadership']) < 5:
			enforcer = False
		if enforcer:
			profession_options['Enforcer'] = {'Name':'Enforcer',
											  'Personnel Type':'Civilian', 
											  'Description':'',
											  'Prerequisites':'Study of the mind and the body, all Physical Characteristic Ratings must be at least 4, Intelligence 5, and Leadership 5.',
											  'Skill Point Mod':6,
											  'Extra Skill Options':['Battlefield','Demolitions', 'Machine Guns', 'Longarms', 'Handguns', 'Paint Gun', 'Recruiting', 'Law', 'Military Ground Vehicles'],
											  'Benefits':{'A':['500 Mils Cash'],
		                 								  'B':['1.5 Trans Cash'],
		                								  'C':['3 Trans Cash', 'Civ Level 5 Pistol'],
		           									      'D':['10 Trans Cash', 'Civ Level 8 Laser Pistol'],
		   									              'E':['25 Trans Cash', 'Civ Level 8 Paint Gun'],
		   					      				          'F':['60 Trans Cash', 'Civ Level 8 Paint Gun', 'Civ Level 5 Submachine Gun']}}

		explorer = True
		if 'Business' not in study_choices:
			explorer = False
		if 'Theoretical Science' not in study_choices and 'Applied Science' not in study_choices:
			explorer = False		
		if int(character.stats['Intelligence']) < 7:
			explorer = False
		if int(character.stats['Mental Power']) < 3:
			explorer = False
		if int(character.stats['Empathy']) < 4:
			explorer = False
		if int(value) < 500 and unit == 'Mils':
			explorer = False
		if unit == 'Mil':
			explorer = False
		if int(character.stats['Mental Power']) > 4:
			explorer = True
		if explorer:
			profession_options['Explorer'] = {'Name':'Explorer',
											  'Personnel Type':'Civilian', 
											  'Description':'',
											  'Prerequisites':'Study of business and either theoretical or applied science, Characteristic Ratings of at least Intelligence 7, Mental Power 3, and Empathy 4. Initial wealth must be at least 500 Mils.',
											  'Skill Point Mod':7,
											  'Extra Skill Options':['Handguns','Paint Gun', 'Gunnery', 'Pilot', 'Linguistics', 'Survival', 'Air Vehicles', 'Marine Vehicles', 'Planetology', 'Biology', 'Geology', 'Astronomy', 'Navigation', 'Environ (Any)', 'Gravity (Any)'],
											  'Benefits':{'A':['Nothing'],
		                								  'B':['Initial Wealth x 3'],
		    								              'C':['Initial Wealth x 5', 'Civ Level 8 Bioscanner'],
		          								          'D':['Initial Wealth x 10', 'Civ Level 8 Geoscanner'],
		      								              'E':['Initial Wealth x 25', 'Neuroscanner'],
		            								      'F':['Initial Wealth x 50', 'Manner 50sd Robot w/ Bio, Self-Activation, & Holographer Systems']}}

		freefaller = True
		check = 0
		if 'Applied Science' in study_choices:
			check += 1
		if 'The Body' in study_choices:
			check += 1
		if 'Military' in study_choices:
			check += 1
		if check < 2:
			freefaller = False
		if int(character.stats['Dexterity']) < 6:
			freefaller = False
		if int(character.stats['Agility']) < 7:
			freefaller = False
		if int(character.stats['Aggression']) < 4:
			freefaller = False
		if home_environ.gravity == 'HY' or home_environ.gravity == 'EX':
			freefaller = False
		if freefaller:
			profession_options['Freefaller'] = {'Name':'Freefaller',
												'Personnel Type':'Military', 
											    'Description':'',
											    'Prerequisites':'Study of two of the following: applied science, the body, the military. Characteristic Ratings of at least Dexterity 6, Agility 7, and Aggression 4. Home gravity type may not be HY or EX.',
											    'Skill Point Mod':3,
											    'Extra Skill Options':['Battlefield','Body Armor', 'Machine Guns', 'Arc Guns', 'Longarms', 'Handguns', 'Jetpacks', 'Demolitions', 'EVA', 'Suit Tech', 'Weapon Tech', 'Gravity (NW)'],
											    'Benefits':{'A':['Lancer', '300 Mils Cash'],
		                								    'B':['Corporal', '1 Tran Cash', 'Civ Level 6 Expedition Suit'],
		          									        'C':['Sergeant', '3 Tran Cash', 'Civ Level 7 Expedition Suit'],
		           									        'D':['Lieutenant', '10 Trans Cash', '250 Mils/Year Pension', 'Civ Level 7 Expedition Suit'],
		              									    'E':['Captain', '25 Trans Cash', '750 Mils/Year Pension', 'Civ Level 7 Expedition Suit', 'Arc Gun'],
		         									        'F':['Colonel', '60 Trans Cash', '2.5 Trans/Year Pension', 'Civ Level 7 Expedition Suit', 'Arc Gun', 'Jetpack']}}

		handyman = True
		if study_choices.count('Applied Science') < 2:
			handyman = False
		if int(character.stats['Dexterity']) < 6:
			handyman = False
		if int(character.stats['Intelligence']) < 6:
			handyman = False
		if handyman:
			profession_options['Handyman'] = {'Name':'Handyman',
											  'Personnel Type':'Civilian, Military, Government', 
											  'Description':'',
											  'Prerequisites':'Study of applied science twice. Characteristic Ratings of at least Dexterity 6 and Intelligence 6.',
											  'Skill Point Mod':5,
											  'Extra Skill Options':['Agriculture','Programming', 'Physics', 'Energy Tech', 'Spaceship Tech', 'Weapon Tech', 'Computer/Robot Tech'],
											  'Benefits':{'A':['Basic Repair Kit'],
		                								  'B':['1 Tran Cash', 'Basic Repair Kit'],
		               									  'C':['3 Tran Cash', 'Civ Level 7 Electrokit'],
		               									  'D':['10 Trans Cash', 'Civ Level 8 Electrokit'],
		             								      'E':['20 Trans Cash', 'Civ Level 8 Vehicle Kit'],
		          								          'F':['40 Trans Cash', 'Civ Level 8 Vehicle Kit', 'Civ Level 8 Robot Kit']}}

		interstellar_trader = True
		if 'Business' not in study_choices:
			interstellar_trader = False
		if int(character.stats['Intelligence']) < 6:
			interstellar_trader = False
		if int(character.stats['Mental Power']) < 2:
			interstellar_trader = False
		if self.money != '1 Tran' and unit != 'Trans':
			interstellar_trader = False
		if interstellar_trader:
			profession_options['Interstellar Trader'] = {'Name':'Interstellar Trader',
														 'Personnel Type':'Civilian', 
													     'Description':'',
											  		     'Prerequisites':'Study of business. Characteristic Ratings of at least Intelligence 6 and Mental Power 2. Initial wealth must be at least 1 Tran.',
													     'Skill Point Mod':4,
											  			 'Extra Skill Options':['Longarms','Handguns', 'Arc Gun', 'Gunnery', 'Missile Guidance', 'Space Tactics', 'Pilot','Linguistics', 'Diplomacy', 'Asteroid Mining', 'Astronomy', 'EVA'],
													     'Benefits':{'A':['Nothing, and all Initial Wealth lost'],
													                 'B':['Civ Level 7 Business Computer'],
													                 'C':['Initial Wealth x 2', 'Civ Level 7 Business Computer'],
		          											         'D':['Initial Wealth x 5', 'Civ Level 7 Business Computer'],
		   											                 'E':['Initial Wealth x 12', 'Civ Level 7 Business Computer'],
		     											             'F':['Initial Wealth x 30', 'Brummagen II Robot w/ Spaceship Tech System', 'Civ Level 7 Business Computer']}}

		lawman = True
		if 'The Body' not in study_choices or 'Humanities' not in study_choices:
			lawman = False
		if int(character.stats['Strength']) < 4:
			lawman = False
		if int(character.stats['Endurance']) < 4:
			lawman = False
		if int(character.stats['Dexterity']) < 4:
			lawman = False
		if int(character.stats['Agility']) < 4:
			lawman = False
		if lawman:
			profession_options['Lawman'] = {'Name':'Lawman',
											'Personnel Type':'Government', 
											'Description':'',
											'Prerequisites':'Study of the body and the humanities. All physical Characteristic Ratings must be at least 4.',
											'Skill Point Mod':3,
											'Extra Skill Options':['Machine Guns', 'Longarms', 'Handguns', 'Paint Gun', 'Air Vehicles', 'Marine Vehicles', 'Urban', 'Environ (Any)','Gravity (Any)'],
											'Benefits':{'A':['Patrolman', '250 Mils Cash'],
		                							    'B':['Constable', '700 Mils Cash', 'Civ Level 6 Laser Pistol'],
		      								            'C':['Sergeant', '2 Trans Cash', 'Civ Level 8 Laser Pistol'],
		                 								'D':['Marshal', '7 Trans Cash', 'Civ Level 6 Paint Gun', 'Used ATV'],
		                 								'E':['Inspector', '20 Trans Cash', '500 Mils/Year Pension', 'Civ Level 8 Paint Gun'],
		                 								'F':['Chief', '40 Trans Cash', '2 Trans/Year Pension', 'Civ Level 8 Paint Gun', 'Hand Gun (Any)']}}

		merchant = True
		if study_choices.count('Business') < 2:
			if 'Business' not in study_choices and 'Applied Science' not in study_choices:
				merchant = False
		if int(character.stats['Intelligence']) < 5:
			merchant = False
		if int(character.stats['Empathy']) < 7:
			merchant = False
		if self.money != '1 Tran' and unit != 'Trans':
			merchant = False
		if merchant:
			profession_options['Merchant'] = {'Name':'Merchant',
											  'Personnel Type':'Civilian', 
											  'Description':'',
											  'Prerequisites':'Study of business twice or study of business and applied science. Characteristic Ratings of at least Intelligence 5 and Empathy 7. Initial wealth must be at least 1 Tran.',
											  'Skill Point Mod':5,
											  'Extra Skill Options':['Diplomacy', 'Air Vehicles', 'Marine Vehicles', 'Agriculture', 'Electro Tech', 'Computer/Robot Tech', 'Vehicle Tech', 'Urban', 'Environ (Any)'],
											  'Benefits':{'A':['Nothing, and all Initial Wealth lost'],
		                 								  'B':['Civ Level 7 Business Computer'],
		               									  'C':['Initial Wealth x 3', 'Civ Level 7 Business Computer'],
		               									  'D':['Initial Wealth x 10', 'Civ Level 7 Business Computer'],
		             								      'E':['Initial Wealth x 20', 'Civ Level 5 Truck'],
		               									  'F':['Initial Wealth x 40', 'Civ Level 7 Jet']}}

		ranger = True
		if 'Military' not in study_choices or 'The Body' not in study_choices:
			ranger = False
		if int(character.stats['Strength']) < 4:
			ranger = False
		if int(character.stats['Endurance']) < 4:
			ranger = False
		if int(character.stats['Dexterity']) < 4:
			ranger = False
		if int(character.stats['Agility']) < 4:
			ranger = False
		if ranger:
			profession_options['Ranger'] = {'Name':'Ranger',
											'Personnel Type':'Military', 
											'Description':'',
											'Prerequisites':'Study of the military and the body. All physical Characteristic Ratings must be at least 4.',
											'Skill Point Mod':2,
											'Extra Skill Options':['Artillery', 'Machine Guns', 'Paint Gun', 'Bows', 'Military Ground Vehicles', 'Air Vehicles', 'Marine Vehicles', 'Weapon Tech', 'Vehicle Tech', 'Treatment', 'Environ (Any)'],
											'Benefits':{'A':['Ranger', '300 Mils Cash', 'Respirator'],
		                 								'B':['Corporal', '1 Tran Cash', 'Civ Level 6 Respirator Helmet'],
		            							        'C':['Sergeant', '3 Trans Cash', 'Civ Level 8 Respirator Helmet'],
		             								    'D':['Lieutenant', '10 Trans Cash', '250 Mils/Year Pension', 'Civ Level 8 Respirator Helmet', 'Civ Level 6 Laser Pistol'],
		               								    'E':['Captain', '25 Trans Cash', '750 Mils/Year Pension', 'Civ Level 8 Respirator Helmet', 'Civ Level 8 Laser Pistol'],
		               								    'F':['Colonel', '60 Trans Cash', '2.5 Trans/Year Pension', 'Civ Level 8 Respirator Helmet', 'Civ Level 8 Paint Gun']}}

		reporter = True
		if 'Humanities' not in study_choices:
			reporter = False
		if 'Business' not in study_choices and 'Theoretical Science' not in study_choices:
			reporter = False
		if int(character.stats['Intelligence']) < 7:
			reporter = False
		if int(character.stats['Mental Power']) < 2:
			reporter = False
		if int(character.stats['Aggression']) < 5:
			reporter = False
		if reporter:
			profession_options['Reporter'] = {'Name':'Reporter',
											  'Personnel Type':'Civilian', 
											  'Description':'',
											  'Prerequisites':'Study of the humanities and either business or theoretical science. Characteristic Ratings of at least Intelligence 7, Mental Power 2, and Aggression 5.',
											  'Skill Point Mod':7,
											  'Extra Skill Options':['Unarmed Combat', 'Survival', 'Disguise', 'Forgery/Counterfeiting', 'Urban', 'Air Vehicles', 'Programming', 'Electro Tech', 'Recruiting'],
											  'Benefits':{'A':['Audio Recorder'],
		                								  'B':['2 Trans Cash', 'Photographic Equipment', 'Audio Recorder'],
		            								      'C':['500 Mils x Int. Rating Cash', 'Planetary News Credentials', 'Superoid Camera', 'Audio Recorder'],
		           									      'D':['3 Trans x Int. Rating Cash', 'Star System News Credentials', 'Basic Holographer', 'Audio Recorder'],
		             								      'E':['10 Trans x Int. Rating Cash', 'Federation-Wide News Credentials', 'Shoulder Holographer', 'Audio Recorder'],
		               									  'F':['25 Trans x Int. Rating Cash', 'Federation Media Celebrity', 'Manner 38sdf Robot w/ Information & Holographer Systems', 'Audio Recorder']}}

		scientist = True
		check = 0
		if 'Theoretical Science' in study_choices:
			check += 1
		if 'Applied Science' in study_choices:
			check += 1
		if 'Humanities' in study_choices:
			check += 1
		if check < 2:
			scientist = False
		if int(character.stats['Intelligence']) < 8:
			scientist = False
		if scientist:
			profession_options['Scientist'] = {'Name':'Scientist',
											   'Personnel Type':'Civilian, Government', 
											   'Description':'',
											   'Prerequisites':'Study of two of the following: theoretical science, applied science, the humanities. Intelligence Rating of at least 8.',
											   'Skill Point Mod':9,
											   'Extra Skill Options':['Teaching', 'Agriculture', 'Chemistry', 'Planetology', 'Programming', 'Biology', 'Geology', 'Astronomy', 'Energy', 'Computer/Robot Tech'],
											   'Benefits':{'A':['1 Tran Cash'],
		                 								   'B':['2 Trans Cash', 'Civ Level 5 Chemlab'],
		                								   'C':['500 Mils x Int. Rating Cash', 'Civ Level 6 Chemsynthesizer'],
		                 								   'D':['2 Trans x Int. Rating Cash', 'Civ Level 7 Chemlab'],
		               									   'E':['6 Trans x Int. Rating Cash', 'Civ Level 8 Bioscanner', 'Civ Level 8 Geoscanner'],
		             								       'F':['15 Trans x Int. Rating Cash', 'Frazette Amber Robot w/ Geo, Chemical, Bio, & Information Systems']}}

		scout = True
		if 'Theoretical Science' not in study_choices or 'Applied Science' not in study_choices:
			scout = False
		if int(character.stats['Strength']) < 3:
			scout = False
		if int(character.stats['Endurance']) < 3:
			scout = False
		if int(character.stats['Dexterity']) < 3:
			scout = False
		if int(character.stats['Agility']) < 3:
			scout = False		
		if int(character.stats['Mental Power']) < 2:
			scout = False
		if int(character.stats['Empathy']) < 6:
			scout = False
		if int(character.stats['Mental Power']) > 4:
			scout = True
		if scout:
			profession_options['Scout'] = {'Name':'Scout',
										   'Personnel Type':'Military', 
										   'Description':'',
										   'Prerequisites':'Study of theoretical or applied science. All physical Characteristic Ratings must be at least 3, Mental Power 2, Empathy 6.',
										   'Skill Point Mod':4,
										   'Extra Skill Options':['Longarms', 'Handguns', 'Pilot', 'EVA', 'Survival', 'Air Vehicles', 'Marine Vehicles', 'Jetpacks', 'Planetology', 'Treatment', 'Biology', 'Geology', 'Astronomy', 'Suit Tech', 'Environ (Any)', 'Gravity (Any)'],
										   'Benefits':{'A':['Scout Second Class', '300 Mils Cash'],
		                 							   'B':['Scout First Class', '1 Trans Cash', 'Civ Level 6 Expedition Suit'],
		               								   'C':['Master Scout', '3 Trans Cash', 'Civ Level 7 Expedition Suit'],
		                							   'D':['Single Scout', '5 Trans Cash', 'Civ Level 7 Expedition Suit', 'Neuroscanner', 'Rover'],
		              								   'E':['Expedition Leader', '25 Trans Cash', '750 Mils/Year Pension', 'Civ Level 7 Expedition Suit', 'Crawler'],
		              								   'F':['Scout Commodore', '60 Trans Cash', '2.5 Trans/Year Pension', 'Civ Level 7 Expedition Suit', 'Used Explorer Pod']}}

		space_pirate = True
		if 'Humanities' in study_choices:
			space_pirate = False
		if int(character.stats['Strength']) < 5:
			space_pirate = False
		if int(character.stats['Endurance']) < 5:
			space_pirate = False
		if int(character.stats['Dexterity']) < 5:
			space_pirate = False
		if int(character.stats['Agility']) < 5:
			space_pirate = False		
		if int(character.stats['Aggression']) < 7:
			space_pirate = False
		if int(character.stats['Mental Power']) < 2:
			space_pirate = False
		if int(value) > 4 and unit == 'Trans':
			space_pirate = False
		if int(character.stats['Mental Power']) > 4:
			space_pirate = True
		if space_pirate:
			profession_options['Space Pirate'] = {'Name':'Space Pirate',
												  'Personnel Type':'Civilian', 
										   		  'Description':'',
										  		  'Prerequisites':'All physical Characteristic Ratings must be at least 5, Aggression 7, Mental Power 2. Cannot have more than 4 Trans Initial Wealth or have studied the humanities.',
										 		  'Skill Point Mod':6,
										 		  'Extra Skill Options':['Body Armor', 'Handguns', 'Paint Gun', 'Arc Gun', 'Bows', 'Unarmed Combat', 'Gunnery', 'Missile Guidance', 'Space Tactics', 'Pilot', 'Linguistics', 'Disguise', 'Forgery/Counterfeiting', 'EVA', 'Air Vehicles', 'Asteroid Mining', 'Planetology', 'Astronomy', 'Spaceship Tech', 'Weapon Tech', 'Gravity (NW)'],
										 		  'Benefits':{'A':['Internal Gravity Web', 'All Initial Wealth lost'],
		                 									  'B':['Initial Wealth x 2', 'Internal Gravity Web'],
		            									      'C':['Initial Wealth x 4', 'Wanted by Federation', 'Internal Gravity Web'],
		            									      'D':['Initial Wealth x 10', 'Internal Gravity Web'],
		             									      'E':['Initial Wealth x 10', 'Terwillicker 5000 Battlecraft', 'Wanted by Federation', 'Internal Gravity Web'],
		            									      'F':['Initial Wealth x 20', 'Piccolo Spaceship w/ Light Weapon Pod', 'Internal Gravity Web']}}

		space_technician = True
		if study_choices.count('Applied Science') < 2:
			space_technician = False
		if int(character.stats['Dexterity']) < 7:
			space_technician = False
		if int(character.stats['Intelligence']) < 7:
			space_technician = False		
		if int(character.stats['Mental Power']) < 2:
			space_technician = False
		if space_technician:
			profession_options['Space Technician'] = {'Name':'Space Technician',
													  'Personnel Type':'Civilian, Military, Government', 
										   		  	  'Description':'',
										  		  	  'Prerequisites':'Study of applied science twice, Characteristic Ratings of at least Dexterity 7, Intelligence 7, Mental Power 2.',
										 		  	  'Skill Point Mod':8,
										 		  	  'Extra Skill Options':['Psion Tech', 'EVA', 'Programming', 'Astronomy', 'Physics', 'Energy Tech', 'Spaceship Tech', 'Computer/Robot Tech'],
										 		  	  'Benefits':{'A':['500 Mils Cash'],
		         									        	  'B':['2 Trans Cash'],
		             									    	  'C':['5 Trans Cash', 'Civ Level 7 Electrokit'],
		            									    	  'D':['15 Trans Cash', 'Civ Level 8 Electrokit'],
		             								     		  'E':['30 Trans Cash', 'Civ Level 7 Spaceship Kit'],
		                										  'F':['60 Trans Cash', 'Frazette Amber Robot w/ Spaceship Tech, Electro Tech, & Self-Activation Systems']}}

		spacetrooper = True
		if 'Military' not in study_choices or 'The Body' not in study_choices:
			spacetrooper = False
		if int(character.stats['Strength']) < 6:
			spacetrooper = False
		if int(character.stats['Endurance']) < 6:
			spacetrooper = False
		if int(character.stats['Dexterity']) < 6:
			spacetrooper = False
		if int(character.stats['Agility']) < 6:
			spacetrooper = False		
		if int(character.stats['Aggression']) < 5:
			spacetrooper = False
		if home_environ.gravity == 'NW':
			spacetrooper = False
		if spacetrooper:
			profession_options['Spacetrooper'] = {'Name':'Spacetrooper',
												  'Personnel Type':'Military', 
										   		  'Description':'',
										  		  'Prerequisites':'Study of the military and the body, all physical Characteristic Ratings must be at least 6, Aggression 5, Home gravity cannot be NW.',
										 		  'Skill Point Mod':5,
										 		  'Extra Skill Options':['Body Armor', 'Artillery', 'Machine Guns', 'Paint Gun', 'Arc Gun', 'Military Ground Vehicles', 'Suit Tech', 'Environ (Any)', 'Gravity (Any except NW)'],
										 		  'Benefits':{'A':['Trooper', '300 Mils Cash', 'Civ Level 6 Armor Vest', 'Civ Level 6 Respirator Helmet'],
		                 									  'B':['Corporal', '1 Tran Cash', 'Civ Level 6 Reflective Body Armor'],
		                 									  'C':['Sergeant', '3 Trans Cash', 'Civ Level 7 Impact Body Armor'],
		                 									  'D':['Lieutenant', '10 Trans Cash', '250 Mils/Year Pension', 'Civ Level 7 Reflect/Impact Body Armor'],
		                 									  'E':['Captain', '25 Trans Cash', '1 Tran/Year Pension', 'Civ Level 8 Reflective Body Armor'],
		                 									  'F':['Colonel', '60 Trans Cash', '3 Trans/Year Pension', 'Civ Level 8 Reflect/Impact Body Armor', 'Arc Gun']}}

		spy = True
		if 'The Mind' not in study_choices or 'The Body' not in study_choices:
			spy = False
		if int(character.stats['Dexterity']) < 7:
			spy = False
		if int(character.stats['Agility']) < 5:
			spy = False		
		if int(character.stats['Intelligence']) < 6:
			spy = False
		if int(urban_skill) < 1:
			spy = False
		if spy:
			profession_options['Spy'] = {'Name':'Spy',
										 'Personnel Type':'Government', 
										 'Description':'',
										 'Prerequisites':'Study of the mind and the body, Characteristic Ratings of at least Dexterity 7, Agility 5, Intelligence 6, Urban Skill of at least 1.',
										 'Skill Point Mod':7,
										 'Extra Skill Options':['Demolitions', 'Longarms', 'Handguns', 'Paint Gun', 'Arc Gun', 'Bows', 'Linguistics', 'Disguise', 'Forgery/Counterfeiting', 'Weapon Tech', 'Urban'],
										 'Benefits':{'A':['False Identity Papers'],
		                 							 'B':['Civ Level 6 Plastic Pistol', 'False Identity Papers'],
		                 							 'C':['Any one Handgun or Laser Pistol', 'False Identity Papers'],
		                 							 'D':['700 Mils Cash', 'Civ Level 8 Laser Pistol', 'Any second Handgun', 'False Identity Papers'],
		                 							 'E':['4 Trans Cash', 'Civ Level 8 Paint Gun', 'Any second Handgun', 'False Identity Papers'],
		                 							 'F':['20 Trans Cash', 'Arc Gun', 'Any second Handgun', 'False Identity Papers']}}

		star_sailor = True
		if 'Military' not in study_choices:
			star_sailor = False
		if 'Applied Science' not in study_choices and 'The Body' not in study_choices:
			star_sailor = False
		if int(character.stats['Agility']) < 5:
			star_sailor = False		
		if int(character.stats['Intelligence']) < 7:
			star_sailor = False
		if int(character.stats['Mental Power']) < 2:
			star_sailor = False
		if home_environ.gravity == 'EX':
			star_sailor = False
		if int(character.stats['Mental Power']) > 4:
			star_sailor = True
		if star_sailor:
			profession_options['Star Sailor'] = {'Name':'Star Sailor',
												 'Personnel Type':'Military', 
										         'Description':'',
										         'Prerequisites':'Study of the military and either applied science or the body, Characteristic Ratings of at least Agility 5, Intelligence 7, Mental Power 2. Home gravity cannot be EX.',
										         'Skill Point Mod':6,
										         'Extra Skill Options':['Pilot', 'Astronomy', 'Energy Tech', 'Suit Tech', 'Spaceship Tech', 'Weapon Tech', 'Space Tactics', 'Gunnery', 'Missile Guidance', 'EVA', 'Gravity (NW)'],
										         'Benefits':{'A':['Midshipman', '500 Mils Cash', 'Internal Gravity Web'],
		                 									 'B':['Ensign', '1.5 Mils Cash', 'Internal Gravity Web', '10 LY Free Passage'],
		                									 'C':['Lieutenant', '4 Trans Cash', '300 Mils/Year Pension', 'Internal Gravity Web', '20 LY Free Passage'],
		                 									 'D':['Captain', '15 Trans Cash', '1 Tran/Year Pension', 'Internal Gravity Web', '50 LY Free Passage'],
		                 									 'E':['Commander', '36 Trans Cash', '3 Trans/Year Pension', 'Internal Gravity Web', '100 LY Free Passage'],
		                									 'F':['Admiral', '80 Trans Cash', '10 Trans/Year Pension', 'Internal Gravity Web', 'Perpetual Free Passage']}}

		thinker = True
		if 'The Mind' not in study_choices:
			thinker = False
		if 'Applied Science' not in study_choices and 'Humanities' not in study_choices:
			thinker = False
		if int(character.stats['Intelligence']) < 7:
			thinker = False
		if int(character.stats['Mental Power']) < 5:
			thinker = False
		if thinker:
			profession_options['Thinker'] = {'Name':'Thinker',
											 'Personnel Type':'Civilian, Government', 
										     'Description':'',
										     'Prerequisites':'Study of the mind and either applied science or the humanities, Characteristic Ratings of at least Intelligence 7, Mental Power 5.',
										     'Skill Point Mod':10,
										     'Extra Skill Options':['Navigation', 'Mind Control', 'Psychokinesis', 'Psion Tech', 'Teaching'],
										     'Benefits':{'A':['None'],
		                 								 'B':['Interstellar Comlink'],
		                 								 'C':['1 Tran Cash', 'Interstellar Comlink'],
		                 								 'D':['3 Trans Cash', 'Psionic Rig'],
		                 								 'E':['10 Trans Cash', 'Psionic Rig'],
		                 								 'F':['25 Trans Cash', 'Augmented Jump Pod']}}

		zero_g_miner = True
		if 'Applied Science' not in study_choices and 'Business' not in study_choices:
			zero_g_miner = False	
		if int(character.stats['Dexterity']) < 5:
			zero_g_miner = False
		if int(character.stats['Agility']) < 3:
			zero_g_miner = False
		if int(value) < 500 and unit == 'Mils':
			zero_g_miner = False
		if unit == 'Mil':
			zero_g_miner = False
		if home_environ.gravity == 'EX':
			zero_g_miner = False
		if zero_g_miner:
			profession_options['Zero-G Miner'] = {'Name':'Zero-G Miner',
												  'Personnel Type':'Civilian', 
										     	  'Description':'',
										     	  'Prerequisites':'Study of applied science or business, Characteristic Ratings of at least Dexterity 5, Agility 3. Initial Wealth must be at least 500 Mils, Home Gravity may not be EX.',
										     	  'Skill Point Mod':4,
										     	  'Extra Skill Options':['Pilot', 'Economics', 'Trading', 'EVA', 'Mining', 'Asteroid Mining', 'Geology', 'Electro Tech', 'Gravity (NW)'],
										     	  'Benefits':{'A':['None'],
		                 									  'B':['Initial Wealth x 2'],
		                									  'C':['Initial Wealth x 3', 'Rock Blaster'],
		               										  'D':['Initial Wealth x 5', 'Civ Level 8 Geoscanner'],
		               										  'E':['Initial Wealth x 10', 'Rock Blaster', 'Civ Level 8 Geoscanner'],
		               										  'F':['Initial Wealth x 20', 'Manner 44 Robot w/ Force Field, Geo, Pilot, and Chemical Systems']}}

		print ""
		print "Determining profession options: "
		status_bar()
		print ""

		return(profession_options)

	def choose_profession(self, profession_options):

		print "You are eligible for the following professions: "
		print ""
		print "==============="
		for profession in sorted(profession_options.keys()):
			print profession
		print "==============="
		print ""
		print "To see more information about a profession, enter its name: "

		done = False
		while not done:
			choice = raw_input().title()
			print ""
			if choice not in profession_options.keys():
				print "That is not an eligible profession, please try again: "
			else:
				pretty(profession_options[choice])
				print ""
				print "Would you like to choose " + choice + " as your profession? (Y/N)"
				response = y_n_response()
				if response == 'Y':
					profession = profession_options[choice]
					done = True
				else:
					print ""
					print "To see more information about a profession, enter its name: "

		self.profession = profession['Name']
		return (profession)				

	def choose_years_experience(self, profession):
		print ""
		print "Your character has a base age of 20 years old; you may declare how long they have been employed (4, 8, 12, 16, 20 years)."
		print "Longer employment gives a higher chance at additional benefits (as seen in the profession description), but can also reduce your characteristic ratings."
		print "NOTE: The declared number of years employed may differ from the true number used; this difference reflects years of unemployment, and is determined randomly."
		print "NOTE: Military professions cannot be unemployed, but the number of years served may differ from the declared number, determined randomly."
		print "Enter number of years employed: "

		year_check = True
		year_opt = [4, 8, 12, 16, 20]
		while year_check:
			years = raw_input()
			try:
				years = int(years)
				if years in year_opt:
					year_check = False
				else:
					print "Invalid response, please try again: "
			except:
				print "Invalid response, please try again: "

		d10 = random.randint(1,10)
		file = open('years_employed.txt')
		i=0
		for line in file:
			year_info = line.strip().split('\t')
			i+=1
			if i > (d10-1):
				break
		employed_years = int(year_info[years/4])

		if profession['Name'] == 'Colonist' or profession['Name'] == 'Thinker':
			age = years + 20
			employed_years = years
		elif profession['Personnel Type'] == 'Military':
			age = employed_years + 20
		else:
			age = years + 20
		self.age = age

		return(employed_years)

	def adjust_ratings(self):
		if self.age < 28:
			loss_check = 0
		else:
			loss_check = self.age + random.randint(1,10)

		file = open('adjust_ratings.txt')
		for line in file:
			adj_min, adj_max, points_lost = line.strip().split('\t')
			if int(adj_min) <= loss_check <= int(adj_max):
				break

		reduced_stats = [self.stats['Endurance'], self.stats['Agility'], self.stats['Strength'], self.stats['Dexterity']]

		points_lost = int(points_lost)
		stat_iter = iter(reduced_stats)

		while points_lost > 0:
			for stat in reduced_stats:
				if stat > 1:
					stat += -1
					points_lost += -1

		self.stats['Endurance'] = reduced_stats[0]
		self.stats['Agility'] = reduced_stats[1]
		self.stats['Strength'] = reduced_stats[2]
		self.stats['Dexterity'] = reduced_stats[3]

		print ""
		print "Reducing physical characteristics due to aging: "
		status_bar()
		print ""
		if points_lost > 0:
			print "ERROR in point reduction"

	def add_skill_points(self, employed_years, profession):
		extra_skills_check = [[1,2,2,3,3,4,4],[4,5,6,6,7,7,8],[6,7,8,8,9,10,11],[7,8,9,10,11,12,13],[7,8,10,11,12,14,15]]
		skill_roll = random.randint(1,10) + self.stats['Intelligence'] + profession['Skill Point Mod']
		i = employed_years/4 - 1
		if 0 < skill_roll <= 5:
			j = 0
		elif 6 <= skill_roll <= 9:
			j = 1
		elif 10 <= skill_roll <= 13:
			j = 2
		elif 14 <= skill_roll <= 17:
			j = 3
		elif 18 <= skill_roll <= 21:
			j = 4
		elif 22 <= skill_roll <= 26:
			j = 5
		else:
			j = 6
		num_extra_skills = extra_skills_check[i][j]

		print ""
		print "Adding skill points from profession selection: "
		status_bar()
		print ""

		return(num_extra_skills)

	def choose_professional_skills(self, skill_choices, num_extra_skills, study_choices, urban_skill, profession, employed_years):
		study_choices.append('General')
		study_choices.append('Professional')
		skill_dict = {'Theoretical Science':['Chemistry', 'Physics', 'Programming', 'Biology', 'Geology', 'Astronomy'],
		              'Applied Science':['Suit Tech', 'Electro Tech', 'Construction', 'Vehicle Tech', 'Programming'],
		              'Business':['Programming', 'Recruiting', 'Law', 'Economics', 'Trading'],
		              'Humanities':['Linguistics', 'Diplomacy', 'Law', 'Teaching'],
		              'The Mind':['Psionic Boost', 'Psionic Communication', 'Life Sense'],
		              'The Body':['Unarmed Combat', 'Ambush', 'EVA', 'Home Gravity', 'Jetpacks', 'Survival'],
		              'Military':['Battlefield', 'Longarms', 'Handguns', 'Demolitions', 'Grenades'],
		              'General':['Streetwise', 'Stun Gun', 'Gambling', 'Blades', 'Ground Vehicles', 'Urban', 'Home Environ'],
		              'Professional':profession['Extra Skill Options']}

		skill_subset = []
		for field in set(study_choices):
			if field in skill_dict.keys():
				for skill in skill_dict[field]:
					skill_subset.append(skill)
		if urban_skill < 1:
			skill_subset.remove('Urban')
		
		i = 1
		skill_subset_dict = {}
		for skill in set(skill_subset):
			skill_subset_dict[i] = skill
			i += 1

		if employed_years == 4:
			max_skill_val = 3
		elif employed_years == 8 or employed_years == 12:
			max_skill_val = 4
		elif employed_years == 16 or employed_years == 20:
			max_skill_val = 5
		else:
			print "ERROR in determining maximum skill value"

		print ""
		print "You have " + str(num_extra_skills) + " additional skill points to assign to skills appropriate to your profession and chosen fields of study. Each skill costs 1 point."
		print "The maximum value of any given skill is determined by your years of employment; your character may not have any skill greater than " + str(max_skill_val) + "."
		print "The skills available to you are listed below. Make your selections by entering the numbers associated with the appropriate fields."
		print ""
		print "CURRENT SKILLS"
		print "-------------------------"
		for skill in skill_choices:
			print skill
		print "-------------------------"
		print ""
		print "AVAILABLE SKILLS"
		print "-------------------------"
		for number, field in sorted(skill_subset_dict.iteritems()):
			print number, '\t', field
		print "-------------------------"
		print ""
		print "Your selections (one entry at a time):"

		while num_extra_skills > 0:
			choice = raw_input()
			if choice.isdigit():
				choice = int(choice)
				if choice in skill_subset_dict.keys():
					if skill_choices.count(skill_subset_dict[choice]) < max_skill_val:
						skill_choices.append(skill_subset_dict[choice])
						num_extra_skills += -1
					else:
						print "You have reached the maximum level for that skill, please try again:"
				else:
					print "Invalid selection, please try again:"
			else:
				print "Invalid selection, please try again:"

		self.skills = skill_choices

	def determine_benefits(self, employed_years, profession):
		print ""
		print "Determining professional benefits: "
		status_bar()
		print ""

		benefits_roll = random.randint(1,10) + employed_years
		if 0 <= benefits_roll <= 10:
			benefits = profession['Benefits']['A']
			print "Your benefit level is 'A': " + str(benefits)
		elif 11 <= benefits_roll <= 14:
			benefits = profession['Benefits']['B']
			print "Your benefit level is 'B': " + str(benefits)
		elif 15 <= benefits_roll <= 18:
			benefits = profession['Benefits']['C']
			print "Your benefit level is 'C': " + str(benefits)
		elif 19 <= benefits_roll <= 23:
			benefits = profession['Benefits']['D']
			print "Your benefit level is 'D': " + str(benefits)
		elif 24 <= benefits_roll <= 28:
			benefits = profession['Benefits']['E']
			print "Your benefit level is 'E': " + str(benefits)
		else:
			benefits = profession['Benefits']['F']
			print "Your benefit level is 'F': " + str(benefits)

		self.items = benefits

	def final_checks(self, profession, environ_skill):
		if profession['Personnel Type'] == 'Military':
			self.title = self.items[0]
			del self.items[0]

		if self.profession == 'Lawman':
			self.title = self.items[0]
			del self.items[0]

		if self.profession == 'Freefaller':
			if self.gravity['NW'] < 2:
				self.gravity['NW'] = 2

		if self.profession == 'Spacetrooper':
			for grav in self.gravity.keys():
				if self.gravity[grav] < 0:
					self.gravity[grav] = 0

		if self.profession == 'Star Sailor':
			if self.gravity['NW'] < 0:
				self.gravity['NW'] = 0

		if self.profession == 'Zero-G Miner':
			if self.gravity['NW'] < 0:
				self.gravity['NW'] = 0

		if 'Home Environ' in self.skills:
			environ_skill += int(self.skills.count('Home Environ'))
			self.skills[:] = (skill for skill in self.skills if skill != 'Home Environ')

		if 'Urban' in self.skills:
			self.urban += int(self.skills.count('Urban'))
			self.skills[:] = (skill for skill in self.skills if skill != 'Urban')

		if 'Nothing' in self.items:
			self.items.remove('Nothing') 


class Home_Environ:
	def __init__(self):
		self.environ = 'Environ'
		self.gravity = 'Gravity'
		self.temperature = 'Temperature'

	def create_environ(self, mults):
		d10_1 = random.randint(1,10)
		d10_2 = random.randint(1,10)+floor(int(mults['phys_mult']))-floor(int(mults['coord_mult']))+3
		row = int(10*d10_2+d10_1)
		file = open('home_environs.txt')
		i=0
		for line in file:
			environ_skill, land_cont, land_feat, home_grav, home_temp, urban_skill = line.strip().split('\t')
			i+=1
			if i > row:
				break

		environ_skill, urban_skill = int(environ_skill), int(urban_skill)

		if land_feat != 'None':
			self.environ = land_cont+', '+land_feat
		else:
			self.environ = land_cont
		self.gravity = home_grav
		self.temperature = home_temp

		print "Constructing home environ:"
		status_bar()
		print ""
		print "Environ Skill = " + str(environ_skill)
		print "Home Environ features: " + self.environ
		print ""
		return(environ_skill,urban_skill)

def status_bar():
	tform = '{l_bar}{bar}|{percentage:3.0f}%'
#	desc = desc
	for i in tqdm(range(30), desc=None, bar_format=tform, ncols=100):
		time.sleep(0.05)

def y_n_response():
	response = raw_input().upper()
	test = 1
	while test == 1:
		if response == 'Y':
			test = 0
		elif response == 'N':
			test = 0
		else:
			print "Unrecognized response! Please try again:"
			response = raw_input().upper()
	return(response)

def pretty(d, indent=0):
	for key, value in sorted(d.items()):
		print('\t' * indent + str(key).upper())
		if isinstance(value, dict):
			for key, value2 in sorted(value.items()):
				print('\t' * (indent+1) + str(key).upper() + ": " + str(value2))
		else:
			print('\t' * (indent+1) + str(value))

def save(character, home_environ, environ_skill):
	print "Save this character? (Y/N): "
	response = y_n_response()
	if response == 'Y':
		print "Enter a filename (.txt will be added as an extension): "
		filename = raw_input()
		savefile = open(filename + '.txt', 'w')
		savefile.write("NAME:\t" + character.name + '\n')
		savefile.write("AGE:\t" + str(character.age) + '\n')
		savefile.write("PROFESSION:\t" + character.profession + '\n')
		if character.title:
			savefile.write("TITLE:\t" + character.title + '\n')
		savefile.write("BACKGROUND:\t" + character.social + '\n')
		savefile.write("WEALTH:\t" + str(character.money) + '\n' + '\n')
		savefile.write("ITEMS:\n")
		for item in character.items:
			savefile.write(item + '\n')
		savefile.write("\nSTATS:\n")
		for stat in character.stats:
			savefile.write(stat + '\t' + str(character.stats[stat]) + '\n')
		savefile.write("\nSKILLS:\n")
		for skill in set(character.skills):
			savefile.write(skill + '\t' + str(character.skills.count(skill)) + '\n')
		savefile.write('\n')
		savefile.write("ENVIRON:\n")
		savefile.write(home_environ.environ + '\n')
		savefile.write(home_environ.gravity + '\n')
		savefile.write(home_environ.temperature + '\n')

character = Character()
home_environ = Home_Environ()
character.create_name()
mults, study_points = character.determine_multipliers()
environ_skill,urban_skill = home_environ.create_environ(mults)
character.urban = urban_skill
environ_mod = character.create_grav_skills(home_environ, environ_skill, urban_skill)
init_skill_mod = character.create_social_standing(mults, environ_skill, urban_skill)
environ_skill = environ_skill - environ_mod
num_skill_points = character.create_skill_points(init_skill_mod)
study_choices = character.choose_fields_of_study(study_points)
skill_choices = character.choose_initial_skills(study_choices, num_skill_points, urban_skill)
character.create_stats(study_choices, mults)
profession_options = character.create_profession_options(study_choices, home_environ, urban_skill)
profession = character.choose_profession(profession_options)
employed_years = character.choose_years_experience(profession)
character.adjust_ratings()
num_extra_skills = character.add_skill_points(employed_years, profession)
character.choose_professional_skills(skill_choices, num_extra_skills, study_choices, urban_skill, profession, employed_years)
character.determine_benefits(employed_years, profession)
character.final_checks(profession, environ_skill)
save(character, home_environ, environ_skill)
#print character


