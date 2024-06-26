from demoparser2 import DemoParser
import json
import os


class JsonDemoParser:

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def dem_to_json(self, demo_path):
        parser = DemoParser(demo_path)

        event_df = parser.parse_event("player_death", player=["X", "Y", "last_place_name", "team_name"],
                                      other=["total_rounds_played", "game_time", "round_start_time"])
        event_df["player_died_time"] = event_df["game_time"] - event_df["round_start_time"]

        event_dict = event_df.to_dict(orient='records')

        data = {
            "events": event_dict,
        }

        json_filename = os.path.splitext(os.path.basename(demo_path))[0] + ".json"
        json_filepath = os.path.join(self.folder_path, json_filename)

        with open(json_filepath, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f'Data has been printed to {json_filepath}')

    def process_demos_folder(self):
        files = os.listdir(self.folder_path)
        demo_files = [file for file in files if file.endswith('.dem')]

        for demo_file in demo_files:
            demo_path = os.path.join(self.folder_path, demo_file)
            self.dem_to_json(demo_path)
