from p4a.formats.rap.text import Reader, Writer
from p4a.formats.rap import Klass
from copy import deepcopy
import math, os
import settings as cfg

class Vector:
	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)
	def __add__(self, v):
		return Vector(self.x + v.x, self.y + v.y)
	def __mul__(self, v):
		return Vector(self.x * v, self.y * v)
	def perp(self):
		return Vector(self.y, -self.x)

spawns = dict(
	det5 = dict(
		azimuth = 240,
		pos = Vector(594,1189),
		limit = 'x',
		max = 2,
	),
	ana = dict(
		azimuth = 403,
		pos = Vector(580,1121),
		limit = 'y',
		max = 10,
	),
	marines = dict(
		azimuth = 224,
		pos = Vector(608,1150),
		limit = 'y',
		max = 10,
	),
	ukbaf = dict(
		azimuth = 264,
		pos = Vector(595,1131),
		limit = 'y',
		max = 10,
	),
	abe = dict(
		azimuth = 224,
		pos = Vector(604,1153),
		limit = 'y',
		max = 10,
	),
	acr = dict(
		azimuth = 123,
		pos = Vector(608,1157),
		limit = 'y',
		max = 10,
	),
	cdn = dict(
		azimuth = 220,
		pos = Vector(584,1148),
		limit = 'y',
		max = 2,
	),
)

for v in spawns.values():
	v['count'] = 0
	v['curpos'] = v['pos']
	
	v['unit'] = Vector(round(math.sin(v['azimuth']*math.pi/180), 3), round(math.cos(v['azimuth']*math.pi/180), 3))

teams = {}
teams['det5'] = dict(
	spawn = 'det5',
	name = 'SFOD-A',
	faction = 'det5',
	side = 'WEST',
	groups = [
		[
			{ 'role': "MAJ Singleton", 'loadout': 'officer_det5', 'medic': 1, 'callsign': 'SABRE',},
			{ 'role': "SGM Dodds", 'loadout': 'sniper_det5', 'medic': 1, },
			{ 'role': "CPT Moore", 'loadout': 'officer_det5', 'medic': 1, },
			{ 'role': "CW4 Pierce", 'loadout': 'officer_det5', 'medic': 1, },
			{ 'role': "MSG Nichols", 'loadout': 'rifleman_det5', 'medic': 1, },
			{ 'role': "SFC Furlong", 'loadout': 'sniper_det5', 'medic': 1, },
			{ 'role': "SFC Cannon", 'loadout': 'gunner_det5', 'medic': 1, },
			{ 'role': "SFC Bryhni", 'loadout': 'gunner_det5', 'medic': 1, },
			{ 'role': "SFC Cline", 'loadout': 'rifleman_det5', 'medic': 1, },
			{ 'role': "SFC Lee", 'loadout': 'medic_det5', 'medic': 1},
			{ 'role': "SSG Andresen", 'loadout': 'medic_det5', 'medic': 1},
			{ 'role': "SFC Sage", 'loadout': 'commo_det5', 'medic': 1, },
		],
	],
)
teams['sfqc'] = dict(
	spawn = 'det5',
	name = 'SOT-A',
	faction = 'det5',
	side = 'WEST',
	groups = [
		[
			{ 'role': "SGT Smith", 'loadout': 'rifleman_det5', 'medic': 1, },
			{ 'role': "SSG Bayley", 'loadout': 'commo_det5', 'medic': 1, },
			{ 'role': "SGT Griffin", 'loadout': 'medic_det5_1tk', 'medic': 1, },
			{ 'role': "SFC Knezevic", 'loadout': 'rifleman_det5', 'medic': 1, },
			{ 'role': "SGT Shearer", 'loadout': 'commo_det5', 'medic': 1, },
		]
	],
)

teams['soar'] = dict(
	spawn = 'cdn',
	name = 'USAF',
	side = 'WEST',
	faction = 'cdn',
	groups = [
		[
			{ 'role': "Pilot", 'loadout': 'soar_pilot', 'callsign': 'RAPTOR',},
			{ 'role': "Pilot", 'loadout': 'soar_pilot', },
			{ 'role': "Pilot", 'loadout': 'soar_pilot', },
			{ 'role': "Pilot", 'loadout': 'soar_pilot', },
			{ 'role': "Pilot", 'loadout': 'soar_pilot', },
			{ 'role': "Pilot", 'loadout': 'soar_pilot', },
			{ 'role': "Pilot", 'loadout': 'soar_pilot', },
			{ 'role': "Pilot", 'loadout': 'soar_pilot', },
			{ 'role': "Crew Chief", 'loadout': 'soar_crew', },
			{ 'role': "Crew Chief", 'loadout': 'soar_crew', },
			{ 'role': "Crew Chief", 'loadout': 'soar_crew', },
			{ 'role': "Crew Chief", 'loadout': 'soar_crew', },
			{ 'role': "Crew Chief", 'loadout': 'soar_crew', },
			{ 'role': "Crew Chief", 'loadout': 'soar_crew', },
		],
	],
)

