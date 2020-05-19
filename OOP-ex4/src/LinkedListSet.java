import java.util.LinkedList;

public class LinkedListSet {

    LinkedList<String> linkedList;

    public LinkedListSet() {
        linkedList = new LinkedList<String>();
    }


    /**
     * Appends the specified element to the end of this linked list.
     *
     * @param newValue - the element to be add to the linkedList
     * @return true if the add method of the linked list returned true and false otherwise.
     */
    public boolean add(String newValue) {
        return linkedList.add(newValue);
    }

    /**
     * Returns true if this linked list contains the specified element.
     *
     * @param searchVal - the element whose presence in this list is to be tested
     * @return true if the contains method of the linked list returned true and false otherwise.
     */
    public boolean contains(String searchVal) {
        return linkedList.contains(searchVal);
    }

    /**
     * Removes the first occurrence of the specified element from this linked list, if it is present. If this
     * linked list does not contain the element, it is unchanged.
     *
     * @param toDelete - the element to be removed from this list, if present
     * @return true if the delete method of the linked list returned true and false otherwise.
     */
    public boolean delete(String toDelete) {
        return linkedList.remove(toDelete);
    }

    /**
     * Returns the number of elements in this linked list.
     *
     * @return the number of elements in this linked list
     */
    public int size() {
        return linkedList.size();
    }

    /**
     * Returns an array containing all of the elements in this linked list in proper sequence (from first
     * to last element).
     * @return an array containing all of the elements in this linked list in proper sequence
     */
    public Object[] toArray() {
        return linkedList.toArray();
    }
}

