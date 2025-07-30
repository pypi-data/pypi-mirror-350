AA_1to3 = {'A': 'Ala', 'C': 'Cys', 'D': 'Asp',
           'E': 'Glu', 'F': 'Phe', 'G': 'Gly',
           'H': 'His', 'I': 'Ile', 'K': 'Lys',
           'L': 'Leu', 'M': 'Met', 'N': 'Asn',
           'P': 'Pro', 'Q': 'Gln', 'R': 'Arg',
           'S': 'Ser', 'T': 'Thr', 'V': 'Val',
           'W': 'Trp', 'Y': 'Tyr'}

AA_3to1 = {v: k for k, v in AA_1to3.items()}


def write_fasta(sequence, id, description, fh):
    fh.write(">" + id + ' ' + description + "\n")
    fh.write(sequence + "\n")
