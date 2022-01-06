package model;

public class Size{

    private Integer rows;
    private Integer columns;

    public Size(Integer rows, Integer columns){
        this.rows = rows;
        this.columns = columns;
    }

    public Integer getRows(){
        return this.rows;
    }
    public void setRows(Integer rows){
        this.rows = rows;
    }

    public Integer getColumns(){
        return this.columns;
    }
    public void setColumns(Integer columns){
        this.columns = columns;
    }
}
