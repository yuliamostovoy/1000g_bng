import sys
import argparse

def main():
	parser = argparse.ArgumentParser(description='Evaluate molecule support for two different references. Use after aligning molecules to both versions using nosplit=2 and BestRef=0. Specify one or more critical regions on the two references that a molecule alignment needs to fully span in order for the molecule to be informative. If multiple critical regions are specified, a molecule is considered informative if its alignment spans any of them.\n')
	parser.add_argument('xmap', help='xmap file containing alignment result', metavar="xmap_file")
	parser.add_argument('-c1', '--critical_region_ref1', action='append', nargs=2, metavar=('START','END'), required=True, dest='c1', type=float, help='Space-separated start and end coordinates of critical region for reference #1. Multiple critical regions can be specified with additional -c1 entries (each must have one set of start and end coordinates).')
	parser.add_argument('-c2', '--critical_region_ref2', action='append', nargs=2, metavar=('START','END'), required=True, dest='c2', type=float, help='Space-separated start and end coordinates of critical region for reference #2. Multiple critical regions can be specified with additional -c2 entries (each must have one set of start and end coordinates).')
	args = parser.parse_args()

	try:
		xmap = open(args.xmap,'r')
	except:
		sys.stderr.write("Error opening xmap file %s\n" % args.xmap)
		sys.exit(1)

	# parse xmap
	mols = {}
	sample = ''
	for line in xmap:
		if line.startswith("#"):
			# get location of _r.cmap
			if line.startswith("# Ref"):
				line = line.strip().split('\t')
				sample = line[1].split('/')[-1].split('_')[0]
			continue
		line = line.strip().split('\t')
		ID = line[1]
		start, end, conf = float(line[3]), float(line[4]), float(line[8])
		if ID not in mols:
			mols[ID] = [{"length":abs(end-start),"conf":conf,"ref_start":float(line[5]), "ref_end":float(line[6])}]
		else:
			mols[ID].append({"length":abs(end-start),"conf":conf, "ref_start":float(line[5]), "ref_end":float(line[6])})
	xmap.close()

	# evaluate xmap entries
	first, second = 0,0
	first_mols = []
	second_mols = []
	for mol in mols:
		if len(mols[mol]) != 2:
			sys.stderr.write("Error: %d entries for query_id %s (should be 2)\n" % (len(mols[mol]), mol))
			continue
		if mols[mol][0]['conf'] > mols[mol][1]['conf']:
			if critical_region_matched(args.c1, mols[mol][0]['ref_start'], mols[mol][0]['ref_end']):
				first += 1
				first_mols.append(mol)
		elif mols[mol][1]['conf'] > mols[mol][0]['conf']:
			if critical_region_matched(args.c2, mols[mol][1]['ref_start'], mols[mol][1]['ref_end']):
				second += 1
				second_mols.append(mol)
	print "%s\t%d\t%d\tmap1:%s\tmap2:%s" % (sample, first, second, ','.join(first_mols), ','.join(second_mols))

def critical_region_matched(critical_regions, aln_start, aln_end):
	for start, end in critical_regions:
		if start>end:
			start, end = end, start
		if aln_start<=start and aln_end>=end:
			return True
	return False

if __name__=="__main__":main()
