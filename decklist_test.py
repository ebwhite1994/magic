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
    
    # Check to see if the dataframe contains headers
    # For now, see if "Name" is in the default header
    decklist = pd.read_csv(decklist_path)
    if "Name" in list(decklist):
        # Collection has headers
        # Compare "Name" column to collection "Name" column
        print("same")
    #if the decklist has only one column, assume the column is the name of the card
    if decklist.shape[1] == 1:
        decklist = pd.read_csv(decklist_path, header = None)[0]
        # Create a list of things to search for in the collection
        # This allows the search for all cards in the decklist to be done in one commander
        pattern = '|'.join(decklist)
        # Create the mask which is applied to the collection
        # True == the card in the decklist is in the collection
        mask = names.str.contains(pattern, case = False, regex = True)
        # Apply the mask to collection to get cards in the collection.
        cards_in_collection = collection[mask]
        # Determine which cards in the decklist aren't in the collection
        pattern2 = '|'.join(cards_in_collection)
        mask2 = decklist.str.contains(pattern2, case = False, regex = True)
        # Apply the opposite of the mask to determine what isn't in the collection
        cards_not_in = decklist[~mask2]
        # Output the results
        return(cards_in_collection, cards_not_in)
    # We will need to add more if statements or call other functions once we have more input types (TCGPlayer, TappedOut, etc.)
    # For now, I have Moxfield working (if not as efficiently as it could be)
    else:
        # For the case of a Moxfield input
        decklist = pd.read_csv(decklist_path, header = None, sep = "|", names = ['test'])
        # Split the DataFrame by the first space
        # Do this so that we don't split it by every space in the strings
        decklist[['Quantity', 'Name']] = decklist['test'].str.split(n=1, expand = True)
        # Split the DataFrame by the ( around the set code
        # Splits it such that now we have name and set code in their own columns
        decklist[['Name', "Set Code"]] = decklist['Name'].str.split('(', expand = True)
        # Split the Dataframe by the ) around the set code
        # Splits it such that now we have set code and card ID (number of the card in the set) in their own columns
        decklist[['Set Code','Collector Number']] = decklist['Set Code'].str.split(')', expand = True)
        # The way we have split these columns, there is an excess space " " in a few columns
        # ex. "Swamp ", "EOE", " 221"
        # Need to remove the excess spaces so they can match up with the labels in the database/dataframe
        decklist['Name'] = decklist['Name'].str[:-1]
        decklist['ID'] = decklist["Collector Number"].str[1:]
        # Adjust the Dataframe such that it only uses the columns we have defined
        decklist = decklist[['Quantity', "Name", 'Set Code', "Collector Number"]]
        print(decklist["Name"][0])
        pattern = '|'.join(decklist['Name'])
        mask = names.str.contains(pattern, case = False, regex = True)
        cards_in_collection = names[mask]
        # Drop duplicates for determing if cards are in the collection at all
        # We will deal with duplicates and specific printings later. 
        cards_in_collection_single = cards_in_collection.drop_duplicates()
        print(cards_in_collection_single)
        # You now have which cards are in the collection, but we also want to output the cards we still need
        # Create a searchable list of cards in the collection
        pattern2 = '|'.join(cards_in_collection)
        print(pattern2)
        # Create a mask to the decklist 
        mask2 = decklist["Name"].str.contains(pattern2, case = False, regex = True)
        cards_not_in = decklist["Name"][~mask2]
        
        # If we're just interested in the fact that there are copies of the cards in the collection,
        # then cards_in_collection and cards_not_in will cover it. 
        # If we want to see if the exact printing and/or number are in the collection, we need to go further. 

        # We also want to know if the quantity of cards is the same 
        # In otherwords, you might have a card, but the decklist calls for four of them. 
        # You might want to know if you have more than one copy too even if the deck only calls for one. 
        # To that same idea, we can check Set Code and Collector Number 
        
        #Get the quantity of cards, considering only cards we own in the decklist
        # card_quant = collection['Quantity'][mask]
        # return(collection, decklist, mask, mask2)

        # Determine if the exact printing is in the collection
        

        return(cards_in_collection, cards_not_in)
        
    # #Output the results. 
    # #Ideally, this will be applied to some GUI.
    # #Maybe the cards you have are highlighted green and the ones you need are in red
    #     #Or white and grey/red for colorblind accessibility
    #     #Maybe yellow highlight for have the card but not the printing in the decklist file. 
    #     #Option to turn that on/off for people who don't care about the exact art. 
    # return(cards_in_collection, cards_not_in)
