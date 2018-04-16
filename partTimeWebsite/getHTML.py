import argparse
import urllib.request
import sys
import re
from bs4 import BeautifulSoup

def main(args):
    argsHtml = args.html
    if args.html[:4] != "http":
        argsHtml = "https://" + args.html
    print(argsHtml)
    f=urllib.request.urlopen(argsHtml) 
    response=f.read()
    html = BeautifulSoup(response, "html.parser")
    title = str(html.select('title'))[8:-9]
    # re.sub(['\"','\'','\s'],'', str(title))
    title = title.replace(" ", "")
    print(title)
    with open('{}.html'.format(title), 'wb') as htmlFile:
        htmlFile.write(response)

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("html", type = str,
        help = "please input the address of website")
    return parser.parse_args(argv)


if __name__ == "__main__":
    main(parse_arguments(sys.argv[1:])) 
