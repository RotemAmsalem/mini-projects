package filesprocessing.filters;

import filesprocessing.Filter;
import java.io.File;
import java.util.ArrayList;


/*this class builds a filter*/
public class FilterFactory {

    /*the separator of the filter line (between name and value and NOT)*/
    private final static String SEPARATOR = "#";

    /*the all filter*/
    private final static String ALL_FILTER = "all";

    /*the between filter*/
    private final static String BETWEEN_FILTER = "between";

    /*the contains filter*/
    private final static String CONTAINS_FILTER = "contains";

    /*the executable filter*/
    private final static String EXECUTABLE_FILTER = "executable";

    /*the file filter*/
    private final static String FILE_FILTER = "file";

    /*the greater_than filter*/
    private final static String GREATER_THAN_FILTER = "greater_than";

    /*the hidden filter*/
    private final static String HIDDEN_FILTER = "hidden";

    /*the prefix filter*/
    private final static String PREFIX_FILTER = "prefix";

    /*the smaller_than filter*/
    private final static String SMALLER_THAN_FILTER = "smaller_than";

    /*the suffix filter*/
    private final static String SUFFIX_FILTER = "suffix";

    /*the writable filter*/
    private final static String WRITABLE_FILTER = "writable";

    /*the NOT suffix*/
    private final static String NOT = "NOT";


    /**
     * finds the filter according to the filter line
     * @param line - the filter line
     * @param files - the files to be filtered
     * @return the relevant filter
     */
    public static Filter findFilter(String line, ArrayList<File> files){
        String[] lineArray = line.split(SEPARATOR);
        String filter = lineArray[0];
        Boolean isNot = checkNot(lineArray);
        switch (filter){
            case ALL_FILTER:
                return new AllFilter(files, isNot);
            case BETWEEN_FILTER:
                return new BetweenFilter(files, isNot, Double.parseDouble(lineArray[1]), Double.parseDouble
                        (lineArray[2]));
            case CONTAINS_FILTER:
                return new ContainsFilter(files, isNot, lineArray[1]);
            case EXECUTABLE_FILTER:
                return new ExecutableFilter(files, isNot, lineArray[1]);
            case FILE_FILTER:
                return new FileFilter(files, isNot, lineArray[1]);
            case GREATER_THAN_FILTER:
                return new GreaterThanFilter(files, isNot, Double.parseDouble(lineArray[1]));
            case HIDDEN_FILTER:
                return new HiddenFilter(files, isNot, lineArray[1]);
            case PREFIX_FILTER:
                return new PrefixFilter(files, isNot, lineArray[1]);
            case SMALLER_THAN_FILTER:
                return new SmallerThanFilter(files, isNot, Double.parseDouble(lineArray[1]));
            case SUFFIX_FILTER:
                return new SuffixFilter(files, isNot, lineArray[1]);
            case WRITABLE_FILTER:
                return new WritableFilter(files, isNot, lineArray[1]);
        }
        return null;
    }

    /**
     * checks if NOT occurs in the filter line
     * @param lineArray - the line of the filter
     * @return true if there is NOT, false otherwise
     */
    private static Boolean checkNot(String[] lineArray){
        if (lineArray.length > 1 && lineArray[0].equals(ALL_FILTER) && lineArray[1].equals(NOT)){
            return true;
        }
        if (lineArray.length > 2 && !lineArray[0].equals(ALL_FILTER) && !lineArray[0].equals
                (BETWEEN_FILTER) && lineArray[2].equals(NOT)){
            return true;
        }
        if (lineArray.length > 3 && lineArray[0].equals(BETWEEN_FILTER) && lineArray[3].equals(NOT)) {
            return true;
        }
        return false;
    }
}
