import java.util.*;

public class LR0Parser {

    protected HashMap<String, Integer>[] goToTable;
    protected HashMap<String, Action>[] actionTable;
    protected Grammar grammar;
    private ArrayList<LR0State> canonicalCollection;

    public LR0Parser(Grammar grammar) {
        this.grammar = grammar;
        this.createStates();
        this.createGoToTable();
        this.createActionTableForLR0();
    }

    public void createStates() {
        this.canonicalCollection = new ArrayList<>();
        HashSet<LR0Item> start = new HashSet<>();
        start.add(new LR0Item(this.grammar.getRules().get(0)));

        LR0State startState = new LR0State(this.grammar, start);
        this.canonicalCollection.add(startState);

        for (int i = 0; i < this.canonicalCollection.size(); i++) {
            HashSet<String> stringWithDot = new HashSet<>();
            for (LR0Item item : this.canonicalCollection.get(i).getItems()) {
                if (item.getCurrentTerminal() != null) {
                    stringWithDot.add(item.getCurrentTerminal());
                }
            }
            for (String str : stringWithDot) {
                HashSet<LR0Item> nextStateItems = new HashSet<>();
                for (LR0Item item : this.canonicalCollection.get(i).getItems()) {

                    if (item.getCurrentTerminal() != null && item.getCurrentTerminal().equals(str)) {
                        LR0Item temp = new LR0Item(item);
                        temp.goTo();
                        nextStateItems.add(temp);
                    }
                }
                LR0State nextState = new LR0State(this.grammar, nextStateItems);
                boolean isExist = false;
                for (int j = 0; j < this.canonicalCollection.size(); j++) {
                    if (this.canonicalCollection.get(j).getItems().containsAll(nextState.getItems())
                            && nextState.getItems().containsAll(this.canonicalCollection.get(j).getItems())) {
                        isExist = true;
                        this.canonicalCollection.get(i).addTransition(str, canonicalCollection.get(j));
                    }
                }
                if (!isExist) {
                    this.canonicalCollection.add(nextState);
                    this.canonicalCollection.get(i).addTransition(str, nextState);
                }
            }
        }

    }

    public void createGoToTable(){
        this.goToTable = new HashMap[this.canonicalCollection.size()];
        for (int i = 0; i < this.goToTable.length; i++) {
            this.goToTable[i] = new HashMap<>();
        }
        for (int i = 0; i < this.canonicalCollection.size(); i++) {
            for (String s : this.canonicalCollection.get(i).getTransition().keySet()) {
                if (this.grammar.getNonTerminals().contains(s)) {
                    this.goToTable[i].put(s, findStateIndex(this.canonicalCollection.get(i).getTransition().get(s)));
                }
            }
        }
    };

    private boolean createActionTableForLR0() {
        this.actionTable = new HashMap[this.canonicalCollection.size()];
        for (int i = 0; i < this.goToTable.length; i++) {
            this.actionTable[i] = new HashMap<>();
        }
        for (int i = 0; i < this.canonicalCollection.size(); i++) {
            for (String s : this.canonicalCollection.get(i).getTransition().keySet()) {
                if (this.grammar.getTerminals().contains(s)) {
                    this.actionTable[i].put(s, new Action(ActionType.SHIFT, findStateIndex(this.canonicalCollection.get(i).getTransition().get(s))));
                }
            }
        }
        for (int i = 0; i < this.canonicalCollection.size(); i++) {
            for (LR0Item item : this.canonicalCollection.get(i).getItems()) {
                if (item.getDotPointer() == item.getRightSide().length) {
                    if (item.getLeftSide().equals("S'")) {
                        this.actionTable[i].put("$", new Action(ActionType.ACCEPT, 0));
                    } else {
                        Set<String> terminals = grammar.getTerminals();
                        terminals.add("$");
                        Rule rule = new Rule(item.getLeftSide(), item.getRightSide().clone());
                        int index = this.grammar.findRuleIndex(rule);
                        Action action = new Action(ActionType.REDUCE, index);
                        for (String str : terminals) {
                            if (this.actionTable[i].get(str) != null) {
                                System.out.println("it has a REDUCE-" + this.actionTable[i].get(str).getType() + " confilct in state " + i);
                                return false;
                            } else {
                                this.actionTable[i].put(str, action);
                            }
                        }
                    }
                }
            }
        }
        return true;
    }

