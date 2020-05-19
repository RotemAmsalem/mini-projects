public class ClosedHashSetCell {

    /*a string the class holds*/
    private String str;

    /*a flag represent whether the string has been deleted or not*/
    private boolean isDeleteFlag;

    /**
     * A default constructor. Constructs a new, empty string with default initial flag (false).
     */
    ClosedHashSetCell(){
        str = null;
        isDeleteFlag = false;
    }

    /**
     * sets the str the new value
     * @param newVal - the new value to assign.
     */
    public void setStr(String newVal) {
        str = newVal;
    }

    /**
     * sets the isDelete flag the new value
     * @param newVal - the new value to assign.
     */
    public void setFlag(boolean newVal) {
        isDeleteFlag = newVal;
    }

    /**
     * gets the value of the str
     * @return - the str
     */
    public String getStr() {
        return str;
    }

    /**
     * gets the value of the flag
     * @return - the isDelete flag
     */
    public Boolean getFlag() {
        return isDeleteFlag;
    }

    /**
     * this function assign the newValue to the string str and update its flag to be false
     * @param newValue - the value to assign
     */
    public void add(String newValue){
        setStr(newValue);
        setFlag(false);
    }

    /**
     * this function checks if the string str is null, if so than the paramter does not equals to str and
     * it returns false, otherwise it returns true if the value of the searchVal is equal to the value of
     * the str.
     * @param searchVal - the val to search for
     * @return true if str and searchVal contains the same value, false otherwise.
     */
    public boolean contains(String searchVal) {
        if (getStr() == null){
            return false;
        }
        return str.equals(searchVal);
    }

    /**
     * this function delete the string and update the flag to be true.
     */
    public void delete() {
        setStr(null);
        setFlag(true);
    }

}
