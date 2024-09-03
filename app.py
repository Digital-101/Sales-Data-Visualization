import tkinter as tk
from tkinter import messagebox
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

# Function to handle form submission
def submit_data():
    product_name = entry_product_name.get().strip()
    try:
        cost_price = float(entry_cost_price.get())
        sell_price = float(entry_sell_price.get())
    except ValueError:
        messagebox.showerror("Input Error", "Cost price and Selling price must be valid numbers.")
        return
    month = entry_month.get().strip()
    region = entry_region.get().strip()
    
    if not (product_name and month and region):
        messagebox.showerror("Input Error", "All fields must be filled.")
        return
    
    profit_loss = sell_price - cost_price
    
    headers = ["Product", "Cost", "Sell", "Month", "Region", "Profit/Loss"]
    dataFile = 'Gui_data.csv'
    
    # Check if file exists and write data
    file_exists = os.path.isfile(dataFile)
    
    with open(dataFile, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow([product_name, cost_price, sell_price, month, region, profit_loss])
    
    messagebox.showinfo("Success", f"{dataFile} Saved Successfully!")

def visualize_data():
    dataFile = 'Gui_data.csv'
    
    if not os.path.isfile(dataFile):
        messagebox.showerror("File Error", "Data file does not exist.")
        return
    
    # Read data from CSV
    df = pd.read_csv(dataFile)
    
    # Ensure data is not empty
    if df.empty:
        messagebox.showinfo("No Data", "No data to visualize.")
        return
    
    # Plotting Sales Data
    plt.figure(figsize=(14, 7))

    # Product sales by month
    plt.subplot(1, 2, 1)
    sales_by_product_month = df.groupby(['Product', 'Month'])['Profit/Loss'].sum().unstack()
    sales_by_product_month.plot(kind='bar', stacked=True, ax=plt.gca())
    plt.title('Sales by Product and Month')
    plt.xlabel('Top Selling Products')
    plt.ylabel('Total Profit/Loss')
    plt.legend(title='Month')
    
    # Sales by Region and Month
    plt.subplot(1, 2, 2)
    sales_by_region_month = df.groupby(['Region', 'Month'])['Profit/Loss'].sum().unstack()
    sales_by_region_month.plot(kind='bar', stacked=True, ax=plt.gca())
    plt.title('Sales by Region and Month')
    plt.xlabel('Region/Area')
    plt.ylabel('Total Profit/Loss')
    plt.legend(title='Month')

    plt.tight_layout()
    plt.show()

# Create the main window
root = tk.Tk()
root.title("Product Data Entry")

# Create and place widgets
tk.Label(root, text="Product Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_product_name = tk.Entry(root)
entry_product_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Cost Price:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_cost_price = tk.Entry(root)
entry_cost_price.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Selling Price:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_sell_price = tk.Entry(root)
entry_sell_price.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Month (YYYY-MM):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_month = tk.Entry(root)
entry_month.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Region/Area:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_region = tk.Entry(root)
entry_region.grid(row=4, column=1, padx=10, pady=5)

tk.Button(root, text="Submit", command=submit_data).grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(root, text="Visualize Data", command=visualize_data).grid(row=6, column=0, columnspan=2, pady=10)

# Start the GUI event loop
root.mainloop()