from .constant import Constant
from .response import Response


import json
import os
import pandas as pd


class DellCalendar(Constant):
    def get(self, conditions={}):

        script_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(script_dir, "year_quar_week.json"), "r", encoding="utf-8") as f:
            data = json.load(f)

        # conditions=condition={"week_new": "WK09","updatetime": ["2024-01-02","2024-01-03","2024-01-01"]}

        # def filter_data(data, conditions):
        #     return [item for item in data if all(item.get(k) == v for k, v in conditions.items())]

        # filtered = filter_data(data, conditions)

        df = pd.DataFrame(data)

        for key, value in conditions.items():
            if isinstance(value, list):
                df = df[df[key].isin(value)]
            else:
                df = df[df[key] == value]

        return Response(data=df.to_dict("records"))
