# NIX Suite

A set of tools used to format NIX compatible databases. 

## Installation

```bash
pip install nixWrapper 
```

## Usage

```python
import nixWrapper
nixWrapper.loadLibrary('labkeyInterface')
import labkeyInterface
...
```

## Use with virtualenv

Create virtualenv called `nix` where we will use nixWrapper:
```bash
:~$ cd $HOME
:~$ mkdir venv
:~$ cd venv
:~/venv$ virtualenv -p python3 nix
:~/venv$ . ./nix/bin/activate
(nix) $:~/venv$ cd
(nix) $:~$ pip install nixWrapper
```
Whenever you need `nixWrapper` in your code, simply run:
```bash
:~$ ~/venv/nix/python3 yourScript.py
```
where in your script `yourScript.py` you use nixWrapper directly like in Usage section.

## Use virtualenv in jupyter

To integrate `nixWrapper` installed in virtualenv with your jupyter code, jupyter needs
to be aware of virtualenv. To do that:
```bash
:~$ . ~/venv/nix/bin/activate
(nix) :~$ pip install ipykernel
(nix) :~$ python -m ipykernel install --user --name=nix
Installed kernelspec nix in /home/<your name>/.local/share/jupyter/kernels/nix
```
More info [here][venvJupyter].

## Developer notes

[Packaging][pypiTutorial] howto.

[pypiTutorial]: https://packaging.python.org/en/latest/tutorials/packaging-projects/
[venvJupyter]: https://docs.support.arc.umich.edu/python/jupyter_virtualenv/
