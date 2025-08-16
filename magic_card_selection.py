import pandas as pd
green = pd.read_csv('c:/Users/Moose/OneDrive/Documents/magic_project/Green_Binder.csv')
test_path = 'c:/Users/Moose/OneDrive/Documents/magic_project/Green_Binder.csv'

def selection(path, min_price, max_price, min_quantity):
    cards = pd.read_csv(path, usecols=['Name', 'Set code', 'Purchase price', 'Quantity'])
    cards = cards[(cards['Purchase price'] > min_price) & (cards['Purchase price'] < max_price) & (cards['Quantity'] >= min_quantity)]
    return(cards)


#Function to check if cards in a decklist are in your collection or not
#takes in the path to a collection and the path to a decklist
#outputs a list of cards in that collection and a list of cards outside the collection
###
# The way Moxfield outputs a decklist puts the set code in parenthesis next to the card name.
# We will probably need to put a filter on the decklist such that it cuts off each string when it reaches a "("
# and then remove off the end [:-1] to get rid of the extra space. 
###
# Something to add would be to check if the exact printing the decklist listed was in your collection instead of just
# any version of the card. 
def decklist_match(collection, decklist):
    #get the names of the cards in the collection
    collection = pd.read_csv(collection)
    names = collection['Name']
    #Depending on how the decklist is set up, this would need to change. 
    #Moxfield doesn't have a header like our collection files do, so header = None
    #Need to turn it into an object instead of a pandas DataFrame, so apply the [0]
    decklist = pd.read_csv(decklist, header = None)[0]
    #Create a list of things to search for in the collection
    #This allows the search for all cards in the decklist to be done in one command
    pattern = '|'.join(decklist)
    #Create the mask which is applied to the collection
    #True == the card in the decklist is in the collection
    mask = names.str.contains(pattern, case = False, regex = True)
    #Apply mask to collection names to get names of cards in the collection.
    cards_in_collection = names[mask]
    #Apply the opposite of the mask to get the names of cards you still need. 
    cards_not_in = names[~mask]
    #Output the results. 
    #Ideally, this will be applied to some GUI.
    #Maybe the cards you have are highlighted green and the ones you need are in red
        #Or white and grey/red for colorblind accessibility
        #Maybe yellow highlight for have the card but not the printing in the decklist file. 
        #Option to turn that on/off for people who don't care about the exact art. 
    return(cards_in_collection, cards_not_in)
