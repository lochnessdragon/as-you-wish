# [As You Wish](https://www.youtube.com/watch?v=3toktnaqAyE)
A simple python configuration library that works like Minecraft Forge's Config classes.
I was fed up by the fact that the ```configparser``` library had little to no support for comments on values
and also support for restoring configurations from a corrupted state.
I also wanted a library that would validate that certain config values where of the correct type, so this is it.

## Backends
The only current backend is the ```configparser``` library, but I would might add support for more,
such as yaml, json, toml, etc.

## Installation
Run ```pip install as-you-wish``` to use this project.

## Usage
Example program usage:
```python
from as_you_wish import Config

settings = Config()
settings.define('service.api_key', 'YOUR_API_KEY', 'needed to connect to the api service')

settings.load('settings.ini')

print(f"API_KEY={settings.get('service.api_key')}")
```

Also check out the [docs]() and [tests]() for more api usage.

## Contributing
We'd love the help. Unfortunately we don't have a Contributing.md document yet, but if you find an issue/bug/feature request, feel free to submit it with a PR or under the Issues tab.

Thanks for checking us out! (The Kingdom of Florin 🏰 is yours.)