    public boolean accept(ArrayList<String> inputs) {

        inputs.add("$");
        int index = 0;
        Stack<String> stack = new Stack<>();
        stack.add("0");
        while(index < inputs.size()){
            int state = Integer.valueOf(stack.peek());
            String nextInput = inputs.get(index);
            Action action = this.actionTable[state].get(nextInput);
            if(action == null){
                return false;
            }else if(action.getType() == ActionType.SHIFT){
                stack.push(nextInput);
                stack.push(action.getOperand()+"");
                index++;
            }else if(action.getType() == ActionType.REDUCE){
                int ruleIndex = action.getOperand();
                Rule rule = this.grammar.getRules().get(ruleIndex);
                String leftSide = rule.getLeftSide();
                int rightSideLength = rule.getRightSide().length;
                for(int i=0; i <2*rightSideLength ; i++){
                    stack.pop();
                }
                int nextState = Integer.valueOf(stack.peek());
                stack.push(leftSide);
                int variableState = this.goToTable[nextState].get(leftSide);
                stack.push(variableState+"");
            }else if(action.getType() == ActionType.ACCEPT){
                return true;
            }
        }
        return false;
    }

    public String goToTableStr() {
        String str = "Go TO Table : \n";
        str += "          ";
        for (String variable : this.grammar.getNonTerminals()) {
            str += String.format("%-6s",variable);
        }
        str += "\n";

        for (int i = 0; i < this.goToTable.length; i++) {
            for (int j = 0; j < (this.grammar.getNonTerminals().size()+1)*6+2; j++) {
                str += "-";
            }
            str += "\n";
            str += String.format("|%-6s|",i);
            for (String variable : this.grammar.getNonTerminals()) {
                str += String.format("%6s",(this.goToTable[i].get(variable) == null ? "|" : this.goToTable[i].get(variable)+"|"));
            }
            str += "\n";
        }
        for (int j = 0; j < (this.grammar.getNonTerminals().size()+1)*6+2; j++) {
            str += "-";
        }
        return str;
    }

    public String actionTableStr() {
        String str = "Action Table : \n";
        Set<String> terminals = new HashSet<>(this.grammar.getTerminals());
        terminals.add("$");
        str += "                ";
        for (String terminal : terminals) {
            str += String.format("%-10s" , terminal);
        }
        str += "\n";

        for (int i = 0; i < this.actionTable.length; i++) {
            for (int j = 0; j < (terminals.size()+1)*10+2; j++) {
                str += "-";
            }
            str += "\n";
            str += String.format("|%-10s|",i);
            for (String terminal : terminals) {
                str += String.format("%10s",(this.actionTable[i].get(terminal) == null ? "|" : this.actionTable[i].get(terminal) + "|"));
            }
            str += "\n";
        }
        for (int j = 0; j < (terminals.size()+1)*10+2; j++) {
            str += "-";
        }
        return str;
    }

    private int findStateIndex(LR0State state) {
        for (int i = 0; i < this.canonicalCollection.size(); i++) {
            if (this.canonicalCollection.get(i).equals(state)) {
                return i;
            }
        }
        return -1;
    }

    public Grammar getGrammar() {
        return this.grammar;
    }

    public String canonicalCollectionStr() {
        String str = "Canonical Collection : \n";
        for (int i = 0; i < canonicalCollection.size(); i++) {
            str += "State " + i + " : \n";
            str += canonicalCollection.get(i)+"\n";
        }
        return str;
    }

    public static void main(String[] args) {
        Grammar grammar = new Grammar("C:\\Faculta\\Anu'3\\FLCD\\Lab 6\\src\\g1.txt");
        LR0Parser parser = new LR0Parser(grammar);
        System.out.println(parser.goToTableStr());
    }
}
