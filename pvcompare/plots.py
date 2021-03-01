from pvcompare import check_inputs
import pvcompare.main as main
import pvcompare.constants as constants
import os
import pandas as pd
import shutil
import glob
import matplotlib.pyplot as plt
import logging
import numpy as np
import seaborn as sns

sns.set()


def plot_all_flows(
    scenario_name=None,
    outputs_directory=None,
    timeseries_directory=None,
    timeseries_name="timeseries_all_busses.xlsx",
    month=None,
    calendar_week=None,
    weekday=None,
):

    """
    Plots all flows of the energy system for a given period of time.

    Parameters
    ----------
    scenario_name: str
        Name of the Scenario. The name should follow the scheme:
        "Scenario_A1", "Scenario_A2", "Scenario_B1" etc.
    outputs_directory: str or None
        Path to the directory in which the plot should be saved.
        Default: None.
        If None: `outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY`
    timeseries_directory: str or None
        Path to the timeseries directory.
        If None: `timeseries_directory = outputs_directory`.
        Default: None.
    timeseries_name: str or None
        Default: timeseries_all_busses.xlsx
    month: int
        Number of month that should be plotted.
        Only fill in a number here, if you want to plot over one month.
        If None: will plot over week, weekday or the whole year. Default: None
    calendar_week: int
        the week (number in calender weeks) that should be plotted.
        Only fill in a number here, if you want to plot over one a week or a weekday.
        if None: will plot over one month or the whole year. Default: None
    weekday: int
        The day of the caldendar_week (from 0-6 with 0 : Monday and 6: Sunday.
        If None: the next greater period is plotted. Default: None

    Returns
    -------
        None
        Saves figure into outputs_directory
    -------


    """
    # check if weekday is a valid day
    if weekday not in range(0, 6, 1):
        logging.error(
            "The weekday is not valid. Please choose a number "
            "between 0-6 with 0:Monaday and 6:Sunday."
        )

    # read timeseries
    # check if scenario is specified or the timeseries directory is given
    if timeseries_directory is None:
        if outputs_directory == None:
            outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY
        scenario_folder = os.path.join(outputs_directory, scenario_name)
        if timeseries_directory == None:
            timeseries_directory = os.path.join(scenario_folder, "mvs_outputs")
        if not os.path.isdir(timeseries_directory):
            logging.warning(
                "The timeseries directory does not exist. Please check "
                "the scenario name or specify the timeseries directory."
            )
    df = pd.read_excel(
        os.path.join(timeseries_directory, timeseries_name),
        sheet_name="Electricity bus",
        index_col=0,
    )
    # Converting the index as date
    df.index = pd.to_datetime(df.index)

    # define period for the plot
    if month is None:
        if calendar_week is None:
            period = "year"
            pass
            if weekday is not None:
                logging.error(
                    "If you want to create a plot over one weekday, please "
                    "define a caldendar_week as well. Otherwise set"
                    " weekday to 'None'."
                )
        else:
            if weekday is not None:
                df = df[df.index.week == calendar_week]
                df = df[df.index.weekday == weekday]
                period = "day_" + str(calendar_week) + "_" + str(weekday)
            else:
                df = df[df.index.week == calendar_week]
                period = "caldendar_week_" + str(calendar_week)
    else:
        if calendar_week is not None:
            if weekday is None:
                logging.warning(
                    "You inserted a month and a week. In this case the "
                    "plot will cover one caldendar_week. If you want to plot "
                    "over one month please set the calendar_week to 'None'"
                )
                df = df[df.index.week == calendar_week]
                period = "week_" + str(calendar_week)
            else:
                logging.warning(
                    "You inserted a month, a caldendar_week and a weekday. In this case the "
                    "plot will cover one weekday only. If you want to plot "
                    "over one month please set the caldendar_week and weekday to 'None'"
                )
                df = df[df.index.week == calendar_week]
                df = df[df.index.weekday == weekday]
                period = "day_" + str(calendar_week) + "_" + str(weekday)
        else:
            df = df[df.index.month == month]
            period = "month_" + str(month)

    # plot
    plt.title("All Flows", color="black")
    df.plot().legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.0)
    plt.xlabel("time")
    plt.ylabel("kW")

    # save plot into output directory
    plt.savefig(
        os.path.join(timeseries_directory, f"plot_{timeseries_name[:-5]}_{period}.png"),
        bbox_inches="tight",
    )


