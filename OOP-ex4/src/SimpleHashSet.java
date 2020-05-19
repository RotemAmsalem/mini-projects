public abstract class SimpleHashSet implements SimpleSet {

    /*Describes the higher load factor of a newly created hash set*/
    protected static final float DEFAULT_HIGHER_CAPACITY = 0.75f;

    /*Describes the lower load factor of a newly created hash set*/
    protected static final float DEFAULT_LOWER_CAPACITY = 0.25f;

    /*Describes the capacity of a newly created hash set*/
    protected static final int INITIAL_CAPACITY = 16;

    /*the upper load factor of the hash table*/
    protected float upperLoad;

    /*the lower load factor of the hash table*/
    protected float lowerLoad;


    /**
     * Constructs a new hash set with capacity INITIAL_CAPACITY.
     * @param upperLoadFactor - the upper load factor before rehashing.
     * @param lowerLoadFactor - the lower load factor before rehashing.
     */
    protected SimpleHashSet(float upperLoadFactor, float lowerLoadFactor){
        upperLoad = upperLoadFactor;
        lowerLoad = lowerLoadFactor;
    }

    /**
     * Constructs a new hash set with the default capacities given in DEFAULT_LOWER_CAPACITY and
     * DEFAULT_HIGHER_CAPACITY.
     */
    protected SimpleHashSet(){
        upperLoad = DEFAULT_HIGHER_CAPACITY;
        lowerLoad = DEFAULT_LOWER_CAPACITY;
    }

    /**
     *
     * @return The current capacity (number of cells) of the table.
     */
    public abstract int capacity();


    /**
     * Clamps hashing indices to fit within the current table capacity.
     * @param index - the index before clamping.
     * @return an index properly clamped.
     */
    protected abstract int clamp(int index);


    /**
     *
     * @return The lower load factor of the table.
     */
    protected float getLowerLoadFactor(){
        return lowerLoad;
    }

    /**
     *
     * @return The higher load factor of the table.
     */
    protected float getUpperLoadFactor(){
        return upperLoad;
    }

    /**
     * update the upper load factor of the hash table to be the new upper load factor.
     * @param newUpperLoadFactor - the new upper load factor.
     */
    protected void setUpperLoadFactor(float newUpperLoadFactor){
        upperLoad = newUpperLoadFactor;
    }

    /**
     * update the upper load factor of the hash table to be the new upper load factor.
     * @param newLowerLoadFactor - the new lower load factor.
     */
    protected void setLowerLoadFactor(float newLowerLoadFactor){
        lowerLoad = newLowerLoadFactor;
    }
}
