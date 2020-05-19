package filesprocessing;

import filesprocessing.filters.FilterException;
import filesprocessing.filters.FilterFactory;
import filesprocessing.orders.OrderException;
import filesprocessing.orders.OrderFactory;
import java.io.*;
import java.util.ArrayList;


/**
 * this class managing all the sections
 */
public class DirectoryProcessor {

    /*represent the ORDER sub-section*/
    private final static String ORDER = "ORDER";

    /*represent the FILTER sub-section*/
    private final static String FILTER = "FILTER";

    /*represent the all filter*/
    private final static String ALL_FILTER = "all";

    /*represent the between filter*/
    private final static String BETWEEN_FILTER = "between";

    /*represent the contains filter*/
    private final static String CONTAINS_FILTER = "contains";

    /*represent the executable filter*/
    private final static String EXECUTABLE_FILTER = "executable";

    /*represent the file filter*/
    private final static String FILE_FILTER = "file";

    /*represent the greater_than filter*/
    private final static String GREATER_THAN_FILTER = "greater_than";

    /*represent the hidden filter*/
    private final static String HIDDEN_FILTER = "hidden";

    /*represent the prefix filter*/
    private final static String PREFIX_FILTER = "prefix";

    /*represent the smaller_than filter*/
    private final static String SMALLER_THAN_FILTER = "smaller_than";

    /*represent the suffix filter*/
    private final static String SUFFIX_FILTER = "suffix";

    /*represent the writable filter*/
    private final static String WRITABLE_FILTER = "writable";

    /*represent the abs order*/
    private final static String ABS_ORDER = "abs";

    /*represent the size order*/
    private final static String SIZE_ORDER = "size";

    /*represent the type order*/
    private final static String TYPE_ORDER = "type";

    /*represent the NOT suffix*/
    private final static String NOT = "NOT";

    /*represents the NO value*/
    private final static String NO = "NO";

    /*represents the YES value*/
    private final static String YES = "YES";

    /*a separator between name, value and NOT/REVERSE suffix*/
    private final static String SEPARATOR = "#";

    /*an message for errors of type 1*/
    private final static String WARNING = "Warning in line ";

    /*string for the number of line there is error at*/
    private final static String ERROR_LINE = "ERROR LINE-";

    /*a message for the I/O exception*/
    private final static String IO_ERROR_LINE = "ERROR: errors occurring while accessing the" +
            " Commands File";

    /*an array of all the filters*/
    private static String[] FILTERS = new String[]{ALL_FILTER, BETWEEN_FILTER, CONTAINS_FILTER,
            EXECUTABLE_FILTER, FILE_FILTER, GREATER_THAN_FILTER, HIDDEN_FILTER, PREFIX_FILTER,
            SMALLER_THAN_FILTER, SUFFIX_FILTER, WRITABLE_FILTER};

    /*an array of the orders*/
    private static String[] ORDERS = new String[]{ABS_ORDER, SIZE_ORDER, TYPE_ORDER};


    /**
     * this function reads the command file and enter its lines into an array
     * @param commandFileName - the command file to read
     * @return the array of the lines of the file
     * @throws IOException - in case the'r are I/O Exceptions
     */
    private ArrayList<String> readCommandFile(String commandFileName) throws IOException {
        ArrayList<String> commandFileArray = new ArrayList<>();
        String line;
        BufferedReader buff = new BufferedReader(new FileReader(commandFileName));
        while ((line = buff.readLine()) != null){
            commandFileArray.add(line);
        }
        buff.close();
        return commandFileArray;
    }

    /**
     * this function checks if a value (filter or order) is in an array (filters or orders array)
     * @param valuesArray - the array to check if a value is in
     * @param valueName - the value to check
     * @return true if the value is in the array, false otherwise
     */
    private Boolean checkValue(String[] valuesArray, String valueName){
        for (String filter : valuesArray){
            if (filter.equals(valueName)){
                return true;
            }
        }
        return false;
    }

