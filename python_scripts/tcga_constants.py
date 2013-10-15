PLATFORMS=("IlluminaHiSeq_RNASeqV2",)

#NUM_CENTERS is the count of the contributing centers-- see the "Center" table at https://tcga-data.nci.nih.gov/datareports/codeTablesReport.htm
NUM_CENTERS=32
CENTERS=(i+1 for i in range(NUM_CENTERS))

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
