import argparse

def main():
    parser = argparse.ArgumentParser(description="Sort lines of a file.")
    parser.add_argument("file", help="The file to sort.")
    parser.add_argument("-r", "--reverse", action="store_true", help="Reverse the order of lines instead of sorting alphabetically.")
    parser.add_argument("-o", "--output", metavar="OUTPUT", help="Write output to a file.")
   
    args = parser.parse_args()

    print("=== Parsed Command Line Input ===")
    print(f"  Positional argument - file: {args.file}")
    print(f"  Optional flag - reverse: {args.reverse}")
    print(f"  Optional option - output: {args.output}")

    try:
        with open(args.file, 'r') as f:
            lines = f.readlines()
        print("\n[DEBUG] Lines after reading file:")
        print(repr(lines))
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        return

    # Fix missing newline characters at the end of lines
    lines = [line if line.endswith('\n') else line + '\n' for line in lines]
    print("\n[DEBUG] Lines after fixing missing newlines:")
    print(repr(lines))

    # Reverse order or sort ascending
    if args.reverse:
        lines = lines[::-1]  # Reverse the original line order
    else:
        lines.sort()         # Sort alphabetically ascending
    print("\n[DEBUG] Lines after processing (reverse/sort):")
    print(repr(lines))

    if args.output:
        print("\n[DEBUG] Writing the following lines to output file:")
        print(repr(lines))
        with open(args.output, 'w') as f:
            f.writelines(lines)
        print(f"\nSorted lines written to '{args.output}'")
    else:
        print("\n=== Sorted Lines ===")
        print("".join(lines))

if __name__ == "__main__":
    main()
