import unittest
from pathlib import Path

from src.wrath_and_glory_space_hulk_generator.random_table import RandomTable
from src.wrath_and_glory_space_hulk_generator.sequenced_die import SequencedDie


class TestRandomTable(unittest.TestCase):

    def test_read_all_tables_in_folder_expect_all_dice_to_be_correct(self):
        d6 = SequencedDie(sides=6, number_of_dice=1)
        d66 = SequencedDie(sides=6, number_of_dice=2)
        table_die_map = {"Occupations": d66,
                         "Hazards": d6,
                         "Purposes": d66,
                         "Rooms": d66,
                         "Origins": d66}
        for table_file in Path("../src/wrath_and_glory_space_hulk_generator/assets/").glob("table_*.json"):
            with self.subTest(i=table_file.name):
                table = RandomTable.parse_file(table_file)
                self.assertEqual(table._die, table_die_map[table.table_name])


if __name__ == '__main__':
    unittest.main()
