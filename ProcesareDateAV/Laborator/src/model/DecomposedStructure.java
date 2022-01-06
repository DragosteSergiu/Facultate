package model;

import java.util.ArrayList;
import java.util.List;


public class DecomposedStructure {

    static double[][] q = {{6, 4, 4, 6, 10, 16, 20, 24},
                        {5, 5, 6, 8, 10, 23, 24, 22},
                        {6, 5, 6, 10, 16, 23, 28, 22},
                        {6, 7, 9, 12, 20, 35, 32, 25},
                        {7, 9, 15, 22, 27, 44, 41, 31},
                        {10, 14, 22, 26, 32, 42, 45, 37},
                        {20, 26, 31, 35, 41, 48, 48, 40},
                        {29, 37, 38, 39, 45, 40, 41, 40}};

    private Size size;
    private List<Block> yBlocks;
    private List<Block> uBlocks;
    private List<Block> vBlocks;

    public DecomposedStructure(){ }

    public DecomposedStructure(Size size){
        this.size = size;
        this.initializeBlocks();
    }

    public void initializeBlocks(){
        this.yBlocks = new ArrayList<>();
        this.uBlocks = new ArrayList<>();
        this.vBlocks = new ArrayList<>();
    }

    public Size getSize(){ return this.size ;}
    public void setSize(Size size) { this.size = size; this.initializeBlocks(); }

    public List<Block> getYBlocks(){ return this.yBlocks; }
    public List<Block> getUBlocks(){ return this.uBlocks; }
    public List<Block> getVBlocks(){ return this.vBlocks; }
    public void setYBlocks(List<Block> yBlocks) { this.yBlocks = yBlocks; }
    public void setUBlocks(List<Block> uBlocks) { this.uBlocks = uBlocks; }
    public void setVBlocks(List<Block> vBlocks) { this.vBlocks = vBlocks; }

    public void addYBlock(Block block){
        this.yBlocks.add(block);
    }
    public void addUBlock(Block block){
        this.uBlocks.add(block);
    }
    public void addVBlock(Block block){
        this.vBlocks.add(block);
    }

    public Block modifyOneBlock(Block block){
        Block newBlock = new Block(new Size(block.getSize().getRows() / 2, block.getSize().getColumns() / 2), block.getRow(), block.getColumn());
        for (int i = 1; i < block.getSize().getRows(); i += 2){
            for (int j = 1; j < block.getSize().getColumns(); j += 2){
                int average = (int)((block.getElementFromPosition(i - 1, j - 1) + block.getElementFromPosition(i - 1, j)
                        + block.getElementFromPosition(i, j - 1) + block.getElementFromPosition(i, j)) / 4);
                newBlock.addInBlockAtPosition(average, i / 2, j / 2);
            }
        }
        return newBlock;
    }
    public void modifyBlocks(){
        List<Block> newUBlocks = new ArrayList<>();
        for (Block block : this.uBlocks){
            newUBlocks.add(this.modifyOneBlock(block));
        }
        this.uBlocks = newUBlocks;

        List<Block> newVBlock = new ArrayList<>();
        for (Block block: this.vBlocks){
            newVBlock.add(this.modifyOneBlock(block));
        }

        this.vBlocks = newVBlock;
    }

    public Block recomposeOneBlock(Block block){
        Block newBlock = new Block(new Size(8, 8), block.getRow() * 2, block.getColumn() * 2);
        for (int i = 0; i< 8; i++){
            for (int j = 0; j < 8; j++){
                newBlock.addInBlockAtPosition(block.getElementFromPosition(i/2, j/2), i, j);
            }
        }
        return newBlock;
    }

    public void recomposeBlocks(){
        List<Block> uBlocks = new ArrayList<>();
        for (Block block : this.uBlocks){
            uBlocks.add(this.recomposeOneBlock(block));
        }
        this.uBlocks = uBlocks;

        List<Block> vBlock = new ArrayList<>();
        for (Block block: this.vBlocks){
            vBlock.add(this.recomposeOneBlock(block));
        }
        this.vBlocks = vBlock;
    }

    public void subtractValueInOneBlock(Block block, int value){
        for (int i = 0; i < block.getSize().getRows(); i++){
            for (int j = 0; j < block.getSize().getColumns(); j++){
                block.setElementAtPosition(block.getElementFromPosition(i, j) - value, i, j);
            }
        }
    }

    public void subtractValueFromBlocks(int value){
        List<Block> yBlocks = this.getYBlocks();
        for(Block yBlock : yBlocks){
            this.subtractValueInOneBlock(yBlock, value);
        }

        List<Block> uBlocks = this.getUBlocks();
        for(Block uBlock : uBlocks){
            this.subtractValueInOneBlock(uBlock, value);
        }

        List<Block> vBlocks = this.getVBlocks();
        for(Block vBlock : vBlocks){
            this.subtractValueInOneBlock(vBlock, value);
        }
    }


