import math, random, re, json, map_maker_2

class Star:
	def __init__(self):
		self.name = 'Name'
		self.stellar_class = 'Stellar_class'
		self.chz_avg = 'Chz_avg'
		self.chz_min = 'Chz_min'
		self.chz_max = 'Chz_max'
		self.planet_num = 'Planets'

	def create_star_name(self):
		self.name = raw_input("Enter a name for your star: ")

	def create_stellar_class(self):
		stellar_class_dict = {'1':"A", '2':"F", '3':"G", '4':"K", '5':"M"}
		sc1 = str(random.randint(1,5))
		sc2 = str(random.randint(0,9))
		self.stellar_class = str(stellar_class_dict[sc1]+sc2)

	def create_star_zones(self):
		file = open('habitable.txt')
		for line in file:
			s_type,junk,chz_avg=line.strip().split(' ')
			if s_type == self.stellar_class:
				break
		file.close()

		self.chz_avg = float(chz_avg)
		self.chz_min = self.chz_avg*(1-0.5237/2.0)
		self.chz_max = self.chz_avg*(1+0.5237/2.0)

	def create_num_planets(self):
		max_planets = 12
		self.planet_num = []
		if int(self.stellar_class[-1:]) <= 4:
			icheck = 'i'
		else:
			icheck = 'j'
		temp_class = self.stellar_class[:1]+icheck

		planet_check = {'Ai':(2,5), 'Aj':(2,7), 'Fi':(2,8), 'Fj':(2,9), 'Gi':(2,11), 'Gj':(2,10), 'Ki':(2,9), 'Kj':(2,7), 'Mi':(2,6), 'Mj':(2,3)}
		pmin, pmax = planet_check[temp_class]

		for num in range(0, max_planets):
			exist_check = random.randint(1,12)
			if pmin <= exist_check and exist_check <= pmax:
				self.planet_num.append(num)

