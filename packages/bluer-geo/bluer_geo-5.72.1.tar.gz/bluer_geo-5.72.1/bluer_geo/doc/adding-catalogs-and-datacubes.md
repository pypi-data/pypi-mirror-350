# 🌐 adding catalogs and datacubes

to add a new [catalog](../catalog/) or [datacube](../datacube/) follow these steps,

0️⃣ copy and refactor [`notebooks/copernicus-v3.ipynb`](../../notebooks/copernicus-v3.ipynb).

1️⃣ clone [`catalog/copernicus`](../catalog/copernicus/) and define `NovelCatalog`.

2️⃣ clone [`catalog/copernicus/sentinel_2`](../catalog/copernicus/sentinel_2/) and define `NovelDatacube`.

3️⃣ add `NovelCatalog` and `NovelDatacube` to [`catalog/classes.py`](../catalog/classes.py).

4️⃣ add the package extensions to [`setup.py`](../../setup.py).

5️⃣ add the relevant secrets to,
- [`workflows/pytest.yml`](../../.github/workflows/pytest.yml)
- [`env.py`](../../bluer_geo/env.py)
- [`sample.env`](../../bluer_geo/sample.env)
- [`tests/test_env.py`](../../bluer_geo/tests/test_env.py)

6️⃣ add the relevant config variables to,
- [`config.env`](../../bluer_geo/config.env)
- [`env.py`](../../bluer_geo/env.py)
- [`tests/test_env.py`](../../bluer_geo/tests/test_env.py)

7️⃣ add the relevant test cases to,
- [`tests/datacube_get.sh`](../../bluer_geo/.abcli/tests/datacube_get.sh)
- [`tests/datacube_list.sh`](../../bluer_geo/.abcli/tests/datacube_list.sh)
- [`tests/help.sh`](../../bluer_geo/.abcli/tests/help.sh)
- [`tests/assets.py`](../../bluer_geo/tests/assets.py)

8️⃣ copy and refactor [`tests/test_catalog_copernicus_sentinel_2.py`](../../bluer_geo/tests/test_catalog_copernicus_sentinel_2.py).

9️⃣ add a relevant target,
```bash
@targets edit
```

🔟 copy and refactor [`targets/Jasper-template.md`](../../bluer_geo/watch/targets/Jasper-template.md).

1️⃣ 1️⃣ add references to,
- [`README.py`](../../bluer_geo/README.py).
- [`catalog/README.md`](../../bluer_geo/catalog/README.md).
- [`catalog/README.py`](../../bluer_geo/catalog/README.py).
- [`targets/README.py`](../../bluer_geo/watch/targets/README.py)