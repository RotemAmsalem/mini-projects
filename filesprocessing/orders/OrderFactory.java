package filesprocessing.orders;

import filesprocessing.Order;
import java.io.File;
import java.util.ArrayList;


/*this class builds an order*/
public class OrderFactory {

    /*the abs order*/
    private final static String ABS_ORDER = "abs";

    /*the size order*/
    private final static String SIZE_ORDER = "size";

    /*the type order*/
    private final static String TYPE_ORDER = "type";

    /*the REVERSE suffix*/
    private final static String REVERSE = "REVERSE";

    /*the separator of the filter line (between order and REVERSE)*/
    private final static String SEPARATOR = "#";


    /**
     * finds the order according to the order line
     * @param line - the order line
     * @param files - the files to be ordered
     * @return the ordered files
     */
    public static Order findOrder(String line, ArrayList<File> files){
        String[] lineArray = line.split(SEPARATOR);
        String order = lineArray[0];
        Boolean isReverse = checkReverse(lineArray);
        switch (order){
            case ABS_ORDER:
                return new AbsOrder(files, isReverse);
            case SIZE_ORDER:
                return new SizeOrder(files, isReverse);
            case TYPE_ORDER:
                return new TypeOrder(files, isReverse);
        }
        return null;
    }

    /**
     * checks if REVERSE occurs in the order line
     * @param lineArray - the line of the order
     * @return true if there is REVERSE, false otherwise
     */
    private static Boolean checkReverse(String[] lineArray){
        return lineArray.length > 1 && lineArray[1].equals(REVERSE);
    }
}
