#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""PocketMod Creator

This script should be called from the command line with a valid input
file argument. It takes the input PDF and converts it into a pocketmod
format PDF. This pocketmod PDF is output into the directory the script
was called from.

This tool accepts a PDF file as input. PDFs that are longer than 8 pages
will only have the first 8 pages converted into a pocketmod.

This script requires `PyPDF2` be installed within the Python environment
you are running this script in: see https://github.com/mstamy2/PyPDF2.

Example
-------
Run the script from the command line with the PDF file to be converted
as the input argument.

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
	"""Check the input file is a valid PDF file."""
	if not os.path.isfile(input_file):
		raise FileNotFoundError('Please enter a valid filename.')
	if not os.path.basename(input_file)[-3:].lower() == 'pdf':
		raise ValueError('File type is not a pdf.')
	if PdfFileReader(input_file).getNumPages() > 8:
		print('\nInput file contains more than 8 pages.\n'
			'Only the first 8 will be converted.')

def input_size_orientation(input_file):
	"""Determine the paper size and orientation of the input file."""
	media_box = PdfFileReader(input_file).getPage(0).mediaBox
	
	# 0.3528 is the mm approximation of 1/72 of an inch
	# PyPDF2 uses increments of 1/72 of an inch for sizing
	width = round(float(media_box[2]) * 0.3528)
	height = round(float(media_box[3]) * 0.3528)
	
	if width > height:
		orientation = 'Landscape'
	else:
		orientation = 'Portrait'

	return(width, height, orientation)

def pocket_modder(input_file, width, height, orientation):
	"""Convert and output a PDF file into a pocketmod PDF file.

	Parameters
	----------
	input_file : str
		The path of the pdf file to be converted.
	width : int
		The width in mm of the input file's first page.
	height: int
		The height in mm of the input file's first page.
	orientation : str
		The orientation of the input file's first page - either
		'Portrait' or 'Landscape' returned.

	Notes
	-----
	The output PDF will be the same dimension as the input file's first
	page. For example, an A4-sized input PDF will result in an A4-sized
	output PDF, likewise, an A3-sized input PDF will result in an
	A3-sized output PDF.
	"""
	with open(input_file, 'rb') as input_pdf:
		input_pdf = PdfFileReader(input_pdf)
		writer = PdfFileWriter()
		# 0.3528 is the mm approximation of 1/72 of an inch
		# PyPDF2 uses increments of 1/72 of an inch for sizing
		pypdf_scale = 0.3528

		if orientation == 'Landscape':
			width, height = height, width

		# calculate the desired width of single page when it has been converted
		output_width = height / 4
		output_height = width / 2
		# convert the output width and height to the PyPDF2 scale
		x_translation = output_width/ pypdf_scale
		y_translation = output_height / pypdf_scale

		# get best scale as to maximise the area of the converted pdf
		scale = min(output_width / width, output_height / height)

		transformation_dict = {
			'Landscape' : {
				0 : (0, y_translation, 270),
				1 : (x_translation, y_translation, 90),
				2 : ((x_translation * 2), y_translation, 90),
				3 : ((x_translation * 3), y_translation, 90),
				4 : ((x_translation * 4), y_translation, 90),
				5 : (x_translation * 3 , y_translation, 270),
				6 : (x_translation * 2 , y_translation, 270),
				7 : (x_translation , y_translation, 270)},
			'Portrait' : {
				0 : (x_translation, y_translation, 180),
				1 : (0 , y_translation, 0),
				2 : (x_translation, y_translation, 0),
				3 : ((x_translation * 2), y_translation, 0),
				4 : ((x_translation * 3), y_translation, 0),
				5 : (x_translation * 4, y_translation, 180),
				6 : (x_translation * 3, y_translation, 180),
				7 : (x_translation * 2, y_translation, 180)}
			}

		new_pdf = writer.addBlankPage(height / pypdf_scale, width / pypdf_scale)
		i = 0
		while i < 8 and i < input_pdf.getNumPages():
			content_page = input_pdf.getPage(i)
			new_pdf.mergeRotatedScaledTranslatedPage(
				content_page,
				transformation_dict[orientation][i][2],
				scale,
				transformation_dict[orientation][i][0],
				transformation_dict[orientation][i][1],
				expand=False)
			i += 1

		current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
		output_pdf = 'output_{}.pdf'.format(current_time)
		with open(output_pdf, 'wb') as out_file:
			writer.write(out_file)
			print('The file has been converted.',
					' The output file is: {}'.format(output_pdf))

def main():
	"""Collect and parse the command line input argument.
	Check the validity of the input file, then convert and output
	the PDF.
	"""
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('input_file', type=str, help='Input pdf to convert')
	args = parser.parse_args()

	check_input_file(args.input_file)
	width, height, orientation = input_size_orientation(args.input_file)
	pocket_modder(args.input_file, width, height, orientation)

if __name__ == '__main__':
	main()
