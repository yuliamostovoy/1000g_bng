import sys

def main():
	if len(sys.argv)!=6:
		sys.stderr.write("Usage: program.py *.cmap region_start region_end upstream_nicks downstream_nicks\n")
		sys.exit(1)

	ref_cmap = open(sys.argv[1],'r')

	flanking_nick_number_upstream = sys.argv[4]
	flanking_nick_number_downstream = sys.argv[5]
	try:
		flanking_nick_number_upstream = int(flanking_nick_number_upstream)
		flanking_nick_number_downstream = int(flanking_nick_number_downstream)
	except:
		sys.stderr.write("Error: Nick number must be integer\n")
		sys.stderr.write("Usage: program.py *.cmap region_start region_end upstream_nicks downstream_nicks\n")
		sys.exit(1)

	region_start = float(sys.argv[2])
	region_end = float(sys.argv[3])

	if region_start > region_end:
		region_start, region_end = region_end, region_start

	start_nick, end_nick = None, None
	all_nicks = []
	i=0
	for line in ref_cmap:
		if line.startswith("#"):
			continue
		# 3: nick number, 5: position
		line = line.strip().split('\t')
		pos = float(line[5])
		all_nicks.append(pos)
		if start_nick == None and pos >= region_start:
			start_nick = i
		if end_nick == None:
			if pos == region_end:
				end_nick = i
			elif pos > region_end:
				end_nick = i-1
		i+=1
	
	sys.stderr.write("%0.1f %0.1f\n" % (all_nicks[start_nick-flanking_nick_number_upstream], all_nicks[end_nick+flanking_nick_number_downstream]))

if __name__=="__main__": main()
