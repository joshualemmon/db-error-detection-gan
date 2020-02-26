import numpy as np
import argparse

def main(args):
	infile = args.infile
	out = args.out


if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument('--infile', '-i', type=str, required=True)
	ap.add_argument('--out', '-o', type=str, required=True)
	main(ap.parse_args())