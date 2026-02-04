import pandas as pd
import matplotlib.pyplot as plt

def plot_population(df, outpath, title):
    plt.figure()
    plt.plot(df["year"], df["group_a"], label="Group A")
    plt.plot(df["year"], df["group_b"], label="Group B")
    plt.legend()
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath, dpi=300)

def plot_proportion(df, outpath, title):
    plt.figure()
    plt.plot(df["year"], df["group_a"] / df["total_population"])
    plt.axhline(0.5, linestyle="--")
    plt.xlabel("Year")
    plt.ylabel("Proportion Group A")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath, dpi=300)

def main():
    real = pd.read_csv(r"results\projections_realistic.csv")
    ext  = pd.read_csv(r"results\projections_extreme.csv")

    plot_population(real, r"results\figures\population_realistic.png", "Population by Group (Realistic Scenario)")
    plot_proportion(real, r"results\figures\proportion_group_a_realistic.png", "Proportion of Group A (Realistic Scenario)")

    plot_population(ext, r"results\figures\population_extreme.png", "Population by Group (Extreme Scenario)")
    plot_proportion(ext, r"results\figures\proportion_group_a_extreme.png", "Proportion of Group A (Extreme Scenario)")

if __name__ == "__main__":
    main()
