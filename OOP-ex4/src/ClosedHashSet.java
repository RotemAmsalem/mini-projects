public class ClosedHashSet extends SimpleHashSet {

    /*a set that contains object of the wrapper-class LinkedListSet*/
    private ClosedHashSetCell[] closedHashCell = new ClosedHashSetCell[INITIAL_CAPACITY];

    /*the size of the set*/
    private int setSize = 0;

    /*an int represents the i’th attempt to find an empty cell for element*/
    private int i;

    /**
     * Constructs a new, empty table with the specified load factors, and the default initial capacity (16).
     * @param upperLoadFactor - The upper load factor of the hash table.
     * @param lowerLoadFactor - The lower load factor of the hash table.
     */
    public ClosedHashSet(float upperLoadFactor, float lowerLoadFactor){
        super(upperLoadFactor, lowerLoadFactor);
        buildClosedHashSet(closedHashCell);
    }

    /**
     * A default constructor. Constructs a new, empty table with default initial capacity (16), upper load
     * factor (0.75) and lower load factor (0.25).
     */
    public ClosedHashSet(){
        super();
        buildClosedHashSet(closedHashCell);
    }

    /**
     * Data constructor - builds the hash set by adding the elements one by one. Duplicate values should be
     * ignored. The new table has the default values of initial capacity (16), upper load factor (0.75),
     * and lower load factor (0.25).
     * @param data - Values to add to the set.
     */
    public ClosedHashSet(java.lang.String[] data){
        setUpperLoadFactor(DEFAULT_HIGHER_CAPACITY);
        setLowerLoadFactor(DEFAULT_LOWER_CAPACITY);
        buildClosedHashSet(closedHashCell);
        for (String str: data){
            add(str);
        }
    }

    @Override
    public int capacity() {
        return closedHashCell.length;
    }

    @Override
    protected int clamp(int index) {
        return ((index +(i+i*i)/2) & (capacity() - 1));
    }

    @Override
    public boolean contains(String searchVal) {
        i = 0;
        while (i < capacity()){
            int index = clamp(searchVal.hashCode());
            if (!closedHashCell[index].getFlag()){
                if (closedHashCell[index].getStr() == null){
                    return false;
                }
                if (closedHashCell[index].getStr().equals(searchVal)){
                    return true;
                }
            }
            i++;
        }
        return false;
    }

    @Override
    public boolean add(String newValue) {
        int index = clamp(newValue.hashCode());
        if (!contains(newValue)){
            setSize++;
            if (getLoadFactor() > getUpperLoadFactor()){
                ClosedHashSetCell[] newClosedHashCell = new ClosedHashSetCell[capacity() * 2];
                reHashing(newClosedHashCell);
                closedHashCell = newClosedHashCell;
            }
            i = 0;
            while (closedHashCell[index].getStr() != null){
                i ++;
                index = clamp(newValue.hashCode());
            }
            closedHashCell[index].add(newValue);
            return true;
        }
        return false;
    }

    @Override
    public boolean delete(String toDelete) {
        int index = clamp(toDelete.hashCode());
        if (contains(toDelete)){
            setSize--;
            if (getLoadFactor() < getLowerLoadFactor() && capacity() > 1){
                ClosedHashSetCell[] newClosedHashCell = new ClosedHashSetCell[capacity() / 2];
                reHashing(newClosedHashCell);
                closedHashCell = newClosedHashCell;
            }
            i = 0;
            while (!closedHashCell[index].contains(toDelete)){
                i ++;
                index = clamp(toDelete.hashCode());
            }
            closedHashCell[index].delete();
            return true;
        }
        return false;
    }

    @Override
    public int size() {
        return setSize;
    }

    private double getLoadFactor(){
        return(double) size() / capacity();
    }

    private void buildClosedHashSet(ClosedHashSetCell[] closedHashArr){
        for (int j = 0; j < closedHashArr.length; j++){
            closedHashArr[j] = new ClosedHashSetCell();
        }
    }

    private void reHashing(ClosedHashSetCell[] closedHashArr){ //change!!!
        buildClosedHashSet(closedHashArr);
        for (int j = 0; j < capacity(); j++){
            String str = closedHashArr[j].getStr();
            if (str != null){
                i = 0;
                int index = (str.hashCode() +(i+i*i)/2) & (closedHashArr.length - 1);
                while (closedHashArr[index].getStr() != null){
                    i ++;
                    index = (str.hashCode() +(i+i*i)/2) & (closedHashArr.length - 1);
                }
                closedHashArr[index].setStr(str);
            }
        }
    }
}
