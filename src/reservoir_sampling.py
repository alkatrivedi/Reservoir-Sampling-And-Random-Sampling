import sys
import random

#function to check the input(or the arguments pased from the terminal to execute this file) 
def check_input():

	if len(sys.argv) != 2:

		print('Wrong format. Try:\n python3 reservoir.py "sample_number_K" "<" "input_file.txt"')
		sys.exit(-1)

	if int(sys.argv[1]) <= 0:

		sys.exit(-1)


#function to apply reservoir sampling
def reservoir_sampling(K, row, row_number, selected_rows):

	#each element will be having probability K/N
	#where,
	#K is the number of messages to be picked
	#N is the number of messages present in the input text file
	if random.random() < min(1, (K / row_number)):

		#if we haven't selected K rows yet insert the randomly selected row to the selected row
		if len(selected_rows) < K:
			
			selected_rows.insert(len(selected_rows), row)
		#otherwise randomly select a row from the input file
		else:

			random_place = random.randint(0, len(selected_rows)-1)
			selected_rows[random_place] = row

	#return the all randomly selected rows
	return selected_rows


#printing extracted sampled rows
def print_rows(sampled_rows):

	for i in range(len(sampled_rows)):

		if sampled_rows[0] != '':
			print('%d. %s' % (i + 1, sampled_rows[i]))


if __name__ == '__main__':

	check_input()
	#getting the value of items need to take from the input text file of unknown size
	K = int(sys.argv[1])	

	#reading input messages
	with open('input.txt', 'r', encoding='UTF-8') as std_in:

		row = std_in.readline()
		row_number = 1
		sampled_rows = []

		while row != ' ':
			#applying reservoir sampling
			sampled_rows = reservoir_sampling(K, row, row_number, sampled_rows)

			try:
				#moving onto next row of the text file
				row = std_in.__next__()
				row_number += 1

			except StopIteration:

				break

	#printing the sample rows extracted after applying reservoir sampling
	print_rows(sampled_rows)
	
