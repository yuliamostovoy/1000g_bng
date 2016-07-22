import sys
import copy

def main():
	if len(sys.argv)!=6:
		sys.stderr.write("Usage: program.py *.xmap region_start region_end upstream_nicks downstream_nicks\n")
		sys.exit(1)

	xmap = open(sys.argv[1],'r')

	flanking_nick_number_upstream = sys.argv[4]
	flanking_nick_number_downstream = sys.argv[5]
	try:
		flanking_nick_number_upstream = int(flanking_nick_number_upstream)
		flanking_nick_number_downstream = int(flanking_nick_number_downstream)
	except:
		sys.stderr.write("Error: Nick number must be integer\n")
		sys.stderr.write("Usage: program.py *.xmap region_start region_end upstream_nicks downstream_nicks\n")
		sys.exit(1)

	path = '/'.join(sys.argv[1].split('/')[:-1])
	ref_path, query_path = None, None
	if path:
		path += "/"
	for line in xmap:
		if line.startswith("# Reference"):
			line = line.strip().split('\t')
			ref_path = path+line[1].split("/")[-1]
		elif line.startswith("# Query"):
			line = line.strip().split('\t')
			query_path = path+line[1].split("/")[-1]
		elif ref_path != None and query_path != None:
			break

	query_cmap = open(query_path,'r')
	ref_cmap = open(ref_path,'r')
	region_start = int(round(float(sys.argv[2])))
	region_end = int(round(float(sys.argv[3])))

	if region_start > region_end:
		region_start, region_end = region_end, region_start

	start_nick, end_nick = None, None
	for line in ref_cmap:
		if line.startswith("#"):
			continue
		# 3: nick number, 5: position
		line = line.strip().split('\t')
		if start_nick == None and float(line[5]) >= region_start:
			start_nick = int(line[3])
		if end_nick == None:
			if float(line[5]) == region_end:
				end_nick = int(line[3])
				break
			elif float(line[5]) > region_end:
				end_nick = int(line[3])-1
				break

	molecule_nick_counts = {} # molecule_id-->number of nicks
	for line in query_cmap:
		if line.startswith('#'):
			continue
		line = line.strip().split()
		if line[3] == '1': #new molecule
			molecule_nick_counts[line[0]] = int(line[2])
		else:
			continue
	query_cmap.close()

	for line in xmap:
		flip = False
		if line.startswith('#'):
			continue
		line = line.strip().split()
		mol_id = line[1]
		alignment = get_alignment(line[-1]) #returns ordered list of tuples in format (ref nick, query nick)
		if mol_id not in molecule_nick_counts:
			sys.stderr.write("Error: molecule %s not found in query cmap file\n" % (mol_id))
			continue
		if not (alignment[0][0]<start_nick and alignment[-1][0]>end_nick):
			continue
		query_start = get_first_nick(alignment, start_nick, mol_id)
		query_end = get_last_nick(alignment, end_nick, mol_id)
		if alignment[0][1]>alignment[-1][1]: #query aligns in - orientation
			query_start, query_end = query_end, query_start
			flip = True
		if flip:
			if query_start <= flanking_nick_number_downstream:
				continue
			if query_end > molecule_nick_counts[mol_id]-flanking_nick_number_upstream:
				continue
		else:
			if query_start <= flanking_nick_number_upstream:
				continue
			if query_end > molecule_nick_counts[mol_id]-flanking_nick_number_downstream:
				continue
		print mol_id

	xmap.close()

def get_alignment(align_string):
	#input format is (1,3)(2,6)(3,7) etc: (ref nick, query nick)
	#output is list of tuples
	align_string = align_string.split(")")[:-1] #the last one is an empty string
	alignment = []
	for entry in align_string:
		entry = entry.strip("(").split(",")
		alignment.append((int(entry[0]), int(entry[1])))
	return alignment

def get_first_nick(alignment, region_start, mol_id):
	for ref, query in alignment:
		if ref >= region_start:
			return query
	sys.stderr.write("Error: invalid result in get_first_nick() with molecule %d\n" % mol_id)
	sys.exit(1)

def get_last_nick(alignment, region_end, mol_id):
	prev_query = -1
	for ref, query in alignment:
		if ref < region_end:
			prev_query = query
		else:
			return prev_query
	sys.stderr.write("Error: invalid result in get_last_nick() with molecule %d\n" % mol_id)
	sys.exit(1)


if __name__=="__main__": main()
