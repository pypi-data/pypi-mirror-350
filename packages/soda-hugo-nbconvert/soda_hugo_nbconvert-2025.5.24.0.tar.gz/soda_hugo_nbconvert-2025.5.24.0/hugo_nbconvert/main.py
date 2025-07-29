from .glob_hugo_ipynb import get_files
from sodatools import Path, os
import argparse
import multiprocessing
from .markdown_convert import convert_proc


def get_args():
    parser = argparse.ArgumentParser(usage="""convert ipynb to markdown posts.
supported tags: hide_cell, hide_input, hide_output, collapse_cell, collapse_input, collapse_output.
""")
    parser.add_argument(
        "file_path",
        type=str,
        default="",
        help="ipynb file path (if not specified, will find and process all ipynb files)",
        nargs="?",
    )
    args = parser.parse_args()
    return args


conf_path = Path(__file__).resolve().parent.joinpath("nbconvert_config.py")


def main():
    args = get_args()
    files = []
    if args.file_path == "":
        files = get_files()
    else:
        file_path = Path(os.getcwd()).joinpath(args.file_path).resolve()
        if file_path.suffix == ".ipynb":
            files.append(file_path)

    api_convert_main(files)


def api_convert_main(files: list[Path]):
    processes = []
    for i in files:
        p = multiprocessing.Process(target=convert_proc, args=(i,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()


if __name__ == "__main__":
    main()
