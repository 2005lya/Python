#!/usr/bin/env python
# coding: utf-8

# In[1]:



from matplotlib import pyplot
from matplotlib.patches import Rectangle
import imageIO.png


# In[2]:


def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array


# In[3]:


def readRGBImageToSeparatePixelArrays(input_filename):

    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)


# In[4]:


def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    
    greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    
    for y in range(image_height):
        for x in range(image_width):
            greyscale_pixel_array[y][x]=round(0.299*pixel_array_r[y][x]+0.587*pixel_array_g[y][x]+0.114*pixel_array_b[y][x])
            
    
    return greyscale_pixel_array


# In[5]:


def scaleTo0And255AndQuantize(pixel_array, image_width, image_height):
    newpixel = createInitializedGreyscalePixelArray(image_width, image_height)
    flow=pixel_array[0][0]
    fhigh=pixel_array[0][0]
    for y in range(image_height):
        for x in range(image_width):
            if flow>pixel_array[y][x]:
               flow=pixel_array[y][x]
            if fhigh<pixel_array[y][x]:
               fhigh=pixel_array[y][x]
    for y in range(image_height):
        for x in range(image_width):
            if flow!=fhigh:
             newpixel[y][x]=round((pixel_array[y][x]-flow)*(255/(fhigh-flow)));
            else:
             newpixel[y][x]=0
    return newpixel


# In[ ]:





# In[6]:


def computeHorizontalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    horizontal_edges=createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(image_height):
        for j in range(image_width):
            if(i==0 or j==0 or i==image_height-1 or j==image_width-1 ):
                horizontal_edges[i][j]=0.000
            else:
                horizontal_edges[i][j]=(1.0/8)*(pixel_array[i-1][j-1]-pixel_array[i+1][j-1]+2*(pixel_array[i-1][j]-pixel_array[i+1][j])+(pixel_array[i-1][j+1]-pixel_array[i+1][j+1]))
                
    return horizontal_edges      


# In[7]:


def computeVerticalEdgesSobelAbsolute(pixel_array, image_width, image_height):
    vertical_edges=createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(image_height):
        for j in range(image_width):
            if(i==0 or j==0 or i==image_height-1 or j==image_width-1 ):
                vertical_edges[i][j]=0.000
            else:
                vertical_edges[i][j]=(1.0/8)*(pixel_array[i-1][j+1]-pixel_array[i-1][j-1]+2*(pixel_array[i][j+1]-pixel_array[i][j-1])+(pixel_array[i+1][j+1]-pixel_array[i+1][j-1]))
                
    return vertical_edges     


# In[8]:


def edge(horizontal_array,vertical_array,image_width, image_height):
    edges=createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(image_height):
        for j in range(image_width):
            edges[i][j]=pow((horizontal_array[i][j]**2+vertical_array[i][j]**2),0.5)
    return edges
    


# In[9]:


def computeGaussianAveraging3x3RepeatBorder(pixel_array, image_width, image_height):
    result=createInitializedGreyscalePixelArray(image_width, image_height)
    bigger=createInitializedGreyscalePixelArray(image_width+2, image_height+2)
    
    for i in range(image_height+2):
        for j in range(image_width+2):
            bigger[i][j]=0
    for i in range (1, image_height+1):
        for j in range(1, image_width+1):
            bigger[i][j]=pixel_array[i-1][j-1]
    for i in range(1,image_width+1):
        bigger[0][i]=pixel_array[0][i-1]
        bigger[image_height+1][i]=pixel_array[image_height-1][i-1]
    for i in range(1,image_height+1):
        bigger[i][0]=pixel_array[i-1][0]
        bigger[i][image_width+1]=pixel_array[i-1][image_width-1]
    bigger[0][0]=bigger[1][1]
    bigger[image_height+1][0]=bigger[image_height+1][1]
    bigger[0][image_width+1]=bigger[0][image_width]
    bigger[image_height+1][image_width+1]=bigger[image_height][image_width]
    for i in range(1,image_height+1):
        for j in range(1,image_width+1):
            result[i-1][j-1]=(1.0/16)*(bigger[i-1][j-1]+bigger[i-1][j+1]+bigger[i+1][j-1]+bigger[i+1][j+1]+2*(bigger[i-1][j]+bigger[i][j-1]+bigger[i][j+1]+bigger[i+1][j])+4*bigger[i][j])
    return result


