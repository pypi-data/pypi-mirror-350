import os
import unittest

from midas_store import simulator


class TestMidasCSV(unittest.TestCase):
    def setUp(self):
        self.inputs1 = {
            "Database-0": {
                "p_mw": {
                    "DummySim-0.DummyHousehold-0": 0.1,
                    "DummySim-0.DummyHousehold-1": 0.2,
                    "DummySim-1.DummyPV-0": 0.3,
                },
                "q_mvar": {
                    "DummySim-0.DummyHousehold-0": 0.01,
                    "DummySim-0.DummyHousehold-1": 0.02,
                    "DummySim-1.DummyPV-0": 0.03,
                },
                "t_air": {"DummyWeather-0.WeatherCurrent-0": 15.0},
                "schedule": {"DummySim-2.DummyCHP-0": [10, 12, 10]},
            }
        }
        self.inputs2 = {
            "Database-0": {
                "p_mw": {
                    "DummySim-0.DummyHousehold-0": 0.02,
                    "DummySim-0.DummyHousehold-1": 0.02,
                    "DummySim-1.DummyPV-0": 0.03,
                    "DummySim-2.DummyCHP-0": 0.5,
                },
                "q_mvar": {
                    "DummySim-0.DummyHousehold-0": 0.01,
                    "DummySim-0.DummyHousehold-1": 0.015,
                    "DummySim-1.DummyPV-0": 0.01,
                },
                "t_air": {"DummyWeather-0.WeatherCurrent-0": 15.0},
                "wind": {"DummyWeather-1.WeatherForecast-0": 20},
            }
        }

    def test_setup(self):
        """Test store creation and ensure to allow only one instance."""
        dbsim = simulator.MidasCSVStore()

        dbsim.init("MidasCSVStore", step_size=900)

        # Only one instance allowed
        with self.assertRaises(ValueError):
            dbsim.create(2, "DatabaseCSV", filename="there.csv")

        dbsim.create(1, "DatabaseCSV", filename="here.csv")

        self.assertIsNotNone(dbsim.database)
        if dbsim.database is not None:
            self.assertIn("here.csv", dbsim.database.filename)
        self.assertEqual(900, dbsim.step_size)

        # Only one instance allowed
        with self.assertRaises(ValueError):
            dbsim.create(1, "DatabaseCSV", filename="there.csv")

    def test_step(self):
        dbsim = simulator.MidasCSVStore()
        dbsim.init("MidasCSVStore", step_size=900)
        dbsim.create(1, "DatabaseCSV", filename="here.csv")
        dbsim.step(0, self.inputs1)

        with self.assertLogs("midas_store.csv_model", level="ERROR") as cm:
            dbsim.step(900, self.inputs2)
            dbsim.finalize()
        self.assertIn("dict contains fields not in fieldnames", cm.output[0])

    def test_step_no_inputs(self):
        dbfile = "not-there.csv"
        dbsim = simulator.MidasCSVStore()
        dbsim.init("MidasCSVStore", step_size=900)
        dbsim.create(1, "DatabaseCSV", filename=dbfile)
        dbsim.step(0, {})
        dbsim.finalize()
        self.assertFalse(os.path.exists(dbfile))

    def test_huge_dataset(self):
        """Test if a large dataset can be stored. Takes very long
        and should not be necessary most of the time.
        """
        dbsim = simulator.MidasCSVStore()
        dbsim.init("MidasCSVStore", step_size=900)
        dbsim.create(1, "DatabaseCSV", filename="this_is_huge.csv")

        for idx in range(5 * 365 * 24 * 4):
            dbsim.step(idx * 900, self.inputs1)

            if idx % 96 == 0:
                print(idx / 96, end="\r")

        print()
        dbsim.finalize()


if __name__ == "__main__":
    unittest.main()
