#Final Exam | Question4 | Alkiviadis Kariotis 241735

#Importing Libraries

from pyspark import SparkContext
from datetime import datetime

#Date format for parsing the transaction date
DATE_FMT = "%d-%m-%Y"

#Function for checking type 
def parse(line):
    fields = line.split(',')
    if len(fields) < 18:
        print(f"Skipping line due to unexpected format: {line}")
        return None

    try:
        transaction_date = datetime.strptime(fields[1].strip(), DATE_FMT).date()
        month = transaction_date.month
        store_location = fields[4].strip()
        total_bill = float(fields[8].strip())
        product_category = fields[9].strip()
        product_detail = fields[10].strip()
    except ValueError as e:
        print(f"Error parsing line: {e}")
        return None
    
    return (month, store_location, total_bill, product_category, product_detail)

if __name__ == "__main__":
    sc = SparkContext("local[*]", "CoffeeShopAnalysis")
    
    lines = sc.textFile("CoffeeShop.csv")
    header = lines.first()
    
    parsedLines = lines.filter(lambda x: x != header) \
                       .map(parse) \
                       .filter(lambda x: x is not None)
    
    transactionsPerMonth = parsedLines.map(lambda x: (x[0], 1)).reduceByKey(lambda x, y: x + y)
    totalBillsPerMonth = parsedLines.map(lambda x: (x[0], x[2])).reduceByKey(lambda x, y: x + y)
    coffeeTransactionsJune = parsedLines.filter(lambda x: x[0] == 6 and 'Coffee' in x[3]).count()
    
    # Correctly applying fold for Astoria bills
    astoriaBills = parsedLines.filter(lambda x: 'Astoria' in x[1]).map(lambda x: x[2])
    totalAstoriaBills, astoriaCount = astoriaBills.aggregate((0, 0),
                                                             (lambda acc, value: (acc[0] + value, acc[1] + 1)),
                                                             (lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1])))
    avgBillAstoria = totalAstoriaBills / astoriaCount if astoriaCount else 0
    
    transactionsBrazilianOrganicLowerManhattan = parsedLines.filter(lambda x: 'Lower Manhattan' in x[1] and 'Brazilian - Organic' in x[4]).count()

    print("Number of transactions per month:")
    print(transactionsPerMonth.collect())

    print("\nSum of the total bills per month:")
    print(totalBillsPerMonth.collect())

    print(f"\nNumber of transactions in June 2023 with Coffee: {coffeeTransactionsJune}")
    print(f"Average bill amount for the Astoria store: {avgBillAstoria}")
    print(f"Number of transactions for Brazilian-Organic Coffee Beans in Lower Manhattan: {transactionsBrazilianOrganicLowerManhattan}")
