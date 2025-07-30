import pandas as pd
import matplotlib.pyplot as plt
from vizhelper.enhance import enhance_plot

def main():
    # Load the dataset
    data = pd.read_csv("data/healthcare_dataset.csv")
    
    # Convert 'Date of Admission' to datetime and extract the month for grouping
    data["Date of Admission"] = pd.to_datetime(data["Date of Admission"])
    data["Month"] = data["Date of Admission"].dt.to_period("M")
    
    # Summarize the billing amount by month
    monthly_billing = data.groupby("Month")["Billing Amount"].sum()
    
    # Create a figure and an Axes object
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Plot the bar chart on our Axes
    monthly_billing.plot(kind="bar", color="teal", ax=ax)
    plt.xticks(rotation=90)
    plt.grid(True)
    
    # Enhance the plot using our module
    enhance_plot(
        ax,
        interactive=True,
        user_profile="colorblind",  # or 'visually_impaired', 'novice', etc.
        auto_legend=True,          # legend not needed if not using labels in bars
        auto_label=True,
        openai_api_key=None         # replace with your key if desired
    )
    
    plt.show()

if __name__ == "__main__":
    main()
