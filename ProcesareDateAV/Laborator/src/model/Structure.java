package model;

import java.util.ArrayList;
import java.util.List;

public class Structure {

    private Size size;
    private StructureType type;
    private Matrix firstMatrix;
    private Matrix secondMatrix;
    private Matrix thirdMatrix;

    public Structure(){

    }

    public Structure(Size size, StructureType type){
        this.size = size;
        this.type = type;
        this.initializeMatrices(size);
    }

    public void initializeMatrices(Size dimension){
        this.firstMatrix = new Matrix(dimension);
        this.secondMatrix = new Matrix(dimension);
        this.thirdMatrix = new Matrix(dimension);
    }
    public Size getSize(){ return this.size; }

    public void setSize(Size size){ this.size = size ; this.initializeMatrices(size);}

    public StructureType getType() { return type; }

    public void setType(StructureType type) { this.type = type; }

    public Matrix getFirstMatrix(){
        return this.firstMatrix;
    }

    public Matrix getSecondMatrix(){
        return this.secondMatrix;
    }

    public Matrix getThirdMatrix(){
        return this.thirdMatrix;
    }

    public void addInFirstMatrix(int value, int row, int column){
        this.firstMatrix.addValueOnPosition(value, row, column);
    }

    public void addInSecondMatrix(int value, int row, int column){
        this.secondMatrix.addValueOnPosition(value, row, column);
    }

    public void addInThirdMatrix(int value, int row, int column){
        this.thirdMatrix.addValueOnPosition(value, row, column);
    }

    public String toString(){
        String result = "First Matrix\n" + this.firstMatrix.toString();
        result = result + "Second Matrix\n" + this.secondMatrix.toString();
        result = result + "Third Matrix\n" + this.thirdMatrix.toString();
        return result;
    }
}