# In[10]:


def stretchcontrast(pixel_array, image_width, image_height):
    result=createInitializedGreyscalePixelArray(image_width, image_height)
    flow=pixel_array[0][0]
    fhigh=pixel_array[0][0]
    for i in range(image_height):
        for j in range(image_width):
            if flow>pixel_array[i][j]:
                flow=pixel_array[i][j]
    for i in range(image_height):
        for j in range(image_width):
            if fhigh<pixel_array[i][j]:
                fhigh=pixel_array[i][j]
    for i in range(image_height):
        for j in range(image_width):
            result[i][j]=round((pixel_array[i][j]-flow)*(255.0/(fhigh-flow)))
    return result


# In[11]:


def computeThresholdGE(pixel_array, image_width, image_height):
    result=createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(image_height):
        for j in range(image_width):
            if(pixel_array[i][j]>=70):
              result[i][j]=255
            else:
              result[i][j]=0
    return result


# In[12]:


def computeDilation8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    result=createInitializedGreyscalePixelArray(image_width, image_height)
    padding=createInitializedGreyscalePixelArray(image_width+2, image_height+2)
    for i in range(image_height):
        for j in range(image_width):
            padding[i+1][j+1]=pixel_array[i][j]
    for i in range(1,image_height+1):
        for j in range(1,image_width+1):
            if(padding[i][j]>0):
                result[i-1][j-1]=1
            else:
                if(padding[i-1][j-1]>0 or padding[i-1][j]>0 or padding[i-1][j+1]>0 or padding[i][j-1]>0 or padding[i][j+1]>0 or padding[i+1][j-1]>0 or padding[i+1][j]>0 or padding[i+1][j+1]>0):
                    result[i-1][j-1]=1
                else:
                    result[i-1][j-1]=0
    return result


# In[13]:


def computeErosion8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    result=createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(1,image_height-1):
        for j in range(1,image_width-1):
            if(pixel_array[i][j]==0):
                result[i][j]=0
            else:
                if(pixel_array[i-1][j-1]==0 or pixel_array[i-1][j]==0 or pixel_array[i-1][j+1]==0 or pixel_array[i][j-1]==0 or pixel_array[i][j+1]==0 or pixel_array[i+1][j-1]==0 or pixel_array[i+1][j]==0 or pixel_array[i+1][j+1]==0):
                    result[i][j]=0
                else:
                    result[i][j]=1
    return result
                  


# In[14]:


class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


# In[15]:


def computeConnectedComponentLabeling(pixel_array, image_width, image_height):
    result=createInitializedGreyscalePixelArray(image_width, image_height)
    label=1
    visited = set()
    ccsizes={}
    count=0
    for i in range(image_height):
        for j in range(image_width):
            if(pixel_array[i][j]>0 and (i,j) not in visited):
                q=Queue()
                q.enqueue((i,j))
                visited.add((i,j))
                while(q.isEmpty()==False):
                    a,b=q.dequeue()
                    count += 1
                    result[a][b]=label
                    if(a>=1):
                        if(pixel_array[a-1][b]>0 and (a-1,b) not in visited):
                            q.enqueue((a-1,b))
                        visited.add((a-1,b))
                    if(a<image_height-1):
                        if(pixel_array[a+1][b]>0 and (a+1,b) not in visited):
                            q.enqueue((a+1,b))
                        visited.add((a+1,b))
                    if(b>=1):
                        if(pixel_array[a][b-1]>0 and (a,b-1) not in visited):
                             q.enqueue((a,b-1))
                        visited.add((a,b-1))
                    if(b<image_width-1):
                        if(pixel_array[a][b+1]>0 and (a,b+1) not in visited):
                            q.enqueue((a,b+1))
                        visited.add((a,b+1))
                ccsizes[str(label)] = count
                label=label+1
                count=0
    return result,ccsizes       
                            
                    


