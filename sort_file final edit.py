import argparse

def main():
    # Parser set-up + defining arguments
    parser = argparse.ArgumentParser(description="Sort or reverse lines in a file.")
    parser.add_argument("file", help="Input file for processing.")
    parser.add_argument("-r", "--reverse", action="store_true", help="Sort lines in reverse.")
    parser.add_argument("-o", "--output", help="Write values to an output file.")
    args = parser.parse_args()
    # Trying to open input file for read
    try:
        with open(args.file) as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' is not found.")
        return
    except PermissionError:
        print(f"Error: Not given permission to access '{args.file}'.")
        return

    # Every line ends with a newline character
    lines = [line if line.endswith('\n') else line + '\n' for line in lines]
    # Sort lines in reverse
    lines = sorted(lines, reverse=args.reverse)
    # Write sorted lines if output file specified
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.writelines(lines)
        except PermissionError:
            print(f"Error: Not possible to write to '{args.output}' as not permitted ")
    else:
        print("".join(lines))

if __name__ == "__main__":
    main()
