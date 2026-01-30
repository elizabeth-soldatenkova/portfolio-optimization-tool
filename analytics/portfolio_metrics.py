from src.data_loader import load_projects
from src.optimization.greedy import greedy_capex
from src.optimization.linear_programming import linearal_neft
from src.portfolio import portfolio_elements
from src.npv import portfolio_npv
import matplotlib.pyplot as plt

FILE_PATH = "data/exam.xlsx"

def plot_portfolio_elements(portfolio_elements, title):
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(title, fontsize=16)

    if 'CAPEX' in portfolio_elements:
        years = sorted(portfolio_elements['CAPEX'].keys())
        values = [portfolio_elements['CAPEX'][year] for year in years]
        axs[0, 0].bar(years, values, color='b')
        axs[0, 0].set_title('CAPEX')
        axs[0, 0].set_xlabel('Year')
        axs[0, 0].set_ylabel('Value')
        axs[0, 0].axhline(y=5_000_000_000, color='r', linestyle='--', label='CAPEX limit')
        axs[0, 0].legend()

    if 'Oil Production' in portfolio_elements:
        years = sorted(portfolio_elements['Oil Production'].keys())
        values = [portfolio_elements['Oil Production'][year] for year in years]
        axs[0, 1].plot(years, values, color='g')
        axs[0, 1].set_title('Oil and Liquid Production')
        axs[0, 1].set_xlabel('Year')
        axs[0, 1].set_ylabel('Value')
        axs[0, 1].axhline(y=5_000_000, color='r', linestyle='--', label='Oil limit')
        axs[0, 1].legend()

    if 'Liquid Production' in portfolio_elements:
        years = sorted(portfolio_elements['Liquid Production'].keys())
        values = [portfolio_elements['Liquid Production'][year] for year in years]
        axs[1, 0].plot(years, values, color='c')
        axs[1, 0].set_title('Liquid Production')
        axs[1, 0].set_xlabel('Year')
        axs[1, 0].set_ylabel('Value')

    if 'FCF' in portfolio_elements:
        years = sorted(portfolio_elements['FCF'].keys())
        values = [portfolio_elements['FCF'][year] for year in years]
        axs[1, 1].plot(years, values, color='m')
        axs[1, 1].set_title('FCF')
        axs[1, 1].set_xlabel('Year')
        axs[1, 1].set_ylabel('Value')

    plt.tight_layout()
    plt.show()
    fig.savefig(f"reports/{title.replace(' ', '_').lower()}.png", dpi=300)

def main():
    projects = load_projects(FILE_PATH)

    portfolio1 = greedy_capex(projects)
    portfolio2 = linearal_neft(projects, portfolio1)

    print("Portfolio 1 NPV:", portfolio_npv(projects, portfolio1))
    print("Portfolio 2 NPV:", portfolio_npv(projects, portfolio2))

    elements1 = portfolio_elements(projects, portfolio1)
    elements2 = portfolio_elements(projects, portfolio2)

    plot_portfolio_elements(elements1, 'Portfolio 1')
    plot_portfolio_elements(elements2, 'Portfolio 2')



if __name__ == "__main__":
    main()


