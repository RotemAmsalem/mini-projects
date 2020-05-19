package filesprocessing.filters;

import filesprocessing.Filter;
import java.io.File;
import java.util.ArrayList;


/*this class implements the between filter*/
public class BetweenFilter extends Filter {

    /*filtered only files their size is grater than this value (and grater than upperBound)*/
    private double lowerBound;

    /*filtered only files their size is less than this value(and smaller than lowerBound)*/
    private double upperBound;


    /**
     * construct the between filter
     * @param files - the files to be filtered
     * @param notFlag - a boolean value represent whether NOT occurs in the filter line or not.
     * @param minValue - the lower bound of the range the file's size can be at
     * @param maxValue - the upper bound of the range the file's size can be at
     */
    BetweenFilter(ArrayList<File> files, Boolean notFlag, double minValue, double maxValue){
        super(files, notFlag);
        lowerBound = minValue;
        upperBound = maxValue;
        filteredFiles = new ArrayList<>();
    }

    @Override
    protected ArrayList<File> activateFilter() {
        for (File file: filesToFiler){
            if ((double) file.length() / BYTES_TO_KILOBYTES >= lowerBound && (double) file.length() /
                    BYTES_TO_KILOBYTES <= upperBound){
                filteredFiles.add(file);
            }
        }
        if (notAppears){
            return notSuffix(filteredFiles);
        }
        return filteredFiles;
    }
}
