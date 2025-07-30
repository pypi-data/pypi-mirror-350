# cz-nhm

This is a [commitizen](https://commitizen-tools.github.io/commitizen) config used by the Natural History Museum's Informatics team.

Install with:
```shell
pip install git+https://github.com/NaturalHistoryMuseum/cz-nhm.git
```

Then use by setting the commitizen config name to `cz_nhm`, e.g. in `pyproject.toml`:
```toml
[tool.commitizen]
name = "cz_nhm"
version = "1.0.0"
tag_format = "v$version"
version_files = [
    "pyproject.toml:version"
]
```
