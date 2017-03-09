# WGBS_Tools

WGBS_Tools is a versatile toolkit to manipulate and analyze Whole Genome Bisulfite Sequencing data. Any questions or comments may be directed to Keith Dunaway (kwdunaway@ucdavis.edu). If you find any problems, please create a github issue.

### Table of Contents

1. [Installation](#Installation)
1. [Commands](#Commands)
  1. [add_genome](#add_genome)
  1. [process_se](#process_se)
  1. [process_pe](#process_pe)
  1. [trim_sefq](#trim_sefq)
  1. [trim_pefq](#trim_pefq)
  1. [roi](#roi)
  1. [window](#window)
  1. [pm_stats](#pm_stats)
  1. [pm2bg](#pm2bg)
  1. [pm2dss](#pm2dss)
1. [File Formats](#FileFormats)
  1. [info.yaml](#infoyaml)
  1. [pm_bed](#pm_bed)
  1. [meth_table](#meth_table)
1. [Version History](#VersionHistory)

## <a name="Installation"> Installation </a>

**Note:** It is recommended that you set up a virtual environment prior
to installing wgbs_tools. The author uses *venv* and will assume you are
doing the same. While not supported, using a another virtual environment
will most likely not make a difference. 

### Prerequisites:

Before installation, essure that he following programs are installed and
accessible in PATH:

- [Bowtie](http://bowtie-bio.sourceforge.net/manual.shtml)
- [BS-Seeker2](https://github.com/BSSeeker/BSseeker2)
- [Pysam](https://github.com/pysam-developers/pysam)
- [Bedtools2](https://github.com/arq5x/bedtools2)
- [SRA Toolkit](http://www.ncbi.nlm.nih.gov/books/NBK158900/)

Also, the following python packages will be installed if not already:

- click
- pybedtools
- pysam
- pytest
- pyyaml

### Instructions:

1. Change directory to WGBS_tools and type the following:

   ```
   python setup.py develop
   ```
1. Test to ensure everything installed correctly:

   ```
   pytest tests
   ```
1. Brief descriptions of each command are given using:

   ```
   wgbs_tools --help
   ```
   
1. You can also get instructions for a specific command by typing the command name with --help. For instance:

   ```
   wgbs_tools add_genome --help
   ```

1. Download and decompress your genome's fasta file. You can find many using the UCSC download page: http://hgdownload.cse.ucsc.edu/downloads.html

1. Create a BS Seeker2 index from the fasta file. See [BS-Seeker2](https://github.com/BSSeeker/BSseeker2) for instructions.

1. Edit or create your own *info.yaml* file. See [info.yaml](#infoyaml) and [add_genome](#add_genome) for more details.

## <a name="Commands"> Commands </a>

Each command is accessed by typing *wgbs_tools* followed by the command name. Syntax and brief explanations are provided
using the *--help* option. For instance:

   ```
   wgbs_tools roi --help
   ```

This manual is meant to provide additional information and context for the commands. It is assumed that the user typed
*--help* for a given command before reading this manual. If there is still confusion, please email the author
(contact information at the top).

### <a name="add_genome"> add_genome </a>

Adds genome information to info.yaml file. By default it appends the *info.yaml* file in WGBS_Tools directory. 
However, you can change this using the *--infoyaml* option. See [info.yaml](#infoyaml) for more information 
about the *info.yaml* file.

### <a name="process_se"> process_se </a>

The main pipeline to process a single end WGBS experiment. It takes in a single fastq file and outputs the following:

1. Bam containing all of the aligned reads in BS_Seeker format. See [BS-Seeker2](https://github.com/BSSeeker/BSseeker2) for more details.
1. Folder containing a single Percent Methylation bed file for each chromosome. See [pm_bed](#pm_bed) for more information about the format.
1. Log of BS_Seeker2 run which has useful overall information about the sequencing run.
1. Bisulfite conversion efficency information.
1. Summary file containing stats about alignment and conversion efficency.

The defaults are set for determining CpG methylation in a hg38 experiment which used 100bp Illumina reads sequenced on the HiSeq 2000. 
However, the options can modified to work for your specific genome/experiment.

### <a name="process_pe"> process_pe </a>

The main pipeline to process a paired end WGBS experiment. It takes in a pair of fastq files and outputs the same as [process_se](#process_se).

### <a name="trim_pefq"> trim_sefq </a>

Prepares a single end fastq file for alignment by:

1. Filtering out any reads that do not pass Illumina's quality check (if that information is available in the header line of the read).
1. Trims off adapter sequence. This is done by searching the read for the adapter sequence given in the *yaml.info* file, and removing all bases starting at that sequence and on.
1. Removes 10bp from the 3' end of all reads (after adapter trimming). 

### <a name="trim_pefq"> trim_pefq </a>

### <a name="roi"> roi </a>

Finds methylation over Regions of Interest (ROIs). The inputs:

1. INPUT_TSV: Input tab separated file indicating sample names and locations.
  1. The first tab should be sample name
  1. The second tab should be the path to the prefix of bed file
               Ex file format:
               pm01   tests/data/bed/pm01_
               pm02   tests/data/bed/pm02_
1. OUT_TABLE: Name of the table which contains all of the ROI methylation information
1. ROI_FILE: GTF or BED file indicating the ROI (Regions of Interest).
 
 This takes in a BED or GTF file and a  and creates a table that contains the methylation percentage over all Regions
  of Interest (ROIs). Allows creation of an optional 2col table which
  contains the number of methylated and total reads per sample per ROI.

  roi        Calls methylation over ROIs.

### <a name="window"> window </a>
  window     Calls methylation over windows.

### <a name="pm_stats"> pm_stats </a>
  pm_stats   Gets stats of multiple pm_bed files.

### <a name="pm2bg"> pm2bg </a>
  pm2bg      Converts pm_bed to bedgraph format.

### <a name="pm2dss"> pm2dss </a>
  pm2dss     Converts pm_bed to dss format.

## <a name="FileFormats"> File Formats </a>

### <a name="infoyaml"> info.yaml </a>

This is a yaml file that contains system and genome specific information. It is outside of the 
code so that any user can easily modify it to work for whatever WGBS experiment they desire. You can 
create experiment specific *.yaml* files and point to each differently using the *--infoyaml* option.
Alternatively, you can have a single file with multiple genomes, depending on your preferences.

The first two lines of *info.yaml* will most likely not need to be modified:

**adapter:** The adapter sequence for single end reads. This is used to trim reads that have 
adapter contamination. It may need to be changed if you are not using Illumina sequencing.

**bs2_path:** The path for BS Seeker2 aligner. It is set assuming BS Seeker2 is in PATH. 
You can change this to point to a specific instance of BS Seeker 2 or if you did not put it in PATH.

The rest of the file contains genome specific information. You can have multiple genomes represented 
in the same file, but each genome must have a unique name. In order to add your genome of interest, 
use the [add_genome](#add_genome) command. The format is:

**genome:** Genome name. This needs to be unique throughout the *info.yaml* file.

**index:** Path to the BS Seeker2 index for this genome. (2 spaces preceding) 

**fasta:** Location of a single fasta file containing all chromosomal sequences. (2 spaces preceding)

**chroms:** (2 spaces preceding, nothing after the **:** on this line)

***chromname: size*** Chromosome name (as defined by fasta/bs2index) and then size of chromosome 
in bp. Each line represents a different chromosome. You don't need every chromosome listed here, 
just the ones you want analyzed. For instance, there could be unlocalized contig names that you may 
not want to keep in your analysis. (6 spaces preceding)

You can modify the provided *info.yaml* file, or create a new one. Any commands that use this can 
point to a different file using the *--infoyaml* option.

### <a name="pm_bed"> pm_bed </a>

Percent Methylation bed (pm_bed) files contain base specific methylation information (usually for 
a single chromosome). It is based on the 9 column bed format and can be loaded into most genome browsers 
(like the [UCSC browser](http://genome.ucsc.edu/)):

1. chromosome
1. start of C
1. end of C (1 base away)
1. percent methylation and number of reads contributing to the permeth call (separate by a *-*)
1. 0 (placeholder for bed format)
1. strand (if CpG then it says + but is really a combination of both strands)
1. 0 (placeholder for bed format)
1. 0 (placeholder for bed format)
1. color (in RRR,GGG,BBB format)

***Note:*** The first line of the file is usually a header with meta information.

### <a name="meth_table"> meth_table </a>

Methylation tables are created as a way to determine the average methylation over a given area. They
are produced by both the [roi](#roi) and [window](#window) commands. The format for these files are:

1. chromosome
1. start
1. end
1. sample 1 methylation %
1. sample 2 methylation % ... (etc.)

There is also the option for printing the "raw" information. This is useful if you have further
calculations that you want to do and need read counts rather than a percentage of methylation
averaged across the region of interest. The format for these files are:

1. chromosome
1. start
1. end
1. sample 1 methylated read count
1. sample 1 total read count
1. sample 2 methylated read count
1. sample 2 total read count ... (etc.)

## <a name="VersionHistory"> Version History </a>
__0.1__:
Initial conversion of scripts to python. Improvements in multiprocessing, installation, and readability were implimented as well.

__0.0.perl__:
Most of these scripts were originally written in Perl and used in the publications:
http://www.cell.com/cell-reports/fulltext/S2211-1247(16)31631-X
https://www.ncbi.nlm.nih.gov/pubmed/28032673
However, many improvements in performance, installation ease, and understandability were implimented since this version. If you still want those scripts, please go to folder: WGBS_Tools/perl

