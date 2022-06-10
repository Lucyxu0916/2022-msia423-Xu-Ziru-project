import logging.config
import sqlite3
import traceback
import pickle

import numpy as np
import sqlalchemy.exc
from flask import Flask, render_template, request

from src.add_bodymeasurement import UserInputManager

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile("config/flaskconfig.py")

# Configure logger
LOGGING_CONFIG = "config/logging/local.conf"
logging.config.fileConfig(LOGGING_CONFIG, disable_existing_loggers=True)
logger = logging.getLogger("Body Fat App")

# Initialize the database session
application_manager = UserInputManager(app)

try:
    model_path = "models/Lasso.sav"
    model = pickle.load(open(model_path, 'rb'))
except FileNotFoundError as e:
    logger.error("The model file does not exist at %s", model_path)
    raise e
else:
    logger.info("Successfully load the model from %s", model_path)

try:
    scaler_path = "models/scaler.sav"
    scaler = pickle.load(open(scaler_path, 'rb'))
except FileNotFoundError as e:
    logger.error("The scalar file does not exist at %s", scaler_path)
    raise e
else:
    logger.info("Successfully load the scalar from %s", scaler_path)


@app.route('/')
def index():
    try:
        logger.debug("Index page accessed")
        return render_template('index.html')
    except:
        traceback.print_exc()
        logger.warning("Not able to display loan applications information, error page returned")
        return render_template('error.html')


@app.route('/result', methods=['POST', 'GET'])
def add_entry():
    """View that process a POST with new user input
    Add new user body measurement information to UserInputs database and get prediction results
    Returns:
        rendered html template located at: app/templates/result.html if successfully processed,
        rendered html template located at: app/templates/error.html if any error occurs
    """
    if request.method == 'GET':
        return "Visit the homepage to add applicants and get predictions"
    elif request.method == 'POST':
        try:
            name = request.form['name']
            age = request.form['age']
            weight = request.form['weight']
            height = request.form['height']
            neck = request.form['neck']
            chest = request.form['chest']
            abdomen = request.form['abdomen']
            hip = request.form['hip']
            thigh = request.form['thigh']
            knee = request.form['knee']
            ankle = request.form['ankle']
            biceps = request.form['biceps']
            forearm = request.form['forearm']
            wrist = request.form['wrist']
            user_input = [age, weight, height, neck, chest, abdomen, hip, thigh, knee, ankle, biceps, forearm, wrist]

            # Add user body information to RDS for future usages

            application_manager.add_user(name, age, weight, height, neck, chest, abdomen, hip, thigh, knee,
                                             ankle, biceps, forearm, wrist)
            logger.info("New user body measurement is added %s", user_input)

            user_input = [age, weight, height, neck, chest, abdomen, hip, thigh, knee, ankle, biceps, forearm, wrist]
            for _input in user_input:
                if not _input:
                    return render_template('error.html', msg="Error! Please input a value for input fields.")
            user_input = np.array(user_input).reshape(1, -1)
            # scale user input
            user_input_transformed = scaler.transform(user_input)
            # generate prediction
            user_prediction = float(model.predict(user_input_transformed))
            user_prediction = round(user_prediction, 1)
            percentage = user_prediction * 7
            if user_prediction < 8:
                body_percentage = 20
            elif 8 <= user_prediction < 15:
                body_percentage = 82
            elif 15 <= user_prediction <= 18:
                body_percentage = 144
            elif 18 < user_prediction < 25:
                body_percentage = 206
            elif user_prediction >= 30:
                body_percentage = 268

            logger.info("The predicted body fat for the user is %s", user_prediction)

            logger.debug("Result page accessed")

            return render_template('index.html', user_prediction=user_prediction, percentage=percentage,
                                   body_percentage=body_percentage)

        except sqlite3.OperationalError as e:
            logger.error(
                "Error page returned. Not able to add user input to local sqlite "
                "database: %s. Error: %s ",
                app.config['SQLALCHEMY_DATABASE_URI'], e)
            return render_template('error.html',
                                   msg="We are sorry. There was a problem accessing the database. Please try back later.")
        except sqlalchemy.exc.OperationalError as e:
            logger.error(
                "Error page returned. Not able to add user input to MySQL database: %s. "
                "Error: %s ",
                app.config['SQLALCHEMY_DATABASE_URI'], e)
            return render_template('error.html',
                                   msg="We are sorry. There was a problem accessing the database. Please try back later.")


if __name__ == "__main__":
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
