package filesprocessing.filters;

import filesprocessing.Filter;
import java.io.File;
import java.util.ArrayList;


/*this class implements the smaller_than filter*/
public class SmallerThanFilter extends Filter {

    /*Files that there size is strictly less than the given upperBound of k-bytes will be filtered*/
    private double upperBound;

    /**
     * construct the smaller_than filter
     * @param files - the files to be filtered
     * @param notFlag - a boolean value represent whether NOT occurs in the filter line or not.
     * @param maxValue - the upper bound of the range the file's size can be at
     */
    SmallerThanFilter(ArrayList<File> files, Boolean notFlag, double maxValue){
        super(files, notFlag);
        upperBound = maxValue;
        filteredFiles = new ArrayList<>();
    }

    @Override
    protected ArrayList<File> activateFilter() {
        for (File file: filesToFiler){
            if ((double) file.length() / BYTES_TO_KILOBYTES < upperBound){
                filteredFiles.add(file);
            }
        }
        if (notAppears){
            return notSuffix(filteredFiles);
        }
        return filteredFiles;
    }
}
