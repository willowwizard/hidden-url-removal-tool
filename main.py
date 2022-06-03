#!/usr/bin/env python
# Simple URL Search & Destroy
# u/katataru 2022
import os

# generate a list of legal url characters
def legal_url_characters():
	legal_chars = []
	ascii_ranges = [
		[48, 57], # 0-9
		[65, 90], # A-Z
		[97, 122], # a-z
	]
	specials = ["-", ".", "_", "~", ":", "/", "?", "#", "[", "]", "@", "!", "$", "&", "'", "(", ")", "*", "+", ",", ";", "%", "="]
	for ranges in ascii_ranges:
		for decimal in range(ranges[0], ranges[1]+1):
			legal_chars.append(chr(decimal))
	legal_chars = legal_chars + specials
	return legal_chars

# check if given byte is a legal url character
legal_chars = legal_url_characters()
def is_legal(byte):
	return chr(byte) in legal_chars

# simply finds length of legal url characters
def get_url_length(data):
	i = 0
	while is_legal(data[i]):
		i += 1
	return i

# for readability
class URL:
	def __init__(self, data, start, length):
		self.start = start # position of start of url
		self.length = length # length of url
		self.end = start+length # position of end of url
		self.content = data[self.start:self.end].decode() # the url as text data

# finds urls in data, returns (position of url, length of url)
def find_urls(data):
	urls = []
	i = 0
	while i < len(data):
		if(data[i:i+8] == b'https://' or data[i:i+7] == b'http://'): # if I find text starting with http
			url_length = get_url_length(data[i:]) # get the length of that text
			urls.append(URL(data, i, url_length)) # add to list of url positions
		i += 1
	return urls

# write a file with all the urls replaced with null bytes
def write_clean_file(data, urls, output_path):
	try:
		output_fp = open(output_path, 'wb')
		data_i = 0
		urls_i = 0
		current_url = urls[urls_i]
		while data_i < len(data):
			if data_i == current_url.start: # if my current copy position is equivalent to the url start position
				output_fp.write(bytes(current_url.length)) # write null bytes to the file instead of copying over
				data_i += current_url.length
				if (urls_i+1 < len(urls)):
					urls_i += 1
				current_url = urls[urls_i]
				continue
			output_fp.write(data[data_i].to_bytes(1, byteorder="big")) # otherwise, copy data as normal
			data_i += 1
	except:
		print(f"Warning: Something went wrong when attempting to process {input_path}! Stacktrace:")
		traceback.print_exc()
		return

# check the given file path for urls
def process_file(input_path, output_path):
	try:
		print(f"-- Checking {input_path} ... ", end="")
		input_fp = open(input_path, 'rb')
		data = input_fp.read()

		urls = find_urls(data)
		if len(urls) > 0: # print url counts and urls themselves
			print(f"{len(urls)} URL(s) found! --")
			for url in urls:
				print(f" * {url.content}")
			print(f" > Writing clean file to {output_path} ... ", end="")
			write_clean_file(data, urls, output_path)
			print("done!")
		else:
			print("file is clean! --")
	except:
		print(f"Warning: Something went wrong when attempting to process {input_path}! Stacktrace:")
		traceback.print_exc()
		return

input_directory = "input files"
output_directory = "output files"
if not os.path.isdir(output_directory): # making sure output directory exists
	os.mkdir(output_directory)

for filename in os.listdir(input_directory):
	full_input_path = os.path.join(input_directory, filename)
	full_output_path = os.path.join(output_directory, filename)
	process_file(full_input_path, full_output_path)