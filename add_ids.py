f = open('data/loops.csv', 'r')

fo = open('data/loops_id.csv', 'w')

i = 0

for l in f:
    l = l.strip()
    fo.write(l)
    if i == 0:
        fo.write(',id\n')
    else:
        fo.write(f',{i}\n')
    i += 1
    
f.close()
fo.close()
    