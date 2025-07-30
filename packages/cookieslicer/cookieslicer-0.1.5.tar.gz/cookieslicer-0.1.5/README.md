# Library Package: cookieslicer

|   |   |
|---|---|
|Project|[![Version](https://img.shields.io/pypi/v/cookieslicer.svg)](https://pypi.org/project/cookieslicer)  [![Python Versions](https://img.shields.io/pypi/pyversions/cookieslicer.svg)](https://pypi.org/project/cookieslicer)  ![platforms](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)  [![License](https://img.shields.io/github/license/jackdewinter/cookieslicer.svg)](https://github.com/jackdewinter/cookieslicer/blob/main/LICENSE.txt)  [![GitHub top language](https://img.shields.io/github/languages/top/jackdewinter/cookieslicer)](https://github.com/jackdewinter/cookieslicer)|
|Quality|[![GitHub Workflow Status (event)](https://img.shields.io/github/workflow/status/jackdewinter/cookieslicer/Main)](https://github.com/jackdewinter/cookieslicer/actions/workflows/main.yml)  [![Issues](https://img.shields.io/github/issues/jackdewinter/cookieslicer.svg)](https://github.com/jackdewinter/cookieslicer/issues)  [![codecov](https://codecov.io/gh/jackdewinter/cookieslicer/branch/main/graph/badge.svg?token=PD5TKS8NQQ)](https://codecov.io/gh/jackdewinter/cookieslicer)  [![Sourcery](https://img.shields.io/badge/Sourcery-enabled-brightgreen)](https://sourcery.ai)  ![snyk](https://img.shields.io/snyk/vulnerabilities/github/jackdewinter/cookieslicer) |
|  |![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/cookieslicer/black/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/cookieslicer/flake8/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/cookieslicer/pylint/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/cookieslicer/mypy/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/cookieslicer/pyroma/main)  ![GitHub Pipenv locked dependency version (branch)](https://img.shields.io/github/pipenv/locked/dependency-version/jackdewinter/cookieslicer/pre-commit/main)|
|Community|[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/jackdewinter/cookieslicer/graphs/commit-activity) [![Stars](https://img.shields.io/github/stars/jackdewinter/cookieslicer.svg)](https://github.com/jackdewinter/cookieslicer/stargazers)  [![Forks](https://img.shields.io/github/forks/jackdewinter/cookieslicer.svg)](https://github.com/jackdewinter/cookieslicer/network/members)  [![Contributors](https://img.shields.io/github/contributors/jackdewinter/cookieslicer.svg)](https://github.com/jackdewinter/cookieslicer/graphs/contributors)  [![Downloads](https://img.shields.io/pypi/dm/cookieslicer.svg)](https://pypistats.org/packages/cookieslicer)|
|Maintainers|[![LinkedIn](https://img.shields.io/badge/-LinkedIn-black.svg?logo=linkedin&colorB=555)](https://www.linkedin.com/in/jackdewinter/)|

The cookieslicer project was born out of a simple need: to have a templating system
that we could apply multiple times as our knowledge grew.  With multiple open source
projects being maintained, it was becoming difficult to remember which versions
of which files were "the best".  While the [cookiecutter](https://github.com/cookiecutter/cookiecutter)
project is a good first step to solving these problems, we felt it needed something
in front of it to help control the templating.

The cookieslicer application adds three files to a project that assist it in maintaining
good templates.  The source directory is the location of the template to be applied,
and contains a `cookieslicer.json` file that gives addition instructions on how
to handle certain situations that arise when re-applying a template.  The output
directory is the location that the template is applied to.  This directory contains
a `cookiecutter-config.yaml` that is applied to the template in the source directory
using `cookiecutter`.  This directory also contains a `cookieslicer.json` file with
configuration information for the cookieslicer application.

The rest of the process is (mostly) simple.  Cookieslicer uses the `cookiecutter-config.yaml`
file and the source directory to generate a completed template in a temporary directory.
With that template including the source directory's `cookieslicer.json` file, cookieslicer
then checks to see if the source directory's template version is the same as the
output directory's template version, quickly exitting if they are the same.  Otherwise,
the source directory's `cookieslicer.json` file tells Cookieslicer how to alter files
in the output directory.

Outside of a normal file copy, there are three different modes in which this happens.
The `once` mode instructs Cookieslicer to only copy a file if it does not exist
in the output directory.  The `attention` mode instructs Cookieslicer to copy the
file if it is different and to place it on an attention list.  This list is relayed
to the end-user at the end of the templating.  Finally, the `remove` mode instructs
Cookieslicer to remove a file with a specific path from the output directory. While
we are not sure if this is a complete list of actions to take, we feel that it was
a good enough list to start with.

## Requirements

This project required Python 3.8 or later to function.

## Installation

```sh
pip install cookieslicer
```

## How To Use This Package

NOTE: This project is under development.  More to come in the following weeks.

### Examples

For concrete examples that show the power of this library package, please consult
the [Examples Document](./docs/examples.md).  If you come up with a normal example
of how to use our package that we have missed, or come up with a novel example of
how to use our package, please file an issue using the process below and let us
know. From our experience, one example can often paint a picture of how to use our
project that is difficult to explain clearly with just words.

## Issues and Future Plans

If you would like to report an issue with the library or the documentation, please
file an issue [using GitHub](https://github.com/jackdewinter/cookieslicer/issues).
Please remember to fill in as much information as possible including a good, repeatable
pattern for reproducing the issue.  Do not overflow us with too much information,
but provide us with enough information to make the problem evident to us.

If you would like to us to implement a feature that you believe is important, please
file an issue [using GitHub](https://github.com/jackdewinter/cookieslicer/issues)
that includes what you want to add, why you want to add it, and why it is important
to you, and how you think it will help others.  We truly want to listen to what
you see as a good feature, so please do not be upset if we say "no" or "let me
think about it".

Please note that the issue you file will usually be the start of a conversation,
so be ready for more questions.  If you have any Python developer skills, please
mention that as well.  The conversations about "hey, can you..." is a lot different
than "if I do... can I add it to the project?".

## When Did Things Change?

The changelog for this project is maintained [at this location](/changelog.md).

## Still Have Questions?

If you still have questions, please consult our
[Frequently Asked Questions](/docs/faq.md) document.

## Instructions For Contributing

Developer notes on various topics are kept in the the
[Developer Notes](/docs/developer.md) document.

If you attempting to contribute something to this project,
please follow the steps outlined in the
[CONTRIBUTING.md](/CONTRIBUTING.md) file.
