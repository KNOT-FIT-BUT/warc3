# knot-warc - Python library to work with Web ARChive files

*Note: This is one of forks of original WARC repository.*
<details>
<summary>Fork history</summary>

1. https://github.com/internetarchive/warc (original Python 2 library)
2. https://github.com/recrm/warc3 (Python 3 port)
3. https://github.com/jpbruinsslot/warc3 (Python 3 port)
4. https://github.com/Willian-Zhang/warc3 (WET support)
</details>

WARC (Web ARChive) is a file format for storing web crawls (see http://bibnum.bnf.fr/WARC/).

This `warc` library makes it very easy to work with WARC files.:
```python
import warc
with warc.open("test.warc") as f:
    for record in f:
        print(record['WARC-Target-URI'], record['Content-Length'])
```

And WET files.:
```python
import warc
with warc.open("test.warc.wet") as f:
    for record in f:
        print(record['WARC-Target-URI'], record['Content-Length'])
```

## Documentation

The documentation of the warc library is available at http://warc.readthedocs.org/.

Apart from the install from pip, which will not work for this warc3 version, the
interface as described there is unchanged.

### Installation of this version

If you want to use this version of WARC library, use this command for installation (for pip):
```shell
pip install knot-warc
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

**0.2.4**:
- Fix for Python 3.10+

**0.2.3**
- Support seeking in WARC/WET

**0.2.2**
- Allow WET parse

**Older...**
- see https://github.com/internetarchive/warc
