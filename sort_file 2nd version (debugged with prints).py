import argparse

def main():
    parser = argparse.ArgumentParser(description="Sort or reverse lines in a file.")
    parser.add_argument("file", help="Input file to process.")
    parser.add_argument("-r", "--reverse", action="store_true", help="Reverse line order instead of sorting alphabetically.")
    parser.add_argument("-o", "--output", help="Write result to an output file.")
    args = parser.parse_args()

    try:
        with open(args.file) as f:
            lines = [line if line.endswith('\n') else line + '\n' for line in f]
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        return

    lines = lines[::-1] if args.reverse else sorted(lines)

    if args.output:
        with open(args.output, 'w') as f:
            f.writelines(lines)
    else:
        print("".join(lines))

if __name__ == "__main__":
    main()