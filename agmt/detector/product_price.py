import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
# Define the API URL (replace with an actual working API endpoint if available)
API_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?format=json&api-key=579b464db66ec23bdd000001fbdefd9819584455608a9f1f1c1126ac&limit=1000"

# List of selected fruits and vegetables
selected_items = ["Tomato", "Potato", "Onion", "Apple", "Banana"]

# Function to fetch data from API
def fetch_data():
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        data = response.json()
        #print("Data Keys:", data.keys())  # Should include "records"
        #print("Number of records:", len(data.get("records", [])))  # Should be > 0
        print(data)
        return data
    else:
        print("Error fetching data")
        return None

# Process data for visualization
def process_data(data):
    records = data.get("records", [])
    df = pd.DataFrame(records)
    print(df)

    # Convert price values to numeric
    df["modal_price"] = pd.to_numeric(df["modal_price"], errors='coerce') / 100

    # Extract month and year from date
    df["date"] = pd.to_datetime(df["arrival_date"], dayfirst=True)

    df["month"] = df["date"].dt.strftime("%b")  # Short month names (Jan, Feb, ...)
    df["year"] = df["date"].dt.year

    # Filter data for the year 2024 and selected items
    # Find the latest available year
    latest_year = df["year"].max()
    
    # Filter data for the latest available year and selected items
    df = df[(df["year"] == latest_year) & (df["commodity"].isin(selected_items))]

    return df

# Function to plot the data
import matplotlib.pyplot as plt

def plot_data(df):
    plt.figure(figsize=(10, 6))

    # Get the latest date in the dataset
    latest_date = df["date"].max()
    

    # Filter data for the latest date and selected items
    df_latest = df[(df["date"] == latest_date) & (df["commodity"].isin(selected_items))]

    # Group by commodity and calculate the average price
    avg_prices = df_latest.groupby("commodity")["modal_price"].mean()

    # Ensure all selected items are included, even if missing in data
    avg_prices = avg_prices.reindex(selected_items, fill_value=0)  # Fill missing ones with 0

    # Plot bar graph
    avg_prices.plot(kind="bar", color=["red", "orange", "purple", "green", "yellow"])
    
    # Labels and title
    plt.xlabel("Commodity")
    plt.ylabel("Average Modal Price Per Kg(₹)")
    plt.title(f"Price Comparison for Selected Commodities on {latest_date.strftime('%d-%m-%Y')}")
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    #save_path = os.path.join("D:/your_folder_name", "commodity_prices.png")
    #plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()

# Main execution
data = fetch_data()
if data:
    processed_df = process_data(data)
    plot_data(processed_df)
