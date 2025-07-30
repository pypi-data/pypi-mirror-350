# wm-tex

Automatically reference a URL with the wayback machine in BibTeX

## Usage

```
$ wm-tex http://google.com

@misc{xxx98},
  title   = {{}},
  author  = {},
  day     = {11},
  month   = {11},
  year    = {1998},
  url     = {https://web.archive.org/web/20250527083831/https://google.com/},
  ourl    = {http://google.com},
  howpublished = {\href{https://web.archive.org/web/20250527083831/https://google.com/}{http://google.com}},
  urldate = {2025-05-27},
}
```

## Install

**uv** (recommended):

```
uv tool install --compile-bytecode wm-tex
```

Don't have `uv`? https://docs.astral.sh/uv/getting-started/installation

**pip**:

```
pip install wm-tex
```

## Reference

- https://github.com/ecomaikgolf/wm-tex
- https://pypi.org/project/wm-tex/
