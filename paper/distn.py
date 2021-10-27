import pandas as pd
import matplotlib.pyplot as plt

index = 0
def create_hist(df, id):
    global index
    plt.figure(index)
    index += 1
    plt.hist(df['gc_percentage'], range=(20, 80), bins=40, color='orange')
    plt.xlabel('Percent GC')
    plt.ylabel('Number of genomes (all)')
    plt.savefig(id+"_GC.png")

    plt.figure(index)
    index += 1
    plt.hist(df['contig_count'], range=(0, 1000), bins=40, color='blue')
    plt.xlabel('Contig count (max 1000 displayed)')
    plt.ylabel('Number of genomes (all)')
    plt.savefig(id+"_contig.png")

    plt.figure(index)
    index += 1
    plt.hist(df['genome_size'], range=(0, 1.25*10**7), bins=100, color='green')
    plt.xlabel('Genome size (max 1.25Gbp displayed)')
    plt.ylabel('Number of genomes (all)')
    plt.savefig(id+"_genome.png")

path = "/Users/wanxinli/Desktop/project.nosync/MLDSP/samples/arc_bac120_metadata_r202_edit.txt"
GTDB_df = pd.read_csv(path, header=0, index_col=0, sep='\t')
create_hist(GTDB_df, "GTDB_all")

GTDB_rep_df = GTDB_df.loc[GTDB_df['gtdb_representative']=='t']
create_hist(GTDB_rep_df, "GTDB_rep")

path = "/Users/wanxinli/Desktop/project.nosync/MLDSP/samples/rumen_mag_metadata.csv"
GTDB_df = pd.read_csv(path, header=0, index_col=0)
create_hist(GTDB_df, "rumen")

path = "/Users/wanxinli/Desktop/project.nosync/MLDSP/samples/Table_S1_new.csv"
HGR_df = pd.read_csv(path, header=0, index_col=0)
create_hist(HGR_df, "HGR")

path = "/Users/wanxinli/Desktop/project.nosync/MLDSP/samples/ERP108418_metadata.csv"
ERP108418_df = pd.read_csv(path, header=0, index_col=0)
create_hist(ERP108418_df, "ERP108418")