def plot_kpi_loop(
    variable_name, kpi, scenario_dict, outputs_directory=None,
):

    """
    Plots KPI's from the 'mvs_output/scalars_**.xlsx' files in `loop_outputs`
    for a loop over one variable.

    The plot is saved into the `loop_output_directory`.

    Parameters
    ----------
    variable_name: str
        Name of the variable that is changed each loop. Please do not enter
        white spaces within the string.
    kpi: list of str
        List of KPI's to be plotted.
        Possible entries:
            "Degree of NZE"
            "Costs total PV",
            "Installed capacity PV",
            "Total renewable energy use",
            "Renewable share",
            "LCOE PV",
            "self consumption",
            "self sufficiency",
            "Degree of autonomy",
            "Total non-renewable energy use"
    scenario_dict: dictionary
        dictionary with the scenario names that should be compared as keys and
        a label for the scenario as value. e.g.: {"Scenario_A1" : "si", "Scenario_A2": "cpv"}
         Notice: all scenarios you want to compare, need to include the
         loop-outputs for the same variable / steps. The scenario names
         should follow the scheme: "Scenario_A1", "Scenario_A2", "Scenario_B1" etc.
    outputs_directory: str
        Path to output directory.
        Default: constants.DEFAULT_OUTPUTS_DIRECTORY

    Returns
    -------
        None
        saves figure into `loop_output_directory`
    -------


    """
    output_dict = {}
    for scenario_name in scenario_dict.keys():
        if outputs_directory == None:
            outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY
            scenario_folder = os.path.join(outputs_directory, scenario_name)
        else:
            scenario_folder = os.path.join(outputs_directory, scenario_name)
            if not os.path.isdir(scenario_folder):
                logging.warning(f"The scenario folder {scenario_name} does not exist.")
        loop_output_directory = os.path.join(
            scenario_folder, "loop_outputs_" + str(variable_name)
        )
        if not os.path.isdir(loop_output_directory):
            logging.warning(
                f"The loop output folder {loop_output_directory} does not exist. "
                f"Please check the variable_name"
            )
        # parse through scalars folder and read in all excel sheets
        output = pd.DataFrame()
        for filepath in list(
            glob.glob(os.path.join(loop_output_directory, "scalars", "*.xlsx"))
        ):

            file_sheet1 = pd.read_excel(
                filepath, header=0, index_col=1, sheet_name="cost_matrix1"
            )
            file_sheet2 = pd.read_excel(
                filepath, header=0, index_col=1, sheet_name="scalar_matrix1"
            )
            file_sheet3 = pd.read_excel(
                filepath, header=0, index_col=0, sheet_name="scalars1"
            )

            # get variable value from filepath
            split_path = filepath.split("_")
            get_step = split_path[::-1][0]
            step = int(get_step.split(".")[0])
            year = int(split_path[::-1][1])
            # get all different pv assets
            csv_directory = os.path.join(
                scenario_folder,
                "mvs_outputs_loop_"
                + str(variable_name)
                + "_"
                + str(year)
                + "_"
                + str(step),
                "inputs",
                "csv_elements",
            )
            energyProduction = pd.read_csv(
                os.path.join(csv_directory, "energyProduction.csv"), index_col=0
            )
            energyProduction = energyProduction.drop(["unit"], axis=1)
            pv_labels = energyProduction.columns
            # get total costs pv and installed capacity
            index = str(year) + "_" + str(step)
            output.loc[index, "step"] = int(step)
            output.loc[index, "year"] = int(year)
            for pv in pv_labels:
                output.loc[index, "Costs total PV"] = file_sheet1.at[pv, "costs_total"]
                output.loc[index, "Installed capacity PV"] = file_sheet2.at[
                    pv, "optimizedAddCap"
                ]
                output.loc[index, "Total renewable energy"] = file_sheet3.at[
                    "Total renewable energy use", 0
                ]
                output.loc[index, "Renewable factor"] = file_sheet3.at[
                    "Renewable factor", 0
                ]
                output.loc[index, "LCOE PV"] = file_sheet1.at[
                    pv, "levelized_cost_of_energy_of_asset"
                ]
                output.loc[index, "Self consumption"] = file_sheet3.at[
                    "Onsite energy fraction", 0
                ]
                output.loc[index, "Self sufficiency"] = file_sheet3.at[
                    "Onsite energy matching", 0
                ]
                output.loc[index, "Degree of autonomy"] = file_sheet3.at[
                    "Degree of autonomy", 0
                ]
                output.loc[index, "Total emissions"] = file_sheet3.at[
                    "Total emissions", 0
                ]
                output.loc[index, "Total non-renewable energy"] = file_sheet3.at[
                    "Total non-renewable energy use", 0
                ]
                output.loc[index, "Degree of NZE"] = file_sheet3.at["Degree of NZE", 0]

            output_dict_column = output.to_dict()
            output_dict[scenario_dict[scenario_name]] = output_dict_column

    # define y labels
    y_title = {
        "Costs total PV": "Costs total PV \n in EUR",
        "Installed capacity PV": "Installed capacity \nPV in kWp",
        "Total renewable energy": "Total renewable \nenergy in kWh",
        "Renewable factor": "Renewable factor \nin %",
        "LCOE PV": "LCOE PV \nin EUR/kWh",
        "Self consumption": "Self consumption \nin %",
        "Self sufficiency": "Self sufficiency \nin %",
        "Degree of autonomy": "Degree of \nautonomy in %",
        "Total emissions": "Total emissions \nin kgCO2eq/kWh",
        "Total non-renewable energy": "Total non-renewable \n energy in kWh",
        "Degree of NZE": "Degree of NZE \n in %",
    }

    output.sort_index(inplace=True)

    # plot
    hight = len(kpi) * 2
    fig = plt.figure(figsize=(7, hight))
    rows = len(kpi)
    num = (
        rows * 100 + 11
    )  # the setting for number of rows | number of columns | row number
    for i in kpi:
        ax = fig.add_subplot(num)
        num = num + 1
        for key in output_dict.keys():
            df = pd.DataFrame()
            df = df.from_dict(output_dict[key])
            df.plot(
                x="step",
                y=i,
                style=".",
                ax=ax,
                label=key,
                legend=False,
                sharex=True,
                xticks=df.step,
            )
            ax.set_ylabel(y_title[i])
            ax.set_xlabel(variable_name)
            ax.get_yaxis().set_label_coords(-0.13, 0.5)
            ax.set_xlim(ax.get_xlim()[0] - 0.5, ax.get_xlim()[1] + 0.5)

    handles, labels = ax.get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        bbox_to_anchor=(0.96, 0.96),
        loc="upper right",
        borderaxespad=0.0,
    )

    plt.tight_layout()

    name = ""
    for scenario_name in scenario_dict.keys():
        name = name + "_" + str(scenario_name)

    fig.savefig(
        os.path.join(
            outputs_directory,
            "plot_scalars" + str(name) + "_" + str(variable_name) + ".png",
        )
    )