teams['company_hq'] = dict(
	spawn = 'marines',
	name = 'A CO',
	side = 'WEST',
	faction = 'marines',
	groups = [
		[
			{ 'role': "Company Commander", 'loadout': 'marine_pl', 'callsign': 'MUSTANG 6', },
			{ 'role': "Executive Officer", 'loadout': 'marine_pl', 'callsign': 'MUSTANG 7', },
			{ 'role': "First Sergeant", 'loadout': 'marine_pl', },
			{ 'role': "Gunnery Sergeant", 'loadout': 'marine_pl', },
		],
	]
)
teams['rifles'] = dict(
	spawn = 'marines',
	name = '1ST PLATOON',
	side = 'WEST',
	faction = 'marines',
	groups = [
		# rifles plt hq
		[
			{ 'role': "Platoon Leader", 'loadout': 'marine_pl', 'callsign': 'MUSTANG 1-6', },
			{ 'role': "Platoon Sergeant", 'loadout': 'marine_pl', 'callsign': 'MUSTANG 1-7', },
			{ 'role': "Platoon Guide", 'loadout': 'marine_rto', },
			{ 'role': "Corpsmen", 'loadout': 'marine_corpsman', 'medic': 1},
			{ 'role': "Corpsmen", 'loadout': 'marine_corpsman', 'medic': 1},			
		],
		# rifles squad 1
	],
)

for i in range(1,2):
	teams['rifles']['groups'].append([
		{ 'role': "Squad Leader", 'loadout': 'marine_sl', 'callsign': 'MUSTANG 1-%d' % i },
		
		{ 'role': "Team Leader", 'loadout': 'marine_tl', 'callsign': 'MUSTANG 1-%d-A' % i },
		{ 'role': "Automatic Rifleman", 'loadout': 'marine_ar' },
		{ 'role': "Assistant AR", 'loadout': 'marine_aar' },
		{ 'role': "Rifleman", 'loadout': 'marine_rifleman' },
		
		{ 'role': "Team Leader", 'loadout': 'marine_tl', 'callsign': 'MUSTANG 1-%d-B' % i },
		{ 'role': "Automatic Rifleman", 'loadout': 'marine_ar' },
		{ 'role': "Assistant AR", 'loadout': 'marine_aar' },
		{ 'role': "Rifleman", 'loadout': 'marine_rifleman' },
		
		{ 'role': "Team Leader", 'loadout': 'marine_tl', 'callsign': 'MUSTANG 1-%d-C' % i },
		{ 'role': "Automatic Rifleman", 'loadout': 'marine_ar' },
		{ 'role': "Assistant AR", 'loadout': 'marine_aar' },
		{ 'role': "Rifleman", 'loadout': 'marine_rifleman' },
	])

teams['ukbaf'] = dict(
	spawn = 'ukbaf',
	name = 'Wpns Plt.',
	side = 'WEST',
	faction = 'ukbaf',
	groups = [
		# ukbaf hq
		[
			{ 'role': "Troop Commander", 'loadout': 'ukbaf_sl', 'callsign': 'HIGHLANDER 1-6', },
			{ 'role': "Troop Sergeant", 'loadout': 'ukbaf_sl', 'callsign': 'HIGHLANDER 1-7', },
			{ 'role': "Combat Medic", 'loadout': 'ukbaf_combatmedic', 'medic': 1},
			{ 'role': "Combat Medic", 'loadout': 'ukbaf_combatmedic', 'medic': 1},
		],
	],
)

