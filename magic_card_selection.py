import pandas as pd
green = pd.read_csv('c:/Users/Moose/OneDrive/Documents/magic_project/Green_Binder.csv')
test_path = 'c:/Users/Moose/OneDrive/Documents/magic_project/Green_Binder.csv'
# class cards:
#     def __init__(self, min_price, max_price, quantity):
#         self.min_price = min_price
#         self.max_price = max_price
#         self.quantity = quantity

def selection(path, min_price, max_price, min_quantity):
    cards = pd.read_csv(path, usecols=['Name', 'Set code', 'Purchase price', 'Quantity'])
    cards = cards[(cards['Purchase price'] > min_price) & (cards['Purchase price'] < max_price) & (cards['Quantity'] >= min_quantity)]
    return(cards)
    

