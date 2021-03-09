# Comparing two face databases
###### Nick DeMarchis, March 9, 2021, [ned004@](mailto:ned004@bucknell.edu)

## Getting started

All image data to test lives in the `ai-soc/test images` directory. I've stored data from CFD and UTK in `ai-soc/test images/CFD` and `ai-soc/test images/UTKFace` respectively, but hypothetically those folder names should not matter. They aren't stored on this GitLab directory for size considerations.

Ensure that `numpy`, `matplotlib` and `git-lfs` are installed. Run `main.py` to show the graphs for existing data in `ai-soc/data/data.json`. To make the API query, make sure that something is in the `ai-soc/test images` directory and set the `newImgsToCheck` to a number greater than 0.

## What does the code mean?
### `newImgsToCheck`

On line 8, you can see the following:
```python
# set this number for the new entries to check against the API
newImgsToCheck = 0
```
To prevent API overuse, the API will not be called more times than the number set here.

### `def parseData(obj)`
The object that this method takes in, regardless of the source database, is of the format: 
```python
obj = {
    'database': null,
    'fullPath': null,
    'score': null,
    'race': null,
    'gender': null,
}
```

### `def handleDictEntry(dict, obj, attribute)` 

Here, `dict` stands for the dictionary that we're going to incorporate this object into (either `gender`, `race`, or `intersectional`), `obj` is the object as described above, and `attribute` is the type of attribute handled and compared in that dictionary. For instance, in the `genderDict`, the possible `attribute`s are `"M"` or `"F"`.


## Databases used

Ma, D. S., Correll, J., & Wittenbrink, B. (2015). The Chicago face database: A free stimulus set of faces and norming data. Behavior research methods, 47(4), 1122–1135. [https://doi.org/10.3758/s13428-014-0532-5](https://doi.org/10.3758/s13428-014-0532-5)

[UTKFace](https://susanqq.github.io/UTKFace/)