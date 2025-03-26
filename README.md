# Tool for Emulating the PAdES Qualified Electronic Signature

This is a project made for the course of Security of Computer Systems at the Gdańsk University of Technology.

Documentation is available on the [GitHub Pages](https://ketrab2003.github.io/pades-emulation/).

## Requirements

All the requirements are listed in the `requirements.txt` file. You can install them by running:
```bash
pip install -r requirements.txt
```

## Usage

Thare are three GUI applications in this project:

Generate the private and public keys:
```bash
python3 generate.py
```

Sign the file:
```bash
python3 sign.py
```

Verify the signature:
```bash
python3 verify.py
```

## Generating documentation

To generate the documentation, you need to have `doxygen` installed.

To generate the documentation, run in the project root directory:
```bash
doxygen
```

## Authors

- Krawisz Bartłomiej [@ketrab2003](https://github.com/ketrab2003)
- Nieradko Stanisław [@KanarekLife](https://github.com/KanarekLife)