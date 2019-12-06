# HTTP status codes

This little tool gets HTTP status codes from

`https://raw.githubusercontent.com/psf/requests/master/requests/status_codes.py`

It's just a little helper tool to avoid checking various online sources for HTTP status codes.

For now, all the codes are listed when doing:
```
    python get_status_codes.py
```


There are many possible optimisations like:
* Caching values to avoid requesting every time
* Add cli options (`argparse`)
  - Get all.
  - Get single.
* Add `setup.py` with executable script


The result looks like this:
```
100 ['continue']
101 ['switching_protocols']
102 ['processing']
103 ['checkpoint']
122 ['uri_too_long', 'request_uri_too_long']
200 ['ok', 'okay', 'all_ok', 'all_okay', 'all_good', '\\\\o/', '✓']
201 ['created']
202 ['accepted']

```
