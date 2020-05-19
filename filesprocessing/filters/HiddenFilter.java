package filesprocessing.filters;

import filesprocessing.Filter;
import java.io.File;
import java.util.ArrayList;


/*this class implements the hidden filter*/
public class HiddenFilter extends Filter {

    /*filtered only files that are hidden or not, according to isHidden*/
    private String isHidden;

    /**
     * construct the hidden filter
     * @param files - the files to be filtered
     * @param notFlag - a boolean value represent whether NOT occurs in the filter line or not.
     * @param isHidden - a string of YES or NO represents whether the file is hidden or not.
     */
    HiddenFilter(ArrayList<File> files, Boolean notFlag, String isHidden){
        super(files, notFlag);
        this.isHidden = isHidden;
        filteredFiles = new ArrayList<>();
    }

    @Override
    protected ArrayList<File> activateFilter() {
        for (File file: filesToFiler){
            if ((file.isHidden() && isHidden.equals(YES)) || (!file.isHidden() && isHidden.equals(NO))){
                filteredFiles.add(file);
            }
        }
        if (notAppears){
            return notSuffix(filteredFiles);
        }
        return filteredFiles;
    }
}
