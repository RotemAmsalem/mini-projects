package filesprocessing;

import java.io.File;
import java.util.ArrayList;
import java.util.Comparator;


/*this class implements an order*/
public abstract class Order implements Comparator<File> {

    /*a boolean flag represents wither REVERSE suffix appears in the order line or not.*/
    private Boolean reverseAppears;

    /*an array of the files to order*/
    private ArrayList<File> filesToOrder;

    /*an array of the sorted files*/
    protected File[] orderedFiles;


    /*an empty string*/
    protected final static String EMPTY_STRING = "";


    /**
     * construct an order
     * @param input - the files to order
     * @param reverseFlag - a boolean value represents whether REVERSE occurs in filter line or not.
     */
    public Order(ArrayList<File> input, Boolean reverseFlag){
        reverseAppears = reverseFlag;
        filesToOrder = input;
    }

    /**
     * an abstract method of comparing between two files
     * @param a - the first file to compare
     * @param b - the second file to compare
     * @return the result of comparing two files (the order with each other)
     */
    public abstract int compare(File a, File b);

    /**
     * if the REVERSE suffix occurs, this function is called and it returns the files in opposite order of
     * the mentioned one.
     * @param orderedFiles - an array list of the files by order
     * @return the same files in opposite order
     */
    private File[] reverseSuffix(File[] orderedFiles){
        File[] oppositeOrderedFiles = new File[orderedFiles.length];
        for (int i = 0; i < orderedFiles.length; i++){
            oppositeOrderedFiles[orderedFiles.length - 1 - i] = orderedFiles[i];
        }
        return oppositeOrderedFiles;
    }

    /**
     * this function merge the sorted array
     * @param lowerIndex - the lower index of the array
     * @param middle - the middle index of the array
     * @param higherIndex - the higher index of the array
     */
    private void merge(int lowerIndex, int middle, int higherIndex){
        for (int i = lowerIndex; i <= higherIndex; i++){
            orderedFiles[i] = filesToOrder.get(i);
        }
        int n = lowerIndex;
        int m = middle + 1;
        int k = lowerIndex;
        while (n <= middle && m <= higherIndex){
            if (compare(orderedFiles[n], orderedFiles[m]) <= 0){
                filesToOrder.set(k, orderedFiles[n]);
                n++;
            }
            else {
                filesToOrder.set(k, orderedFiles[m]);
                m++;
            }
            k++;
        }
        while (n <= middle){
            filesToOrder.set(k, orderedFiles[n]);
            k++;
            n++;
        }
        for (int i = 0; i < filesToOrder.size(); i++){
            orderedFiles[i] = filesToOrder.get(i);
        }
    }

    /**
     * this function sorts the array and than merge it by calling to merge function
     * @param lowerIndex - the lower index of the array
     * @param higherIndex - the higher index of the array
     */
    private void activateMergeSort(int lowerIndex, int higherIndex){
        if (lowerIndex < higherIndex){
            int middle = lowerIndex + (higherIndex - lowerIndex) / 2;
            activateMergeSort(lowerIndex, middle); //sorts the left side of the array
            activateMergeSort(middle + 1, higherIndex); //sorts the right side of the array
            merge(lowerIndex, middle, higherIndex);// merge both sides.
        }
    }

    /**
     * ordering the files
     * @return the files by the mentioned order
     */
    File[] sort(){
        this.orderedFiles = new File[filesToOrder.size()];
        activateMergeSort(0, filesToOrder.size() - 1);
        if (filesToOrder.size() == 1){
            orderedFiles[0] = filesToOrder.get(0);
        }
        if (reverseAppears){
            return reverseSuffix(orderedFiles);
        }
        return orderedFiles;
    }

}

