package runnables;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

import pojos.*;
import singletons.GenomicMapper;

public class FileProcessingThread extends Thread{


	private String filePath, outputFileSuffix;
	private Map<String, String> sampleMapping;
	public FileProcessingThread(String filePath, Map<String, String> sampleMapping, String outputFileSuffix){
		this.filePath=filePath;
		this.sampleMapping=sampleMapping;
		this.outputFileSuffix=outputFileSuffix;
	}
	
	@Override
	public void run() {	
		parse();	
	}
	
	private void parse(){
		
		File file = new File(this.filePath);
		String sampleId=sampleMapping.get(file.getName()).substring(0,12);
		BufferedReader reader = null;
		String containingDirectory=file.getParent();

		Map<String, List<Double>> data=new HashMap<String, List<Double>>();
		try {
		    reader = new BufferedReader(new FileReader(file));
		    String line = null;
            int lineCount=0;
            Gene currentGene=null;
            List<Double> exonList=new ArrayList<Double>();
		    while ((line = reader.readLine()) != null) {
		    	if(lineCount>0){
		    		Exon ex=parseLineToExon(line);
		    		if (currentGene!=null){
		    			if(!currentGene.contains(ex)){
		    				if(exonList.size()>0){
		    					data.put(currentGene.getGeneName(), new ArrayList<Double>(exonList));
		    			    	//writeToFile(containingDirectory, currentGene.getGeneName(), sampleId, exonList);
		    				}
		    				currentGene=determineGeneForNewExon(ex);
		    				exonList.clear();
		    			}
		    		}
		    		else{
	    				currentGene=determineGeneForNewExon(ex);
	    				exonList.clear();
		    		}
		    		exonList.add(ex.getRpkm());
		    	}
		    	else{
		    		lineCount++;
		    	}
		    }
		    if(currentGene!=null){
				data.put(currentGene.getGeneName(), new ArrayList<Double>(exonList));

		    }
		    writeToFile(containingDirectory, sampleId, data);
		} catch (FileNotFoundException e) {
		    e.printStackTrace();
		} catch (IOException e) {
		    e.printStackTrace();
		} finally {
		    try {
		        if (reader != null) {
		            reader.close();
		        }
		    } catch (IOException e) {
		    	System.out.println("IO exception when closing");
		    }
		}
	}

	private Gene determineGeneForNewExon(Exon ex) {
		
		List<Gene> genesOnChromosome=GenomicMapper.mapping.get(ex.getChromosome());
		if(genesOnChromosome!=null){
			for(Gene g: genesOnChromosome){
				if(g.contains(ex)){
					return g;
				}
			}
		}
		return null;
	}

	private Exon parseLineToExon(String line) {
	    String[] fields=line.split("\t");
	    String genomicPosition=fields[0];
	    String rpkmStr=fields[3];
	    Double rpkm=null;
	    if (rpkmStr.length()>1){
	    	rpkm=Double.parseDouble(rpkmStr.substring(0, fields[3].length()-1));
	    }
	    else{
	    	rpkm=0.0;
	    }
	    String[] info=genomicPosition.split(":");
	    String chr=info[0];
	    String range=info[1];
	    String strand=info[2];
	    String[] positionRange=range.split("-");
	    long start=Integer.parseInt(positionRange[0]);
	    long end=Integer.parseInt(positionRange[1]);
	    return new Exon(chr, start, end, rpkm, strand);
	}
	
	public void writeToFile(String directory, String sampleId, Map<String, List<Double>> data){
		try {
			  
			File file = new File(directory+File.separator+sampleId+this.outputFileSuffix);
			// if file doesnt exists, then create it
			if (!file.exists()) {
				file.createNewFile();
			}
 
			FileWriter fw = new FileWriter(file.getAbsoluteFile());
			BufferedWriter bw = new BufferedWriter(fw);
			
			for(String gene: data.keySet()){
				bw.write(sampleId+":"+gene+"\t");
				List<Double> exonList=data.get(gene);
				for(Double exonExp: exonList){
					bw.write(exonExp+"\t");
				}
				bw.write("\n");
			}
			bw.close();
  
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}
