import pulp
from typing import List, Dict
from src.project import Project
from src.config import OIL_LIMIT, MIN_START_YEAR, END_YEAR
from src.npv import shift_and_npv

def linearal_neft(projects: List[Project], greedy_portfolio: List[Dict[str, int]], neft_limit = OIL_LIMIT) -> List[Dict[str, float]]:
    model = pulp.LpProblem("Maximize_Oil_Production", pulp.LpMaximize)

    greedy_fixed = {item["Project"]: item["Start Year"] for item in greedy_portfolio}

    options = {
        project.name: shift_and_npv(project)
        for project in projects
    }

    x = {
        (project.name, start_year): pulp.LpVariable(
            f"x_{project.name}_{start_year}",
            lowBound=0,
            upBound=1,
            cat="Binary"
        )
        for project in projects
        for start_year in options[project.name]
    }

    model += pulp.lpSum(
        npv * x[(project.name, start_year)]
        for project in projects
        for start_year, (_, npv) in options[project.name].items()
    )

    for project in projects:
        if project.name in greedy_fixed:
            fixed_year = greedy_fixed[project.name]
            for start_year in options[project.name]:
                if start_year == fixed_year:
                    model += x[(project.name, start_year)] == 1
                else:
                    model += x[(project.name, start_year)] == 0
        else:
            model += pulp.lpSum(
                x[(project.name, s)] for s in options[project.name]
            ) <= 1

    oil_project_year = {
        (project.name, t): pulp.lpSum(
            options[project.name][start_year][0]
            .get("Oil Production", {})
            .get(t, 0)
            * x[(project.name, start_year)]
            for start_year in options[project.name]
        )
        for project in projects
        for t in range(MIN_START_YEAR, END_YEAR + 1)
    }

    for t in range(MIN_START_YEAR, END_YEAR + 1):
        model += pulp.lpSum(
            oil_project_year[(project.name, t)]
            for project in projects
        ) >= neft_limit

    model.solve(pulp.PULP_CBC_CMD(msg=True))

    if pulp.LpStatus[model.status] != "Optimal":
        print("Solution is not optimal:", pulp.LpStatus[model.status])

    portfolio = []
    for (project_name, start_year), var in x.items():
        if pulp.value(var) == 1:
            portfolio.append({
                "Project": project_name,
                "Start Year": start_year
            })
    return portfolio