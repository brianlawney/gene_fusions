package pojos;

public class Exon {
	private String chromosome;
	private long start_pos, end_pos;
	private double rpkm;
	private String strand;
	
	public Exon(String chr, long start, long end, double rpkm, String strand){
		this.chromosome=chr;
		this.start_pos=start;
		this.end_pos=end;
		this.rpkm=rpkm;
		this.setStrand(strand);
	}
	
	public String getChromosome() {
		return chromosome;
	}

	public void setChromosome(String chromosome) {
		this.chromosome = chromosome;
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

	public double getRpkm() {
		return rpkm;
	}

	public void setRpkm(double rpkm) {
		this.rpkm = rpkm;
	}

	public String getStrand() {
		return strand;
	}

	public void setStrand(String strand) {
		this.strand = strand;
	}

}
