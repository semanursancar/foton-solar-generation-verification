import pandas as pd
import numpy as np

def ExtractMonthlyData(raw_data_json):
    """
    Objective:
    Extract monthly solar energy generation data from the raw JSON data obtained from the API.

    Parameters:
    raw_data_json (dict): A dictionary containing raw solar energy generation data in JSON format.

    Returns:
    ave_gen_table_selected_coor (DataFrame): A DataFrame containing the monthly solar energy generation data.
                      The DataFrame includes columns for months, average generation in kilowatt-hours, and standard deviation.
    """

    # Extract 'outputs' and 'monthly' data from the raw JSON
    outputs_monthly = raw_data_json['outputs']['monthly']['fixed']

    # Create a pandas DataFrame from the 'outputs_monthly' data
    outputs_monthly_df = pd.DataFrame(outputs_monthly)

    # Select and copy the relevant columns from the DataFrame
    ave_gen_table_selected_coor = outputs_monthly_df[["month", "E_m", "SD_m"]].copy()

    # Rename the columns for better readability
    ave_gen_table_selected_coor.rename(columns={"month": "Months", "E_m": "Average Generation [kWh]", "SD_m": "Standard Dev."}, inplace=True)

    # Return the DataFrame containing the monthly solar energy generation data
    return ave_gen_table_selected_coor


def ConcatJRCnMaxRateAnalysis(max_rate_tb, ave_gen_table_selected_coor, lat, lon):
    """
    Objective:
    Concatenate the solar average generation data and the maximum rate data for the given latitude and longitude.

    Parameters:
    max_rate_tb (pandas.DataFrame): DataFrame containing maximum rate data for different coordinates.
    ave_gen_table_selected_coor (pandas.DataFrame): DataFrame containing average generation data for specific coordinates.
    lat (float): Latitude of the selected coordinate.
    lon (float): Longitude of the selected coordinate.

    Returns:
    ave_gen_n_max_rate (pandas.DataFrame): DataFrame containing concatenated data with average generation and maximum rate for the selected coordinate.
    """

    # Extract the maximum rate data for the specified latitude and longitude
    max_rate_coor_base = max_rate_tb[(max_rate_tb['lat'] == np.floor(lat)) & (max_rate_tb['lon'] == np.floor(lon))].iloc[0, 2:]
    max_rate_coor_base.name = 'Coordinate Base Maximum Rate'
    max_rate_coor_base.reset_index(drop=True, inplace=True)

    # Concatenate average generation data and maximum rate data for the selected coordinate
    ave_gen_n_max_rate = pd.concat([ave_gen_table_selected_coor, max_rate_coor_base], axis=1)

    return ave_gen_n_max_rate


def MaxGenerationCapacityCalculation(ave_gen_n_max_rate):
    """
    Objective:
    Calculate the maximum generation capacity for each month based on average generation and maximum rate data.

    Parameters:
    ave_gen_n_max_rate (pandas.DataFrame): DataFrame containing average generation and maximum rate data for a specific coordinate.

    Returns:
    table (pandas.DataFrame): DataFrame containing the calculated maximum generation capacity for each month.
    """

    # Create a copy of the input DataFrame for further calculations
    table = ave_gen_n_max_rate.copy()

    # Calculate the maximum generation capacity for each month based on the provided formula
    table["Max. Generation Capacity [kWh]"] = (table["Standard Dev."] + table["Average Generation [kWh]"]) * table["Coordinate Base Maximum Rate"]

    return table
