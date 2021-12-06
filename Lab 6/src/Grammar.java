import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

public class Grammar {

    private List<Rule> rules;
    private Set<String> terminals;
    private Set<String> nonTerminals;
    private String startSymbol;

    private BufferedReader bufferedReader;

    public Grammar(String filepath){
        rules = new ArrayList<>();
        terminals = new HashSet<>();
        nonTerminals = new HashSet<>();
        startSymbol = new String();

        try {
            this.bufferedReader = new BufferedReader(new FileReader(filepath));
            this.readFromFile();
        } catch (FileNotFoundException e) {
            this.bufferedReader = null;
            e.printStackTrace();
        }
    }

    public Set<String> getTerminals(){
        return this.terminals;
    }
    public Set<String> getNonTerminals(){
        return this.nonTerminals;
    }
    public List<Rule> getRules(){
        return this.rules;
    }

    public void readFromFile(){
        this.nonTerminals = this.createListFromFile();
        this.terminals = this.createListFromFile();
        this.startSymbol = this.createStartSymbolFromFile();
        this.rules = this.createRulesFromFile();
    }

    public boolean verifyString(String[] string){
        for(String s : string){
            if (!this.terminals.contains(s) && !this.nonTerminals.contains(s))
                return false;
        }
        return true;
    }

    public Set<String> createListFromFile(){
        try {
            String items = Arrays.stream(this.bufferedReader
                                            .readLine()
                                            .split("="))
                                            .collect(Collectors.toList()).get(1);
            return Arrays.stream(items.substring(2, items.length() - 1)
                                            .strip()
                                            .split(", "))
                                            .collect(Collectors.toSet());

        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    public String createStartSymbolFromFile(){
        try {
            return Arrays.stream(this.bufferedReader
                                    .readLine()
                                    .split("="))
                                    .collect(Collectors.toList()).get(1)
                                    .strip();
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    public List<Rule> createRulesFromFile(){
        try {
            List<Rule> rules = new ArrayList<>();
            String line = this.bufferedReader.readLine();
            while (!line.contains("}")){
                line = this.bufferedReader.readLine();
                if (line.contains("}"))
                    break;
                String leftHandSide = Arrays.stream(line.split("->"))
                                                    .collect(Collectors.toList()).get(0)
                                                    .strip();
                List<String> rightHandSide = Arrays.stream(Arrays.stream(line.split("->"))
                                                    .collect(Collectors.toList()).get(1)
                                                    .strip()
                                                    .split("\\|"))
                                                    .collect(Collectors.toList());
                rightHandSide.forEach(e -> {Rule rule = new Rule(leftHandSide, e.strip().split(""));
                if (this.verifyString(rule.getRightSide()) == true) rules.add(rule);});
            }
            return rules;
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    public HashSet<Rule> getRuledByLeftVariable(String variable) {
        HashSet<Rule> variableRules = new HashSet<>();
        for (Rule rule : this.rules) {
            if (rule.getLeftSide().equals(variable)) {
                variableRules.add(rule);
            }
        }
        return variableRules;
    }

    public int findRuleIndex(Rule rule){
        for(int i = 0 ; i < this.rules.size();i++){
            if(this.rules.get(i).equals(rule)){
                return i;
            }
        }
        return -1;
    }

    public boolean isVariable(String s) {
        return nonTerminals.contains(s);
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        final Grammar other = (Grammar) obj;
        if (!Objects.equals(this.rules, other.rules)) {
            return false;
        }
        if (!Objects.equals(this.terminals, other.terminals)) {
            return false;
        }
        if (!Objects.equals(this.nonTerminals, other.nonTerminals)) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        String str = "Rules: {";
        for(Rule rule: rules){
            str += rule + "\n";
        }
        return str + "}";
    }

}
