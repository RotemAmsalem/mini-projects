package filesprocessing;

/*this class represents the exception of type 2 in case the number of arguments isn't 2*/
class InvalidUsageException extends Exception {

    private static final long serialVersionUID = 1L;

    /**
     * exception in case there aren't two arguments
     */
    InvalidUsageException() {
        super("ERROR: The arguments are invalid");
    }
}
