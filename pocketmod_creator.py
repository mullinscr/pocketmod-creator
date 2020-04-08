#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""PocketMod Creator

This script should be called from the command line with a valid input file
argument. It takes the input PDF and converts it into a pocketmod format PDF.
This pocketmod PDF is output into the directory the script was called from.

This tool accepts a PDF file as input. It is assumed that the original PDF
is A4 in size. PDFs that are longer than 8 pages will only have the first
8 pages converted into a pocketmod.

This script requires `PyPDF2` be installed within the Python environment
you are running this script in: see https://github.com/mstamy2/PyPDF2.

Example
-------
Run the script from the command line with a PDF file as an input argument.

$ python pocketmod_creator.py input.pdf
The file has been converted. The output file is: output_20200407123547.pdf

The directory will now have a time-stamped PDF as output from the script.

$ ls
pocketmod_creator.py input.pdf output_20200407123547.pdf
"""

import os
import argparse
import datetime

# PyPDF2 repo: https://github.com/mstamy2/PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter

def check_input_file(input_file):
	""" Check the input file is a valid PDF file."""
	if not os.path.isfile(input_file):
		raise FileNotFoundError('Please enter a valid filename.')
	if not os.path.basename(input_file)[-3:].lower() == 'pdf':
		raise ValueError('File type is not a pdf.')
	if PdfFileReader(input_file).getNumPages() > 8:
		print('\nInput file contains more than 8 pages.\n'
			'Only the first 8 will be converted.')

def pocket_modder(input_file):
	"""Convert and output a PDF file into a pocketmod PDF file.

	Parameters
	----------
	input_file : str
		The PDF file to be converted into a pocket mod.

	Notes
	-----
	The input PDF is assumed to have the dimensions of A4 paper.
	"""
	with open(input_file, 'rb') as input_pdf:
		input_pdf = PdfFileReader(input_pdf)
		writer = PdfFileWriter()
		
		# 0.3528 is the mm approximation of 1/72 of an inch.
		# PyPDF2 uses increments of 1/72 of an inch for sizing. 
		# 297 and 210 are the mm dimensions of A4 paper.
		pdf_width = 297 / 0.3528
		pdf_height = 210 / 0.3528
		# Reduces the page size down to 1/8 of its original dimension.
		scale_factor = 0.3536
		# Calculate the placement of the images on the page
		# so that there are 4 columns and 2 rows.
		x_translation = pdf_width / 4
		y_translation = pdf_height / 2
		
		transformation_dict  = {
			0 : (x_translation, y_translation, 180),
			1 : (0, y_translation, 0),
			2 : (x_translation, y_translation, 0),
			3 : (x_translation * 2, y_translation, 0),
			4 : (x_translation * 3, y_translation, 0),
			5 : (x_translation * 4 , y_translation, 180),
			6 : (x_translation * 3, y_translation, 180),
			7 : (x_translation * 2, y_translation, 180)}
		
		new_pdf = writer.addBlankPage(pdf_width, pdf_height)
		i = 0 
		while i < 8 and i < input_pdf.getNumPages():
			content_page = input_pdf.getPage(i)
			new_pdf.mergeRotatedScaledTranslatedPage(
				content_page,
				transformation_dict[i][2],
				scale_factor,
				transformation_dict[i][0],
				transformation_dict[i][1],
				expand=False)
			i += 1

		current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
		output_pdf = 'output_{}.pdf'.format(current_time)
		with open(output_pdf, 'wb') as out_file:
			writer.write(out_file)
			print('The file has been converted.',
				' The output file is: {}'.format(output_pdf))

def main():
	""" Collect and parse the command line input argument.
	Check the validity of the input file, then convert and output the PDF.
	"""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('input_file', type=str, help='Input pdf to convert')
	args = parser.parse_args()

	check_input_file(args.input_file)
	pocket_modder(args.input_file)

if __name__ == '__main__':
	main()