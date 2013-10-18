package singletons;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import pojos.Gene;

public class GenomicMapper {

	public static String GTF_FILE="//home//tessella//gene_fusions//genes_only.gtf";
	public static final Map<String, List<Gene>> mapping;
	//guard instantiation
	private GenomicMapper(){		
	}

	static{
			
		Map<String, List<Gene>> temp_mapping=new HashMap<String, List<Gene>>();
		
		File file = new File(GTF_FILE);
		BufferedReader reader = null;

		try {
		    reader = new BufferedReader(new FileReader(file));
		    String line = null;

		    while ((line = reader.readLine()) != null) {
		        String[] split_line=line.split("\t");
		        String chromosome=split_line[0];
		        long start_pos=Integer.parseInt(split_line[3]);
		        long end_pos=Integer.parseInt(split_line[4]);
		        String extra_field=split_line[8];

		        String[] extras=extra_field.trim().split(";");
		        String geneName="";
		        for (String e: extras){
		        	e=e.trim();
		        	if(e.contains("gene_name")){
		        		geneName=e.split("\\s")[1]; //has quotes
		        	    geneName=geneName.substring(1, geneName.length()-1);
		        	}
		        }
		        
		        Gene this_gene=new Gene(chromosome, start_pos, end_pos, geneName);

	        	List<Gene> existingList=temp_mapping.get(chromosome);
	        	if (existingList!=null){
	        		existingList.add(this_gene);
	        		temp_mapping.put(chromosome, existingList);
	        	}
	        	else{
	        		List<Gene> newList=new ArrayList<Gene>();
	        		newList.add(this_gene);
	        		temp_mapping.put(chromosome, newList);
	        	}		        
		    }

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
		mapping=Collections.unmodifiableMap(temp_mapping);
	}
}
