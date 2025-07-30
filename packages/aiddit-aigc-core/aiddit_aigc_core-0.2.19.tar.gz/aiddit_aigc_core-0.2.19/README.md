addit aigc core
==============================

## Installation

```bash
pip install aiddit_aigc_core

pip install --upgrade aiddit_aigc_core

pip install aiddit_aigc_core==0.1.1
```

## pypi打包
```bash
pip freeze -> requirements.txt  
```

```bash
rm -rf dist/ build/ *.egg-info 
```

```bash
python setup.py sdist bdist_wheel 
```

```bash
twine upload dist/*
```

