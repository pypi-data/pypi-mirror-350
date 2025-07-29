# hugo-nbconvert
convenient tools for intergrating jupyter notebooks with hugo

## migration notice

project migrated from [soda-hugo-nbconvert][1] to [hugo-nbconvert][2] on PYPI

[1]: https://pypi.org/project/soda-hugo-nbconvert/
[2]: https://pypi.org/project/hugo-nbconvert/

## Usage

in a hugo site's root or parent dir:

- create ipynb post:
```
hugo_nbnew .\test_site\content\post\test-hugo-page
```

- convert:
```
hugo_nbconvert
```