    /**
     * this function checks if the filter in the filter line is s legal line (including its value and suffix)
     * @param line - the filter line
     * @return true if the filter line is legal, false otherwise
     */
    private Boolean checkFilter(String line){
        String[] lineArray = line.split(SEPARATOR);
        String filterName = lineArray[0];
        if (lineArray.length == 1){
            return filterName.equals(ALL_FILTER);
        }
        String filterValue = lineArray[1];
        if (checkValue(FILTERS, filterName)){
            if (filterName.equals(GREATER_THAN_FILTER) || filterName.equals(SMALLER_THAN_FILTER)){
                if (lineArray.length == 2 && Double.parseDouble(filterValue) >= 0){
                    return true;
                }
                else if (lineArray.length > 2){
                    if (!lineArray[2].equals(NOT)){
                        return false;
                    }
                    return Double.parseDouble(filterValue) >= 0;
                }
            }
            else if (filterName.equals(BETWEEN_FILTER)){
                if (lineArray.length == 3 && Double.parseDouble(filterValue) >= 0 && Double.parseDouble
                        (lineArray[2]) >= 0 && Double.parseDouble(filterValue) <= Double.parseDouble
                        (lineArray[2])){
                    return true;
                }
                else if (lineArray.length > 3){
                    if (!lineArray[3].equals(NOT)){
                        return false;
                    }
                    return Double.parseDouble(filterValue) >= 0 && Double.parseDouble
                            (lineArray[2]) >= 0 && Double.parseDouble(filterValue) <= Double.parseDouble
                            (lineArray[2]);
                }
            }
            else if (filterName.equals(WRITABLE_FILTER) || filterName.equals(EXECUTABLE_FILTER) ||
                    filterName.equals(HIDDEN_FILTER)){
                if (lineArray.length == 2){
                    return filterValue.equals(YES) || filterValue.equals(NO);
                }
                else if (lineArray.length > 2){
                    if (!lineArray[2].equals(NOT)){
                        return false;
                    }
                    else return filterValue.equals(YES) || filterValue.equals(NO);
                }
            }
            else if (filterName.equals(ALL_FILTER)){
                return lineArray.length <= 1 || lineArray[1].equals(NOT);
            }
            else if (filterName.equals(FILE_FILTER) || filterName.equals(PREFIX_FILTER) || filterName
                    .equals(SUFFIX_FILTER) || filterName.equals(CONTAINS_FILTER)){
                return lineArray.length <= 2 || lineArray[2].equals(NOT);
            }
        }
        return false;
    }

    /**
     * this function enter the filters (if there legal) of the given array into a new array
     * @param commandFileArray - the array of all the lines in the command files
     * @return array of filters
     * @throws FilterException - in case the FILTER ub-section is missing
     * @throws IndexOutOfBoundsException - in case we exceed the bounds of the array
     */
    private ArrayList<String> getFilters(ArrayList<String> commandFileArray) throws FilterException,
            IndexOutOfBoundsException{

        ArrayList<String> filtersInFile = new ArrayList<>();
        for (int i = 0 ; i < commandFileArray.size() - 1; ){
            if (!commandFileArray.get(0).equals(FILTER)){
                throw new FilterException();
            }
            if (commandFileArray.get(i).equals(FILTER)){
                if (commandFileArray.size() == i + 1){
                    throw new FilterException();
                }
                if (checkFilter(commandFileArray.get(i + 1))){
                    filtersInFile.add(commandFileArray.get(i + 1));
                }
                else {
                    filtersInFile.add(ERROR_LINE + Integer.toString(i + 2));
                }
                i += 3;
            }
        else if ((i != commandFileArray.size() - 1) && (!commandFileArray.get(i + 1).equals(FILTER))) {
                throw new FilterException();
            }
        else{
                i++;
            }
        }
        return filtersInFile;
    }


    /**
     * this function checks if an order line is a valid order
     * @param line - the line to take the order from
     * @return true if it's a legal order, false otherwise
     */
    private Boolean checkOrder(String line){
        String [] lineArray =  line.split(SEPARATOR);
        String order = lineArray[0];
        return checkValue(ORDERS, order);
    }

    /**
     * this function enter the orders (if there legal) of the given array into a new array
     * @param commandFileArray - the array of all the lines in the command files
     * @return array of orders
     * @throws OrderException - in case the ORDER ub-section is missing
     */
    private ArrayList<String> getOrders(ArrayList<String> commandFileArray) throws OrderException {
        ArrayList<String> ordersInFile = new ArrayList<>();
        for (int i = 0; i < commandFileArray.size(); ){
            if (commandFileArray.get(i).equals(FILTER)){
                if (commandFileArray.size() <= i + 2){
                    throw new OrderException();
                }
                if (!commandFileArray.get(i + 2).equals(ORDER)){
                    throw new OrderException();
                }
                else if (i == commandFileArray.size() - 3 || commandFileArray.get(i + 3).equals(FILTER)){
                    ordersInFile.add(ABS_ORDER);
                }
                else{
                    if (checkOrder(commandFileArray.get(i + 3))){
                        ordersInFile.add(commandFileArray.get(i + 3));
                    }
                    else {
                        ordersInFile.add(ERROR_LINE + Integer.toString(i + 4));
                    }
                }
                i += 3;
            }
            else {
                i++;
            }
        }
        return ordersInFile;
    }

