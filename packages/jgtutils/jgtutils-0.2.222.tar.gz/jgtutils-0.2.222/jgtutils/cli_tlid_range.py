#!/usr/bin/env python

import argparse

from jgtpov import calculate_tlid_range as get_tlid_range


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="Calculate tlid range")

    # Add the arguments
    parser.add_argument("-e", type=str, help="The end datetime")
    parser.add_argument("-t", type=str, help="The timeframe")
    parser.add_argument("-c", type=int, help="The number of periods")

    # Parse the arguments
    args = parser.parse_args()

    # Call get_tlid_range with the arguments
    result = get_tlid_range(args.e, args.t, args.c)

    # Print the result
    print(result)


if __name__ == "__main__":
    main()
