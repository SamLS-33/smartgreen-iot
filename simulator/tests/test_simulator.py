import unittest

from simulator import SmartGreenSimulator, load_config


class TestSmartGreen(unittest.TestCase):

    def setUp(self):
        self.c = load_config("config.json")

    def test_ranges(self):
        """Las variables deben mantenerse dentro de sus rangos."""
        simulator = SmartGreenSimulator(self.c)

        for _ in range(100):
            measurements = simulator.generate()["measurements"]

            self.assertTrue(
                0 <= measurements["soil_moisture"] <= 100
            )
            self.assertTrue(
                10 <= measurements["temperature"] <= 45
            )
            self.assertGreaterEqual(
                measurements["water_level"], 0
            )

    def test_unique_ids(self):
        """Cada mensaje debe tener un message_id diferente."""
        simulator = SmartGreenSimulator(self.c)

        message_1 = simulator.generate()
        message_2 = simulator.generate()

        self.assertNotEqual(
            message_1["message_id"],
            message_2["message_id"]
        )

    def test_irrigation_coherence(self):
        """El riego debe aumentar humedad y disminuir agua."""
        config = dict(self.c)
        config["soil_moisture_initial"] = 10
        config["water_level_initial"] = 20

        simulator = SmartGreenSimulator(config)

        before_soil = simulator.soil
        before_water = simulator.water

        message = simulator.generate()
        measurements = message["measurements"]

        self.assertTrue(measurements["irrigation_active"])
        self.assertGreater(simulator.soil, before_soil)
        self.assertLess(simulator.water, before_water)

    def test_no_irrigation_without_enough_water(self):
        """No debe activarse el riego cuando no hay agua suficiente."""
        config = dict(self.c)
        config["soil_moisture_initial"] = 10
        config["water_level_initial"] = 5

        simulator = SmartGreenSimulator(config)
        message = simulator.generate()
        measurements = message["measurements"]

        self.assertFalse(
            measurements["irrigation_active"]
        )

    def test_irrigation_flag_matches_state(self):
        """Detecta una combinación incoherente entre riego y estado del agua."""
        config = dict(self.c)
        config["soil_moisture_initial"] = 10
        config["water_level_initial"] = 20

        simulator = SmartGreenSimulator(config)
        message = simulator.generate()
        measurements = message["measurements"]

        if measurements["irrigation_active"]:
            self.assertLess(
                measurements["water_level"],
                config["water_level_initial"]
            )
            self.assertGreater(
                measurements["soil_moisture"],
                config["soil_moisture_initial"]
            )


if __name__ == "__main__":
    unittest.main()