for i in range(1,3):
	teams['ukbaf']['groups'].append([
		{ 'role': "Section Commander", 'loadout': 'ukbaf_tl', 'callsign': 'HIGHLANDER 1-%d' % i, },
		
		{ 'role': "Lead Scout Observer", 'loadout': 'ukbaf_leadscout', 'callsign': 'HIGHLANDER 1-%d-G' % i },
		{ 'role': "Gunner", 'loadout': 'ukbaf_gunner' },
		{ 'role': "Driver/Radio Operator", 'loadout': 'ukbaf_signaller' },
		{ 'role': "Scout Observer", 'loadout': 'ukbaf_longrange' },
	])

	
teams['ACR'] = dict(
	spawn = 'acr',
	name = 'ARMORED PLATOON.',
	side = 'WEST',
	faction = 'usarmy',
	groups = [		
		# tank platoon
		[
			{ 'role': "M1A1 Platoon Leader", 'loadout': 'acr_commander' },
			{ 'role': "Driver", 'loadout': 'acr_crewman' },
			{ 'role': "Gunner", 'loadout': 'acr_crewman' },
			{ 'role': "Loader", 'loadout': 'acr_crewman' },
		],
		[
			{ 'role': "M1A1 Platoon Sergeant", 'loadout': 'acr_commander' },
			{ 'role': "Driver", 'loadout': 'acr_crewman' },
			{ 'role': "Gunner", 'loadout': 'acr_crewman' },
			{ 'role': "Loader", 'loadout': 'acr_crewman' },
		],
	],
)

teams['SGPF'] = dict(
	spawn = 'ana',
	name = 'ANA',
	faction = 'ana',
	side = 'WEST',
	groups = [
		# pubbie hq
		[
			{ 'role': "Platoon Leader", 'loadout': 'cdf_pl', 'callsign': 'HOMELAND 1-6', },
			{ 'role': "Assistant Platoon Leader", 'loadout': 'cdf_rto', 'callsign': 'HOMELAND 1-7', },
		],
		[
			{ 'name': '3ACR', 'role': "SL / BMP-1 Commander", 'loadout': 'cdf_asl_gunner', 'callsign': 'THUNDER 1-1'},
			{ 'name': '3ACR', 'role': "BMP-1 Driver", 'loadout': 'cdf_crew', },
			{ 'name': '3ACR', 'role': "BMP-1 Gunner", 'loadout': 'cdf_asl_gunner', },
			{ 'role': "Senior Rifleman", 'loadout': 'cdf_tl', 'callsign': 'HOMELAND 1-1'},
			{ 'role': "Machine Gunner", 'loadout': 'cdf_mg', },
			{ 'role': "Medic", 'loadout': 'cdf_medic', 'medic': 1},
			{ 'role': "Grenadier", 'loadout': 'cdf_grenadier' },
			{ 'role': "Asst. Grenadier", 'loadout': 'cdf_grenadier' },
			{ 'role': "Rifleman", 'loadout': 'cdf_rifleman' },
		],
		[
			{ 'name': '3ACR', 'role': "SL / BMP-1 Commander", 'loadout': 'cdf_asl_gunner', 'callsign': 'THUNDER 1-2'},
			{ 'name': '3ACR', 'role': "BMP-1 Driver", 'loadout': 'cdf_crew', },
			{ 'name': '3ACR', 'role': "BMP-1 Gunner", 'loadout': 'cdf_asl_gunner', },
			{ 'role': "Senior Rifleman", 'loadout': 'cdf_tl', 'callsign': 'HOMELAND 1-2'},
			{ 'role': "Machine Gunner", 'loadout': 'cdf_mg', },
			{ 'role': "Medic", 'loadout': 'cdf_medic', 'medic': 1},
			{ 'role': "Grenadier", 'loadout': 'cdf_grenadier' },
			{ 'role': "Asst. Grenadier", 'loadout': 'cdf_grenadier' },
			{ 'role': "Rifleman", 'loadout': 'cdf_rifleman' },
		],
		[
			{ 'name': '3ACR', 'role': "SL / BMP-1 Commander", 'loadout': 'cdf_asl_gunner', 'callsign': 'THUNDER 1-3'},
			{ 'name': '3ACR', 'role': "BMP-1 Driver", 'loadout': 'cdf_crew', },
			{ 'name': '3ACR', 'role': "BMP-1 Gunner", 'loadout': 'cdf_asl_gunner', },
			{ 'role': "Senior Rifleman", 'loadout': 'cdf_tl', 'callsign': 'HOMELAND 1-3'},
			{ 'role': "Machine Gunner", 'loadout': 'cdf_mg', },
			{ 'role': "Medic", 'loadout': 'cdf_medic', 'medic': 1},
			{ 'role': "Grenadier", 'loadout': 'cdf_grenadier' },
			{ 'role': "Asst. Grenadier", 'loadout': 'cdf_grenadier' },
			{ 'role': "Rifleman", 'loadout': 'cdf_rifleman' },
		],
		[
			{ 'name': '3ACR', 'role': "SL / BMP-1 Commander", 'loadout': 'cdf_asl_gunner', 'callsign': 'THUNDER 1-4'},
			{ 'name': '3ACR', 'role': "BMP-1 Driver", 'loadout': 'cdf_crew', },
			{ 'name': '3ACR', 'role': "BMP-1 Gunner", 'loadout': 'cdf_asl_gunner', },
			{ 'role': "Senior Rifleman", 'loadout': 'cdf_tl', 'callsign': 'HOMELAND 1-4'},
			{ 'role': "Machine Gunner", 'loadout': 'cdf_mg', },
			{ 'role': "Medic", 'loadout': 'cdf_medic', 'medic': 1},
			{ 'role': "Grenadier", 'loadout': 'cdf_grenadier' },
			{ 'role': "Asst. Grenadier", 'loadout': 'cdf_grenadier' },
			{ 'role': "Rifleman", 'loadout': 'cdf_rifleman' },
		],
		[
			{ 'name': '3ACR', 'role': "T-72 Commander", 'loadout': 'cdf_asl_gunner', 'callsign': 'THUNDER 2-1' },
			{ 'name': '3ACR', 'role': "Driver", 'loadout': 'cdf_crew' },
			{ 'name': '3ACR', 'role': "Gunner", 'loadout': 'cdf_crew' },
		],	
	]
)

