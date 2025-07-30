# Task Commit

Tool for formatting commits following the Conventional Commits pattern and recognizing Git Flow branches.

## Installation

To install the package, use:

```bash
pip install task-commit
```

## Usage

For first confugure repository:

```bash
task_commit_init

```

For commit:

```bash
task_commit

```

# To Development:

Download the repository: https://github.com/WalefyHG/Task_Commit.git

## Install Poetry:

```bash
pip install poetry

```

## Change config poetry:
```bash
poetry config virtualenvs.in-project true

```

## Create virtual environment:

```bash
poetry shell

```

## Install dependencies:

```bash
poetry install

```

## Install Pre-commit:

```bash
poetry run pre-commit install

```


## Manager Translates:

### Install new language:
```bash
python manage_translations.py addlanguage

```

### Update language:

```bash
python manage_translations.py update

```