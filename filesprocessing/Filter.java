package filesprocessing;

import java.io.File;
import java.util.ArrayList;


/*this  class implements a filter*/
public abstract class Filter {

    /*a boolean flag represents wither NOT suffix appears in the filter line or not.*/
    protected Boolean notAppears;

    /*an array of the files to be filtered*/
    protected ArrayList<File> filesToFiler;

    /*an array of the filtered files*/
    protected ArrayList<File> filteredFiles;

    /*Conversion between bytes and k-bytes*/
    protected final static int BYTES_TO_KILOBYTES = 1024;

    /*string yes for the writable/executable/hidden filters*/
    protected final static String YES = "YES";

    /*string no for the writable/executable/hidden filters*/
    protected final static String NO = "NO";


    /**
     * construct a filter
     * @param input - the files to filter
     * @param notFlag - a boolean value represents whether NOT occurs in filter line or not.
     */
    public Filter(ArrayList<File> input, Boolean notFlag){
        notAppears = notFlag;
        filesToFiler = input;
    }

    /**
     * an abstract method that activate the relevant filter (according to the filter factory) and filtered
     * according to the instruction of each filter
     * @return an array list of the filtered files
     */
    protected abstract ArrayList<File> activateFilter();

    /**
     * if the NOT suffix occurs, this function is called and it returns the files which arne't meets filter
     * requirements
     * @param filteredFiles - the files which meets filter requirements
     * @return the files which arne't meets filter requirements
     */
    protected ArrayList<File> notSuffix(ArrayList<File> filteredFiles){
        ArrayList<File> notFilteredFiles = new ArrayList<>();
        for (File inputFile : filesToFiler) {
            if (!filteredFiles.contains(inputFile)){
                notFilteredFiles.add(inputFile);
            }
        }
        return notFilteredFiles;
    }
}
