# PocketMod Creator

Python script to convert a PDF into a PocketMod PDF.

![usage example](media/explainer.png)

## What is a PocketMod?
See [pocketmod.com](https://pocketmod.com/) or search online for "PocketMod"
for more information.

*Searching online for "pocket mod" (two words) will bring up information*
*about an*
electric scooter
*- this script will **not** create an electric scooter!*

## Installation

Clone or download this repository.

## How to use

### Requirements

Before running this script you will need to have installed:

- [Python](https://www.python.org/) (3.x)
- [PyPDF2](https://github.com/mstamy2/PyPDF2)

PyPDF2 can be installed via pip with:

```bash
$ pip install PyPDF2
```

If you get an ImportError for PyDF2 when running the code make sure that you have installed PyPDF2 into the correct version of Python (if you have multiple versions installed on your machine) and that you are executing the correct version of Python.
See issue [#1][i1].

### Running the script

Go to the directory where the `pocketmod_creator.py` script is located.
Open the terminal and type the following where `input.pdf` is the PDF you want
converted.

```bash
$ python pocketmod_creator.py input.pdf
```

The script will generate and output a time-stamped PDF in the current
directory:

```bash
$ ls
input.pdf  output_20200408112034.pdf  pocketmod_creator.py
```

If `input.pdf` is in another directory then it can referenced as below.
However, the output PDF will still be in the directory of the
`pocketmod_creator.py` script.

```bash
$ python pocketmod_creator.py some/other/location/input.pdf
```
 
> **Currently this script assumes the input file is an A4 size PDF,**
> **and it will generate an A4 size PDF as output.**

## Contact

Email :
  mullinscr@gmail.com

Repo :
  https://github.com/mullinscr/pocket-mod

## Contribute

Create an issue and let me know of any additions or features you would like.
Or fork the repo and send me a pull request.

## License

This project is licensed under the MIT license - see `LICENSE.txt`.

## TODO

- Allow more flexibility with input and output paper sizes (A3, US letter etc.)
- Add another CLI argument for naming the output file.
- Allow for multiple input files.

[i1]: https://github.com/mullinscr/pocketmod-creator/issues/1
