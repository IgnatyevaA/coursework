from src.views import write_json_gl
from src.services import search_to_str
from src.reports import spending_by_weekday
import pandas as pd

df = pd.read_excel("data/operations.xlsx")
operations = df.to_dict(orient='records')
def main():
    print(f'''{write_json_gl('2018-05-28 00:00:00')}
    
{search_to_str(operations, 'Рестораны')}

{spending_by_weekday(df, '2018-05-18 00:00:00')}
''')


if __name__ == "__main__":
    main()