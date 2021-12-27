from argparse import ArgumentParser, Namespace
from find_lang import FindLang


class Main:
    args: Namespace

    def parse_args(self):
        print("MOCK" == "Моск")
        arg_parser = ArgumentParser()
        arg_parser.add_argument("--references-dir", type=str,
                                required=True, dest="references_dir", help="Directory of the reference texts")
        arg_parser.add_argument("--references-chars", type=int,
                                required=False, default=None, dest="references_chars", help="Number of chars to use for all references")
        arg_parser.add_argument("--target-chars", type=int,
                                required=False, default=None, dest="target_chars", help="Number of chars to use for the target")
        arg_parser.add_argument("--target-file", type=str,
                                required=True, dest="target_file", help="File of the target text")
        arg_parser.add_argument("--mode", type=str, dest="mode", required=True,
                                help="Mode of the program, accepted values: locate-lang, find-lang")
        self.args = arg_parser.parse_args()

    def main(self):
        self.parse_args()

        if self.args.mode == "locate-lang":
            pass
        elif self.args.mode == "find-lang":
            find_lang = FindLang(self.args.references_dir,
                                 self.args.target_file, self.args.references_chars, self.args.target_chars)
            results = find_lang.find()
            print(f"Results: {results[0][0]} ({results[0][1]}) bits")
            print("Top 10")

            for i, (lang_name, bits) in enumerate(results[:11]):
                print(f"{i + 1}. {lang_name} ({bits}) bits")
        else:
            print("Unknown mode, accepted values: locate-lang, find-lang")


if __name__ == "__main__":
    Main().main()
