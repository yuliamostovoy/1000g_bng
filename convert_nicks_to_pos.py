import sys
import argparse

def main():
	parser = argparse.ArgumentParser(description="Given a cmap, region coordinates, and a number of flanking nicks, this script calculates the outer coordinates of the region once the flanking nicks are included.")
	parser.add_argument('cmap', help='cmap file from which to pull coordinates', metavar = 'cmap_file')
	parser.add_argument('region_start', help="Start coordinate of the region to work with", type=float)
	parser.add_argument('region_end', help="End coordinate of the region to work with", type=float)
	parser.add_argument('upstream_nicks', metavar="num_upstream_nicks", help="Number of nicks to add upstream of region", type=int)
	parser.add_argument('downstream_nicks', metavar="num_downstream_nicks", help="Number of nicks to add downstream of region", type=int)
	
	args = parser.parse_args()

	ref_cmap = open(args.cmap,'r')

	if args.region_start > args.region_end:
		args.region_start, args.region_end = args.region_end, args.region_start

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
		if start_nick == None and pos >= args.region_start:
			start_nick = i
		if end_nick == None:
			if pos == args.region_end:
				end_nick = i
			elif pos > args.region_end:
				end_nick = i-1
		i+=1
	
	sys.stderr.write("%0.1f %0.1f\n" % (all_nicks[start_nick-args.upstream_nicks], all_nicks[end_nick+args.downstream_nicks]))

if __name__=="__main__": main()
