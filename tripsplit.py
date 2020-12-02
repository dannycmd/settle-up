import csv

class ppl():
    names = []

    def __init__(self, initials, firstName, lastName):
        self.initials = initials
        self.firstName = firstName
        self.lastName = lastName
        self.amountBorrowed = 0
        self.amountPaid = 0
        self.amountOwed = 0
        ppl.names.append(self)
    
    def addPayment(self, amount, recipients=[]):
        """Add a payment that a person has made. Takes the amount and a list of the recipients as arguments."""
        self.amountPaid += int(amount)
        for i in recipients:
            for j in ppl.names:
                if j.initials == i:
                    j.amountBorrowed += (int(amount) / len(recipients))
            
    def totals(self):
        """Calculates the amount each person owes or is owed."""
        self.amountOwed = (self.amountPaid - self.amountBorrowed)

# Enter initials and names of people as class instances
dr = ppl("dr", "Dan", "Rooney")
ss = ppl("ss", "Sam", "Stratton")
sm = ppl("sm", "Sam", "Magowan")
ib = ppl("ib", "Indigo", "Brownhall")
bs = ppl("bs", "Ben", "Stratton")

# Read payments from csv file
with open('payments.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    payments = []
    for row in csv_reader:
        payments.append(row)

# Add payments read from csv file to class using ppl.addPayment() method        
for payment in payments:
    payee = payment['payee']
    amount = payment['amount']
    recipients = (payment['recipients']).split(',')
    for i in ppl.names:
        if i.initials == payee:
            i.addPayment(amount, recipients)

# Calculate total amount each person owes or is owed using ppl.totals() method
for i in ppl.names:
    i.totals()

totals = [[i.amountOwed, i.firstName, i.lastName] for i in [j for j in ppl.names]]  # List of lists of people and the amounts they owe or are owed
owed = [i for i in totals if i[0] > 0]  # List of lists of people who are owed money and the amounts
owe = [i for i in totals if i[0] < 0]  # List of lists of people who owe money and the amounts
for i in owe:
    i[0] = i[0]*-1  # Change sign of amounts people owe to positive
owed.sort(reverse=True, key=lambda x: x[0])  # Sort lists by amount
owe.sort(reverse=True, key=lambda x: x[0])

def settleUp():
    """Prints out a series of payments that need to be made to settle up the debts."""
    a = owed.pop()
    b = owe.pop()
    output = []
    while len(owed) >= 0:
        if a[0] > 0 and b[0] > 0:
            if a[0] == b[0]:
                output.append("{} {} pays {} {} £{}\n".format(b[1], b[2], a[1], a[2], round(b[0], 2)))
                a[0] = 0
                b[0] = 0
            elif a[0] > b[0]:
                output.append("{} {} pays {} {} £{}\n".format(b[1], b[2], a[1], a[2], round(b[0], 2)))
                a[0] -= b[0]
                b[0] = 0
            else:
                output.append("{} {} pays {} {} £{}\n".format(b[1], b[2], a[1], a[2], round(a[0], 2)))
                b[0] -= a[0]
                a[0] = 0
        elif a[0] == 0:
            if len(owed) == 0:
                break
            else:
                a = owed.pop()
        elif b[0] == 0:
            b = owe.pop()
    
    with open('settleup.txt', mode='w') as text_output:
        text_output.writelines(output)

settleUp()