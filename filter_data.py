big_with_ids = open('data/loops_id.csv', 'r')
small_no_ids = open('data/loops-nopk.csv', 'r')
small_with_ids = open('data/loops-nopk_id.csv', 'w')

#Source,Type,Pattern sequence,Pattern structure,Fragment length,Fragment sequence,Fragment structure,Fragment length + stem,Fragment sequence + stem,Fragment structure + stem,Whole length,Whole sequence,Whole structure

def get_id(line):
    l = line.strip().split(',')
    return l[0], l[1], l[2], l[4], l[5], l[7], l[8], l[10], l[11]

filtered = set()
for line in small_no_ids:
    print('!', line, '!')
    filtered.add(get_id(line))

for line in big_with_ids:
    if get_id(line) in filtered:
        small_with_ids.write(line)

big_with_ids.close()
small_no_ids.close()
small_with_ids.close()