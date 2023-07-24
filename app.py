# Import necessary libraries
import flask
import pandas as pd
import numpy as np

# Import custom modules for data formatting and API connections
from coordinatebase_maxgenerationrate_table_import import CoorBaseMaxGenerationRateTableImport
from jrc_api_connection import GETSolarAverageDataFromJRC
import data_formatting 
import user_note

# Create a Flask application instance
app = flask.Flask(__name__)

# Define a function to calculate the monthly average solar generation
def MonthlyAverageSolarGeneration(lat, lon, peakpower):
    """
    Objective:
    Calculate the monthly average solar generation for the specified latitude, longitude, and peak power.

    Parameters:
    lat (float): Latitude of the selected coordinate.
    lon (float): Longitude of the selected coordinate.
    peakpower (float): Peak power value in kilowatts.

    Returns:
    table (pandas.DataFrame): DataFrame containing calculated data for each month.
    note (str): A user note indicating the range of years in the data.
    """

    # Get raw solar energy generation data from the JRC API
    raw_data_json = GETSolarAverageDataFromJRC(lat, lon, peakpower)

    # Extract and format monthly average solar generation data
    ave_gen_table_selected_coor = data_formatting.ExtractMonthlyData(raw_data_json)

    # Import the table containing base maximum generation rate data for different coordinates
    max_rate_tb = CoorBaseMaxGenerationRateTableImport()

    # Concatenate the average generation data and maximum rate data for the selected coordinate
    ave_gen_n_max_rate = data_formatting.ConcatJRCnMaxRateAnalysis(max_rate_tb, ave_gen_table_selected_coor, lat, lon)

    # Calculate the maximum generation capacity for each month based on average generation and maximum rate data
    table = data_formatting.MaxGenerationCapacityCalculation(ave_gen_n_max_rate)

    # Create a user note based on the raw data JSON
    note = user_note.CreateUserNote(raw_data_json)

    return table, note

# Define a route for the home page (GET method)
@app.route('/', methods=['GET'])
def show_form():
    version_info = "0.0.5"
    return flask.render_template('index.html', version_info=version_info)

# Define a route for processing the form data (POST method)
@app.route('/', methods=['POST'])
def process_form():
    version_info = "0.0.5"
    try:
        # Get the latitude, longitude, and peak power values from the HTML form
        num1 = float(flask.request.form['num1'])
        num2 = float(flask.request.form['num2'])
        num3 = float(flask.request.form['num3'])

        # Validate the input values for latitude, longitude, and peak power
        if not (0 <= num1 <= 90) or not (0 <= num2 <= 180):
            raise ValueError("Geçersiz koordinat girişi. Latitude (enlem) değerleri 0-90 aralığında, longitude (boylam) değerleri 0-180 aralığında olmalıdır.")
        
        if num3 <= 0:
            raise ValueError("Geçersiz kurulu güç girişi. Kurulu güç 0'dan büyük olmalıdır.")

        # Calculate the monthly average solar generation using the provided function
        table, user_note = MonthlyAverageSolarGeneration(num1, num2, num3)

        # Prepare data and render the 'result.html' template
        plant_data = "Enlem: {} Boylam: {} Kurulu Güç [kW]: {}".format(num1, num2, num3)
        return flask.render_template('result.html', df=table.to_html(index=False), user_note=user_note, inputs=plant_data,
                               month_labels=table['Months'].to_list(),
                               average_generation_data=table['Average Generation [kWh]'].to_list(),
                               max_gen_cap=table['Max. Generation Capacity [kWh]'].to_list(),
                               version_info=version_info)
    
    except ValueError as ve:
        # Handle invalid input values with appropriate error message
        error_message = str(ve)
        return flask.render_template('error.html', error_message=error_message, version_info=version_info)
    except Exception as e:
        # Handle other possible errors with a general error message
        error_message = "Hata oluştu: {}".format(str(e))
        return flask.render_template('error.html', error_message=error_message, version_info=version_info)

# Run the Flask application if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)