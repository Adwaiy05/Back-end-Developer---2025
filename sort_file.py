import argparse

def main():
    # Create parser for command line arguments
    parser = argparse.ArgumentParser(description="Sort or reverse lines in a file.")

    # Add a positional argument for the input file name
    parser.add_argument("file", help="Input file to process")

    # Add optional flag '-r' to reverse lines instead of sorting
    parser.add_argument("-r", "--reverse", action="store_true", help="Reverse lines instead of sorting")

    # Add optional '-o' to specify output file name
    parser.add_argument("-o", "--output", help="Output file to write results")

    # Parse the arguments given by user
    args = parser.parse_args()

    try:
        # Open and read all lines from the input file
        with open(args.file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        return

    # Remove trailing newlines for uniform processing
    lines = [line.rstrip('\n') for line in lines]

    # Either reverse lines or sort them ascending
    if args.reverse:
        lines = lines[::-1]  # Reverse lines
    else:
        lines.sort()         # Sort alphabetically ascending

    # Add newline character back to each line
    lines = [line + '\n' for line in lines]

    if args.output:
        # Write processed lines to the output file
        with open(args.output, 'w') as f:
            f.writelines(lines)
        print(f"Processed lines written to '{args.output}'")
    else:
        # Print processed lines to the console
        print("".join(lines))

if __name__ == "__main__":
    main()

