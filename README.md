# skimread_pdf

Terrible way to read a paper, wouldn't recommend

## Install
```
sudo apt install vim
pip install pdf2txt
# add skimread_pdf, clean_pdf2txt.py, speedread to path (however you wanna do it)
cp speedread/speedread ~/.local/bin
cp clean_pdf2txt.py ~/.local/bin
cp skimread_pdf ~/.local/bin
```

## Usage
Short pipeline starts with
```
skimread_pdf usage: skimread_pdf [options] in.pdf
optional:
	-m, --man	 [enter vim before speedread]
	-o, --out	 [outdir for .txt files]
  -h, --help [show this message]
```
Which uses this cleanup script to make speedreader have something resembling readable.
```
Usage: clean_pdf2txt.py [OPTIONS] FILENAME

  Removes figure text that clumps in patches

Options:
  -o, --outdir TEXT  Output direectory (default current)
  -r, --auto-ref     Use bad regex to remove reference section  [default:
                     True]
  -f, --auto-fig     Remove figure legends  [default: True]
  -s, --auto-sup     Remove supplementary matertial  [default: True]
  --help             Show this message and exit.
```
Defaults try their harderest to remove figure legends, in text reference to figures, references, and the supplementary section, but it doesn't always work too well.
