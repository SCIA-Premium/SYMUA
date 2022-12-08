# SYMUA

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