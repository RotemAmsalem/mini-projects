import java.util.Collection;

public class CollectionFacadeSet implements SimpleSet {

    protected java.util.Collection<java.lang.String> collection;


    /**
     * Creates a new facade wrapping the specified collection.
     * @param collection - The Collection to wrap.
     */
    public CollectionFacadeSet(java.util.Collection<java.lang.String> collection){
        this.collection = collection;
    }

    @Override
    public boolean add(String newValue) {
        if (!collection.contains(newValue)){
            collection.add(newValue);
            return true;
        }
        return false;
    }

    @Override
    public boolean contains(String searchVal) {
        return collection.contains(searchVal);
    }

    @Override
    public boolean delete(String toDelete) {
        if (!collection.contains(toDelete)){
            return false;
        }
        collection.remove(toDelete);
        return true;
    }

    @Override
    public int size() {
        return collection.size();
    }


}
