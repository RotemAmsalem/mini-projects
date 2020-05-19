package filesprocessing.orders;

import filesprocessing.Order;
import java.io.File;
import java.util.*;


/*this class implements the type order*/
public class TypeOrder extends Order {


    /**
     * construct the type order
     * @param files - the filtered files to be ordered
     * @param reverseFlag - a boolean value represent whether REVERSE occurs in the order line or not.
     */
    TypeOrder(ArrayList<File> files, Boolean reverseFlag) {
        super(files, reverseFlag);
        orderedFiles = new File[files.size()];
    }

    /**
     * finds the extension of the file
     * @param file - the file to find its extension
     * @return the extension of the file
     */
    private String findExtension(File file) {
        String filePath = file.getAbsolutePath();
        int lastIndexOfPeriod = filePath.lastIndexOf(".");
        if (lastIndexOfPeriod == 0 || lastIndexOfPeriod == -1 || lastIndexOfPeriod == file.length() - 1) {
            return EMPTY_STRING;
        }
        return filePath.substring(lastIndexOfPeriod);
    }


    @Override
    public int compare(File a, File b) {
        int compareResult = findExtension(a).compareTo(findExtension(b));
        if (compareResult == 0){
            return (a.getAbsolutePath()).compareTo(b.getAbsolutePath());
        }
        return compareResult;
    }
}
