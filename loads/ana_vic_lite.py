from p4a.loadout import Crate

class cdf_vic_lite(Crate):
	vehicle = True
	def __init__(self):
		super(cdf_vic_lite, self).__init__()
		self.remove('all')	
	weapons = [
		['CSE_FlareWhite', 2],
		['CSE_FlareRed', 2],
	]
	magazines = [
		['CSE_FlareWhite', 2],
		['CSE_FlareRed', 2],
		['rhs_mag_30Rnd_556x45_Mk318_Stanag', 5],
		['rhs_mag_30Rnd_556x45_M855A1_Stanag_Tracer_Red', 5],
		['rhsusf_100Rnd_556x45_soft_pouch', 2],
		['rhs_mag_an_m8hc', 2],
		['rhs_mag_m18_red', 2],
		['rhs_mag_m67', 4],
	]
	items = [
		['cse_bandage_basic', 10],
		['cse_bandageElastic', 5],
		['cse_morphine', 2],
		['cse_epinephrine', 2],
		['cse_saline_iv', 1],
		['cse_saline_iv_500', 2],
		['cse_saline_iv_250', 2],
		['cse_tourniquet', 2],	
	]