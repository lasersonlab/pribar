import sys

from click import command, option
from llutil.unafold import melting_temp, hybrid_ss_min, hybrid_min


def readfq(fp): # this is a generator function
    last = None # this is a buffer keeping the last unprocessed line
    while True: # mimic closure; is it a bad idea?
        if not last: # the first record or a record following a fastq
            for l in fp: # search for the start of the next record
                if l[0] in '>@': # fasta/q header line
                    last = l[:-1] # save this line
                    break
        if not last: break
        name, seqs, last = last[1:].partition(" ")[0], [], None
        for l in fp: # read the sequence
            if l[0] in '@+>':
                last = l[:-1]
                break
            seqs.append(l[:-1])
        if not last or last[0] != '+': # this is a fasta record
            yield name, ''.join(seqs), None # yield a fasta record
            if not last: break
        else: # this is a fastq record
            seq, leng, seqs = ''.join(seqs), 0, []
            for l in fp: # read the quality
                seqs.append(l[:-1])
                leng += len(l) - 1
                if leng >= len(seq): # have read enough quality
                    last = None
                    yield name, seq, ''.join(seqs); # yield a fastq record
                    break
            if last: # reach EOF before reading enough quality
                yield name, seq, None # yield a fasta record instead
                break


@command()
@option('--tm-min', type=float, default=-1)
@option('--tm-max', type=float, default=500)
@option('--ss-dg-min', type=float, default=-10000)
@option('--ss-dg-max', type=float, default=10000)
@option('--self-hyb-dg-min', type=float, default=-10000)
@option('--self-hyb-dg-max', type=float, default=10000)
def main(tm_min, tm_max, ss_dg_min, ss_dg_max, self_hyb_dg_min, self_hyb_dg_max):
    names, seqs, quals = zip(*list(readfq(sys.stdin)))
    tms = melting_temp(seqs)
    ss_dgs = hybrid_ss_min(seqs)
    self_hyb_dgs = hybrid_min(seqs, seqs)
    for name, seq, tm, ss_dg, self_hyb_dg in zip(names, seqs, tms, ss_dgs, self_hyb_dgs):
        conditions = [
            tm < tm_min,
            tm > tm_max,
            ss_dg < ss_dg_min,
            ss_dg > ss_dg_max,
            self_hyb_dg[0] < self_hyb_dg_min,
            self_hyb_dg[0] > self_hyb_dg_max]
        if any(conditions):
            continue
        print(f'>{name}\n{seq}')


if __name__ == '__main__':
    main()
