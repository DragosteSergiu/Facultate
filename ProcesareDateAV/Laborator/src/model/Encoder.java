package model;
import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner; // Import the Scanner class to read text files


public class Encoder {

    private final Image image;

    public Encoder(Image image){
        this.image = image;
    }

    public Size getImageSize(){
        return this.image.getSize();
    }

    public Integer clamp(int value, int min, int max){
        if (value < min)
            value = min;
        else if (value > max)
            value = max;
        return value;
    }

    public int[] convertToRGB(int Y, int U, int V){
        int[] rgb = new int[3];
        rgb[0] = this.clamp((int)(Y + 1.140 * V), 0, 255);
        rgb[1] = this.clamp((int)(Y - 0.395 * U - 0.581 * V), 0, 255);
        rgb[2] = this.clamp((int)(Y + 2.032 * U), 0, 255);
        return rgb;
    }

    public int[] convertToYUV(int R, int G, int B){
        int[] yuv = new int[3];
        yuv[0] = (int)(0.299*R + 0.587*G + 0.114*B);
        yuv[1] = (int)(0.492 * (B - yuv[0]));
        yuv[2] = (int)(0.877 * (R - yuv[0]));
        return yuv;
    }

    public void readStructure(Structure structure){
        try {
            File file = new File(this.image.getFile());
            Scanner scanner = new Scanner(file);
            String fileType = scanner.nextLine();
            if (fileType.equals("P3")){
                this.image.setType(ImageType.P3);
                scanner.nextLine();
                String[] dimension = scanner.nextLine().split(" ");
                int rows = Integer.parseInt(dimension[1]);
                int columns = Integer.parseInt(dimension[0]);
                this.image.setSize(new Size(rows, columns));
                structure.setSize(this.image.getSize());
                structure.setType(StructureType.RGB);
                String maximumValue = scanner.nextLine();
                for (int currentRows = 0; currentRows < rows; currentRows++){
                    for (int currentColumns = 0; currentColumns < columns; currentColumns ++){
                        String R = scanner.nextLine();
                        structure.addInFirstMatrix(Integer.parseInt(R), currentRows, currentColumns);
                        String G = scanner.nextLine();
                        structure.addInSecondMatrix(Integer.parseInt(G), currentRows, currentColumns);
                        String B = scanner.nextLine();
                        structure.addInThirdMatrix(Integer.parseInt(B), currentRows, currentColumns);
                    }
                }
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    }

    public void createYUV(Structure rgbStructure, Structure yuvStructure){
        yuvStructure.setSize(this.image.getSize());
        yuvStructure.setType(StructureType.YUV);
        for(int i = 0; i < rgbStructure.getSize().getRows(); i++){
            for (int j = 0; j < rgbStructure.getSize().getColumns(); j++){
                int R = rgbStructure.getFirstMatrix().getElementFromPosition(i, j);
                int G = rgbStructure.getSecondMatrix().getElementFromPosition(i, j);
                int B = rgbStructure.getThirdMatrix().getElementFromPosition(i, j);
                int[] yuv = this.convertToYUV(R, G, B);
                yuvStructure.addInFirstMatrix(yuv[0], i, j);
                yuvStructure.addInSecondMatrix(yuv[1], i, j);
                yuvStructure.addInThirdMatrix(yuv[2], i, j);
            }
        }
    }

    public Block createBlock(int row, int column, int difference, Matrix matrix){
        Block block = new Block(new Size(difference, difference), row - difference + 1, column - difference + 1);
        int currentRow = 0;
        for (int i = row - difference + 1; i < row + 1; i++){
            int currentColumn = 0;
            for (int j = column - difference + 1; j < column + 1; j++){
                block.addInBlockAtPosition(matrix.getElementFromPosition(i, j), currentRow, currentColumn);
                currentColumn += 1;
            }
            currentRow += 1;
        }
        return block;
    }

    public List<Block> createAllBlocksOfAType(Matrix matrix, int difference){
        List<Block> blocks = new ArrayList<>();
        for (int i = difference - 1; i < matrix.getSize().getRows(); i += difference ){
            for (int j = difference - 1; j < matrix.getSize().getColumns(); j += difference){
                Block block = this.createBlock(i, j, difference, matrix);
                blocks.add(block);
            }
        }
        return blocks;
    }

    public void recomposeBlocks(DecomposedStructure decomposedStructure){
        decomposedStructure.recomposeBlocks();
    }

    public void subtractValueFromBlocks(DecomposedStructure decomposedStructure, int value){
        decomposedStructure.subtractValueFromBlocks(value);
    }

    public void forwardDCT(DecomposedStructure decomposedStructure){
        decomposedStructure.forwardDCT();
    }

    public void inverseDCT(DecomposedStructure decomposedStructure){
        decomposedStructure.inverseDCT();
    }

    public void quantization(DecomposedStructure decomposedStructure){
        decomposedStructure.quantization();
    }

    public void dequantization(DecomposedStructure decomposedStructure){
        decomposedStructure.dequantization();
    }

    public void encode(Structure structure, DecomposedStructure decomposedStructure){
        decomposedStructure.setSize(this.image.getSize());
        decomposedStructure.setYBlocks(this.createAllBlocksOfAType(structure.getFirstMatrix(), 8));
        decomposedStructure.setUBlocks(this.createAllBlocksOfAType(structure.getSecondMatrix(), 8));
        decomposedStructure.setVBlocks(this.createAllBlocksOfAType(structure.getThirdMatrix(), 8));
        decomposedStructure.modifyBlocks();
    }


    public void computeMatrix(Block yBlock, Block uBlock, Block vBlock, Structure structure){
        for (int rows = 0; rows < yBlock.getSize().getRows(); rows ++){
            for (int column = 0; column < yBlock.getSize().getColumns(); column ++){
                int[] rgb = this.convertToRGB(yBlock.getElementFromPosition(rows, column),
                        uBlock.getElementFromPosition(rows / 2, column / 2),
                        vBlock.getElementFromPosition(rows / 2, column / 2));
                structure.addInFirstMatrix(rgb[0], rows + yBlock.getRow(), column + yBlock.getColumn());
                structure.addInSecondMatrix(rgb[1], rows + yBlock.getRow(), column + yBlock.getColumn());
                structure.addInThirdMatrix(rgb[2], rows+ yBlock.getRow(), column + yBlock.getColumn());
            }
        }
    }

    public void decode(DecomposedStructure decomposedStructure, Structure recomposedStructure){
        recomposedStructure.setSize(this.image.getSize());
        recomposedStructure.setType(StructureType.RGB);
        for (int i = 0; i < decomposedStructure.getUBlocks().size(); i ++){
            this.computeMatrix(decomposedStructure.getYBlocks().get(i),
                    decomposedStructure.getUBlocks().get(i),decomposedStructure.getVBlocks().get(i), recomposedStructure);
        }
    }

    public void recreateImage(Structure structure, String filename){

        FileWriter fileWriter = null;
        try {
            fileWriter = new FileWriter(filename);
        } catch (IOException e) {
            e.printStackTrace();
        }
        PrintWriter printWriter = new PrintWriter(fileWriter);
        printWriter.println(this.image.getType().toString());
        printWriter.println("# CREATOR: GIMP PNM Filter Version 1.1");
        printWriter.println(this.getImageSize().getColumns().toString() + " " + this.getImageSize().getRows().toString());
        printWriter.println("255");
        for(int i = 0; i < this.getImageSize().getRows(); i++){
            for(int j = 0; j < this.getImageSize().getColumns(); j++){
                printWriter.println(structure.getFirstMatrix().getElementFromPosition(i, j));
                printWriter.println(structure.getSecondMatrix().getElementFromPosition(i, j));
                printWriter.println(structure.getThirdMatrix().getElementFromPosition(i, j));
            }
        }
        printWriter.close();
    }

    public void writeDecodedImageInFile(DecomposedStructure decomposedStructure, String filename){
        FileWriter fileWriter = null;
        try {
            fileWriter = new FileWriter(filename);
        } catch (IOException e) {
            e.printStackTrace();
        }
        PrintWriter printWriter = new PrintWriter(fileWriter);
        printWriter.println(decomposedStructure.toString());
        printWriter.close();
    }

    public static void main(String[] args) {
        Image image = new Image("C:\\Faculta\\Anu'3\\ProcesareDateAV\\Laborator\\src\\nt-P3.ppm");
        Encoder encoder = new Encoder(image);
        Structure structureRGB = new Structure();
        Structure structureYUV = new Structure();
        DecomposedStructure decomposedStructure = new DecomposedStructure();
        Structure recomposedStructure = new Structure();
        encoder.readStructure(structureRGB);
        encoder.createYUV(structureRGB, structureYUV);
        encoder.encode(structureYUV, decomposedStructure);
        encoder.recomposeBlocks(decomposedStructure);
        encoder.subtractValueFromBlocks(decomposedStructure, 128);
        encoder.forwardDCT(decomposedStructure);
        encoder.quantization(decomposedStructure);
        System.out.println(decomposedStructure.getYBlocks().get(0).toString("Y", 0));
        encoder.dequantization(decomposedStructure);
        encoder.inverseDCT(decomposedStructure);
        encoder.subtractValueFromBlocks(decomposedStructure, -128);
        System.out.println(decomposedStructure.getYBlocks().get(0).toString("Y", 0));
        encoder.decode(decomposedStructure, recomposedStructure);
        //encoder.writeDecodedImageInFile(decomposedStructure, "decomposed-image.txt");
        encoder.recreateImage(recomposedStructure, "newfile.ppm");
    }

}
