# x9

## Description
A high advanced URL generator to detect XSS, Open Redirect in mass hunt.

Suppose you have a lot of urls, gathered from manual crawling or passive recon by GAU or Waybackurls. How you can test injection on all parameters of all urls?
By x9, you will be provided a huge list urls with payload-injected parameters using different strategies to encrease chance finding a reflection or redirection. To test XSS or Open redirect vulnerabilities on these urls, you need suitable nuclei templates.

Under developing ...

## Usage

main.py [-h] -l LIST [-p PARAMETERS] [-c CHUNK] -v VALUE -gs {normal,ignore,combine,all} -vs {replace,suffix} [-o OUTPUT] [-d]

x9

options:
  -h, --help            show this help message and exit
  -l LIST, --list LIST  List of urls to edit
  -p PARAMETERS, --parameters PARAMETERS
                        Parameter wordlist to fuzz
  -c CHUNK, --chunk CHUNK
                        Chunk to fuzz the parameters. [default: 15)]
  -v VALUE, --value VALUE
                        Value for parameters to FUZZ
  -gs {normal,ignore,combine,all}, --generate-strategy {normal,ignore,combine,all}
                        Select the mode strategy from the available choices:
                            normal: Remove all parameters and the wordlist
                            combine: Pitchfork combine on the existing parameters
                            ignore: Don't touch the URL and put the wordlist
                            all: All in one method
  -vs {replace,suffix}, --value-strategy {replace,suffix}
                        Select the value strategy from the available choices:
                            replace: Replace the value with gathered value
                            suffix: Append the value to the end of the parameters
  -o OUTPUT, --output OUTPUT
                        Output results
  -d, --debug           Debug mode

## Example  
```bash
python main.py -l urls.txt -c 40 -v '<b/injected,"injected"' -gs combine -vs suffix
```
