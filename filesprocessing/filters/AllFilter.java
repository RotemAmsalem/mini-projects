package filesprocessing.filters;

import filesprocessing.Filter;
import java.io.File;
import java.util.ArrayList;


/*this class implements the all filter*/
public class AllFilter extends Filter {


    /**
     * construct the all filter
     * @param files - the files to be filtered
     * @param notFlag - a boolean value represent whether NOT occurs in the filter line or not.
     */
    AllFilter(ArrayList<File> files, Boolean notFlag){
        super(files, notFlag);
        filteredFiles = new ArrayList<>();
    }

    @Override
    protected ArrayList<File> activateFilter() {
        filteredFiles.addAll(filesToFiler);
        if (notAppears){
            return notSuffix(filteredFiles);
        }
        return filteredFiles;
    }
}
