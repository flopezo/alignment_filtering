import subprocess
import argparse
import sys
import os
try:
    from dendropy import *
except:
    print "Please install Dendropy. See the README for details."

def parse_args():
    parser = argparse.ArgumentParser(prefix_chars='+-', usage='--protein_file <User File>')
    parser.add_argument("-infile", help="A file containing unaligned AA sequences in FASTA format", required=False, dest="infile", type=str)
    parser.add_argument("-n",dest="threads", type=int, help="Number of processes to use")
    parser.add_argument("-form",dest="form", type=str, help="The file format (usually FASTA)", default="FASTA")
    parser.add_argument("-bootstraps", help="The number of bootstraps to perform", required=False,
            dest="bootstraps")
    parser.add_argument("-alphabet", help="Whether AAs or NTs are used (protein or nucleotide)", type=str,
            default="protein", required=False, dest="alphabet") ##AA or NT, default is AA
    ## Gap penalization is now hard-coded by default in accordance with the original runs

    return parser.parse_args()

def getMafft():
    found = subprocess.call(["which", "mafft"])
    if not found == 0:
        print "MAFFT needs to be installed and on the system path"
        print "See the README on how to do this."

def getFastree():
    found = subprocess.call(["which", "fastree"])
    if not found == 0:
        print "FasTree needs to be installed and on the system path"
        print "See the README on how to do this"

def getRAxML():
    found = subprocess.call(["which", "raxmlHPC"])
    if not found:
        print "RAxML needs to be installed and on the system path"
        print "See the README on how to do this."

def main():
    getMafft()
    getFastree()
    getRAxML()
    args = parse_args()
    user_file = args.infile
    while args.infile is None:
        args.infile = raw_input("Please provide a protein file in FASTA format: ")
    while args.form is None:
        print ""
        args.form = raw_input("Please tell me what format the infile is in.\nIt should be a FASTA file: ")
    if args.threads is None:
        print ""
        print "One thread will be used. To change the number of threads, use the -n flag"
        print "More threads will run faster, but you shouldn't use more than the number of cores in your machine\n"
        args.threads = 1
    if args.bootstraps is None:
        print ""
        print "Ten bootstraps will be performed. To change the number of bootstraps, use the -bootstraps flag\n"
        args.bootstraps = 10
    if args.alphabet is None:
        print "No alphabet was selected, so amino acids will be used by default. Use the -alphabet flag to specify an alphabet.\n"
        args.alphabet = "AA"
    command = "python main.py " + str(args.infile) + " " + str(args.alphabet) + " " + str(args.bootstraps) + " " + str(args.threads)
    subprocess.call(command, shell=True)
    

main()
