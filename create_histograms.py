from matplotlib import pyplot as plt
import os

def to_int(s):
    try:
        s = int(s)
    except:
        s = -100
    return s

def main():
    for fn in os.listdir('results'):
        if '_res.' not in fn: continue
        res = {}
        res['sequence'] = {}
        res['structure'] = {}
        res['sequence_extended'] = {}
        res['structure_extended'] = {}

        
        heatmap = [[0]*21 for _ in range(41)]
        heatmap_ext = [[0]*21 for _ in range(41)]
        
        f = open(f'results/{fn}', 'r')
        
        for l in f:
            l = l.strip().split(';')
            
            seq_score = to_int(l[4])
            struct_score = to_int(l[6])
            
            seq_ext_score = to_int(l[8])
            struct_ext_score = to_int(l[10])
            
            if 0 <= seq_score + 20 <= 40 and 0 <= struct_score <= 20:
                heatmap[seq_score + 20][struct_score] += 1
                
            if 0 <= seq_ext_score + 20 <= 40 and 0 <= struct_ext_score <= 20:    
                heatmap_ext[seq_ext_score + 20][struct_ext_score] += 1
                
            res['sequence'][seq_score] = res['sequence'].get(seq_score, 0) + 1
            res['structure'][struct_score] = res['structure'].get(struct_score, 0) + 1
            
            res['sequence_extended'][seq_ext_score] = res['sequence_extended'].get(seq_ext_score, 0) + 1
            res['structure_extended'][struct_ext_score] = res['structure_extended'].get(struct_ext_score, 0) + 1
            
        
        for mode in res:
            fig, ax = plt.subplots()
            
            hist = res[mode]
            hist = list(hist.items())
            hist.sort()
            
            data = list(zip(*hist))
            print(data[0], data[1])
            
            ax.bar(data[0], data[1])
            fig.savefig(f'plots/{mode}/{fn[:-4]}.pdf')
            plt.close(fig)
            
        fig, ax = plt.subplots()
        ax.imshow(heatmap)
        fig.savefig(f'plots/heatmaps/{fn[:-4]}.pdf')
        plt.close(fig)
        
        fig, ax = plt.subplots()
        ax.imshow(heatmap_ext)
        fig.savefig(f'plots/heatmaps/{fn[:-4]}_ext.pdf')
        plt.close(fig)
        

  
main()
        