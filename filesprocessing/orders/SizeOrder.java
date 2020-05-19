package filesprocessing.orders;

import filesprocessing.Order;
import java.io.File;
import java.util.ArrayList;

/*this class implements the size order*/
public class SizeOrder extends Order {

    /*represents a negative number to the compare value*/
    private final static int NEGATIVE_NUM = -1;

    /*represents a positive number to the compare value*/
    private final static int POSITIVE_NUM = 1;

    /**
     * construct the size order
     * @param files - the filtered files to be ordered
     * @param reverseFlag - a boolean value represent whether REVERSE occurs in the order line or not.
     */
    SizeOrder(ArrayList<File> files, Boolean reverseFlag) {
        super(files, reverseFlag);
        orderedFiles = new File[files.size()];
    }

    @Override
    public int compare(File a, File b) {
        if (a.length() == b.length()) {
            return a.getAbsolutePath().compareTo(b.getAbsolutePath());
        }
        if (a.length() > b.length()){
            return POSITIVE_NUM;
        }
        return NEGATIVE_NUM;
    }
}
