from hugo_nbconvert.date import get_date
import argparse
from pathlib import Path
import os
from hugo_nbconvert.resource import content, content_md

"""usage:

> hugo_nbnew ./content/post/a-demo-post
> hugo_new --ipynb/-n ./content/post/a-demo-post
create ipynb "a-demo-post/index.ipynb".

> hugo_new ./content/post/a-demo-post.ipynb
create ipynb "a-demo-post.ipynb".

> hugo_new ./content/post/a-demo-post.md
create markdown "a-demo-post.md".

> hugo_new ./content/post/a-demo-post
create markdown "a-demo-post/index.md".
"""


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="path and name for the new document")
    parser.add_argument(
        "--ipynb", "-n", help="create ipynb files", action="store_true", default=False
    )
    args = parser.parse_args()
    return args


def new_main():
    args = get_args()
    new(args)


def nbnew():
    args = get_args()
    args.ipynb = True
    new(args)


def new(args):
    name: str = args.name

    if ".md" in name or ".ipynb" in name:
        from hugo_nbconvert.tools import get_title_from_path

        target_path = Path(os.getcwd()).joinpath(name)
        title = get_title_from_path(target_path)
        new_doc = target_path

        # create files
        if ".ipynb" in name:
            content1 = content.replace("{date}", get_date()).replace("{title}", title)

            new_doc.write_text(content1)

            print(f"New content {new_doc} created.")
        else:
            content1 = content_md.replace("{date}", get_date()).replace(
                "{title}", title
            )
            new_doc.write_text(content1)
            print(f"New content {new_doc} created.")

    else:
        # is directory
        target_dir = Path(os.getcwd()).joinpath(name)
        if target_dir.exists():
            print(f"{name} already exists.")
            exit(-1)
        # create it
        target_dir.mkdir(parents=False)

        # get last path and title
        last_path: str = name.replace("\\", "/")
        if "/" in last_path:
            last_path = last_path[last_path.rfind("/") + 1 :]
        name2 = last_path.split("-")
        title = " ".join(map(str.title, name2))

        # create files
        if args.ipynb:
            new_doc = target_dir.joinpath("index.ipynb")
            content1 = content.replace("{date}", get_date()).replace("{title}", title)

            new_doc.write_text(content1)

            print(f"New content {new_doc} created.")
        else:
            new_doc = target_dir.joinpath("index.md")
            content1 = content_md.replace("{date}", get_date()).replace(
                "{title}", title
            )
            new_doc.write_text(content1)
            print(f"New content {new_doc} created.")
