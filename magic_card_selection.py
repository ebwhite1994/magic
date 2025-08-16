#!/usr/bin/env python3

# STL
import argparse
from pathlib import Path

# Third Party Imports
import pandas as pd

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
    # Get names of cards in collection
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

def select_by_price_example(collection:pd.DataFrame, min_price:float=None, max_price:float=None, min_quantity:float=None) -> pd.DataFrame:
    """
    Select cards in collection within a given price range.

    Parameters
    ----------
    collection : pd.DataFrame
        collection you'd like to interact with
    min_price : float,optional
        the minimum price allowed in the selection
    max_price : float,optional
        the maximum price allowed in the selection
    min_quantity : float,optional
        the minimum quantity allowed in the selection

    Returns
    -------
    pd.DataFrame
        filtered card information
    """
    # TODO: Actually make these filters optional
    # TODO: We don't need to define all the filters, we can accept *args and **kwargs and pass them to pandas
    return [
        (collection['Purchase price'] >= min_price) &
        (collection['Purchase price'] <= max_price) &
        (collection['Quantity'] >= min_quantity)
    ]

def import_collection_csv(path:Path) -> pd.DataFrame:
    """
    Attempts to load a CSV from a path.

    Parameters
    ----------
    path : Path
        the path to your collection CSV that you'd like to import

    Returns
    -------
    pd.Data
        card information from CSV
    """
    if not path:
        return None

    collection = pd.read_csv(path)

    # TODO: Add any parsing / validations you want on collection

    return collection

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description='Utilities for managing your Magic: the Gathering Collection'
    )

    parser.add_argument('filename', type=Path, help='Path to the collection CSV you want to import')
    parser.add_argument('--print', '-p', action='store_true', help='Print the imported CSV to the terminal')

    args = parser.parse_args()

    # Import collection
    collection = pd.read_csv(args.filename)

    if args.print:
        print(collection)

if __name__ == '__main__':
    main()
