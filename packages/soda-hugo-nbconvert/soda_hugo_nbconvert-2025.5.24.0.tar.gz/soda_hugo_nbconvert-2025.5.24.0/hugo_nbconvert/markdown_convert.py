from .markdown_processor import post_process
from sodatools import Path
from nbconvert import MarkdownExporter
from .markdown_processor import CollapsePreprocessor
from traitlets.config import Config


# reference: https://racedorsey.com/posts/2024/jupyter-notebook-hugo/
def get_config():
    c = Config()

    c.TagRemovePreprocessor.enabled = True
    c.TagRemovePreprocessor.remove_cell_tags = ["hide_cell"]
    c.TagRemovePreprocessor.remove_input_tags = ["hide_input"]
    c.TagRemovePreprocessor.remove_all_outputs_tags = ["hide_output"]
    c.MarkdownExporter.preprocessors = [CollapsePreprocessor]
    return c


def convert_proc(file: Path):
    CustomExporter = MarkdownExporter(config=get_config())
    (body, resources) = CustomExporter.from_file(file)
    if file.stem == "index":
        resource_dir = file.parent.joinpath(file.stem + "_files")
        if resource_dir.exists() and resource_dir.is_file():
            resource_dir.unlink()

        md_text = body
        if len(resources["outputs"]) >= 1:
            resource_dir.mkdir(exist_ok=True)
            for fn, content in resources["outputs"].items():
                resource_dir.joinpath(fn).write_bytes(content)
                md_text = md_text.replace(f"({fn})", f"({file.stem + '_files'}/{fn})")
    else:
        resource_dir = file.parent  # post
        resource_dir = resource_dir.parent  # content
        resource_dir = resource_dir.parent  # site
        resource_dir = resource_dir.joinpath("assets")

        if not resource_dir.exists():
            print("fatal: cannot find assets directory")
            exit(-1)

        md_text = body
        if len(resources["outputs"]) >= 1:
            resource_dir.mkdir(exist_ok=True)
            for fn, content in resources["outputs"].items():
                new_file_name = file.stem + "-" + fn
                resource_dir.joinpath(new_file_name).write_bytes(content)
                md_text = md_text.replace(f"({fn})", f"(/{new_file_name})")

    md_text = post_process(md_text)
    markdown_file = file.with_suffix(".md")
    # markdown_file = markdown_file.with_stem(markdown_file.stem + "-gen")
    markdown_file.write_text(md_text, encoding="utf8")
