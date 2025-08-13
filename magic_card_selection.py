import pandas as pd
green = pd.read_csv('c:/Users/Moose/OneDrive/Documents/magic_project/Green_Binder.csv')

# class cards:
#     def __init__(self, min_price, max_price, quantity):
#         self.min_price = min_price
#         self.max_price = max_price
#         self.quantity = quantity

def selection(path, min_price, max_price, quantity):
    cards = pd.read_csv(path, usecols=['Name', 'Set code', 'Purchase price', 'Quantity'])
    return(cards)
    
print("file has run")

