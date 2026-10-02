"""Calculate survival statistics. No plotting here: data in, numbers out."""


def overall_survival_rate(df):
    """Return the fraction of passengers who survived (0 to 1)."""
    return df["survived"].mean()


def survival_rate_by(df, column):
    """Return the survival rate for each value in `column`, highest first."""
    return (
        df.groupby(column, observed=True)["survived"]
        .mean()
        .sort_values(ascending=False)
    )


def summary_statistics(df):
    """Return count, mean, min, max, etc. for the numeric columns."""
    return df.describe()


def print_report(df):
    """Print a short, readable survival report."""
    print("=== Titanic Survival Report ===")
    print(f"Passengers: {len(df)}")
    print(f"Overall survival rate: {overall_survival_rate(df):.1%}\n")

    for column in ["sex", "pclass", "age_group"]:
        print(f"Survival rate by {column}:")
        rates = survival_rate_by(df, column)
        for value, rate in rates.items():
            print(f"  {str(value):<12} {rate:.1%}")
        print()

    print("Summary statistics:")
    print(summary_statistics(df).round(2).to_string())
