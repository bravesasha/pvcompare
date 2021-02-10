import pvcompare.outputs as outputs
import pvcompare.constants as constants
import pvcompare.main as main
import os
import pandas as pd


class Scenarios:
    @classmethod
    def setup_class(self):
        # DEFINE USER INPUTS
        # For scenarios in germany
        self.latitude_germany = 52.5243700
        self.longitude_germany = 13.4105300
        self.years_germany = [
            2011,
            2013,
            2016,
        ]  # 2011 (good), 2013 (bad), 2016 (medium)
        self.country_germany = "Germany"

        # For scenarios in spain

        self.latitude_spain = 40.416775
        self.longitude_spain = -3.703790
        self.years_spain = [2013, 2015, 2017]  # 2017 (good), 2013 (bad), 2015 (medium)
        self.country_spain = "Spain"

        # general parameters
        self.storeys = 5
        self.user_inputs_pvcompare_directory = (
            constants.DEFAULT_USER_INPUTS_PVCOMPARE_DIRECTORY
        )

    def run_scenario_a1(self):
        """

        :return:
        """

        scenario_name = "Scenario_A1"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "psi"
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_mvs(
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            variable_name="lifetime",
            variable_column="PV psi",
            csv_file_variable="energyProduction.csv",
            start=5,
            stop=20,
            step=1,
            outputs_directory=None,
            user_inputs_mvs_directory=None,
            scenario_name=scenario_name,
        )

    def run_scenario_a2(self):
        """

        :return:
        """

        scenario_name = "Scenario_A2"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "psi"
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_mvs(
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            variable_name="lifetime",
            variable_column="PV psi",
            csv_file_variable="energyProduction.csv",
            start=5,
            stop=20,
            step=1,
            outputs_directory=None,
            user_inputs_mvs_directory=None,
            scenario_name=scenario_name,
        )

    def run_scenario_a3(self):
        """

        :return:
        """

        scenario_name = "Scenario_A3"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "psi"
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_mvs(
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            variable_name="specific_costs",
            variable_column="PV psi",
            csv_file_variable="energyProduction.csv",
            start=500,
            stop=1300,
            step=50,
            outputs_directory=None,
            user_inputs_mvs_directory=None,
            scenario_name=scenario_name,
        )

    def run_scenario_a4(self):
        """

        :return:
        """

        scenario_name = "Scenario_A4"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "psi"
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_mvs(
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            variable_name="specific_costs",
            variable_column="PV psi",
            csv_file_variable="energyProduction.csv",
            start=500,
            stop=1300,
            step=50,
            outputs_directory=None,
            user_inputs_mvs_directory=None,
            scenario_name=scenario_name,
        )

    def run_scenario_a5(self):
        """

        :return:
        """

        scenario_name = "Scenario_A5"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "cpv"
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_mvs(
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            variable_name="specific_costs",
            variable_column="PV psi",
            csv_file_variable="energyProduction.csv",
            start=700,
            stop=1500,
            step=50,
            outputs_directory=None,
            user_inputs_mvs_directory=None,
            scenario_name=scenario_name,
        )

    def run_scenario_a6(self):
        """

        :return:
        """

        scenario_name = "Scenario_A6"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "cpv"
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_mvs(
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            variable_name="specific_costs",
            variable_column="PV psi",
            csv_file_variable="energyProduction.csv",
            start=700,
            stop=1500,
            step=50,
            outputs_directory=None,
            user_inputs_mvs_directory=None,
            scenario_name=scenario_name,
        )

    def run_scenario_a7(self):
        """

        :return:
        """

        scenario_name = "Scenario_A7"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_germany,
            longitude=self.longitude_germany,
            years=self.years_germany,
            storeys=self.storeys,
            country=self.country_germany,
            loop_type="technology",
            loop_dict={"step1": "si"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )

    def run_scenario_a8(self):
        """

        :return:
        """

        scenario_name = "Scenario_A8"
        data_path = os.path.join(self.user_inputs_pvcompare_directory, "pv_setup.csv")
        # load input parameters from pv_setup.csv
        pv_setup = pd.read_csv(data_path)
        pv_setup.at[0, "technology"] = "si"
        pv_setup.to_csv(data_path, index=False)

        outputs.loop_pvcompare(
            scenario_name=scenario_name,
            latitude=self.latitude_spain,
            longitude=self.longitude_spain,
            years=self.years_spain,
            storeys=self.storeys,
            country=self.country_spain,
            loop_type="technology",
            loop_dict={"step1": "si"},
            user_inputs_mvs_directory=None,
            outputs_directory=None,
            user_inputs_pvcompare_directory=None,
        )


if __name__ == "__main__":

    scenarios = Scenarios()
    scenarios.setup_class()
    scenarios.run_scenario_a1()