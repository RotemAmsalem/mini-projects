package filesprocessing.orders;

import filesprocessing.Order;
import java.io.File;
import java.util.ArrayList;


/*this class implements the abs order*/
public class AbsOrder extends Order {


    /**
     * construct the abs order
     * @param files - the filtered files to be ordered
     * @param reverseFlag - a boolean value represent whether REVERSE occurs in the order line or not.
     */
    AbsOrder(ArrayList<File> files, Boolean reverseFlag) {
        super(files, reverseFlag);
        orderedFiles = new File[files.size()];
    }

    @Override
    public int compare(File a, File b) {
        return a.getAbsolutePath().compareTo(b.getAbsolutePath());
    }
}
