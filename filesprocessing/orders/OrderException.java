package filesprocessing.orders;

/*this class represents the exception of type 2 in case the order sub section is missing or incorrect*/
public class OrderException extends Exception {

    private static final long serialVersionUID = 1L;

    /**
     * exception in case the order sub section is missing or incorrect
     */
    public OrderException () {
        super("ERROR: ORDER sub-section missing");
    }
}
