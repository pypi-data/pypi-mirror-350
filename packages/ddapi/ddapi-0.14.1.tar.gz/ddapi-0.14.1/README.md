ddapi is an api from the ddnet and qwik website

## Installation

```bash
  pip install ddapi
```

or

```bash
  pip install git+https://github.com/ByFox213/ddapi
```

## Usage/Examples

DDnet

```python
import asyncio

from ddapi import DDnetApi, DDPlayer


async def main():
    async with DDnetApi() as obj:
        user: DDPlayer = await obj.player("Cor")
    if user is not None:
        text = f"{user.player}: {user.points.points}/{user.points.total}"
        percent = round(user.points.total / user.points.points * 100)
        print(f"{text}({percent}%)")
        # Cor: 32950/32950(100%)
    else:
        print("Player not found")


asyncio.run(main())
```

Tested on Python
| 3.11 | 3.12 | 3.13 |
|------|------|------|
| ✅ | ✅ | ✅ |

[other examples](https://github.com/ByFox213/ddapi/tree/main/example)
