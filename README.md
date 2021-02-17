# marko-backlinks

<div align="center">

[![Build status](https://github.com/jb-delafosse/marko-backlinks/workflows/build/badge.svg?branch=master&event=push)](https://github.com/jb-delafosse/marko-backlinks/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/marko-backlinks.svg)](https://pypi.org/project/marko-backlinks/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/jb-delafosse/marko-backlinks/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/jb-delafosse/marko-backlinks/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/jb-delafosse/marko-backlinks/releases)
[![License](https://img.shields.io/github/license/jb-delafosse/marko-backlinks)](https://github.com/jb-delafosse/marko-backlinks/blob/master/LICENSE)

</div>

## 🤔 Description

This project provide a markdown to markdown converter that adds a [Bi-Directional Link](https://maggieappleton.com/bidirectionals)
Section at the end of each markdown files that is converted.


The project also provide a [pre-commit hook](https://pre-commit.com/) so you can easily integrate it within your own projects easily

It relies heavily on the [Marko](https://github.com/frostming/marko/tree/master/marko) python package that is the only 
Markdown Parser with a Markdown Renderer that I know of.

## 💭 Why

I believe a great amount of information can be extracted from collaborative notes if we take time to structure them correctly.

I wanted:
- To make collaborative notes
- To organize the notes in a [Roam](https://roamresearch.com/) like manner
- Everyone to be able to navigate through the notes without installing anything
- This system to be easily adopted by a software engineering team.

Using git and this converter as a pre-commit, I can easily do all of this ! 🚀

## 🏃 Getting Started
<details>
  <summary>Installation as a python package with pip</summary>

Considering you already have python available. You can simply add th

```bash
pip install --user marko-backlinks
```

or install with `Poetry`

Then you can see all the option of the CLI using

```bash
marko-backlinks --help
```

</details>

<details>
  <summary>Installation as a pre-commit hook</summary>
This pre-commit hook use the [pre-commit](https://pre-commit.com) tool that you will
need to install.

Add the following line to your pre-commit configuration (`.pre-commit-config.yaml`) at the root of your 
repository.

```yaml
repos:
-   repo: https://github.com/jb-delafosse/marko-backlinks
    rev: v0.2.3
    hooks:
      - id: marko-backlinks
        args: ['directory-containing-my-markdown']
```

and install the hook using `pre-commit install`
</details>

## 🛡 License

[![License](https://img.shields.io/github/license/jb-delafosse/marko-backlinks)](https://github.com/jb-delafosse/marko-backlinks/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/jb-delafosse/marko-backlinks/blob/master/LICENSE) for more details.

## 📃 Citation

```
@misc{marko-backlinks,
  author = {jb-delafosse},
  title = {Awesome `marko-backlinks` is a Python cli/package created with https://github.com/TezRomacH/python-package-template},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/jb-delafosse/marko-backlinks}}
}
```

## Credits

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).
