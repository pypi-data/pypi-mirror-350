from collection import occur_once, load_from_file
import argparse

def main():
    parser = argparse.ArgumentParser(description='Occurring once in the text')
    parser.add_argument('--file', type=str, help='Enter filename')
    parser.add_argument('--string', type=str, help='Enter a text')
    args = parser.parse_args()
    if args.file:
        text = load_from_file(args.file)
        result = occur_once(text)
        print(result)
    else:
        result = occur_once(args.string)
        print(result)


if __name__ == '__main__':
    main()