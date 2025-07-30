# Library Description

The core of this Python library is the C++ one. It consists of `.cpp` and `.h` files. It is built using the `premake` build system. It is recommended to use the `make_win.bat` script, which provides an example of the build process.

To facilitate usage, a Python wrapper is implemented, enabling the creation and use of the `ImageTopoDec` library.

# Connecting the Python Library

Compatible systems required for library integration:

- **Operating Systems:** Windows 10, Linux (compatible with `manylinux_2_28`), macOS (ARM architecture).
- **Python:** Version 3.13 x86_64.
- **C++ Support:** Required on Windows only ([link](https://aka.ms/vs/16/release/vc_redist.x86.exe) for installing the redistributable package).
- **Package Manager:** `pip`.

The library is installed using `pip`:

For Linux:

```bash
python3 -m pip install ImageTopoDec
```

For Windows:

```bash
py -m pip install ImageTopoDec
```

For macOS, it is recommended to use a virtual environment:

```bash
python3 -m venv .venv
source ./.venv/bin/activate
pip install ImageTopoDec
```

**Example Usage**

```python
import ImageTopoDec as bc
import ImageTopoDec.barcode as bcc
import cv2
import matplotlib.pyplot as plt

# Load image
img = cv2.imread('/Users/sam/Edu/bar/12/1.png', cv2.IMREAD_GRAYSCALE)
plt.imshow(img, cmap='gray')
```

![](https://github.com/Noremos/Barcode/blob/main/PrjBarlib/modules/python/Figure1.png?raw=true)

Figure 1. Source image

```python
# Create barcode and visualize the largest component
cont = bc.barstruct()
cont.proctype = bc.ProcType.f255t0
barc =  bcc.create_barcode(img, cont)

cmp = barc.get_largest_component()
img = bcc.combine_components_into_matrix(cmp, img.shape, img.dtype)

plt.imshow(img, cmap='gray')

cmp = barc.get_largest_component()
img = bcc.combine_components_into_matrix(cmp, img.shape, img.dtype)
plt.imshow(img, cmap='gray')
```
![](https://github.com/Noremos/Barcode/blob/main/PrjBarlib/modules/python/Figure2.png?raw=true)

Figure 2. Visualization of the largest component


```python
binmap = barc.segmentation(False)

plt.imshow(binmap, cmap='gray')
```

![](https://github.com/Noremos/Barcode/blob/main/PrjBarlib/modules/python/Figure3.png?raw=true)

Figure 3. Segmentation by each component (parameter set to False in the segmentation method) with overlap.

```python
binmap = barc.segmentation(True)
plt.imshow(binmap, cmap='gray')
```

![](https://github.com/Noremos/Barcode/blob/main/PrjBarlib/modules/python/Figure4.png?raw=true)

Figure 4. Binary segmentation (parameter set to True in the segmentation method).

```python
filterd = barc.filter(100)
plt.imshow(filterd, cmap='gray')
```

![](https://github.com/Noremos/Barcode/blob/main/PrjBarlib/modules/python/Figure5.png?raw=true)

Figure 5. Reconstructed image without components whose length is less than 100.

```python
import ImageTopoDec.barplot as bcp
bcp.plot_barcode_lines(barc, 'test', True, False)
```

![](https://github.com/Noremos/Barcode/blob/main/PrjBarlib/modules/python/Figure6.png?raw=true)

Figure 6. Barcode visualization: an image named 'test' will be created, which will be visualized (parameter True) and not saved to disk (parameter False).



# Python Library

The Python library is a wrapper for the C++ library. All classes listed in Table 1 are translated to Python with the same method and field names. If a method returns a vector or array, the Python wrapper returns a `set`.

The library also includes its own functions and a class, as shown in Tables 4 and 5.

To use the library, import it:

```python
import ImageTopoDec as bcc
```

Barcodes are created using the `create_barcode` method:

```python
barc = bcc.create_barcode(img, cont)
```

## Table 1. Python Library Custom Functions

| **Function Interface**                         | **Description**                                             |
|------------------------------------------------|-------------------------------------------------------------|
| `create_barcode(img, struct: barstruct) -> Barcode` | Creates a barcode object from an image `img` with options `struct`. |
| `append_line_to_matrix(barline: Barline, matrix: np.array)` | Appends a matrix from the `barline` component to the output matrix `matrix`. |
| `combine_components_into_matrix(barlines: list[Barline] \| Barline, shape: tuple, type = np.uint8)` | Creates a matrix from components or a single component.     |

## Table 2. Python Library Custom Classes

| **Class Name** | **Method/Field**                      | **Description**                                         |
|-----------------|---------------------------------------|---------------------------------------------------------|
| `Barcode`       | `__init__(self, img: np.ndarray, build_options: barstruct)` | Constructor that builds and stores metadata.           |
|                 | `item`                                | Field storing the original barcode wrapped in `Baritem`. |
|                 | `get_largest_component()`             | Returns the largest component (by matrix size).        |
|                 | `get_first_component()`               | Returns the first component in the barcode.            |
|                 | `restore()`                           | Constructs an image from the barcode.                  |

---

**Visualization Module**

The library includes a `barplot` module for visualizing barcodes using Matplotlib. To use it:

```python
import ImageTopoDec.barplot as bcp
```

The module provides one function:

```python
plot_barcode_lines(lines: set[bc.Barline] | bc.Baritem | bc.Barline, name, show=False, save=False)
```

This function can display or save the plot.

---


# C++ Library Interface

The library uses the `bc` namespace, where all classes are defined. These classes can be categorized into interface classes (used by the user) and internal classes. Tables 3-5 provide descriptions of the interface classes and enumerations.

## Table 3. C++ Library Interface Description

| **Class**       | **Description**                                                                                                                |
|------------------|-------------------------------------------------------------------------------------------------------------------------------|
| `BarcodeCreator` | Constructs barcodes. Can act as a factory or directly invoked using a static method to create a barcode.                      |
| `DatagridProvider` | Wrapper interface for transferring images for barcode creation.                                                             |
| `BarImg`         | Example implementation of `DatagridProvider`, storing data in an internal array.                                              |
| `BarNdarray`     | Wrapper class for `DatagridProvider`, allowing processing of NumPy arrays (data is taken by reference).                        |
| `barstruct`      | Structure for setting barcode creation configurations.                                                                        |
| `BarConstructor` | Stores configuration settings. Used to create multiple barcodes from a single image.                                          |
| `bc::Baritem`    | Stores the barcode and its metadata after creation.                                                                           |
| `bc::Barcontainer` | Stores a collection of barcodes created from a single image using multiple configurations.                                  |
| `barline`        | Structure storing information about a barcode component (line).                                                               |
| `Barscalar`      | Class for storing the value (usually brightness) of a barcode.                                                                |
| `BarRect`        | Class for storing the coordinates of a rectangular area.                                                                      |
| `barvalue`       | Class storing the value and position of a matrix element.                                                                     |
| `point`          | Structure storing the X and Y positions.                                                                                      |

## Table 4. Enumerations

| **Enumeration**   | **Enumeration Element**    | **Value**                                                                 |
|--------------------|----------------------------|---------------------------------------------------------------------------|
| **CompireFunction**| CommonToLen               | Option for comparison by length.                                         |
|                    | CommonToSum               | Option for comparison of barcodes by the sum of lengths.                 |
| **ComponentType**  | Component                 | Barcode construction type - components.                                  |
|                    | Hole                      | Barcode construction type - holes.                                       |
| **ProcType**       | f0t255                    | Pixel traversal strategy – from minimum brightness to maximum. Suitable for detecting light objects. |
|                    | f255t0                    | Pixel traversal strategy – from maximum brightness to minimum. Suitable for detecting dark objects.  |
|                    | Radius                    | Pixel traversal strategy in pairs ordered by increasing brightness difference in these pairs. |
| **ColorType**      | gray                      | Convert (if necessary) the input image to grayscale.                     |
|                    | native                    | Process the input image as is.                                           |
|                    | rgb                       | Convert (if necessary) the input image to RGB.                           |
| **ReturnType**     | barcode2d                 | Returns lines constructed based on component lifetimes.                  |
|                    | barcode3d                 | Returns lines constructed based on component lifetimes and adds an array for each component. |
| **AttachMode**     | firstEatSecond            | The parent component is the one that appeared earlier during attachment. |
|                    | secondEatFirst            | The parent component is the one that appeared later during attachment.   |
|                    | createNew                 | A new "proxy" component is created during attachment, becoming the parent. |
|                    | dontTouch                 | Do not attach components.                                                |
|                    | morePointsEatLow          | The parent component is the one that consumed more pixels during attachment. |
| **BarType**        | BYTE8_1                   | The scalar stores the value as 1 byte (for grayscale).                   |
|                    | BYTE8_3                   | The scalar stores the value as 3 bytes (for RGB).                        |
|                    | BYTE8_4                   | The scalar stores the value as 4 bytes (for RGBA).                       |
|                    | FLOAT32_1                 | The scalar stores the value as 4 bytes (for floating-point numbers).     |
|                    | INT32_1                   | The scalar stores the value as 4 bytes (for integers).                   |

---

### Table 5. Description of Class Elements from Table 4

| **Class**            | **Method/Field Interface**                                                                                                                                                                      | **Description**                                                                                             |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| **BarcodeCreator**    | `bc::Barcontainer* createBarcode(const bc::DatagridProvider* img, const BarConstructor& structure);`                                                                                         | Creates multiple barcodes from a single image `img` using the settings array in `structure`.               |
|                       | `bc::Baritem* createBarcode(const bc::DatagridProvider* img, const barstruct& structure);`                                                                                                   | Creates a single barcode from an image `img` using an instance of `structure` settings.                    |
|                       | `static std::unique_ptr<bc::Baritem> create(const bc::DatagridProvider& img, const barstruct& structure = {});`                                                                               | Static method for creating a single barcode from an image `img` using an instance of `structure` settings. |
| **DatagridProvider**  | `virtual int wid() const = 0;`                                                                                                                                                                | Returns the width of the image.                                                                            |
|                       | `virtual int hei() const = 0;`                                                                                                                                                                | Returns the height of the image.                                                                           |
|                       | `virtual int channels() const = 0;`                                                                                                                                                           | Returns the number of channels in a pixel.                                                                 |
|                       | `virtual void maxAndMin(Barscalar& min, Barscalar& max) const = 0;`                                                                                                                           | Finds the extremes of brightness.                                                                          |
|                       | `virtual size_t typeSize() const = 0;`                                                                                                                                                        | Returns the size of one pixel in bytes.                                                                    |
|                       | `virtual Barscalar get(int x, int y) const = 0;`                                                                                                                                              | Returns the pixel at the specified coordinates.                                                            |
| **barstruct**         | `float maxLen = 999999;`                                                                                                                                                                      | The maximum allowable lifetime of a component during construction.                                         |
|                       | `float maxRadius = 999999;`                                                                                                                                                                   | The maximum allowable brightness difference for a pixel to join a component.                               |
|                       | `float minAttachRadius = 0;`                                                                                                                                                                 | The minimum allowable brightness difference for components to merge.                                       |
|                       | `ReturnType returnType = ReturnType::barcode2d;`                                                                                                                                              | The type of construction.                                                                                  |
|                       | `bool createGraph = false;`                                                                                                                                                                  | Whether to create a tree-like graph of relationships.                                                      |
|                       | `bool createBinaryMasks = false;`                                                                                                                                                            | Whether to create matrices during construction.                                                            |
|                       | `bool killOnMaxLen = false;`                                                                                                                                                                 | Whether a component should disappear upon reaching the maximum allowable size.                             |
| **BarConstructor**    | `void addStructure(ProcType pt, ColorType colT, ComponentType comT);`                                                                                                                         | Adds a structure for barcode construction.                                                                 |
| **Baritem** | Barscalar<br>Sum() const | Returns the sum of all line lengths. |
|| void relength() | Normalizes the appearance time of all components relative to the first one. |
|| Barscalar maxLen() const; | Returns the longest line in the barcode. |
|| Baritem* clone() | Returns a full copy of the current item. |
|| BarType getType() | Returns the data type used for storing barcode values. |
|| std::array&lt;int, 256&gt; getBettyNumbers() const; | Calculates the Betti numbers from the barcode. |
|| void removeByThreshold(Barscalar const porog); | Removes all lines shorter than the specified threshold. |
|| void preprocessBarcode(Barscalar const& porog, bool normalize); | Combines `removeByThreshold` and `relength` methods. |
|| float compareFull(const Barbase* bc, bc::CompareStrategy strat) const; | Compares barcode lines linearly. |
|| float compareBestRes(Baritem const* bc, bc::CompareStrategy strat) const; | Compares barcode lines, finding the best match for each line. |
|| float compareOccurrence(Baritem const* bc, bc::CompareStrategy strat) const; | Finds the best barcode occurrence and returns the percentage of matches. |
|| void normalize(); | Normalizes the barcode based on its start time. |
|| template&lt;class TSTR, typename TO_STR&gt;<br>void getJsonObject(TSTR &out, bool exportGraph = false,<br>bool export3dbar = false,<br>bool expotrBinaryMask = false) const | Saves the barcode as a JSON object. |
|| template&lt;class TSTR, typename TO_STR&gt;<br>void getJsonLinesArray(TSTR &out, bool exportGraph = false,<br>bool export3dbar = false,<br>bool expotrBinaryMask = false) const | Saves the barcode as a JSON array. |
|| bc::BarRoot* getRootNode() | Returns the root element in the graph. |
|| getBarcodeLinesCount | Returns the number of components (lines) in the barcode. |
|| sortByLen | Sorts barcode lines by component length. |
|| sortBySize | Sorts barcode lines by the number of points in them. |
|| sortByStart | Sorts barcode lines by their appearance time. |
|**Barcontainer** | Barscalar<br>Sum() const | Returns the sum of all line lengths. |
|| void relength() | Normalizes the appearance time of all components relative to the first one. |
|| Barscalar maxLen() const; | Returns the longest line in the barcode. |
| Baritem* clone() | Returns a full copy of the current item. |
|| size_t count(); | Returns the number of barcodes in the container. |
|| Baritem *getItem(size_t i); | Returns the barcode by its index. |
|| Baritem *extractItem(size_t index) | Extracts the barcode by its index. |
|| void removeLast() | Removes the last barcode from the container. |
|| Baritem* lastItem(); | Returns the last barcode in the container. |
|| void removeByThreshold(Barscalar const porog); | Removes all components in each barcode that are smaller than the specified threshold. |
|| void preprocessBarcode(Barscalar const& porog, bool normalize); | Preprocesses each barcode in the collection. |
|| float compareFull(const Barbase* bc, bc::CompareStrategy strat) const; | Compares each barcode in the collection and returns the best match. |
|| float compareBest (Baritem const* bc, bc::CompareStrategy strat) const; | Compares each barcode in the collection and returns the best match. |
|| size_t getBarcodesCount() const | Returns the number of barcodes in the container. |
|| void clear() | Clears the container. |
| **barline** | Barscalar getStart() const | Returns the start time of the component. |
|| Barscalar getLength() const | Returns the lifespan of the component. |
|| Barscalar getEnd() const | Returns the disappearance time of the component. |
|| const barvector& getMatrix() const | Returns non-zero points of the matrix in dictionary format `{Point: matrix value at the point, ...}`. |
|| barvector& getMatrix() | Returns non-zero points of the matrix in list format `{Matrvalue, ...}`. |
|| size_t getMatrixCount() const | Returns the count of non-zero points in the matrix. |
|| size_t getPointsSize() const | Returns the number of points in the component. |
|| BarRect getBarRect() const | Returns the bounding rectangle described by coordinates. |
|| barline* clone(bool cloneMatrix = true) const | Copies the current object. |
|| float lenFloat() const | Returns the line length as a float. |
|| int getDeath() | Returns the depth of the current component in the decomposition graph. |
|| getParrent | Returns the parent of the current component (the component that absorbed this one). |
|| bc::barline* getChild(uint id) const | Returns the child component. |
|| size_t getChildrenCount() const | Returns the number of components absorbed by the current one. |
|| template&lt;class TSTR, typename TO_STRING&gt;<br>void getJsonObject(TSTR& outObj,<br>ExportGraphType exportGraph = ExportGraphType::noExport,<br>bool export3dbar = false,<br>bool expotrBinaryMask = false) const | Saves the current component as a JSON object. |
|**Barscalar**| BarType type | Data type in which the scalar value is stored. |
|| unsigned char getByte8() const | Returns the scalar as an 8-byte value. |
|| int getInt() const | Returns the scalar as a 32-bit integer. |
|| float getFloat() const | Returns the scalar as a 32-bit floating-point value. |
|| unsigned char getRGB(int id) const | Retrieves one of the RGB color channels. |
|| float getAvgFloat() const | Returns the scalar value converted to a 32-bit integer. |
|| uchar getAvgUchar() const | Returns the scalar value converted to an 8-byte unsigned integer. |
|| float val_distance(const Barscalar& R) const | Returns the Euclidean distance between the current and the provided scalar. |
|| Barscalar absDiff(const Barscalar& R) const | Computes the absolute difference between the current and the provided scalar. |
| **BarRect** |  int x | Position of the rectangle relative to the left edge. |
|| int y | Position of the rectangle relative to the top edge. |
|| int width | Width of the rectangle. |
|| int height | Height of the rectangle. |
|| float coof() | Returns the aspect ratio of the rectangle. |
|| int right() | Returns the position of the rectangle's right edge. |
|| int botton() | Returns the position of the rectangle's bottom edge. |
|| int area() | Returns the area of the rectangle. |
|| bool isItemInside(BarRect anItem) | Determines whether the given rectangle is entirely within the current rectangle. |
|**barvalue**| unsigned short x | Position of the matrix element relative to the left edge. |
|| unsigned short y | Position of the matrix element relative to the top edge. |
|| Barscalar value | Matrix value at the given position. |
|**point**| int x | Position relative to the left edge. |
|| int y | Position relative to the top edge. |

