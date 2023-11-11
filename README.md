# knot-warc - Python library to work with Web ARChive files

*Note: This is one of forks of original WARC repository. It was primarily created for projects of [Knowledge Technology Research Group](https://knot.fit.vutbr.cz/), but its public-wide usage isn't limited.*
<details>
<summary>Fork history</summary>

1. https://github.com/internetarchive/warc (original Python 2 library)
2. https://github.com/recrm/warc3 (Python 3 port)
3. https://github.com/jpbruinsslot/warc3 (Python 3 port)
4. https://github.com/Willian-Zhang/warc3 (WET support)
</details>

WARC (Web ARChive) is a file format for storing web crawls (see http://bibnum.bnf.fr/WARC/).

## Examples

This `warc` library makes it very easy to work with WARC files:
```python
import warc
with warc.open("test.warc") as f:
    for record in f:
        print(record['WARC-Target-URI'], record['Content-Length'])
```

And WET files:
```python
import warc
with warc.open("test.warc.wet") as f:
    for record in f:
        print(record['WARC-Target-URI'], record['Content-Length'])
```

There are some examples provided without warranty and support (just for inspiration) in [examples](https://github.com/KNOT-FIT-BUT/warc3/tree/master/examples) folder. They are not updated at all, too.

## Documentation

The documentation of this fork of the warc library is on [Github Pages](https://knot-fit-but.github.io/warc3) (alternatively see [original documentation](http://warc.readthedocs.org/)).

## Installation

You can install this fork of warc library using [pip](http://www.pip-installer.org/):
```shell
pip install warc-knot
```

## License

This software is licensed under GPL v2. See [LICENSE](http://github.com/internetarchive/warc/blob/master/LICENSE) file for details.

## Authors

**Original Python2 Versions:**
- Anand Chitipothu
- Noufal Ibrahim

**Python3 Port:**
- Ryan Chartier 
- Jan Pieter Bruins Slot
- Almer S. Tigelaar

**Modifications:**
- Willian Zhang
- Michal Šmahel

## Change Log

This is just a changelog for older releases created by older contributors to the WARC project (throw various forks).
Change log of this fork is available in GitHub [releases](https://github.com/KNOT-FIT-BUT/warc3/releases).

**0.2.3**
- Support seeking in WARC/WET

**0.2.2**
- Allow WET parse

**Older...**
- see https://github.com/internetarchive/warc
