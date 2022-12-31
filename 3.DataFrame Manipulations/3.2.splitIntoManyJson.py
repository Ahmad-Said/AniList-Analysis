# you need to add you path here
import os
from pathlib import Path
import pandas

# filePath = os.path.abspath('../data/medias.json')
filePath = os.path.abspath('../data/staffs.json')
# filePath = os.path.abspath('../data/characters.json')
# filePath = os.path.abspath('../data/studios.json')
dirPath = os.path.abspath(os.path.join(filePath, os.pardir))
name_of_file = os.path.basename(filePath)
basename = os.path.splitext(name_of_file)[0]
outputDirPath = os.path.join(dirPath, "split")
outputDirPath = os.path.join(outputDirPath, basename)

my_data_T = pandas.read_json(filePath)
os.makedirs(outputDirPath, exist_ok=True)

print('Total number of records data: ', len(my_data_T))

size_of_the_split = 5000
total = len(my_data_T) // size_of_the_split

# in here you will get the Number of splits
print(f'Total number of splits : {total + 1}')

for i in range(total + 1):
    print(f'splitting from {i * size_of_the_split} to {min((i + 1) * size_of_the_split, len(my_data_T))}')
    my_data_T[i * size_of_the_split:(i + 1) * size_of_the_split].to_json(
        os.path.join(outputDirPath, f'{basename}{i + 1}.json'))
