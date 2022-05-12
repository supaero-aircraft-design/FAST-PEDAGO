import csv


def csv_to_table(path):
    table = []
    f = open(path)
    myreader = csv.reader(f, delimiter=';')
    headings = next(myreader)
    for row in myreader:
        table.append(row[0])
    return table
    
    

    
    



