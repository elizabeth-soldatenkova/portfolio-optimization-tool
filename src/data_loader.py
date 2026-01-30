import pandas as pd
from typing import List, Dict
from src.project import Project
from src.config import MIN_START_YEAR, MAX_START_YEAR, END_YEAR

LEN_OF_TABLE = 37

def load_projects(file_path: str) -> List[Project]:
    all_sheets = pd.read_excel(file_path, sheet_name=None, header=None, engine='openpyxl')
    projects = []

    for sheet_name, df in all_sheets.items():
        mandatory: bool = df.iloc[0, 1] == 'Yes'
        min_year: int = int(df.iloc[1, 1]) if pd.notna(df.iloc[1, 1]) and df.iloc[1, 1] != " " else MIN_START_YEAR
        max_year: int = int(df.iloc[2, 1]) if pd.notna(df.iloc[2, 1]) and df.iloc[2, 1] != " " else MAX_START_YEAR
        elements: Dict[str, Dict[int, float]] = {}
        for i in range(5, len(df)):
            row_name = str(df.iloc[i, 0])
            if pd.notna(row_name):
                values = [float(x) if pd.notna(x) and x != " " else 0.0 for x in df.iloc[i, 1: LEN_OF_TABLE]]
                elements[row_name] = dict(zip(range(min_year, END_YEAR + 1), values))
        project = Project(
            name=sheet_name,
            mandatory=mandatory,
            min_year=min_year,
            max_year=max_year,
            elements=elements
        )
        projects.append(project)
    return projects