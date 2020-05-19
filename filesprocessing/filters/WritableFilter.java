package filesprocessing.filters;

import filesprocessing.Filter;
import java.io.File;
import java.util.ArrayList;

/*this class implements the writable filter*/
public class WritableFilter extends Filter {

    /*filtered only files that their writing permission is according to hasPermission*/
    private String hasPermission;


    /**
     * construct the writable filter
     * @param files - the files to be filtered
     * @param notFlag - a boolean value represent whether NOT occurs in the filter line or not.
     * @param hasPermission - a string of YES or NO represents whether the file has permission to write or
     *                      not.
     */
    WritableFilter(ArrayList<File> files, Boolean notFlag, String hasPermission){
        super(files, notFlag);
        this.hasPermission = hasPermission;
        filteredFiles = new ArrayList<>();
    }

    @Override
    protected ArrayList<File> activateFilter() {
        for (File file: filesToFiler){
            if ((file.canWrite() && hasPermission.equals(YES)) || (!file.canWrite() &&
                    hasPermission.equals(NO))){
                filteredFiles.add(file);
            }
        }
        if (notAppears){
            return notSuffix(filteredFiles);
        }
        return filteredFiles;
    }
}