mish = Reader(os.path.join(cfg.mish,'mission.sqm')).read()
top_id = id_count = mish.nextid()
g_count = mish('Mission')('Groups')['items']

fh = open('slots.txt', 'w')

kys = ['SGPF','ACR','ukbaf','company_hq','rifles','soar','det5','sfqc']

for team in kys:
	for grp in teams[team]['groups']:
		for unit in grp:
			s =  "%s | %s" % (teams[team]['name'], unit['role'])
			if 'callsign' in unit:
				s += " // %s" % (unit['callsign'])
			fh.write(s+"\n")
		fh.write("\n")

for team in kys:
	for grp in teams[team]['groups']:
		
		g = Klass('Item' + str(g_count))
		g['side'] = teams[team]['side']
		
		v = Klass('Vehicles')
		v_count = 0
		for unit in grp:
			u = Klass('Item' + str(v_count))
			
			spwn = spawns[teams[team]['spawn']]
			if spwn['limit'] == 'x':
				pos = spwn['pos'] + (spwn['unit'] * int(spwn['count']/spwn['max'])) + (spwn['unit'].perp() * int(spwn['count'] % spwn['max']))
			else:
				pos = spwn['pos'] + (spwn['unit'].perp() * int(spwn['count']/spwn['max'])) + (spwn['unit'] * int(spwn['count'] % spwn['max']))
			spwn['count'] += 1
			u['position'] = [pos.x, 0, pos.y]
			u['azimut'] = spwn['azimuth']
			u['id'] = id_count
			u['side'] = teams[team]['side']
			u['vehicle'] = 'sh_faction_%s_unit' % teams[team]['faction']

			if id_count == top_id:
				u['player'] = 'PLAYER COMMANDER'
			else:
				u['player'] = 'PLAY CDG'
			u['skill'] = 0.60000002
			u['text'] = "%s_%d_%d" % (team, g_count, v_count)
			t = teams[team]['name']
			if 'name' in unit:
				t = unit['name']
			u['description'] = "%s // %s" % (t, unit['role'])
			if 'callsign' in unit:
				u['description'] += " // %s" % (unit['callsign'])

			#u['init'] = "this setVariable ['sux_loadout', '%s'];" % unit['loadout']
			u['init'] = '[this, "%s"] call suxlo_fnc_init_loadout;' % unit['loadout']

			if 'medic' in unit:
				u['init'] += "[this] call kh_fnc_make_medic;"
			id_count += 1
			v_count += 1
			v['items'] = v_count
			v(u)
		g(v)
		g_count += 1
		mish('Mission')('Groups')['items'] = g_count
		mish('Mission')('Groups')(g)

Writer(os.path.join(cfg.mish,'mission.sqm')).write(mish)

