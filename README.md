Guide to single-molecule evaluation of complex regions:

1. Identify major SVs at the complex locus using assembled contigs. Create alternate cmaps representing each SV. Note the coordinates of long duplicated regions involved in the SV, if any. (If none, it may not be necessary to do single-molecule analysis because the assembly is likely to be accurate.) For each SV, create a cmap file containing both the reference and the alternate version (with different cmap IDs).

2. Identify molecules that are informative for characterizing the SV. These should be molecules that flank the breakpoint(s) of the SV and contain enough unique nicks to definitively distinguish their position with respect to long duplicated regions. For example, for an inversion mediated by two copies of a duplication, informative molecules should span the entire duplication and contain flanking nicks on both sides of the duplication.
3. 
  An example from locus 15q13, where an inversion is mediated by duplications at 30406019-30617125 and 32390212-32601693:
  python get_molecules_with_flanking_nicks.py HG03133/contigs/alignmolvref/merge/alignmolvref_contig15.xmap 30406019 30617125 4 4 > HG03133_15q13_inversion
  python get_molecules_with_flanking_nicks.py HG03133/contigs/alignmolvref/merge/alignmolvref_contig15.xmap 32390212 32601693 4 4 >> HG03133_15q13_inversion

3. Generate a cmap of the molecules selected in step 2:
  pull_out_contigs_from_cmap.sh HG03133_15q13_inversion HG03133/contigs/alignmolvref/merge/alignmolvref_contig15_q.cmap > HG03133_15q13_inversion.cmap

4. Run alignment to a cmap containing both the reference and the alternate chromosome:
  ~/irys/tools/RefAligner -ref hg38_chr15_ref_and_major_inversion.cmap -i HG03133_15q13_inversion.cmap -o HG03133_15q13_inversion -endoutlier 1e-2 -f -outlier 1e-4 -A 5 -biaswt 0 -M 5 -Mfast 0 -T 1e-6 -BestRef 0 -nosplit 2 -stdout -stderr

5. Identify the coordinates of the critical region(s) to which molecules have to align in order to be informative. This is often just the coordinates of the duplicated region + flanking nicks, as identified in step 2. The coordinates may be different for the two different references.
  python convert_nicks_to_pos.py hg38_chr15.cmap 30406019 30617125 4 4
  30392581.0 30664155.0
  python convert_nicks_to_pos.py hg38_chr15.cmap 32390212 32601693 4 4
  32359609.0 32634560.0
  python convert_nicks_to_pos.py hg38_chr15_major_inversion.cmap 30406019 30617125 4 4
  30392581.0 30647728.0
  python convert_nicks_to_pos.py hg38_chr15_major_inversion.cmap 32390212 32601693 4 4
  32343182.0 32634560.0
  
6. Analyze the xmap produced in step 4 to see which molecules support which version of the reference:
  python compare_aln_to_two_refs.py HG03133_15q13_inversion.xmap -c1 30392581.0 30664155.0 -c1 32359609.0 32634560.0 -c2 30392581.0 30647728.0 -c2 32343182.0 32634560.0 > HG03133_15q13_inversion_result