class Planet:
	def __init__(self):
		self.name = 'Name'
		self.location = 'Location'
		self.distance = 'Distance'
		self.zone = 'Zone'
		self.size = 'Size'
		self.gravity = 'Gravity'
		self.climate = 'Climate'
		self.temperature = 'Temperature'
		self.atmosphere = 'Atmosphere'
		self.hydrograph = 'Hydrograph'
		self.abundance = 'Abundance'
		self.moon_num = 'Moons'
		self.moons = {}
		self.environ_dist = 'Environs'
		self.resources = []

	def __repr__(self):
		return json.dumps(self.__dict__, indent=2)

	def create_planet_name(self, planet_name):
		self.name = planet_name

	def create_planet_distance(self):
		file = open('planet_dists.txt')
		planet_dist_info = file.readlines()
		file.close()

		loc = int(re.search(r'\d+$', self.name).group())

		p_num,p_dist_min,p_dist_avg,p_dist_max = planet_dist_info[loc].split('\t')
		p_dist = round(random.uniform(float(p_dist_min),float(p_dist_max)), 2)

		self.location = loc
		self.distance = p_dist

	def create_planet_zone(self, my_star):
		cnz1_min = my_star.chz_min-0.5*(my_star.chz_max-my_star.chz_min)
		cnz1_max = my_star.chz_min
		cnz2_min = my_star.chz_max
		cnz2_max = my_star.chz_max+2.0*(my_star.chz_max-my_star.chz_min)

		if my_star.chz_min <= self.distance <= my_star.chz_max:
			self.zone = 'Habitable'
		elif cnz1_min <= self.distance <= cnz1_max:
			self.zone = 'Neutral (N)'
		elif cnz2_min <= self.distance <= cnz2_max:
			self.zone = 'Neutral (F)'
		elif self.distance < cnz1_min:
			self.zone = 'Hostile (N)'
		else:
			self.zone = 'Hostile (F)'

	def create_planet_specs(self):
		file = open('planet_specs.txt')
		planet_specs_info = file.readlines()
		file.close()

		if self.zone == 'Habitable':
			ipoint = random.randint(1,80)
		elif self.zone == 'Neutral (N)' or self.zone == 'Neutral (F)':
			ipoint = random.randint(20,100)
		else:
			ipoint = random.randint(1,10)+90

		self.size, self.climate, self.abundance = planet_specs_info[ipoint-1].strip().split('\t')

	def create_planet_gravity(self):
		file = open('gravity.txt')
		gravity_info = file.readlines()
		file.close()

		try:
			line_num, p_gravity, g_desc = gravity_info[int(self.size)-1].strip().split('\t')
		except:
			line_num, p_gravity, g_desc = 0, '0', 'NW'

		self.gravity = p_gravity + ' (' + g_desc + ')'

	def create_planet_atmosphere(self):
		if self.size == 'A' or self.size < 2:
			atmo_check = 1
		else:
			atmo_check = int(self.size)+random.randint(1,10)

		file = open('atmospheres.txt')
		for line in file:
			line_num, e, t, h = line.strip().split('\t')
			if int(line_num) == atmo_check:
				if self.climate == 'Earth-like':
					self.atmosphere = e
				elif self.climate == 'Tolerable':
					self.atmosphere = t
				elif self.climate == 'Hostile':
					self.atmosphere = h
				else:
					print "Unrecognized climate type in atmosphere generation!"
					print self.climate
				break
		file.close()

	def create_planet_temperature(self, my_star):
		if int(self.distance) < my_star.chz_min:
			temp_check = random.randint(7,16) - 6
		elif int(self.distance) > my_star.chz_max:
			temp_check = random.randint(7,16) + 6
		else:
			temp_check = random.randint(7,16)

		file = open('temperatures.txt')
		for line in file:
			line_num, e, t, h = line.strip().split('\t')
			if int(line_num) == temp_check:
				if self.climate == 'Earth-like':
					self.temperature = e + ' (F)'
				elif self.climate == 'Tolerable':
					self.temperature = t + ' (F)'
				elif self.climate == 'Hostile':
					self.temperature = h + ' (F)'
				else:
					print "Unrecognized climate type in temperature generation!"
					print self.climate
				break
		file.close()

	def create_planet_hydrograph(self):
		if self.atmosphere != 'None':
			hydro_check = random.randint(1,10)
			if self.temperature == '50 (F)' or self.temperature == '75 (F)':
				file = open('hydrograph1.txt')
				for line in file:
					line_num, s3, s4, s5, s69 = line.strip().split('\t')
					if int(line_num) == hydro_check:
						if self.size == '3':
							self.hydrograph = s3
						elif self.size == '4':
							self.hydrograph = s4
						elif self.size == '5':
							self.hydrograph = s5
						else:
							self.hydrograph = s69
						break
				file.close()
			elif self.temperature == '0 (F)' or self.temperature == '25 (F)':
				file = open('hydrograph2.txt')
				for line in file:
					line_num, s2, s3, s4, s5, s69 = line.strip().split('\t')
					if int(line_num) == hydro_check:
						if self.size == '2':
							self.hydrograph = s2
						elif self.size == '3':
							self.hydrograph = s3
						elif self.size == '4':
							self.hydrograph = s4
						elif self.size == '5':
							self.hydrograph = s5
						else:
							self.hydrograph = s69
						break
				file.close()
			elif self.temperature == '100 (F)' or self.temperature == '125 (F)':
				file = open('hydrograph2.txt')
				for line in file:
					line_num, s2, s3, s4, s5, s69 = line.strip().split('\t')
					if int(line_num) == hydro_check:
						if self.size == '2':
							self.hydrograph = s2
						elif self.size == '3':
							self.hydrograph = s3
						elif self.size == '4':
							self.hydrograph = s4
						elif self.size == '5':
							self.hydrograph = s5
						else:
							self.hydrograph = s69
						break
				file.close()
			else:
				self.hydrograph = 0
		else:
			self.hydrograph = 0

	def create_num_moons(self):
		file = open('moon_specs1.txt')
		moon_info1 = file.readlines()
		file.close()

		moon_check = random.randint(0,9)*9
		try:
			self.moon_num = int(moon_info1[int(self.size)+moon_check-1].strip())
		except:
			self.moon_num = 0

	def define_moons(self):
		for i in range(0, self.moon_num):
			name = self.name+'-M'+str(i)
			self.moons[name]=Moon()
			self.moons[name].create_moon_name(name)
			self.moons[name].create_moon_size(self)
			self.moons[name].create_moon_gravity(self)
			self.moons[name].create_moon_specs(self)

	def create_environ_dist(self):
		file = open('environ_dist.txt')

		for line in file:
			size_check = int(line.split('\t')[0].strip())
			hydro_check = int(line.split('\t')[1].strip())
			if self.size != 'A':
				if int(self.size) == size_check and int(self.hydrograph) == hydro_check:
					environ_list = line.strip().split('\t')
					del environ_list[:2]
					self.environ_dist = map(int ,environ_list)
					break
			else:
				self.environ_dist = [0, 0, 0, 0, 0, 0, 0]

