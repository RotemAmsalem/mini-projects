package filesprocessing.filters;

import filesprocessing.Filter;
import java.io.File;
import java.util.ArrayList;


/*this class implements the contains filter*/
public class ContainsFilter extends Filter {

    /*filtered the files which their names contain the nameValue*/
    private String nameValue;

    /**
     * construct the contains filter
     * @param files - the files to be filtered
     * @param notFlag - a boolean value represent whether NOT occurs in the filter line or not.
     * @param nameValue - the string the files need to contain in order to be filtered
     */
    ContainsFilter(ArrayList<File> files, Boolean notFlag, String nameValue){
        super(files, notFlag);
        this.nameValue = nameValue;
        filteredFiles = new ArrayList<>();
    }


    @Override
    protected ArrayList<File> activateFilter() {
        for (File file: filesToFiler){
            if (file.getName().contains(nameValue)){
                filteredFiles.add(file);
            }
        }
        if (notAppears){
            return notSuffix(filteredFiles);
        }
        return filteredFiles;
    }
}
