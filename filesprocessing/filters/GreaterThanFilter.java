package filesprocessing.filters;

import filesprocessing.Filter;
import java.io.File;
import java.util.ArrayList;


/*this class implements the greater_than filter*/
public class GreaterThanFilter extends Filter {

    /*Files that there size is strictly greater than the given lowerBound of k-bytes will be filtered*/
    private double lowerBound;

    /**
     * construct the greater_than filter
     * @param files- the files to be filtered
     * @param notFlag - a boolean value represent whether NOT occurs in the filter line or not.
     * @param minValue - the lower bound of the range the file's size can be at
     */
    GreaterThanFilter(ArrayList<File> files, Boolean notFlag, double minValue){
        super(files, notFlag);
        lowerBound = minValue;
        filteredFiles = new ArrayList<>();
    }

    @Override
    protected ArrayList<File> activateFilter() {
        for (File file: filesToFiler){
            if ((double) file.length() / BYTES_TO_KILOBYTES > lowerBound){
                filteredFiles.add(file);
            }
        }
        if (notAppears){
            return notSuffix(filteredFiles);
        }
        return filteredFiles;
    }
}
