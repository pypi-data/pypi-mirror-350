<p align="center">
    <a href="https://pypi.org/project/moex"><img src="https://gitlab.com/aioboy/moex/-/raw/master/assets/cover.gif" alt="MOEX"></a>
</p>
<p align="center">
    <a href="https://pypi.org/project/moex"><img src="https://img.shields.io/pypi/v/moex.svg?style=flat-square&logo=appveyor" alt="Version"></a>
    <a href="https://pypi.org/project/moex"><img src="https://img.shields.io/pypi/l/moex.svg?style=flat-square&logo=appveyor&color=blueviolet" alt="License"></a>
    <a href="https://pypi.org/project/moex"><img src="https://img.shields.io/pypi/pyversions/moex.svg?style=flat-square&logo=appveyor" alt="Python"></a>
    <a href="https://pypi.org/project/moex"><img src="https://img.shields.io/pypi/status/moex.svg?style=flat-square&logo=appveyor" alt="Status"></a>
    <a href="https://pypi.org/project/moex"><img src="https://img.shields.io/pypi/format/moex.svg?style=flat-square&logo=appveyor&color=yellow" alt="Format"></a>
    <a href="https://pypi.org/project/moex"><img src="https://img.shields.io/pypi/wheel/moex.svg?style=flat-square&logo=appveyor&color=red" alt="Wheel"></a>
    <a href="https://pypi.org/project/moex"><img src="https://img.shields.io/gitlab/pipeline-status/aioboy%2Fmoex?branch=master&style=flat-square&logo=appveyor" alt="Build"></a>
    <a href="https://pypi.org/project/moex"><img src="https://gitlab.com/aioboy/moex/-/raw/master/assets/coverage.svg" alt="Coverage"></a>
    <a href="https://pepy.tech/project/moex"><img src="https://static.pepy.tech/personalized-badge/moex?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads" alt="Downloads"></a>
    <br><br><br>
</p>

# MOEX

A little bit complex and more powerful implementation for [ISS Queries](https://iss.moex.com/iss/reference/).

## INSTALL

```bash
pip install moex
```

## USAGE

```python
import asyncio
from moex import AsyncMoex


async def main(amoex):
    async with amoex:
        amoex.show_templates()

        template_id = 409
        for tmpl in amoex.find_template("/candles"):
            print(f"Template: {tmpl.id}. Path: {tmpl.path}")
            await amoex.show_template_doc(tmpl.id)
            template_id = tmpl.id

    async with amoex:
        for stock in ("SNGSP", "YNDX"):
            url = amoex.render_url(
                template_id, engine="stock", market="shares", security="SNGSP", board="TQBR"
                )
            dt_params = {"from": "2025-05-01", "till": "2025-05-20", "interval": "60"}
            candles = await amoex.execute(url=url, **dt_params)
            df = candles.to_df()
            print(df)

amoex = AsyncMoex()
loop = asyncio.get_event_loop()
loop.run_until_complete(main(amoex))
```
