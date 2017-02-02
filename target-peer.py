#!/usr/bin/env python
from __future__ import print_function
import csv
import requests
import json
import argparse
from pprint import pprint
import os.path



def loadQuery(query_file):
	# load json query
	print("  -- Loading query file") 
	if os.path.isfile(query_file):
		with open (query_file) as json_data:
			return(json.load(json_data))
	else:
		print("did not find the file")


def queryData(url,headers,query):
	print("  -- Sending query to Kentik API")
# populate variable 'response' with response object
	response = requests.post(url,headers=headers,json=query)
	print("  -- Recieved reply")
	# convert the response object to a dictionary
	return(response.json())


def writeFile(filename):
	print("  -- Writing output to {}".format(filename))
	if isCSV is True:
		with open(filename, 'w') as f:
			writer = csv.DictWriter(f, extrasaction='ignore', fieldnames=COLUMNS.split(','))
			writer.writeheader()
			rows = (row for bucket in data_dict['results'] for row in bucket['data'])
			writer.writerows(rows)
	if isCSV is False:
		with open(filename, 'w') as out:
			pprint(data_dict, stream=out)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Script to run GTT target net reports. Script requires two files: source_nets.json and dest_nets.json to be located in the same directory.')
	parser.add_argument('filename', help='Filename to write output to. Must be of type .csv or .json. Defaults to report.csv', default='report')
	parser.add_argument('email', help='Admin user email')
	parser.add_argument('api', help='API key for configured user')
	parser.add_argument('direction', choices=['source', 'dest'], help='Select inbound report or outbound peering report')
	args = parser.parse_args()
	
	# variables 
	filename = args.filename
	email = args.email
	api = args.api
	direction = args.direction
	url = 'https://api.kentik.com/api/v5/query/topxdata'
	headers = {'X-CH-Auth-Email': email, 'X-CH-Auth-API-Token': api}
	
	
	if filename.split('.')[1] == 'csv':
		isCSV = True
		print("Generating CSV report ", end="") 
	if filename.split('.')[1] == 'json':
		isCSV = False
		print("Generating JSON report ", end="")
	else:
		sys.exit("Filename must end in .csv or .json")
	
	if direction == 'source':
		print("of source traffic peering targets from Kentik Portal data")
		COLUMNS = 'i_device_name,i_src_as_name,Geography_src,input_port,max_bits_per_sec,p95th_bits_per_sec,avg_bits_per_sec'
		json_file='source_nets.json'
	else:
		print("of dest traffic peering targets from Kentik Portal data")
		COLUMNS = 'i_device_name,i_dst_as_name,Geography_dst,i_dst_nexthop_as_name,max_bits_per_sec,p95th_bits_per_sec,avg_bits_per_sec'
		json_file='dest_nets.json'
		
	# build the query
	query = loadQuery(json_file)
	# make the request
	data_dict = queryData(url,headers,query)
	
	if data_dict:
		writeFile(filename)
	
