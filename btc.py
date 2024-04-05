#Final Exam | Question3 | Alkiviadis Kariotis 241735

#Importing Libraries

import csv
from datetime import datetime
import sys

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def process_data(filepath):
    closing_prices_2020 = []
    dates_over_60000 = 0
    days_less_avg_price = 0
    highest_prices = []
    monthly_prices = {}

    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['ticker'] == 'BTC' and is_valid_date(row['date']):
                date = datetime.strptime(row['date'], '%Y-%m-%d')
                close_price = float(row['close'])
                high_price = float(row['high'])
                low_price = float(row['low'])
                
                #Average closing price in 2020
                if date.year == 2020:
                    closing_prices_2020.append(close_price)
                
                #Dates with closing price over $60,000
                if close_price > 60000:
                    dates_over_60000 += 1
                
                #Days closing price was less than the average of the highest and lowest price
                if close_price < (high_price + low_price) / 2:
                    days_less_avg_price += 1
                
                #Ten highest closing prices
                highest_prices.append((close_price, row['date']))
                
                #Average monthly prices
                month_year = (date.year, date.month)
                if month_year not in monthly_prices:
                    monthly_prices[month_year] = []
                monthly_prices[month_year].append(close_price)

    highest_prices.sort(reverse=True)
    avg_prices_within_range = {
        month_year: sum(prices) / len(prices)
        for month_year, prices in monthly_prices.items()
        if 20000 <= sum(prices) / len(prices) <= 22000
    }

    return {
        'avg_2020': sum(closing_prices_2020) / len(closing_prices_2020) if closing_prices_2020 else 0,
        'dates_over_60000': dates_over_60000,
        'days_less_avg_price': days_less_avg_price,
        'highest_prices': highest_prices[:10],
        'avg_prices_within_range': avg_prices_within_range
    }

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python btc.py <path to BTC.csv>")
        sys.exit(1)

    filepath = sys.argv[1]
    results = process_data(filepath)

    print(f"Average closing price of BTC in 2020: {results['avg_2020']}")
    print(f"Number of dates for which the closing price was over 60000 USD: {results['dates_over_60000']}")
    print(f"Number of days for which the closing price was less than the avg of the highest and lowest price: {results['days_less_avg_price']}")
    print("The ten highest closing prices and the corresponding dates:")
    for price, date in results['highest_prices']:
        print(f"Price: {price}, Date: {date}")
    print("The year and month for which the average closing price was between 20000 and 22000 USD:")
    for (year, month), avg_price in results['avg_prices_within_range'].items():
        print(f"Year: {year}, Month: {month}, Avg Price: {avg_price}")
