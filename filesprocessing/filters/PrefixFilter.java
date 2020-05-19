package filesprocessing.filters;

import filesprocessing.Filter;
import java.io.File;
import java.util.ArrayList;


/*this class implements the prefix filter*/
public class PrefixFilter extends Filter {

    /*filtered the files which their names starts with the mentioned prefix*/
    private String prefix;

    /**
     * construct the prefix filter
     * @param files - the files to be filtered
     * @param notFlag - a boolean value represent whether NOT occurs in the filter line or not.
     * @param prefix - the prefix which only files names starts with will be filtered.
     */
    PrefixFilter(ArrayList<File> files, Boolean notFlag, String prefix){
        super(files, notFlag);
        this.prefix = prefix;
        filteredFiles = new ArrayList<>();
    }

    @Override
    protected ArrayList<File> activateFilter() {
        for (File file: filesToFiler){
            if (file.getName().startsWith(prefix)){
                filteredFiles.add(file);
            }
        }
        if (notAppears){
            return notSuffix(filteredFiles);
        }
        return filteredFiles;
    }
}
