import test_data
import json

#Creates and returns a GameLibrary object(defined in test_data) 
#from loaded json_data
def make_game_library_from_json( json_data ):
    #Initialize a new GameLibrary
    game_library = test_data.GameLibrary()
    
    ### Begin Add Code Here ###
    #Loop through the json_data
    for g in json_data["games"]:
        #Create a new Game object from the json_data by reading
        #  title
        #  year
        #  platform (which requires reading name and launch_year)
        platform = test_data.Platform(name=g["platform"]["name"], 
                                      launch_year=g["platform"]["launch_year"])
        game = test_data.Game(title=g["title"], platform=platform, 
                              year=g["year"])
        #Add that Game object to the game_library
        game_library.add_game(game)
    ### End Add Code Here ###
    
    return game_library


#Part 2
input_json_file = "data/test_data.json"

### Begin Add Code Here ###
#Open the file specified by input_json_file
with open(input_json_file, "r") as reader:
    #Use the json module to load the data from the file
    test_json_data = json.load(reader)

#Use make_game_library_from_json(json_data) to convert the data 
#to GameLibrary data
library = make_game_library_from_json(test_json_data)

#Print out the resulting GameLibrary data using print()
print(library)
