from src.data_loader import load_projects
from src.optimization.greedy import greedy_capex
from src.optimization.linear_programming import linearal_neft
from src.config import END_YEAR
from src.npv import shift_and_npv, portfolio_npv
import matplotlib.pyplot as plt
import numpy as np

FILE_PATH = "data/exam.xlsx"

def main():
    projects = load_projects(FILE_PATH)

    portfolio1 = greedy_capex(projects)
    portfolio2 = linearal_neft(projects, portfolio1)

    fig, (ax1, ax3) = plt.subplots(2, 1, figsize=(8, 10), gridspec_kw={'hspace': 0.3})

    # graph1
    names_projects = []
    y_ticks_position = []

    for index, item in enumerate(portfolio1, start=1):
        project_name = item['Project']
        start_year = item['Start Year']

        names_projects.append(project_name)
        y_ticks_position.append(index)

        x_points = np.array([start_year, END_YEAR])
        y_points = np.array([index, index])
        ax1.plot(x_points, y_points, linewidth=4, color='b')

    font_title = {'family': 'serif', 'size': 12}
    font_axis = {'family': 'serif', 'color': 'slategray', 'size': 9}
    font_names = {'family': 'serif', 'size': 10}

    ax1.set_yticks(y_ticks_position)
    ax1.set_yticklabels(names_projects, fontdict=font_names)
    ax1.set_xlabel("Project Timeline", fontdict=font_axis)
    ax1.set_ylabel("Started Projects", fontdict=font_axis)
    ax1.set_title("Portfolio under Constraint 1 (CAPEX Limit)", fontdict=font_title)

    # graph2
    names_projects = []
    y_ticks_position = []

    for index, item in enumerate(portfolio2, start=1):
        project_name = item['Project']
        start_year = item['Start Year']

        names_projects.append(project_name)
        y_ticks_position.append(index)

        x_points = np.array([start_year, END_YEAR])
        y_points = np.array([index, index])
        ax3.plot(x_points, y_points, linewidth=4, color='b')

    ax3.set_yticks(y_ticks_position)
    ax3.set_yticklabels(names_projects, fontdict=font_names)
    ax3.set_xlabel("Project Timeline", fontdict=font_axis)
    ax3.set_ylabel("Started Projects", fontdict=font_axis)
    ax3.set_title("Portfolio under Constraint 2 (CAPEX and Oil Production Constraints)", fontdict=font_title)

    # tables-----------------1
    fig_table, axes = plt.subplots(2, 2, figsize=(9, 4))
    ax2, ax4, ax5, ax6 = axes.flatten()

    table_data = []
    for item in portfolio1:
        project_name = item['Project']
        start_year = item['Start Year']

        project = next((p for p in projects if p.name == project_name), None)

        if project:
            options = shift_and_npv(project)
            if start_year in options:
                _, npv = options[start_year]
                npv_new = npv / 1_000_000
                table_data.append([project_name, f"{npv_new:,.2f} mln."])

    columns = ['Started Project Names', 'NPV']

    if table_data:
        table = ax2.table(cellText=table_data, colLabels=columns, loc='center', cellLoc='center', fontsize=15)
        ax2.axis('off')
        table.scale(1, 1.5)

        for (row, col), cell in table.get_celld().items():
            if row == 0:
                cell.set_fontsize(14)
            else:
                cell.set_fontsize(120)
    else:
        ax2.text(0.5, 0.5, 'No Started Projects', ha='center', va='center', fontsize=15)
        ax2.axis('off')

    ##--------------2
    portfolio1_npv = portfolio_npv(projects, portfolio1)
    portfolio2_npv = portfolio_npv(projects, portfolio2)

    portfolio1_npv_new = portfolio1_npv / 1_000_000
    portfolio2_npv_new = portfolio2_npv / 1_000_000

    table_data = [
        ["Portfolio 1", f"{portfolio1_npv_new:,.2f} mln."],
        ["Portfolio 2", f"{portfolio2_npv_new:,.2f} mln."]
    ]
    columns = ['Portfolio Summary', 'NPV']
    table = ax4.table(cellText=table_data, colLabels=columns, loc='center', cellLoc='center')
    ax4.axis('off')
    table.scale(1, 1.5)

    ##---------3
    all_projects = [project.name for project in projects]
    project_in_case1 = [item['Project'] for item in portfolio1]
    project_in_case2 = [item['Project'] for item in portfolio2]
    proj_not_in_case1 = set(all_projects) - set(project_in_case1)
    proj_not_in_case2 = set(all_projects) - set(project_in_case2)

    table_data = [[project] for project in proj_not_in_case1]
    if table_data:
        table = ax5.table(cellText=table_data, colLabels=['Projects Not Started under Constraint 1'], loc='center',
                          cellLoc='center')
        ax5.axis('off')
        table.scale(1, 1.5)
    else:
        ax5.text(0.5, 0.5, 'No Excluded Projects', ha='center', va='center', fontsize=10)
        ax5.axis('off')

    ##---------------4
    table_data = [[project] for project in proj_not_in_case2]
    if table_data:
        table = ax6.table(cellText=table_data, colLabels=['Projects Not Started under Constraint 2'], loc='center',
                          cellLoc='center')
        ax6.axis('off')
        table.scale(1, 1.5)
    else:
        ax6.text(0.5, 0.5, 'No Excluded Projects', ha='center', va='center', fontsize=10)
        ax6.axis('off')

    plt.tight_layout()
    plt.show()
    fig.savefig("reports/portfolio_timeline.png", dpi=300)
    fig_table.savefig("reports/portfolio_tables.png", dpi=300)


if __name__ == "__main__":
    main()