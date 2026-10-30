import collections,json,gzip
def load(f):
    best={}
    for l in open(f):
        q,s,pid,ln,ql,sl,ev,bs=l.split('\t'); bs=float(bs)
        if q not in best or bs>best[q][-1]: best[q]=(s,float(pid),int(ln),int(ql),int(sl),bs)
    return best
def n(f): return sum(1 for l in gzip.open(f,'rt') if l.startswith('>'))
H=n('human.fa.gz'); B=n('banana.fa.gz')
out={}
for name,f,tot in [('banana->human','b2h.tsv',B),('human->banana','h2b.tsv',H)]:
    b=load(f); k=len(b)
    mean=sum(v[1] for v in b.values())/k
    wmean=sum(v[1]*v[2] for v in b.values())/sum(v[2] for v in b.values())
    cov=sum(min(1,v[2]/v[3]) for v in b.values())/k
    out[name]=dict(queries=tot,with_hit=k,pct_with_hit=round(100*k/tot,1),mean_pident=round(mean,1),len_weighted_pident=round(wmean,1),mean_query_coverage=round(100*cov,1))
    if name=='human->banana':
        # amino acids identical across aligned regions -> coding nucleotides (x3) vs genome
        ident_aa=sum(v[1]/100*v[2] for v in b.values()); tot_aa=sum(int(x) for x in [0])
        out['identical_aligned_residues_human']=int(ident_aa)
        out['codon_bases_equiv']=int(ident_aa*3)
        out['pct_of_3.1Gb_genome_upper_bound']=round(100*ident_aa*3/3.1e9,3)
        humanaa=0
        for l in gzip.open('human.fa.gz','rt'):
            if not l.startswith('>'): humanaa+=len(l.strip())
        out['human_proteome_residues']=humanaa
        out['proteome_coding_bases_pct_of_genome']=round(100*humanaa*3/3.1e9,2)
        out['pct_human_proteome_residues_identical_in_banana_best_hit']=round(100*ident_aa/humanaa,1)
print(json.dumps(out,indent=1)); json.dump(out,open('../results.json','w'),indent=1)
