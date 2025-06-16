import csv
from datetime import datetime

def load_transactions(filename='financial_transactions.csv'):
    transactions = []
    try:
            with open(filename, 'r', newline='') as csvfile:
             reader = csv.DictReader(csvfile)
        
            for row in reader:
                try:
                    transaction_date = datetime.strptime(row['date'], '%Y-%m-%d')

                    amount = float(row['amount'])
                    if row['type'].lower() == 'debit':
                            amount = -amount

                    transaction = {
                            'date': transaction_date,
                            'amount': amount,
                            'type': row['type'],
                            'description': row['description'],
                    } 

                    transactions.append(transaction)


                except ValueError as e:
                    print(f"ValueError: {e} in row {row}")
                    continue

    except FileNotFoundError:
            print(f"Error: The file at {filename} was not found")

    return transactions

def add_transaction(transactions):
         
        try:
              date_str = input("Enter the date (YYYY-MM-DD): ").strip()
              transaction_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
             print("Invalid date format. Please use YYYY-MM-DD.")
             return
        
        customer_id = input("Enter customer ID: ").strip()

        try:
             amount = float(input("Enter the amount: ").strip())
        except ValueError:
             print("Invalid amount. Please enter a number.")
             return
        
        txn_type = input("Enter the transaction type (credit/debit/transfer): ").strip().lower()
        if txn_type not in ['credit', 'debit', 'transfer']:
             print("Invalid type. Must be 'credit', 'debit', or transfer.")
             return
        
        description = input("Enter a description").strip()

        if transactions:
             transaction_id = max(t.get('transaction_id', 0) for t in transactions) + 1
        else:
             transaction_id = 1
        
        if txn_type == 'debit':
             amount = -abs(amount)
        else:
             amount = abs(amount)
        #transfer = leave amount as entered
        transaction = {
             'transaction_id': transaction_id,
             'date' : transaction_date,
             'customer_id' : customer_id,
             'amount' : amount,
             'type' : txn_type,
             'description': description
        }

        transactions.append(transaction)
        print("Transaction added successfully!")

def view_transactions(transactions):
         
         if not transactions:
              print("No transactions to display.")
              return
         
         print(f"{'ID':<5} {'Date':<12} {'Customer ID':<12} {'Amount':>10} {'Type':<8} {'Description'}")
         print("-" * 60)


         for txn in transactions:
              txn_id = txn.get('transaction_id', 'N/A')
              date = txn['date'].strftime("%Y-%m-%d") if isinstance(txn['date'], datetime) else str(txn['date'])
              customer_id = txn.get('customer_id', 'N/A')
              amount = f"{txn['amount']:,.2f}"
              txn_type = txn.get('type', 'N/A').capitalize()
              description = txn.get('description', '')

              print(f"{txn_id:<5} {date:<12} {customer_id:<12} {amount:>10} {txn_type:<8} {description}")

def update_transaction(transactions):
         
         if not transactions:
              print("No trnasactions available to update.")
              return
         
         print("Transactions:")
         for i, txn in enumerate(transactions):
              date = txn['date'].strftime('%Y-%m-%d') if isinstance(txn['date'], datetime) else str(txn['date'])
              print(f"{i}: ID={txn.get('transaction_id', 'N/A')}, Date={date}, Amount={txn['amount']}, Type={txn['type']}, Desc={txn['description']}")

         try:
              index = int(input("Enter the number of the transaction to update: "))
              if index < 0 or index >= len(transactions):
                   print("Invalid transaction number.")
                   return
              
         except ValueError:
              print("Invalid input. Please enter a number.")
              return
         
         txn = transactions[index]

         field = input("Which field would you like to update? (date, customer_id, amount, type, description): ").strip().lower()

         if field not in ['date', 'customer_id', 'amount', 'type', 'description']:
              print("Invalid field.")
              return
         
         new_value = input(f"Enter new value for {field}: ").strip()

         try:
              if field == 'date':
                   txn['date'] = datetime.strptime(new_value, '%Y-%m-%d')
              elif field == 'amount':
                   txn['amount'] = float(new_value)
              elif field == 'type':
                   if new_value.lower() not in ['credit', 'debit', 'transfer']:
                        print("Invalid type. Must be 'credit', 'debit', or 'transfer'.")
                        return
                   txn['type'] = new_value.lower()
                   if txn['type'] == 'debit':
                        txn['amount'] = -abs(txn['amount'])
                   else:
                        txn['amount'] = abs(txn['amount'])
              else:
                   txn[field] = new_value

              print("Transaction updated successfully!")

         except ValueError as e:
              print(f"Error: {e}")

