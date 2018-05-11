from click import command, option
from llutil.seqs import random_dna_seq


@command()
@option('-n', '--number', type=int, required=True)
@option('-l', '--length', type=int, required=True)
@option('-p', '--prefix', default='primer')
def main(number, length, prefix):
    for i in range(number):
        name = f'{prefix}{i:06d}'
        seq = random_dna_seq(length)
        print(f'>{name}\n{seq}')


if __name__ == '__main__':
    main()
