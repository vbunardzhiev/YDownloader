import re
def get_volume_level(string):
	first_match = re.findall('max_volume: ' + r'.+' , string)[0]
	return float(re.findall(r'-?[0-9]{1,3}[.][0-9]{1}', first_match)[0])