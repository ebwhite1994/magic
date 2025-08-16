#!/usr/bin/env python3

# STL
import argparse
from pathlib import Path

# Third Party Imports
import pandas as pd

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
