# SYMUA [![Profile][title-img]][profile]

[title-img]:https://img.shields.io/badge/-SCIA--PRIME-red
[profile]:https://github.com/Pypearl


## AUTHORS
Adrien Houpert \<adrien.houpert@epita.fr\>\
Alexandre Lemonnier \<alexandre.lemonnier@epita.fr\>\
Alexandre Rulleau \<alexandre.rulleau@epita.fr\>\
Baptiste Bourdet \<baptiste.bourdet@epita.fr\>\
Sarah Gutierez \<sarah.gutierez@epita.fr\> \
Victor Simonin \<victor.simonin@epita.fr\>

---

## The project

For our project, we have chosen to represent a pedestrian flow simulation. We choose this project
due to the recent events that happened in Seoul where people have been crushed to death during
Halloween at Itaewon. Also, we decided to test our agent model on the heavy pedestrian traffic of
Shibuya crossing to analyze at which point this place is too crowded to circulate or even survive.


To ease our task we started from the crowddynamics project which already implements the engine we
need. Therefore, we started this project and implemented our idea by adding new agent behaviors
and maps, we also fixed pre-existing bugs.

---

## Usage

The environment installation could be made and run with the following commands :

```bash
cd src/qtgui
conda create --name symua python=3.8
conda activate symua
pip install -r require.txt
conda install -c conda-forge scikit-fmm
conda install shapely
python cli.py run
```

Open test.py file in GUI.