    private double fOuterSum(int[][] representation, int u, int v) {
        double sum = 0.0;
        for (int x = 0; x < 8; x++)
            sum += fInnerSum(representation, u, v, x);
        return sum;
    }

    private double fInnerSum(int[][] representation, int u, int v, int x) {
        double sum = 0.0;
        for (int y = 0; y < 8; y++)
            sum += fProduct(representation[x][y], x, y, u, v);
        return sum;
    }

    private double fProduct(int value, int x, int y, int u, int v) {
        double cosU = Math.cos(
                ((2 * x + 1) * u * Math.PI) / 16
        );

        double cosV = Math.cos(
                ((2 * y + 1) * v * Math.PI) / 16
        );

        return value * cosU * cosV;
    }

    private double iOuterSum(int[][] representation, int x, int y) {
        double sum = 0.0;
        for (int u = 0; u < 8; u++)
            sum += iInnerSum(representation, x, y, u);
        return sum;
    }

    private double iInnerSum(int[][] representation, int x, int y, int u) {
        double sum = 0.0;
        for (int v = 0; v < 8; v++)
            sum += iProduct(representation[u][v], x, y, u, v);
        return sum;
    }

    private double iProduct(double value, int x, int y, int u, int v) {
        double cosU = Math.cos(
                ((2 * x + 1) * u * Math.PI) / 16
        );

        double cosV = Math.cos(
                ((2 * y + 1) * v * Math.PI) / 16
        );

        return alpha(u) * alpha(v) * value * cosU * cosV;
    }

    private double alpha(int value) {
        return value > 0 ? 1 : (1 / Math.sqrt(2.0));
    }

    public int[][] fDCT(int[][] representation){
        int[][] G = new int[8][8];
        double constant = (double) 1 / 4;

        for (int u = 0; u < 8; u++)
            for (int v = 0; v < 8; v++)
            {
                G[u][v] = (int) (constant * alpha(u) * alpha(v) * fOuterSum(representation, u, v));
            }

        return G;
    }

    private int[][] iDCT(int[][] representation) {
        int[][] f = new int[8][8];
        double constant = (double) 1 / 4;

        for (int x = 0; x < 8; x++)
            for (int y = 0; y < 8; y++)
            {
                f[x][y] = (int) (constant * iOuterSum(representation, x, y));
            }

        return f;
    }

    public void forwardDCT(){
        for (Block block : this.yBlocks){
            block.setRepresentation(this.fDCT(block.getRepresentation()));
        }

        for (Block block : this.uBlocks){
            block.setRepresentation(this.fDCT(block.getRepresentation()));
        }

        for (Block block: this.vBlocks){
            block.setRepresentation(this.fDCT(block.getRepresentation()));
        }

    }

    public void inverseDCT(){
        for (Block block : this.yBlocks){
            block.setRepresentation(this.iDCT(block.getRepresentation()));
        }

        for (Block block : this.uBlocks){
            block.setRepresentation(this.iDCT(block.getRepresentation()));
        }

        for (Block block: this.vBlocks){
            block.setRepresentation(this.iDCT(block.getRepresentation()));
        }
    }

    public int[][] divideMatrices(int[][] a){
        int[][] result = new int[8][8];
        double aux;
        for(int i = 0; i < 8; i++){
            for(int j = 0; j < 8; j++){
                aux = a[i][j] / q[i][j];
                if (aux < 0)
                    result[i][j] = (int) Math.ceil(aux);
                else
                    result[i][j] = (int) Math.floor(aux);
            }
        }
        return result;
    }

    public int[][] multiplyMatrices(int[][] a){
        int[][] result = new int[8][8];
        for(int i = 0; i < 8; i++){
            for(int j = 0; j < 8; j++){
                result[i][j] = (int)(a[i][j] * q[i][j]);
            }
        }
        return result;
    }

    public void quantization(){
        for(Block block : this.yBlocks){
            block.setRepresentation(this.divideMatrices(block.getRepresentation()));
        }

        for(Block block : this.uBlocks){
            block.setRepresentation(this.divideMatrices(block.getRepresentation()));
        }

        for(Block block : this.vBlocks){
            block.setRepresentation(this.divideMatrices(block.getRepresentation()));
        }
    }

    public void dequantization() {
        for(Block block : this.yBlocks){
            block.setRepresentation(this.multiplyMatrices(block.getRepresentation()));
        }

        for(Block block : this.uBlocks){
            block.setRepresentation(this.multiplyMatrices(block.getRepresentation()));
        }

        for(Block block : this.vBlocks){
            block.setRepresentation(this.multiplyMatrices(block.getRepresentation()));
        }
    }

    public String toString(){
        String result = "";
        for (int i = 0; i < this.yBlocks.size(); i++){
            result = result + this.getYBlocks().get(i).toString("Y", i);
            result = result + "\n";
            result = result + this.getUBlocks().get(i).toString("Y", i);
            result = result + "\n";
            result = result + this.getVBlocks().get(i).toString("Y", i);
            result = result + "\n";
        }
        return result;
    }
}
