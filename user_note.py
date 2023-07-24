
def CreateUserNote(raw_data_json):
    """
    Objective:
    Create a user note based on the raw data JSON, specifying the range of years in the data.

    Parameters:
    raw_data_json (dict): A dictionary containing raw solar energy generation data in JSON format.

    Returns:
    str: A user note indicating the range of years in the data.
    """

    # Extract the minimum and maximum years from the raw data JSON
    year_min = raw_data_json['inputs']['meteo_data']['year_min']
    year_max = raw_data_json['inputs']['meteo_data']['year_max']

    # Create the user note by formatting the extracted years into the string
    user_note = "The data includes the average of {} and {}.".format(year_min, year_max)

    return user_note
