import java.util.HashSet;
import java.util.LinkedList;
import java.util.TreeSet;

public class SimpleSetPerformanceAnalyzer {

    private final static int NUM_OF_DATA_STRUCTURES = 5;

    private SimpleSet[] dataStructureArray;

    private final static int WARM_UP = 70000;

    private final static int LINKED_LIST_WARM_UP = 7000;

    private final static int NANO_TO_MILLI = 1000000;

    private String[] types;

    private final static String OPEN_HASH_SET_NAME = "OpenHashSet";

    private final static String CLOSED_HASH_SET_NAME = "ClosedHashSet";

    private final static String TREE_SET_NAME = "TreeSet";

    private final static String LINKED_LIST_NAME = "LinkedList";

    private final static String HASH_SET_NAME = "HashSet";


    public SimpleSetPerformanceAnalyzer() {
        dataStructureArray = new SimpleSet[NUM_OF_DATA_STRUCTURES];
        types = new String[NUM_OF_DATA_STRUCTURES];
        setDataStructureArray(dataStructureArray);
        setTypes(types);
    }

    private void setDataStructureArray(SimpleSet[] dataStructureArray){
        dataStructureArray[0] = new OpenHashSet();
        dataStructureArray[1] = new ClosedHashSet();
        TreeSet treeSet = new TreeSet();
        dataStructureArray[2] = new CollectionFacadeSet(treeSet);
        LinkedList linkedList = new LinkedList();
        dataStructureArray[3] = new CollectionFacadeSet(linkedList);
        HashSet hashSet = new HashSet();
        dataStructureArray[4] = new CollectionFacadeSet(hashSet);
    }
    private void setTypes(String[] types){
        types[0] = OPEN_HASH_SET_NAME;
        types[1] = CLOSED_HASH_SET_NAME;
        types[2] = TREE_SET_NAME;
        types[3] = LINKED_LIST_NAME;
        types[4] = HASH_SET_NAME;
    }




    private void addData(String[] stringsArray, int dataNum) {
        System.out.println("These values correspond to the time it takes (in ms) to insert data" + dataNum
                + " to all data structures");
//        System.out.println("The following represents the time it took for each one of the data structures " +
//                "to add all the words in data" + dataNum + ":\n");
        long difference;
        for (int j = 0; j < dataStructureArray.length; j++) {
            long timeBefore = System.nanoTime();
            for (String word : stringsArray) {
                dataStructureArray[j].add(word);
            }
            difference = (System.nanoTime() - timeBefore) / NANO_TO_MILLI;
            System.out.println(types[j] + "_AddData" + dataNum + " = " + difference);
//            System.out.println("The " + types[j] + " data structures added the words in data"
//                    + dataNum + " in " + difference + " milliseconds.\n");
        }
    }

    private void warmUpContainsData(String word, SimpleSet dataStruct, int warmUp) {
        for (int i = 0; i < warmUp; i++) {
            dataStruct.contains(word);
        }
    }


    private void containsData(String word, int dataNum) {
        System.out.println("These values correspond to the time it takes (in ns) to check if " + word +
                " is contained in the data structures initialized with data" + dataNum);
//        System.out.println("The following represents the time it took for each one of the data structures " +
//                "to check whiter the word " + word + " is in data" + dataNum + " or not:\n");
        long difference;
        long timeBefore;
        for (int j = 0; j < dataStructureArray.length; j++) {
            if (!types[j].equals(LINKED_LIST_NAME)) {
                warmUpContainsData(word, dataStructureArray[j], WARM_UP);
                timeBefore = System.nanoTime();
                warmUpContainsData(word, dataStructureArray[j], WARM_UP);
                difference = (System.nanoTime() - timeBefore) / WARM_UP;
            } else {
                timeBefore = System.nanoTime();
                warmUpContainsData(word, dataStructureArray[j], LINKED_LIST_WARM_UP);
                difference = (System.nanoTime() - timeBefore) / LINKED_LIST_WARM_UP;
            }
            System.out.println(types[j] + "_Contains_" + word + " = " + difference);
//            System.out.println("The " + types[j] + " data structures looked for the word " +
//                    word + " in data" + dataNum + " in " + difference + " nanoseconds.\n");
        }

    }

    public static void main(String[] args) {
        SimpleSetPerformanceAnalyzer data1Results = new SimpleSetPerformanceAnalyzer();
        SimpleSetPerformanceAnalyzer data2Results = new SimpleSetPerformanceAnalyzer();

        String[] data1 = Ex4Utils.file2array(args[0]);
        String[] data2 = Ex4Utils.file2array(args[1]);

        data1Results.addData(data1, 1); //magicNum??
        data2Results.addData(data2, 2);

        data1Results.containsData("hi", 1);
        data1Results.containsData("-13170890158", 1);
        data2Results.containsData("23", 2);
        data2Results.containsData("hi", 2);
    }
}