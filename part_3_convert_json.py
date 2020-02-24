import cc_classes as ccc
import cc_dat_utils as ccdu
import json

#Part 3

#Load your custom JSON file
def read_level_pack_json(json_file):
	with open(json_file, "r") as reader:
		json_data = json.load(reader)
	return json_data

#Convert JSON data to CCLevelPack
def convert_json_to_level_pack(json_data):
	
	level_pack = ccc.CCLevelPack()
	for level_json in json_data["levels"]:
		level = convert_json_to_level(level_json)
		level_pack.add_level(level)
	
	return level_pack

#Convert JSON data for a level to CCLevel
def convert_json_to_level(level_json):
	level = ccc.CCLevel()
	
	print(level_json)
	level.level_number = level_json["level_number"]
	level.time = level_json["time"]
	level.num_chips = level_json["num_chips"]
	level.upper_layer = level_json["upper_layer"]
	level.lower_layer = level_json["lower_layer"]
	
	# Iterate over all optional fields and create appropriate CCFields.
	for field_json in level_json["optional_fields"]:
	
		# Title field
		if field_json["type_val"] == 3:
			field = ccc.CCMapTitleField(field_json["value"])
			
		# Trap control field
		elif field_json["type_val"] == 4:
			traps = []
			# Iterate over the list of trap coordinates...
			for coords in field_json["value"]:
				traps.append(CCTrapControl(coords[0], coords[1], coords[2], coords[3]))
			# then add them to the field.
			traps = ccc.CCTrapControlsField(traps)
			
		# Cloning machine field
		elif field_json["type_val"] == 5:
			machines = []
			# Iterate over the list of machine coordinates...
			for coords in field_json["value"]:
				machines.append(CCCloningMachineControl(coords[0], coords[1], coords[2], coords[3]))
			# then add them to the field.
			machines = ccc.CCCloningMachineControlsField(traps)
			
		# Encoded password field
		elif field_json["type_val"] == 6:
			field = ccc.CCEncodedPasswordField(field_json["value"])
			
		# Map hint field
		elif field_json["type_val"] == 7:
			field = ccc.CCMapHintField(field_json["value"])
			
		# Monster movement field
		elif field_json["type_val"] == 10:
			monsters = []
			# Iterate over the list of monster coordinates...
			for coords in field_json["value"]:
				monsters.append(CCCoordinate(coords[0], coords[1]))
			# then add them to the field.
			field = ccc.CCMonsterMovementField(monsters)
		
		# Failing all else, a generic field.
		else:
			field = ccc.CCField(field_json["type_val"], field_json["value"])
		
		level.optional_fields.append(field)
	
	return level
	

def convert_level(filepath):
	print("Reading JSON data...")
	json_data = read_level_pack_json(filepath)
	print(json_data)
	
	print("Converting JSON data to level pack...")
	level_pack = convert_json_to_level_pack(json_data)
	print(level_pack)
	
	dat_filepath = filepath.replace(".json", ".dat")
	print("Writing level pack to", dat_filepath)
	ccdu.write_cc_level_pack_to_dat(level_pack, dat_filepath)
	
	print("Writing .dac file...")
	with open(filepath.replace(".json", ".dac"), "w") as dacfile:
		dacfile.write("file=" + dat_filepath.split("/")[-1] + "\nruleset=ms\n")
		
	print("Done.")

def main():
	convert_level("data/test_level.json")
	#cc_level_pack = ccdu.make_cc_level_pack_from_dat("data/pfgd_test.dat")
	#ccdu.write_cc_level_pack_to_dat(cc_level_pack, "data/TEST.dat")

main()