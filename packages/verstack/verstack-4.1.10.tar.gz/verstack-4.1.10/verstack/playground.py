import pandas as pd
from verstack import DateParser

df = pd.read_csv("/Users/danil/Downloads/datetime_cols_DateParser_cannot_find.csv")

dp = DateParser()
dff = dp.fit_transform(df)
