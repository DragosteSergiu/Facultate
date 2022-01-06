import model.Grammar;

/**
 * Main Class for running the program
 */
public class Main {
    /**
     * Main method for running the program
     * @param args args for determining specific behaviour of the program
     */
    public static void main(String[] args) {
        var grammar = new Grammar();
        System.out.println(grammar);
        System.out.println(grammar.isContextFreeGrammar());
    }
}
