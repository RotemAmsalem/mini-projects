package filesprocessing.filters;

import filesprocessing.Filter;
import java.io.File;
import java.util.ArrayList;


/*this class implements the suffix filter*/
public class SuffixFilter extends Filter {

    /*filtered the files which their names ends with the mentioned suffix*/
    private String suffix;

    /**
     * construct the suffix filter
     * @param files - the files to be filtered
     * @param notFlag - a boolean value represent whether NOT occurs in the filter line or not.
     * @param suffix - the suffix which only files names ended up with will be filtered.
     */
    SuffixFilter(ArrayList<File> files, Boolean notFlag, String suffix){
        super(files, notFlag);
        this.suffix = suffix;
        filteredFiles = new ArrayList<>();
    }


    @Override
    protected ArrayList<File> activateFilter() {
        for (File file: filesToFiler){
            if (file.getName().endsWith(suffix)){
                filteredFiles.add(file);
            }
        }
        if (notAppears){
            return notSuffix(filteredFiles);
        }
        return filteredFiles;
    }
}
