package pojos;

public class Gene {

	private String chromosome, geneName;
	private long start_pos, end_pos;
	
	public Gene(String chr, long start, long end, String name){
		this.chromosome=chr;
		this.start_pos=start;
		this.end_pos=end;
		this.geneName=name;
	}

	public String getChromosome() {
		return chromosome;
	}

	public void setChromosome(String chromosome) {
		this.chromosome = chromosome;
	}

	public String getGeneName() {
		return geneName;
	}

	public void setGeneName(String geneName) {
		this.geneName = geneName;
	}

	public long getStart_pos() {
		return start_pos;
	}

	public void setStart_pos(long start_pos) {
		this.start_pos = start_pos;
	}

	public long getEnd_pos() {
		return end_pos;
	}

	public void setEnd_pos(long end_pos) {
		this.end_pos = end_pos;
	}
	
	public boolean contains(Exon exon){
		if(exon.getChromosome().equals(this.chromosome)){
			if(exon.getStart_pos()>=this.start_pos && exon.getEnd_pos()<=this.end_pos){
				return true;
			}
		}
		return false;
	}

	@Override
	public String toString() {
		return "Gene [chromosome=" + chromosome + ", geneName=" + geneName
				+ ", start_pos=" + start_pos + ", end_pos=" + end_pos + "]";
	}
	
	
	
}
