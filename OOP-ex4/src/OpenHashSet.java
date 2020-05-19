public class OpenHashSet extends SimpleHashSet {

    /*a set that contains object of the wrapper-class LinkedListSet*/
    private LinkedListSet[] linkedListHashSet =  new LinkedListSet[INITIAL_CAPACITY];

    /*the size of the set*/
    private int setSize = 0;
    /**
     * Constructs a new, empty table with the specified load factors, and the default initial capacity (16).
     * @param upperLoadFactor - The upper load factor of the hash table.
     * @param lowerLoadFactor - The lower load factor of the hash table.
     */
    public OpenHashSet(float upperLoadFactor, float lowerLoadFactor){
        super(upperLoadFactor, lowerLoadFactor);
        buildOpenHashSet(linkedListHashSet);
    }

    /**
     * A default constructor. Constructs a new, empty table with default initial capacity (16), upper load
     * factor (0.75) and lower load factor (0.25).
     */
    public OpenHashSet(){
        super();
        buildOpenHashSet(linkedListHashSet);
    }


    /**
     * Data constructor - builds the hash set by adding the elements one by one. Duplicate values should be
     * ignored. The new table has the default values of initial capacity (16), upper load factor (0.75),
     * and lower load factor (0.25).
     * @param data - Values to add to the set.
     */
    public OpenHashSet(java.lang.String[] data){
        setUpperLoadFactor(DEFAULT_HIGHER_CAPACITY);
        setLowerLoadFactor(DEFAULT_LOWER_CAPACITY);
        buildOpenHashSet(linkedListHashSet);
        for (String str: data){
            add(str);
        }
    }

    @Override
    public int capacity() {
        return linkedListHashSet.length;
    }



    @Override
    protected int clamp(int index) {
        return (index & (capacity() - 1));
    }



    @Override
    public boolean contains(String searchVal) {
        int index = clamp(searchVal.hashCode());
        return linkedListHashSet[index].contains(searchVal);
    }


    @Override
    public boolean add(String newValue) {
        int index = clamp(newValue.hashCode());
        if (!contains(newValue)){
            setSize++;
            if (getLoadFactor() > getUpperLoadFactor()){
                LinkedListSet[] newLinkedListHashSet = new LinkedListSet[capacity() * 2];
                reHashing(newLinkedListHashSet);
                linkedListHashSet = newLinkedListHashSet;
            }
        }
        return linkedListHashSet[index].add(newValue);
    }


    @Override
    public boolean delete(String toDelete) {
        int index = clamp(toDelete.hashCode());
        if (contains(toDelete)){
            setSize--;
            if (getLoadFactor() < getLowerLoadFactor() && capacity() > 1){
                LinkedListSet[] newLinkedListHashSet = new LinkedListSet[capacity() / 2];
                buildOpenHashSet(newLinkedListHashSet);
                reHashing(newLinkedListHashSet);
                linkedListHashSet = newLinkedListHashSet;
            }
        }
        return linkedListHashSet[index].delete(toDelete);
    }


    @Override
    public int size() {
        return setSize;
    }

    private void buildOpenHashSet(LinkedListSet[] linkedListArr){
        for (int i = 0; i < linkedListArr.length; i++){
            linkedListArr[i] = new LinkedListSet();
        }
    }

    private double getLoadFactor(){
        return(double) size() / capacity();
    }

    private void reHashing(LinkedListSet[] linkedListArr){
        buildOpenHashSet(linkedListArr);
        for (LinkedListSet someLinkedList : linkedListHashSet) {
            for (Object obj : someLinkedList.toArray()) {
                int index = obj.hashCode() & (linkedListArr.length - 1); // -1??
                linkedListArr[index].add((String) obj);
            }
        }
    }
}
