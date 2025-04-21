from src.reports import spending_by_weekday
from src.services import search_to_str
from src.views import write_json_gl
import pandas as pd

df = pd.read_excel("data/operations.xlsx")
operations_df = df.to_dict(orient='records')

def main():
    print(spending_by_weekday(df, "2018-09-18 00:00:00"))
if __name__ == "__main__":
    main()