class Moon:
	def __init__(self):
		self.name = 'Name'
		self.size = 'Size'
		self.gravity = 'Gravity'
		self.climate = 'Climate'
		self.abundance = 'Abundance'
		self.resources = []

	def create_moon_name(self, moon_name):
		self.name = moon_name

	def create_moon_size(self, planet):
		file = open('moon_specs3.txt')
		moon_info3 = file.readlines()
		file.close()

		size_check = int(planet.size) + random.randrange(1,10)
		self.size = moon_info3[size_check-1].strip()

	def create_moon_gravity(self, planet):
		file = open('gravity.txt')
		gravity_info = file.readlines()
		file.close()

		try:
			line_num, m_gravity, g_desc = gravity_info[int(self.size)-1].strip().split('\t')
		except:
			line_num, m_gravity, g_desc=0,'0','NW'

		self.gravity = m_gravity + ' (' + g_desc + ')'

	def create_moon_specs(self, planet):
		file = open('moon_specs2.txt')
		moon_info2 = file.readlines()
		file.close()

		if planet.zone == 'Habitable':
			ipoint=random.randint(1,40)
		elif planet.zone == 'Neutral (N)' or planet.zone == 'Neutral (F)':
			ipoint=random.randint(11,50)
		else:
			ipoint=random.randint(1,5)+45
		self.climate, self.abundance = moon_info2[ipoint-1].strip().split('\t')
		allocate_resources(self)


def define_planets():
	planets = {}
	for i in my_star.planet_num:
		name = my_star.name+'-P'+str(i)
		planets[name]=Planet()
	return(planets)


def asc_planet_sort(value):
	return int(re.search(r'\d+$', value).group())

def allocate_resources(body):
	r_file = open('resource_table.txt', 'r')
	r_table = []
	for line in r_file:
		r_table.append(line.strip().split('\t'))
	if body.climate == 'Earth-like':
		mod = 50
	elif body.climate == 'Tolerable':
		mod = 25
	else:
		mod = 0
	if body.abundance == 'Poor':
		if body.size != 'A':
			tot_rolls = int(body.size)
		else:
			tot_rolls = 1
	elif body.abundance == 'Rich':
		if body.size != 'A':
			tot_rolls = int(body.size) + 8
		else:
			tot_rolls = 9
	else:
		print "Error in determining resource rolls!"
		print "Expecting 'Rich' or 'Poor', received: ", body.abundance
		quit()
	rolls = 0

	while rolls < tot_rolls:
		roll = random.randint(1,100) + mod
		for entry in r_table:
			if int(entry[0]) <= roll and roll <= int(entry[1]):
				if body.climate == 'Earth-like':
					resource = [entry[2],entry[3]]
				elif body.climate == 'Tolerable':
					resource = [entry[2],entry[4]]
				elif body.climate == 'Hostile':
					resource = [entry[2],entry[5]]
				elif body.climate == 'Ring':
					resource = [entry[2],entry[5]]
				else:
					print 'CANNOT IDENTIFY CLIMATE TYPE TO ALLOCATE RESOURCES!'
					print "Expecting 'Earth-like', 'Tolerable', 'Hostile', received: ", body.climate
					quit()

				if body.resources.count(resource) < 2:
					body.resources.append(resource)
					rolls+=1

	for resource in body.resources:
		if body.resources.count(resource) == 2:
			body.resources.remove(resource)
			body.resources.remove(resource)
			if resource[1] != 'S':
				resource = [resource[0],str(int(resource[1])*2)]
			else:
				resource = [resource[0],'1']
			body.resources.append(resource)

