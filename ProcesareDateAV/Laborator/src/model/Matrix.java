package model;

public class Matrix {

    private Size size;
    private int[][] representation;

    public Matrix(Size size){
        this.size = size;
        this.representation = new int[size.getRows()][size.getColumns()];
    }

    public Matrix(int rows, int columns){
        this.size = new Size(rows, columns);
        this.representation = new int[rows][columns];
    }

    public Size getSize() { return size; }

    public int[][] getMatrix(){
        return this.representation;
    }

    public void setMatrix(Size size, int[][] representation){
        if (this.size.getRows().equals(size.getRows()) && this.size.getColumns().equals(size.getColumns()))
        {
            this.representation = representation;
        }
    }

    public int[] getSpecifiedRow(int row){
        return this.representation[row];
    }

    public int getElementFromPosition(int row, int column){
        return this.representation[row][column];
    }

    public void addValueOnPosition(int value, int row, int column){
        this.representation[row][column] = value;
    }

    public String toString(){
        String result = "";
        for (int i = 0; i < this.size.getRows(); i++){
            for (int j = 0; j < this.size.getColumns(); j++){
                if (i > 0)
                    result = result + ", " + Integer.toString(this.representation[i][j]);
                else
                    result = result + Integer.toString(this.representation[i][j]);
            }
            result += "\n";
        }
        return result;
    }

}
