# Igor's Utilities
I made these tools for myself, but you're welcome to use them if they're helpful.


## Download
```bash
pip install xmelutils
```

> if new version released add: --update

## Quickstart

```python
from xmelutils import many_count

text = "zxc123QWERTYwasd"

print(many_count(text, "z1w")) # result: 4 (case_insensitive=False by default)


print(many_count(text, "Wx1", case_insensitive=True)) # result: 3 (case_insensitive=True -> "w" != "W")
```

## Documentation

Full documentation available on [Read the Docs](https://xmelutils.readthedocs.io/)

## License

Project used [MIT License](LICENSE)

## Contributing

To contribute into the project follow instructions in [Contributing file](CONTRIBUTING.md)