package filesprocessing.filters;

/*this class represents the exception of type 2 in case the filter sub section is missing or incorrect*/
public class FilterException extends Exception {

    private static final long serialVersionUID = 1L;

    /**
     * exception in case the filter sub section is missing or incorrect
     */
    public FilterException () {
        super("ERROR: FILTER sub-section missing");
    }
}
