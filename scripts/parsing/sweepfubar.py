## Sweep across posterior probability cutoffs. Mostly useful for ROC curve.
## Note that this must be run on a gene-by-gene basis to prevent file sizes from getting out of hand.

### USAGE: python sweepfubar.py <dataset> <gene> ### 

import re, os, sys, subprocess, fnmatch, csv, shutil
from numpy import *
from Bio import AlignIO, SeqIO
import re, os, sys, subprocess, fnmatch, csv, shutil
from numpy import *
from Bio import AlignIO, SeqIO
import parsing_fxns



################### Input arguments ###################
dataset = sys.argv[1]
gene = sys.argv[2]
assert (dataset == 'HA' or dataset == 'GP41'), "Must specify either HA or GP41 as the dataset."
assert (gene == 'rho' or gene == 'prk'), "Must specify either rho or prk as a gene."
if dataset == 'GP41':
	datadir += 'GP41/'
	posStart = 10
elif dataset == 'HA':
	datadir += 'HA/'
	posStart = 18
######################################################	
	

################## Important stuff ####################
datadir='/Users/sjspielman/Dropbox/aln/results/'

# Directories: fubar output, alignments (all made with linsi, except for true alignments as generated by Indelible)
fudir   = datadir+'fubar/fubar_'+gene+'/'
alndir  = datadir+'alntree/nucguided_'+gene+'/'
	
# Directories: true simulated alignments and evolutionary rate categories
truerates_dir=datadir+'Simulation/truerates/'+gene+'/'
truealn_dir=datadir+'Simulation/sequences/'+gene+'/'

# Only use the penalization algorithms
algs=['refaln', 'GuidanceP', 'BMweightsP', 'PDweightsP']
cutoffs=arange(0,1.01,0.01)
######################################################

outfile='/Users/sjspielman/Research/alignment_filtering/data/parsed_data/fubarsweep_'+dataset+'_'+gene+'.txt'
outhandle=open(outfile, 'w')
outhandle.write('count\tcutoff\ttprate\tfprate\ttnrate\tfnrate\taccuracy\tcase\tgene\tmethod\tpenal\n')

		
for n in range(100):
	print str(n)
	
	## File names (refaln, truealn, truerates)
	refaln=alndir+'refaln'+str(n)+'.fasta'
	trfile=truerates_dir+'truerates'+str(n)+'.txt'
	truealn=truealn_dir+'truealn_codon'+str(n)+'.fasta'
			
	## Read in the reference alignment and collect some relevant info
	handle = open(refaln, 'r')
	refparsed=AlignIO.read(refaln, 'fasta')
	handle.close()
	alnlen=len(refparsed[0])
	numseq=len(refparsed)
	
	## Read in the true alignment
	handle = open(truealn, 'r')
	trueparsed=AlignIO.read(handle, 'fasta')
	handle.close()
	true_alnlen = len(trueparsed[0])
		
	## Build map to true alignment and obtain simulated positive selection state (binary - 0=notpos, 1=pos)
	mapRef, mapTrue = consensusMap(trueparsed, refparsed, numseq, alnlen)	
	truepos = parseTrueRates(trfile, mapTrue, posStart)
	
	################################ Accuracy assessment ###################################
	for alg in algs:
		
		## Get file names and whether or not gap-penalized algorithm
		if alg=='refaln':
			penal='zero'
			fubar=fudir+'refaln'+str(n)+'.fasta.fubar'
			aln=refaln
			parsed=refparsed
		
		elif case=='Guidance' or case=='BMweights' or case=='PDweights':
			penal='no'
			name = alg+'_50_'+str(n)+'.fasta'
			aln=alndir+name		
			fubar=fudir+name+'.fubar'
			parsed=AlignIO.read(aln, 'fasta')
		
		else:
			penal='yes'
			name = alg+'_50_'+str(n)+'.fasta'
			aln=alndir+name
			fubar=fudir+name+'.fubar'
			parsed=AlignIO.read(aln, 'fasta')	
		
		# Get case info
		testprobs = parseFUBAR(mapRef, fubar)	
		assert(len(truepos)==len(testprobs)), "FUBAR Mapping has failed."
	

		## Accuracy across posterior probability cutoffs
		for x in cutoffs:
			(tp,tn,fp,fn,tprate,fprate,tnrate,fnrate,accuracy)=sweepRates(float(x), truepos, testprobs)
			outhandle.write(str(n)+'\t'+str(x)+'\t'+str(tprate)+'\t'+str(fprate)+'\t'+str(fnrate)+'\t'+str(fnrate)+'\t'+str(accuracy)+'\t'+alg+'\t'+gene+'\tfubar\t'+penal+'\n')	

outhandle.close()

		
		
		
	
			
		
		
		
		
			
			