def compare_weather_years(
    latitude,
    longitude,
    country,
    static_inputs_directory=None,
    outputs_directory=None,
    user_inputs_mvs_directory=None,
):
    """
    Barplot that shows yearly aggregated weather parameters: ghi, dni, dhi and
    temperature.


    Parameters
    ----------
    latitude: float
        latitude of the location
    longitude: float
        longitude of the location
    country: str
        country of simulation
    static_inputs_directory: str
        if None: 'constants.DEFAULT_STATIC_INPUTS_DIRECTORY'
    outputs_directory: str
        if None: 'constants.DEFAULT_OUTPUTS_DIRECTORY
    user_inputs_mvs_directory: str or None
        Directory of the mvs inputs; where 'csv_elements/' is located. If None,
        `constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY` is used as user_inputs_mvs_directory.
        Default: None.
    Returns
    -------
        None
        The plot is saved into the `output_directory`.
    -------

    """

    if static_inputs_directory == None:
        static_inputs_directory = constants.DEFAULT_STATIC_INPUTS_DIRECTORY
    if user_inputs_mvs_directory == None:
        user_inputs_mvs_directory = constants.DEFAULT_USER_INPUTS_MVS_DIRECTORY
    timeseries_directory = os.path.join(user_inputs_mvs_directory, "time_series")
    if outputs_directory == None:
        outputs_directory = constants.DEFAULT_OUTPUTS_DIRECTORY

    ghi = pd.DataFrame()
    temp = pd.DataFrame()
    dni = pd.DataFrame()
    dhi = pd.DataFrame()
    electricity_demand = pd.DataFrame()
    heat_demand = pd.DataFrame()

    for file in os.listdir(static_inputs_directory):
        if file.startswith("weatherdata_" + str(latitude) + "_" + str(longitude)):
            year = file.split(".")[2].split("_")[1]
            weatherdata = pd.read_csv(
                os.path.join(static_inputs_directory, file), header=0
            )
            ghi[year] = weatherdata["ghi"]
            temp[year] = weatherdata["temp_air"]
            dni[year] = weatherdata["dni"]
            dhi[year] = weatherdata["dhi"]

    for file in os.listdir(timeseries_directory):
        if file.startswith("electricity_load_"):
            if file.endswith(str(country) + "_5.csv"):
                year = int(file.split(".")[0].split("_")[2])
                electricity_load = pd.read_csv(
                    os.path.join(timeseries_directory, file), header=0
                )
                electricity_demand[year] = electricity_load["kWh"]
        elif file.startswith("heat_load_"):
            if file.endswith(str(country) + "_5.csv"):
                year = int(file.split(".")[0].split("_")[2])
                heat_load = pd.read_csv(
                    os.path.join(timeseries_directory, file), header=0
                )
                heat_demand[year] = heat_load["kWh"]

    ghi = ghi.reindex(sorted(ghi.columns), axis=1)
    temp = temp.reindex(sorted(temp.columns), axis=1)
    dni = dni.reindex(sorted(dni.columns), axis=1)
    dhi = dhi.reindex(sorted(dhi.columns), axis=1)
    electricity_demand = electricity_demand.reindex(
        sorted(electricity_demand.columns), axis=1
    )
    heat_demand = heat_demand.reindex(sorted(electricity_demand.columns), axis=1)

    ghi_sum = ghi.sum(axis=0)
    temp_sum = temp.sum(axis=0)
    dni_sum = dni.sum(axis=0)
    dhi_sum = dhi.sum(axis=0)
    el_sum = electricity_demand.sum(axis=0)
    he_sum = heat_demand.sum(axis=0)

    # data to plot
    n_groups = len(ghi.columns)

    # create plot
    fig = plt.figure(figsize=(11, 7))  # Create matplotlib figure
    ax = fig.add_subplot(111)  # Create matplotlib axes
    bar_width = 0.15
    opacity = 0.8

    ax2 = ax.twinx()

    ghi_sum.plot(
        kind="bar",
        color="tab:orange",
        ax=ax,
        alpha=opacity,
        width=bar_width,
        label="ghi",
        position=3,
    )
    dni_sum.plot(
        kind="bar",
        color="gold",
        ax=ax,
        alpha=opacity,
        width=bar_width,
        label="dni",
        position=2,
    )
    dhi_sum.plot(
        kind="bar",
        color="tab:green",
        ax=ax,
        alpha=opacity,
        width=bar_width,
        label="dhi",
        position=1,
    )
    el_sum.plot(
        kind="bar",
        color="tab:blue",
        ax=ax2,
        alpha=opacity,
        width=bar_width,
        label="electricity load",
        position=0,
    )
    #    he_sum.plot(kind='bar', color = "purple", ax=ax2, alpha = opacity,width=bar_width, label="heat load", position = 0)

    plt.xlabel("year")
    ax.set_ylabel("Irradiance in kW/year")
    ax2.set_ylabel("Demand in kWh/year")
    #    plt.title("yearly energy yield")
    #    plt.xticks(index + bar_width, (ghi.columns))
    ax.set_xlim(ax.get_xlim()[0] - 0.5, ax.get_xlim()[1] + 0.1)
    # Put a legend to the right of the current axis
    ax.legend(loc="lower right", bbox_to_anchor=(-0.05, 0))
    ax2.legend(loc="lower left", bbox_to_anchor=(1.05, 0))
    #    plt.tight_layout()

    # save plot into output directory
    plt.savefig(
        os.path.join(
            outputs_directory, f"plot_compare_weatherdata_{latitude}_{longitude}.png"
        ),
        bbox_inches="tight",
    )


if __name__ == "__main__":
    scenario_name = "Scenario_A2"
    # plot_all_flows(
    #     scenario_name=scenario_name,
    #     month=None,
    #     calendar_week=None,
    #     weekday=5,
    #     timeseries_directory=os.path.join(
    #         constants.DEFAULT_OUTPUTS_DIRECTORY,
    #         scenario_name,
    #         "mvs_outputs_loop_hp_temp_15",
    #     ),
    # )

    # scenario_dict = {"Scenario_A2": "psi", "Scenario_A9": "psi_HP"}
    # plot_kpi_loop(
    #     scenario_dict=scenario_dict,
    #     variable_name="lifetime",
    #     kpi=[
    #         "Installed capacity PV",
    #         "Total emissions",
    #         "Degree of autonomy",
    #     ],
    # )
    #
    # compare_weather_years(
    #     latitude=latitude,
    #     longitude=longitude,
    #     country=country,
    #     static_inputs_directory=None,
    # )