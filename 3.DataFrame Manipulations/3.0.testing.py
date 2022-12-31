# Here we define our query as a multi-line string
import pandas as pd

from IPython.core.display_functions import display

resultDataFrame = pd.read_json("characters.json")


resultDataFrame.transpose().to_json("characters_transposed.json")

from datetime import datetime

# Filter dataframe
# Get characters that have birthday today

today = datetime.now()

resultDataFrame.loc[resultDataFrame.dateOfBirth == {'month':today.now().month, 'day': today.now().day}]

display(resultDataFrame)

