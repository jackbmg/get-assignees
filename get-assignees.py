#!/usr/bin/env python
import sys
import csv
import xlwt
import xlsxwriter
from iptools.client import Client, ClientError

#if len(sys.argv) != 2:
#        sys.exit("usage: api-snippets.py <csv input file>")
lines = [line.rstrip('\n') for line in open(sys.argv[1], 'r')]
#c = Client(token='', host='lit-iptoolstest2.swg.usma.ibm.com')
c = Client(token='', host='iptools.swg.usma.ibm.com')
# print lines
validhost=[]
row = 0
col = 0
row += 1
filename='assigneeout'
target=open(filename, 'w')
for item in lines:
	host=c.ipv4addresses.get(item)
	if host['status']=='S':
		validhost.append(host)
for host in validhost:
	target.write(host['fqdn']['hostname'])
	target.write(',')
	target.write(host['address'])
	target.write(',')
	for i in host['assignees']:
		target.write(i['display_name'])
		target.write(',')
	target.write('\n')
target.close()

file_reader = csv.reader(open('assigneeout', 'rb'), delimiter=',')
file_writer = csv.writer(open('output.csv', 'wb'), delimiter=',')
file_writer.writerow(["HostName", "IP Address", "Assignees"])
for row in file_reader:
    file_writer.writerow(row)

workbook = xlsxwriter.Workbook('assignees.xlsx')
worksheet = workbook.add_worksheet()
worksheet.set_column('A:B', 20)
worksheet.set_column('C:T', 25) 
row=1
col=0
worksheet.write('A1', 'Hostname')
worksheet.write('B1', 'IP Address')
worksheet.write('C1', 'Assignees')
for host in validhost:
	worksheet.write(row, col, host['fqdn']['hostname'])
	col+=1
	worksheet.write(row, col, host['address'])
	for i in host['assignees']:
		col+=1
		worksheet.write(row, col, i['display_name'])
	col=0
	row+=1
workbook.close()
