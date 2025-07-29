# TopoVec

## Installation

### Prerequisites

We recommend to Install [UV](https://docs.astral.sh/uv/) package manager according to the [manual](https://docs.astral.sh/uv/getting-started/installation/).

### Normal installation

If only GUI or scripts are going to be used, `topovec` can be installed as a tool.
E.g. using [UV](https://docs.astral.sh/uv/)

```sh
uvx tool install topovec
```

or using [pipx](https://github.com/pypa/pipx):

```sh
pipx install topovec
```

To use `topovec` in [jupter](https://jupyter.org/) or [marimo](https://github.com/marimo-team/marimo) notebook,
we suggest to use virtual environment.
UV provides very convenient way to proceed.
First create directory for you project:

```sh
uv init <your_project>
```

Then enter into the just create folder and install `topovec`:

```sh
cd <your_project>
uv add topovec
```

Most functionality of `topovec` are in plugins.
All the plugins can be installed using

```sh
uv add topovec --all-extras
```

Now you can start notebook as described [below](#First-steps).

### For development

Clone or download the repository:

```sh
git clone https://gitlab.com/alepoydes/topovec.git
```

Switch to the newly created directory:

```sh
cd topovec
```

Run UV to create virtual environment and install the library.

```sh
uv sync --all-extras
```

Most of the functionality are provided by plugins which have dependencies on external packages.
`--all-extras` will install all dependencies, which may lead to long installation time 
or incompatibilities with already installed software.
You can select which plugins to choose using `--extra` key.
For example, if we are interested only in OpenGL functionality, we can install only `mgl` plugin.

```sh
uv sync --extra mgl
```

## First steps

It is convenient to prepare plots for publication in a notebook.
To run [Jupter](https://jupyter.org/) Lab inside the environment associated with `topovec`,
run in the `topovec` folder the following command:

```sh
uv run --with jupyter jupyter lab
```

Demonstration of basic functionality of the library can be found in the notebook
[notebooks/demo1.ipynb](notebooks/demo1.ipynb).