package model;

public class Block {

    private Size size;
    private int row;
    private int column;
    private int[][] representation;

    public Block(Size size, int row, int column){
        this.size = size;
        this.row = row;
        this.column = column;
        this.representation = new int[size.getRows()][size.getColumns()];
    }

    public int getRow() {
        return this.row;
    }

    public int getColumn() {
        return this.column;
    }

    public Size getSize(){
        return this.size;
    }

    public int[][] getRepresentation() { return this.representation; }

    public void setRepresentation(int[][] representation) { this.representation = representation; }

    public void addInBlockAtPosition(int value, int row, int column){
        this.representation[row][column] = value;
    }
    public int getElementFromPosition(int row, int column){
        return this.representation[row][column];
    }
    public void setElementAtPosition(int value, int row, int column) { this.representation[row][column] = value; }

    public String toString(String type, int number)
    {
        String result = "Block type: " + type + ", number: " + Integer.toString(number) + "\n";
        for(int i = 0; i < this.size.getRows(); i++){
            for(int j = 0; j < this.size.getColumns(); j++){
                if (j > 0){
                    result = result + ", " + Integer.toString(this.getElementFromPosition(i, j));
                }
                else
                {
                    result = result + Integer.toString(this.getElementFromPosition(i, j));
                }
            }
            result += "\n";
        }
        return result;
    }
}
