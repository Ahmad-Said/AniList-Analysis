# Here we define our query as a multi-line string
import pandas as pd

from IPython.core.display_functions import display

resultDataFrame = pd.read_json("characters_old.json")

display(resultDataFrame)

