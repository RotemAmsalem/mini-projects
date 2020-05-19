package filesprocessing.filters;

import filesprocessing.Filter;
import java.io.File;
import java.util.ArrayList;

/*this class implements the file filter*/
public class FileFilter extends Filter {

    /*filtered the files which their names equal the fileName (excluding path)*/
    private String fileName;

    /**
     * construct the file filter
     * @param files - the files to be filtered
     * @param notFlag - a boolean value represent whether NOT occurs in the filter line or not.
     * @param fileName - the name that only the files with the exact same name are filtered.
     */
    FileFilter(ArrayList<File> files, Boolean notFlag, String fileName){
        super(files, notFlag);
        this.fileName = fileName;
        filteredFiles = new ArrayList<>();
    }


    @Override
    protected ArrayList<File> activateFilter() {
        for (File file: filesToFiler){
            if (file.getName().equals(fileName)){
                filteredFiles.add(file);
            }
        }
        if (notAppears){
            return notSuffix(filteredFiles);
        }
        return filteredFiles;
    }
}
