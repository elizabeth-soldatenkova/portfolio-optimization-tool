from typing import List, Dict, Tuple
from src.project import Project
from src.config import END_YEAR, DISCOUNT_RATE

def shift_and_npv(project: Project, rate: float = DISCOUNT_RATE) -> Dict[int, Tuple[Dict[str, Dict[int, float]], float]]:
    results = {}
    for start_year in range(project.min_year, project.max_year + 1):
        shifted_elements = {}
        npv = 0.0
        for element, values in project.elements.items():
            shifted_values = {}
            for year, value in values.items():
                shifted_year = year + (start_year - project.min_year)
                if shifted_year > END_YEAR:
                    continue
                shifted_values[shifted_year] = value + shifted_values.get(shifted_year, 0)
                if element == 'FCF':
                    degree = shifted_year - project.min_year + 0.5
                    npv += value / (rate ** degree)
            shifted_elements[element] = shifted_values
        results[start_year] = (shifted_elements, npv)
    return results

def max_npv(projects: List[Project]) -> List[Dict[str, float]]:
    best_npv_for_each_project = []
    for project in projects:
        max_npv: int = -100000000000000000000000000000000000000
        options = shift_and_npv(project)
        for start_year, (shifted_elements, npv) in options.items():
            if npv > max_npv:
                max_npv = npv
        best_npv_for_each_project.append({'Project': project.name, 'Max npv': max_npv})
    return best_npv_for_each_project

def portfolio_npv(projects: List[Project], portfolio: List[Dict[str, int]]) -> float:
    total_npv = 0.0

    for item in portfolio:
        project_name = item['Project']
        start_year = item['Start Year']
        project = next(p for p in projects if p.name == project_name)
        _, npv = shift_and_npv(project)[start_year]

        total_npv += npv
    return total_npv

