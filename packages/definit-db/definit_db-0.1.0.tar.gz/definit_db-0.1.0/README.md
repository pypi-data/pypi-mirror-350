# DefinIT database

## Build and upload the package
```
(optional cleanup) rm -rf dist/ build/ src/*.egg-info/

python -m build

python -m twine upload dist/*
```
## Generate tracks
```
python -m definit_db.data.track.track
```