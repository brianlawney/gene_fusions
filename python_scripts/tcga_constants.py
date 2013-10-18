FILE_MERGE_JAR='/home/tessella/gene_fusions/java/build/jar/MergeFiles.jar'

MAPPED_FILE_SUFFIX='_mapped.txt'
MERGED_FILE='merged_samples.txt'

EXON_FILE_EXTENSION='exon_quantification.txt'

MERGED_FILE_NAME='merged_samples.txt'
GTF_FILE='/home/tessella/gene_fusions/genes_only.gtf'

PLATFORMS=("IlluminaHiSeq_RNASeqV2",)

#NUM_CENTERS is the count of the contributing centers-- see the "Center" table at https://tcga-data.nci.nih.gov/datareports/codeTablesReport.htm
NUM_CENTERS=32
CENTERS=[i+1 for i in range(NUM_CENTERS)]

TCGA_COHORTS=(
"LAML",
"ACC",
"BLCA",
"LGG",
"BRCA",
"CESC",
"LCML",
"COAD",
"ESCA",
"GBM",
"HNSC",
"KICH",
"KIRC",
"KIRP",
"LIHC",
"LUAD",
"LUSC",
"DLBC",
"MESO",
"OV",
"PAAD",
"PCPG",
"PRAD",
"READ",
"SARC",
"SKCM",
"STAD",
"TGCT",
"THCA",
"UCS",
"UCEC",
"UVM")
