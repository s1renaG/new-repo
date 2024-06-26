import unittest
from unittest.mock import patch, mock_open, MagicMock, call
from json_demo_parser import JsonDemoParser


class TestJsonDemoParser(unittest.TestCase):

    @patch('json_demo_parser.DemoParser')
    @patch('json_demo_parser.os.path.splitext')
    @patch('json_demo_parser.os.path.basename')
    @patch('json_demo_parser.os.path.join')
    @patch('json_demo_parser.open', new_callable=mock_open)
    def test_dem_to_json(self, mock_open, mock_path_join, mock_path_basename, mock_path_splitext, MockDemoParser):
        # Setup
        mock_path_basename.return_value = 'demo.dem'
        mock_path_splitext.return_value = ('demo', '.dem')
        mock_path_join.return_value = '/fake/path/demo.json'

        mock_parser_instance = MockDemoParser.return_value
        mock_event_df = MagicMock()
        mock_event_df.to_dict.return_value = [{'event': 'data'}]
        mock_parser_instance.parse_event.return_value = mock_event_df

        parser = JsonDemoParser('/fake/path')
        demo_path = '/fake/path/demo.dem'

        # Act
        parser.dem_to_json(demo_path)

        # Assert
        mock_parser_instance.parse_event.assert_called_once_with(
            "player_death", player=["X", "Y", "last_place_name", "team_name"],
            other=["total_rounds_played", "game_time", "round_start_time"]
        )
        mock_event_df.to_dict.assert_called_once_with(orient='records')
        mock_open.assert_called_once_with('/fake/path/demo.json', 'w')

        handle = mock_open()
        handle.write.assert_has_calls([
            call('{'),
            call('\n    '),
            call('"events"'),
            call(': '),
            call('[\n        '),
            call('{'),
            call('\n            '),
            call('"event"'),
            call(': '),
            call('"data"'),
            call('\n        '),
            call('}'),
            call('\n    '),
            call(']'),
            call('\n'),
            call('}')
        ])

    @patch('json_demo_parser.os.listdir')
    @patch('json_demo_parser.os.path.join')
    def test_process_demos_folder(self, mock_path_join, mock_listdir):
        # Setup
        mock_listdir.return_value = ['file1.dem', 'file2.txt', 'file3.dem']
        mock_path_join.side_effect = lambda folder, file: f"{folder}/{file}"

        parser = JsonDemoParser('/fake/path')

        # Act
        with patch.object(parser, 'dem_to_json') as mock_dem_to_json:
            parser.process_demos_folder()

        # Assert
        mock_dem_to_json.assert_any_call('/fake/path/file1.dem')
        mock_dem_to_json.assert_any_call('/fake/path/file3.dem')
        self.assertEqual(mock_dem_to_json.call_count, 2)


if __name__ == '__main__':
    unittest.main()
