import pandas as pd

pd1 = pd.read_json("staffs_352.json")
pd2 = pd.read_json("staffs_354.json")
frames = [pd1, pd2]
pd = pd.concat(frames, ignore_index=True)
# pd.reset_index(inplace=True)

pd.to_json("staffs.json")


pd3 = pd.read_json("staffs.json")
