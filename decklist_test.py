import pandas as pd
import argparse
from pathlib import Path

green = pd.read_csv('c:/Users/Moose/OneDrive/Documents/magic_project/Green_Binder.csv')
test_path = 'c:/Users/Moose/OneDrive/Documents/magic_project/Green_Binder.csv'
deck = 'c:/Users/Moose/OneDrive/Documents/magic_project/test_decklist.txt'
moxfield = 'c:/Users/Moose/OneDrive/Documents/magic_project/test_moxfield.txt'
def get_decklist_from_collection(collection:pd.DataFrame, decklist_path:Path) -> (pd.DataFrame, pd.DataFrame):
    """
    Find if cards in a decklist are in your collection or not.

    Parameters
    ----------
    collection : pd.DataFrame
        the collection we're checking against
    decklist : Path
        path to the decklist CSV that we're interested in checking

    Returns
    -------
    (pd.DataFrame, pd.DataFrame)
        tuple containing a DataFrame with the cards that are in your collection and a DataFrame
    including the cards that are not in your collection.
    """
    print(decklist_path)
    # Get names of cards in collection
    names = collection['Name']
    #Depending on how the decklist is set up, this would need to change. 
    #Moxfield doesn't have a header like our collection files do, so header = None
    #Need to turn it into an object instead of a pandas DataFrame, so apply the [0]
    decklist = pd.read_csv(decklist_path, header = None)[0]
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


#for the case of moxfield input
test = pd.read_csv(moxfield, header = None, sep = '^', names = ['test'])
#split the DataFrame by the first space
#Do this so that we don't split it by every space in the strings
test[['Number', 'Name']] = test['test'].str.split(n=1, expand = True)
#Split the DataFrame by the ( around the set code
#Splits it such that now we have name and set code in their own columns
test[['Name', "Set Code"]] = test['Name'].str.split('(', expand = True)
#split the Dataframe by the ) around the set code
#splits it such that now we have set code and card ID (number of the card in the set) in their own columns
test[['Set Code','ID']] = test['Set Code'].str.split(')', expand = True)
test = test[['Number', "Name", 'Set Code', "ID"]]