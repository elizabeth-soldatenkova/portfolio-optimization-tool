from typing import List, Dict
from src.project import Project
from src.config import CAPEX_LIMIT
from src.npv import max_npv, shift_and_npv
from src.portfolio import sum_capex

def condition_npv_capex(projects: List[Project]) -> List[Dict[str, float]]:
    npv_capex = []
    npv = max_npv(projects)
    capex = sum_capex(projects)
    dict_npv = {item['Project']: item['Max npv'] for item in npv}
    dict_capex = {item['Project']: item['Sum capex'] for item in capex}
    for project in projects:
        project_name = project.name
        if project_name in dict_npv and project_name in dict_capex:
            npv_value = dict_npv[project_name]
            capex_value = dict_capex[project_name]
            if capex_value != 0:
                rate = npv_value / capex_value
                if project.mandatory:
                    rate += 1000
            else:
                rate = float('inf')
            npv_capex.append({'Project': project_name, 'Max NPV/CAPEX': rate})
    npv_capex_descending: List[Dict[str, float]] = sorted(npv_capex, key=lambda item: item['Max NPV/CAPEX'], reverse=True)
    return npv_capex_descending


def greedy_capex(projects: List[Project], capex_limit: float = CAPEX_LIMIT) -> List[Dict[str, float]]:
    npv_capex_descending = condition_npv_capex(projects)
    total_first_condition_portfolio = []
    yearly_capex = {}

    for item in npv_capex_descending:
        project_name = item['Project']
        project = next((p for p in projects if p.name == project_name), None)
        if project:
            options = shift_and_npv(project)
            for start_year, (shifted_elements, npv) in options.items():
                capex = shifted_elements.get('CAPEX', {})
                can_add = True
                for year, cap in capex.items():
                    if yearly_capex.get(year, 0) + cap > capex_limit:
                        can_add = False
                        print(f"{project.name} could not be started in {start_year} (CAPEX limit exceeded)")
                        break
                if can_add:
                    for year, cap in capex.items():
                        yearly_capex[year] = yearly_capex.get(year, 0) + cap
                    total_first_condition_portfolio.append({'Project': project.name, 'Start Year': start_year})
                    break
    return total_first_condition_portfolio