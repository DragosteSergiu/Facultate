package model;

public class Image {

    private final String file;
    private ImageType imageType;
    private Size size;

    public Image(String file){
        this.file = file;
    }

    public String getFile(){
        return this.file;
    }

    public ImageType getType(){
        return this.imageType;
    }
    public void setType(ImageType imageType){
        this.imageType = imageType;
    }

    public Size getSize(){
        return this.size;
    }
    public void setSize(Size size){
        this.size = size;
    }

}
