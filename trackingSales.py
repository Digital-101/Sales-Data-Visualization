import csv

product_name = input("Enter product name: ").strip()
cost_price = float(input("Enter cost price: "))
sell_price = float(input("Enter selling price: "))
month = input("Enter month in the format: ('YYYY-MM'): ").strip()
region = input("Enter region/area: ").strip()

headers = ["Product", "Cost", "Sell", "Month", "Region", "Profit/Loss"]

profit_loss = sell_price - cost_price

dataFile = 'New_data.csv'
file_Exists = True

try:
    with open(dataFile, 'r') as file:
        file_Exists = True
except FileNotFoundError:
    file_Exists = False    

with open(dataFile, 'a', newline='') as file:
    writer = csv.writer(file)
    if file_Exists:
        #writer.writerow(headers)
        writer.writerow([product_name, cost_price, sell_price, month, region, profit_loss])
    file.close()
print(dataFile+" Saved Successfully!")