def save_star(star, outfile):
	outfile.write("STAR NAME: "+star.name+"\n")
	outfile.write("STELLAR CLASS: "+star.stellar_class+"\n")
	outfile.write("PLANETS: "+str(len(star.planet_num))+"\n")
	outfile.write("\n")
	outfile.write("==============================================="+"\n")
	outfile.write("\n")
	return

def save_planet(planet, outfile, count):
	outfile.write("Planet "+str(count)+"\n")
	outfile.write("NAME: "+planet.name+"\n")
	outfile.write("SIZE: "+planet.size+"\n")
	outfile.write("DISTANCE: "+str(planet.distance)+" AU"+"\n")
	outfile.write("ZONE: "+planet.zone+"\n")
	outfile.write("GRAVITY: "+planet.gravity+"\n")
	outfile.write("ATMOSPHERE: "+planet.atmosphere+"\n")
	outfile.write("CLIMATE: "+planet.climate+"\n")
	outfile.write("TEMPERATURE: "+planet.temperature+"\n")
	outfile.write("HYDROGRAPH: "+str(planet.hydrograph)+" %"+"\n")
	outfile.write("RESOURCES: "+"\n")
	for resource in planet.resources:
		for item in resource:
			outfile.write(item+" ")
		outfile.write("\n")
	outfile.write("MOONS: "+str(planet.moon_num)+"\n")
	outfile.write("\n")
	if planet.moon_num==0:
		outfile.write("==============================================="+"\n")
		outfile.write("\n")
	return

def save_moon(moon, outfile, count):
	outfile.write("Moon "+str(count)+"\n")
	outfile.write("NAME: "+moon.name+"\n")
	outfile.write("SIZE: "+moon.size+"\n")
	outfile.write("GRAVITY: "+moon.gravity+"\n")
	outfile.write("CLIMATE: "+moon.climate+"\n")
	outfile.write("RESOURCES: "+ "\n")
	for resource in moon.resources:
		for item in resource:
			outfile.write(item+" ")
		outfile.write("\n")
	outfile.write("\n")
	return

outfile = open('star.txt', 'w')
my_star = Star()
my_star.create_star_name()
my_star.create_stellar_class()
my_star.create_star_zones()
my_star.create_num_planets()

save_star(my_star, outfile)
planets = define_planets()

count=0
count2=0
for body in planets.keys():
	planets[body].create_planet_name(body)
	planets[body].create_planet_distance()
	planets[body].create_planet_zone(my_star)
	planets[body].create_planet_specs()
	planets[body].create_planet_gravity()
	planets[body].create_planet_atmosphere()
	planets[body].create_planet_temperature(my_star)
	planets[body].create_planet_hydrograph()
	planets[body].create_num_moons()
	planets[body].define_moons()
	planets[body].create_environ_dist()
#	map_maker_2.create_hex_map(planets[body])
	allocate_resources(planets[body])
#	print planets[body].resources
	count+=1
	save_planet(planets[body],outfile,count)
	for moon in planets[body].moons.keys():
		count2+=1
		save_moon(planets[body].moons[moon], outfile, count2)
		if count2==planets[body].moon_num:
			outfile.write("==============================================="+"\n")
			outfile.write("\n")

sorted(planets, key = asc_planet_sort)
#print repr(planets)

