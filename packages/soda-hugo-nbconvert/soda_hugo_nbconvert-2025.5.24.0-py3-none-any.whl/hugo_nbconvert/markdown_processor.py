from nbconvert.preprocessors import Preprocessor
import uuid


class CollapsePreprocessor(Preprocessor):
    def preprocess(self, nb, resources):
        grouped_cells = []
        collapse_group = []

        def generate_cell_id(id_length=8):
            return uuid.uuid4().hex[:id_length]

        def append_collapsed():
            # add details shorttag to beginning and end of collapse group.
            if len(collapse_group) == 1:
                grouped_cells.append(
                    {
                        "cell_type": "markdown",
                        "id": generate_cell_id(),
                        "metadata": {"tags": []},
                        "source": '{{< details summary="1 cell collapsed:" altSummary="1 cell expanded:" >}}',
                    }
                )
            else:
                grouped_cells.append(
                    {
                        "cell_type": "markdown",
                        "id": generate_cell_id(),
                        "metadata": {"tags": []},
                        "source": f'{{{{< details summary="{len(collapse_group)} cells collapsed:" altSummary="{len(collapse_group)} cells expanded:" >}}}}',
                    }
                )

            for c_cell in collapse_group:
                grouped_cells.append(c_cell)
            grouped_cells.append(
                {
                    "cell_type": "markdown",
                    "id": generate_cell_id(),
                    "metadata": {"tags": []},
                    "source": "{{< /details >}}",
                }
            )

        for cell in nb.cells:
            # check for cell.id
            if not hasattr(cell, "id") or cell.id is None:
                cell.id = generate_cell_id()

            # check for collapse_cell tag and add to collapse group
            if "collapse_cell" in cell.metadata.get("tags", []):
                collapse_group.append(cell)
            else:
                # format and add collapse group to grouped_cells
                if collapse_group:
                    append_collapsed()
                    collapse_group = []

                # collapse input/output
                if cell.cell_type == "code":
                    if "collapse_input" in cell.metadata.get("tags", []):
                        cell.source = f"{{{{< detailsInput >}}}}\n```python\n{cell.source}\n```\n{{{{< /detailsInput >}}}}"
                    if "collapse_output" in cell.metadata.get("tags", []):
                        new_outputs = []
                        for output in cell.outputs:
                            if "text" in output:
                                output["text"] = (
                                    f"{{{{< detailsOutput >}}}}\n{output['text']}\n{{{{< /detailsOutput >}}}}"
                                )
                            new_outputs.append(output)
                        cell.outputs = new_outputs

                # add cell to grouped cells
                grouped_cells.append(cell)

        # format and append last cells
        if collapse_group:
            append_collapsed()

        nb.cells = grouped_cells
        return nb, resources


def post_process(content: str) -> str:
    # collapsed inputs/outputs
    content = content.replace(
        "```python\n{{< detailsInput >}}",
        '{{< details summary="Input collapsed:" altSummary="Input expanded:" >}}',
    )
    content = content.replace(
        "{{< /detailsInput >}}\n```", "{{< /details >}}\n"
    )
    content = content.replace(
        "    {{< detailsOutput >}}",
        '{{< details summary="Output collapsed:" altSummary="Output expanded:" >}}',
    )
    content = content.replace(
        "    {{< /detailsOutput >}}", "{{< /details >}}\n"
    )

    return content