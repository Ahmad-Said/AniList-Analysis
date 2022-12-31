import matplotlib.pyplot as plt
import pandas
import seaborn as sns
import numpy

# read dataset from json file
# datasetCharacters = pandas.read_json("../data/split/characters/characters1.json")
datasetCharacters = pandas.read_json("../data/characters.json")

# Flatten dateOfBirth.month object in new column in the dataset
all_months_count = []
for index, character in datasetCharacters.iterrows():
    all_months_count.append(character['dateOfBirth']['month'])

datasetCharacters['dateOfBirthMonth'] = all_months_count

# Count values of month (None value are excluded)
datasetCharactersMonthCount = datasetCharacters.dateOfBirthMonth.value_counts()

# Line plot
# sns.lineplot(data=datasetMonthValueCount) # if printed alone
sns.lineplot(x=datasetCharactersMonthCount.index - 1, y=datasetCharactersMonthCount.values)

# Bar plot
sns.barplot(x=datasetCharactersMonthCount.index, y=datasetCharactersMonthCount.values)

# Adding label description
plt.xlabel('Month of the year')
plt.ylabel('Count of characters')
plt.title(f'Birthday month of {sum(datasetCharactersMonthCount.values)} '
          f'characters out of total {len(all_months_count)}')
plt.savefig("BirthdayMonthsCharacters.png")
plt.show()
