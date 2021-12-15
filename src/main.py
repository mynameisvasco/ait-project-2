from argparse import ArgumentParser, Namespace
from find_lang import FindLang


class Main:
    args: Namespace

    def parse_args(self):
        arg_parser = ArgumentParser()
        arg_parser.add_argument("--references-dir", type=str,
                                required=True, dest="references_dir", help="Directory of the reference texts")
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
            find_lang = FindLang(self.args.references_dir)
            print(find_lang.find(self.args.target_file))
        else:
            print("Unknown mode, accepted values: locate-lang, find-lang")


if __name__ == "__main__":
    Main().main()