    /**
     * this function combine the filters and order so there will be filter and than order several times
     * @param commandFileName - the name of the command file
     * @return a combined array of filters and orders
     * @throws OrderException - in case the ORDER ub-section is missing
     * @throws FilterException - in case the FILTER ub-section is missing
     */
    private ArrayList<String> combineFiltersOrders(ArrayList<String> commandFileName) throws OrderException,
            FilterException{
        ArrayList<String> combinedArray = new ArrayList<>();
        ArrayList<String> filters = getFilters(commandFileName);
        ArrayList<String> orders = getOrders(commandFileName);
        for (int i = 0 ; i < filters.size(); i++){
            combinedArray.add(filters.get(i));
            combinedArray.add(orders.get(i));
        }
        return combinedArray;
    }

    /**
     * this function finds all the file in the given directory
     * @param sourcedir - the directory to take the files from
     * @return an array of all the files in the directory
     */
    private ArrayList<File> allFilesInDirectory(String sourcedir){
        File directory = new File(sourcedir);
        File [] allFiles = directory.listFiles();
        ArrayList<File> filesInDirectory = new ArrayList<>();
//        assert allFiles != null;
        for (File file: allFiles){
            if (file.isFile()){
                filesInDirectory.add(file);
            }
        }
        return filesInDirectory;
    }

    /**
     * this function checks if the number of arguments is two
     * @param args - the arguments
     * @throws InvalidUsageException - in case the number of arguments isn't right
     */
    private void checkUsage(String[] args) throws InvalidUsageException{
        if (args.length != 2){
            throw new InvalidUsageException();
        }
    }

    /**
     * this function managing the program
     * @param args - the arguments of the program
     */
    public static void main(String[] args){
        DirectoryProcessor processor = new DirectoryProcessor();
        try{
            processor.checkUsage(args);
            ArrayList<String> commandFileArray = processor.readCommandFile(args[1]);
            ArrayList<String> filtersAndOrders = processor.combineFiltersOrders(commandFileArray);
            ArrayList<File> filesInDirectory = processor.allFilesInDirectory(args[0]);
            for (int i = 0 ; i < filtersAndOrders.size() ; ){
                Filter filter;
                Order order;
                if (filtersAndOrders.get(i).contains(ERROR_LINE)){
                    int index = filtersAndOrders.get(i).lastIndexOf("-");
                    String lineNum = filtersAndOrders.get(i).substring(index + 1);
                    System.err.println(WARNING + lineNum);
                    filter = FilterFactory.findFilter(ALL_FILTER, filesInDirectory);
                }
                else {
                    filter = FilterFactory.findFilter(filtersAndOrders.get(i), filesInDirectory);
                }
//                assert filter != null;
                ArrayList<File> filteredFiles = filter.activateFilter();
                if (filtersAndOrders.get(i + 1).contains(ERROR_LINE)){
                    int index = filtersAndOrders.get(i + 1).lastIndexOf("-");
                    String lineNum = filtersAndOrders.get(i + 1).substring(index + 1);
                    System.err.println(WARNING + lineNum);
                    order = OrderFactory.findOrder(ABS_ORDER, filteredFiles);
                }
                else {
                    order = OrderFactory.findOrder(filtersAndOrders.get(i + 1), filteredFiles);
                }
//                assert order != null;
                File[] orderedFiles = order.sort();
                for (File file : orderedFiles){
                    if (file != null){
                        System.out.println(file.getName());
                    }
                    else {
                        System.out.println("1");
                    }
                }

                i += 2;
            }
        }
        catch (IOException ex){
            System.err.println(IO_ERROR_LINE);
        }
        catch (InvalidUsageException | OrderException | FilterException ex){
            System.err.println(ex.getMessage());
        }
    }
}
