import json



def write( symbol):
	"""
	SAVE LISTING INTO LOCAL JSON FILE
	"""
	with open("log.txt", 'a', encoding="utf-16") as f:
		f.write(symbol + "\n")

def load_errors(file):	

	"""
	UPDATE JSON FILE
	"""
	with open(file, "r+") as f:
		return json.load(f)