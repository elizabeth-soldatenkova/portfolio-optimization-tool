from typing import List, Dict
from src.project import Project
from src.npv import shift_and_npv

def sum_capex(projects: List[Project]) -> List[Dict[str, float]]:
    best_npv_capex_for_project = []
    for project in projects:
        if 'CAPEX' in project.elements:
            capex_value = project.elements['CAPEX']
            sum_capex = sum(capex_value.values())
        best_npv_capex_for_project.append({'Project': project.name, 'Sum capex': sum_capex})
    return best_npv_capex_for_project


def portfolio_elements(projects, portfolio):
    summary_elements = {}

    for item in portfolio:
        project_name = item['Project']
        start = item['Start Year']

        project = next((p for p in projects if p.name == project_name), None)
        if project:
            options = shift_and_npv(project)
            if start in options:
                shifted_elements, _ = options[start]

                for element, values in shifted_elements.items():
                    if element not in summary_elements:
                        summary_elements[element] ={}

                    for year, value in values.items():
                        if year in summary_elements[element]:
                            summary_elements[element][year] += value
                        else:
                            summary_elements[element][year] = value

    return summary_elements