big_with_ids = open('data/loops_id.csv', 'r')
small_no_ids = open('data/loops-nopk.csv', 'r')
small_with_ids = open('data/loops-nopk_id.csv', 'w')

filtered = set()
for line in small_no_ids:
    line = line.strip()
    filtered.add(line)

for line in big_with_ids:
    line = line.strip()
    line_no_id = ','.join(line.split(',')[:-1])
    if line_no_id in filtered:
        small_with_ids.write(line)
        small_with_ids.write('\n')


big_with_ids.close()
small_no_ids.close()
small_with_ids.close()