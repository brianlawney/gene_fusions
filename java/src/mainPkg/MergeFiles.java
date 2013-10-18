package mainPkg;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import pojos.Gene;
import runnables.CohortThread;
import runnables.FileProcessingThread;
import singletons.GenomicMapper;

public class MergeFiles {

	private static final String EXON_FILE_EXTENSION="exon_quantification.txt";
	private static final String SAMPLE_MAP_FILE="FILE_SAMPLE_MAP.txt";

	
	public static void main(String[] args) {

		String directoryPath=args[0];
		String outputFileSuffix=args[1];
		System.out.println("reading files in "+directoryPath);
		File dir=new File(directoryPath);
		
		List<File> allFiles=addFiles(null, dir);
		List<String> exonFiles=new ArrayList<String>();
		String mapFilePath="";
		for (File f:allFiles){
			if(f.getAbsolutePath().endsWith(EXON_FILE_EXTENSION)){
				exonFiles.add(f.getAbsolutePath());
			}
			if(f.getAbsolutePath().endsWith(SAMPLE_MAP_FILE)){
				mapFilePath=f.getAbsolutePath();
			}
		}
		
		Map<String, String> fileToSampleMap=createFileToSampleMap(mapFilePath);
		
		//spawn a thread for each of the files that needs to be processed
		List<Thread> threads=new ArrayList<Thread>();
        for (String file: exonFiles){

    		Thread t=new FileProcessingThread(file, fileToSampleMap, outputFileSuffix);
    		threads.add(t);
    		t.start();
        }
        
        for (Thread thread:threads){
        	try {
				thread.join();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
        }
	}

	
	private static List<File> addFiles(List<File> files, File dir)
	{
	    if (files == null)
	        files = new ArrayList<File>();

	    if (!dir.isDirectory())
	    {
	        files.add(dir);
	        return files;
	    }

	    for (File file : dir.listFiles())
	        addFiles(files, file);
	    return files;
	}
	
	private static Map<String, String> createFileToSampleMap(String mapFilePath) {
		Map<String, String> map=new HashMap<String, String> ();
		File file = new File(mapFilePath);
		BufferedReader reader = null;
		try {
		    reader = new BufferedReader(new FileReader(file));
		    String line = null;
            int lineCount=0;
		    while ((line = reader.readLine()) != null) {
		    	if (lineCount>0){
		    		String[] lineData=line.split("\t");
		    		if(lineData[0].endsWith(EXON_FILE_EXTENSION)){
		    			map.put(lineData[0], lineData[1]);
		    		}
		    	}
		    	else{
		    		lineCount++;
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
		return map;
	}
    
}