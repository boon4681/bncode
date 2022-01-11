# BNCODE

A BN code (an initialism for Boon code) is a type of data storage as an image that design for low resolution work with low data quality.
in this version it can be store 32 bit or 4 bytes that can store number from 0 upto 4,294,967,295

## Design
BN code is detected by a 2-dimensuinal digital image sensor and program. 

<table>
  <tr>
    <td valign="top"><img align=center src="https://media.discordapp.net/attachments/558622428754870272/930335073138511932/qrcode.png" width="200px" />
    <p align=center>Normal QRcode</p>
    </td>
    <td valign="top"><img align=center src="https://media.discordapp.net/attachments/558622428754870272/930332559672492072/brcode.png" width="200px"/>
    <p align=center>BNcode version 1, 8x8 pixel</p>
    </td>
  </tr>
</table>

### **Storage Capacity with version 1**
| Input Mode  | Max. Capacity |
| ------------- | ------------- |
| Numeric  | 0 - 4,294,967,295 |
| Character | 4 characters (8 bit per char) |

### **Encoding**

The format information records two things: bit data and ref bit. bit data is your data and bit ref is bit that the scanner will compare with the bit data.

<table>
  <tr>
    <td valign="top">
    <img align=center alt="border section" src="https://media.discordapp.net/attachments/558622428754870272/930340411472506890/unknown.png" width="170px">
    <p align=center>border section</p>
    </td>
    <td valign="top">
    <img align=center alt="data section" src="https://media.discordapp.net/attachments/558622428754870272/930340819767005194/unknown.png" width="170px">
    <p align=center>data section</p>
    </td>
    <td valign="top">
    <img align=center alt="mirror blocking" src="https://media.discordapp.net/attachments/558622428754870272/930343819755536404/unknown.png" width="170px">
    <p align=center>mirror blocking</p>
    </td>
  </tr>
</table>


color black and white refer to 0,1 in binary the decoder will read color on image from top-down,left to right

**why mirror blocking is important**
because BNcode store binary directly to image the flipped image with cause a worng data reading


### **Decoding**

read the encoding section ---

<div class="py-10"></div>

## **Installation**
```sh
pip install bncode
```

## **Example Code**
**Read and write**

```python
from bncode import create, scan
import cv2

cv2.imwrite("bncode.png",create(123456)) # create image
print(scan(cv2.imread('bncode.png'))) # scan image
```
**Scan from camera**
```python
from bncode import create, scan
import cv2

cam = cv2.VideoCapture(0)
while True:
    c,img = cam.read() # read image from camera
    print(scan(img)) # scan image
    cv2.waitKey(1)
```