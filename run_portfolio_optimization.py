from src.data_loader import load_projects
from src.optimization.greedy import greedy_capex, condition_npv_capex
from src.optimization.linear_programming import linearal_neft
from src.npv import max_npv, portfolio_npv
from src.portfolio import portfolio_elements

FILE_PATH = "data/exam.xlsx"

def main():
    projects = load_projects(FILE_PATH)
    options_npv_capex = condition_npv_capex(projects)
    npv_project = max_npv(projects)

    for option in options_npv_capex:
        print(f"Max NPV/CAPEX for {option['Project']}: {option['Max NPV/CAPEX']}")

    portfolio1 = greedy_capex(projects)
    print("\nPortfolio under Constraint 1:")
    for item in portfolio1:
        print(f"Project: {item['Project']}, Start Year: {item['Start Year']}")
    print()
    portfolio2 = linearal_neft(projects, portfolio1)
    print("\nPortfolio under Constraint 2:")
    for item in portfolio2:
        print(f"Project: {item['Project']}, Start Year: {item['Start Year']}")

    portfolio1_npv = portfolio_npv(projects, portfolio1)
    portfolio2_npv = portfolio_npv(projects, portfolio2)

    print(f"\nTotal Portfolio 1 NPV: {portfolio1_npv}")
    print(f"Total Portfolio 2 NPV: {portfolio2_npv}")

    all_projects = [project.name for project in projects]
    project_in_case1 = [item['Project'] for item in portfolio1]
    project_in_case2 = [item['Project'] for item in portfolio2]
    proj_not_in_case1 = set(all_projects) - set(project_in_case1)
    proj_not_in_case2 = set(all_projects) - set(project_in_case2)

    print("\nProjects Not Started in the Portfolio 1:")
    for project in proj_not_in_case1:
        print(project)
    print("\nProjects Not Started in the Portfolio 2:")
    for project in proj_not_in_case2:
        print(project)

    print()
    portfolio1_elements = portfolio_elements(projects, portfolio1)
    portfolio2_elements = portfolio_elements(projects, portfolio2)

    print("Aggregated Portfolio 1 Metrics:")
    for element, years in portfolio1_elements.items():
        print(f"{element}: {years}")

    print("\nAggregated Portfolio 2 Metrics:")
    for element, years in portfolio2_elements.items():
        print(f"{element}: {years}")

    ##  if you want to see shifted_projects

    # for project in projects:
    #     results = shift_and_npv(project)
    #     print(repr(project))
    #     for start_year, (shifted_elements, npv) in results.items():
    #         print(f"Project name: {project.name}, Start Year: {start_year}, NPV: {npv}")
    #         for element, values in shifted_elements.items():
    #             print(f"  {element}: {values}")
    #         print()


if __name__ == "__main__":
    main()