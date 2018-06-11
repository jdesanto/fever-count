import simplejson as json
import argparse
from collections import defaultdict

def get_user_data(fname):
	'''Get user data. Assumes 1 line header.'''

	user_data = {}

	# Loop through file.
	with open(args.user_data, 'r') as fh:
		fh.readline() # skip header
		for l in fh:
			ls = l.strip('\n')
			uid, zipcode, name = ls.split(',',2)
			user_data[uid] = {'name': name, 'zipcode': zipcode}

	return user_data

if __name__ == '__main__':

	# Get command line arguments. Run with -h to show help
	parser = argparse.ArgumentParser(description='Run the flow aggregator.')
	parser.add_argument('-readings', type=str, default='./readings.jsonl', help='Readings file (jsonl format)')
	parser.add_argument('-user_data', type=str, default='./user_data.csv', help='User data file (csv format)')
	parser.add_argument('-output', type=str, default='./results.txt', help='Output file name')
	args = parser.parse_args()

	# Get user data
	user_data = get_user_data(args.user_data)

	# Create dict to hold zip->fever count
	zip_fever_count = defaultdict(int)

	# Iterate through readings file and count zips with fever
	with open(args.readings, 'r') as fh:
		for l in fh:
			data = json.loads(l)
			uid = data['user']['id']
			if data['temperature'] > 99.5:
				zip_fever_count[user_data[uid]['zipcode']] += 1

	# Create output file
	with open(args.output, 'w') as fh:
		for k in sorted(zip_fever_count.keys()):
			fh.write('{},{}\n'.format(k, zip_fever_count[k]))