def delete_transaction(transactions):
         if not transactions:
              print("No transactions to delete.")
              return

         print("Transactions: ")
         for i, txn in enumerate(transactions):
              date = txn['date'].strftime('%Y-%m-%d') if isinstance(txn['date'], datetime) else str(txn['date'])
              print(f"{i}: ID={txn.get('transaction_id', 'N/A')}, Date={date}, Amount={txn['type']}, Desc={txn['description']}")

         try:
              index = int(input("Enter the number of the transaction to delete: "))
              if index < 0 or index >= len(transactions):
                   print("Invalid transaction number.")
                   return
         except ValueError:
              print("Invalid input. Please enter a number.")
              return

         confirm = input(f"Are you sure you want to delete transaction {index}? (yes/no): ").strip().lower()
         if confirm in ['yes', 'y']:
              removed = transactions.pop(index)
              print(f"Transaction ID {removed.get('transaction_id', 'N/A')} deleted successfully.")
         else:
              print("Deletion cancelled.")

def analyze_finances(transactions):
     if not transactions:
          print("No transactions available to analyze.")
          return
     
     total_credits = 0.0
     total_debits = 0.0
     summary_by_customer = {}

     for txn in transactions:
          customer_id = txn.get('customer_id', 'Unknown')
          amount = txn['amount']
          txn_type = txn.get('type', '').lower()

          if txn_type == 'credit':
               total_credits += amount
          elif txn_type == 'debit':
               total_debits += abs(amount)

          if customer_id not in summary_by_customer:
               summary_by_customer[customer_id] = 0.0
          summary_by_customer[customer_id] += amount

     net_balance = total_credits - total_debits
     

     print("\n=== Financial Summary ===")
     print(f"Total Credits: ${total_credits:,.2f}")
     print(f"Total Debits:  ${total_debits:,.2f}")
     print(f"Net Balance:  ${net_balance:,.2f}")

     print("\n=== Balance by Customer ===")
     for customer, total in summary_by_customer.items():
        print(f"{customer}: ${total:,.2f}")

def save_transactions(transactions, filename='financial_transactions.csv'):
    if not transactions:
        print("No transactions to save.")
        return

    fieldnames = ['transaction_id', 'date', 'customer_id', 'amount', 'type', 'description']

    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for txn in transactions:
                try:
                    writer.writerow({
                        'transaction_id': int(txn.get('transaction_id', 0)),
                        'date': txn['date'].strftime('%Y-%m-%d') if isinstance(txn['date'], datetime) else txn['date'],
                        'customer_id': txn.get('customer_id', ''),
                        'amount': f"{float(txn['amount']):.2f}",
                        'type': txn.get('type', '').lower(),
                        'description': txn.get('description', '')
                    })
                except (ValueError, TypeError) as e:
                    print(f"Skipping transaction due to error: {e} - Transaction: {txn}")
                    continue

        print(f"Transactions saved successfully to '{filename}'.")

    except IOError as e:
        print(f"Error saving transactions: {e}")


def generate_report(transactions, filename='report.txt'):
     
     if not transactions:
          print("No transactions to report.")
          return
     
     total_credits = 0.0
     total_debits = 0.0
     summary_by_customer = {}

     for txn in transactions:
          customer_id = txn.get('customer_id', 'Unknown')
          amount = txn['amount']
          txn_type = txn.get('type', '').lower()
          
          if txn_type == 'credit':
               total_credits += amount
          elif txn_type == 'debit':
               total_debits += abs(amount)
          
          if customer_id not in summary_by_customer:
               summary_by_customer[customer_id] = 0.0
          summary_by_customer[customer_id] += amount

     net_balance = total_credits - total_debits

     try:
          with open(filename, 'w') as f:
               f.write("=== Financial Report ===\n")
               f.write(f"Total Credits: ${total_credits:,.2f}\n")
               f.write(f"Total Debits:  ${total_debits:,.2f}\n")
               f.write(f"Net Balance:   ${net_balance:,.2f}\n\n")

               f.write("=== Balance by Customer ===\n")
               for customer, total in summary_by_customer.items():
                    f.write(f"{customer}: ${total:,.2f}\n")

          print(f"Report successfully written to '{filename}'.")

     except IOError as e:
          print(f"Error writing report: {e}")

def main():
     transactions = []
     while True:
          print("\nSmart Personal Finance Analyzer")
          print("1. Load Transactions")
          print("2. Add Transaction")
          print("3. View Transactions")
          print("4. Update Transaction")
          print("5. Delete Transaction")
          print("6. Analyze Finances")
          print("7. Save Transactions")
          print("8. Generate Report")
          print("9. Exit")

          choice = input("Select an option: ").strip()

          if choice == '1':
               transactions = load_transactions()
          elif choice == '2':
               add_transaction(transactions)
          elif choice == '3':
               view_transactions(transactions)
          elif choice == '4':
               update_transaction(transactions)
          elif choice == '5':
               delete_transaction(transactions)
          elif choice == '6':
               analyze_finances(transactions)
          elif choice == '7':
               save_transactions(transactions)
          elif choice == '8':
               generate_report(transactions)
          elif choice == '9':
               print("Goodbye!")
               break
          else:
               print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
     main()