# In[21]:


def boundingbox(pixel_array, image_width, image_height):
    listone=[]
    for i in range(image_height):
        for j in range(image_width):
            if pixel_array[i][j]>0:
                listone.append(i)
                listone.append(j)
    return listone[0],listone[1],listone[-2],listone[-1]


# In[33]:


def prepareRGBImageForImshowFromIndividualArrays(r,g,b,w,h):
    rgbImage = []
    for y in range(h):
        row = []
        for x in range(w):
            triple = []
            triple.append(r[y][x])
            triple.append(g[y][x])
            triple.append(b[y][x])
            row.append(triple)
        rgbImage.append(row)
    return rgbImage


# In[36]:


def main():
    filename = "./images/covid19QRCode/poster1small.png"

    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(filename)
    greyscale_pixel_array=computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)
    newpixel=scaleTo0And255AndQuantize(greyscale_pixel_array, image_width, image_height)
    horizontal_edges=computeHorizontalEdgesSobelAbsolute(newpixel,image_width, image_height)
    vertical_edges=computeVerticalEdgesSobelAbsolute(newpixel,image_width, image_height)
    edgeImage=edge(horizontal_edges,vertical_edges,image_width, image_height)
    edgemagnitude1=computeGaussianAveraging3x3RepeatBorder(edgeImage, image_width, image_height)
    edgemagnitude2=computeGaussianAveraging3x3RepeatBorder(edgemagnitude1, image_width, image_height)
    edgemagnitude3=computeGaussianAveraging3x3RepeatBorder(edgemagnitude2, image_width, image_height)
    edgemagnitude4=computeGaussianAveraging3x3RepeatBorder(edgemagnitude3, image_width, image_height)
    edgemagnitude5=computeGaussianAveraging3x3RepeatBorder(edgemagnitude4, image_width, image_height)
    edgemagnitude6=computeGaussianAveraging3x3RepeatBorder(edgemagnitude5, image_width, image_height)
    edgemagnitude7=computeGaussianAveraging3x3RepeatBorder(edgemagnitude6, image_width, image_height)
    edgemagnitude8=computeGaussianAveraging3x3RepeatBorder(edgemagnitude7, image_width, image_height)
    edgemagnitude9=computeGaussianAveraging3x3RepeatBorder(edgemagnitude8, image_width, image_height)
    edgemagnitude10=computeGaussianAveraging3x3RepeatBorder(edgemagnitude9, image_width, image_height)
    edgemagnitude11=computeGaussianAveraging3x3RepeatBorder(edgemagnitude10, image_width, image_height)
    stretch=stretchcontrast(edgemagnitude11, image_width, image_height)
    Threshold=computeThresholdGE(stretch, image_width, image_height)
    Dilation=computeDilation8Nbh3x3FlatSE(Threshold, image_width, image_height)
    Erosion=computeErosion8Nbh3x3FlatSE(Dilation, image_width, image_height)
    (ima,size)=computeConnectedComponentLabeling(Erosion, image_width, image_height)
    label=str(1)
    for i in size.keys():
        if size[label]<size[i]:
            label=i
    num=int(label)
    
    new=createInitializedGreyscalePixelArray(image_width, image_height)
    for i in range(image_height):
        for j in range(image_width):
            if ima[i][j]==num:
                new[i][j]=ima[i][j]
                
    (minx,miny,maxx,maxy)=boundingbox(new, image_width, image_height)
    pyplot.imshow(prepareRGBImageForImshowFromIndividualArrays(px_array_r, px_array_g, px_array_b, image_width, image_height))
    #pyplot.imshow(new,cmap='gray')

    # get access to the current pyplot figure
    axes = pyplot.gca()
    # create a 70x50 rectangle that starts at location 10,30, with a line width of 3
    rect = Rectangle( (minx-38, miny+32), maxx-minx+6, maxy-miny+6, linewidth=3, edgecolor='g', facecolor='none' )
    # paint the rectangle over the current plot
    axes.add_patch(rect)

    # plot the current figure
    pyplot.show()



if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:





# In[ ]:




