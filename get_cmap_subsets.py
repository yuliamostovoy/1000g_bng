import sys

def main():
	if len(sys.argv) != 3:
		sys.stderr.write("Usage: program.py cmap_file subset_file\n")
		sys.stderr.write("Subset file must be in this format: contig start end (tab-delimited)\n")
		sys.exit(1)

	subset_file = open(sys.argv[2],'r')
	subsets = {}
	for line in subset_file:
		line = line.strip().split('\t')
		if line[0] not in subsets:
			subsets[line[0]] = [(float(line[1]), float(line[2]))]
		else:
			subsets[line[0]].append((float(line[1]), float(line[2])))
	subset_file.close()

	cmap_file = open(sys.argv[1],'r')

	#CMapId	ContigLength	NumSites	SiteID	LabelChannel	Position	StdDev	Coverage	Occurrence
	cmaps = {}
	for line in cmap_file:
		if line.startswith("#"):
			print line.strip()
			continue
		line = line.strip().split('\t')
		if line[0] not in cmaps:
			cmaps[line[0]] = [(int(line[4]), float(line[5]))]
		else:
			cmaps[line[0]].append((int(line[4]), float(line[5])))
	cmap_file.close()

	pos = []
	cur_subset = {'id':None,'end':None}
	labels = []
	for contig in subsets:
		i=0
		for start,end in subsets[contig]:
			i+=1
			for j, (label,position) in enumerate(cmaps[contig],start=1):
				if not pos:
					if position>=start:
						pos.append(position)
						labels.append(label)
				else:
					if position==end or j==len(cmaps[contig]):
						pos.append(position)
						labels.append(label)
						finish(labels, pos, contig, i)
						pos, labels = [], []
						break
					elif position>end:
						finish(labels, pos, contig, i)
						pos, labels = [], []
						break
					else:
						pos.append(position)
						labels.append(label)

def finish(labels, pos, contig, i):
	if not labels[-1]==0:
		pos.append(pos[-1]+100)
		labels.append(0)
	total_nicks = len(pos)-1				
	total_length = pos[-1]-pos[0]+100
	for j in range(len(pos)):
		print "%s000%d\t%.1f\t%d\t%d\t%d\t%.1f\t%d\t%d\t%d" % (contig, i, total_length, total_nicks, j+1, labels[j], pos[j]-pos[0]+100, labels[j], labels[j], labels[j])

if __name__=="__main__":main()
