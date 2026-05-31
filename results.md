###### window, or input fields or any way to manually enter data while the script is running.

###### Variables can be set via:

###### assignments in the script

###### the Customizer

###### -D at the command line interface

###### accessing data in a few file formats (stl, dxf, png, etc).

###### With the exception of DXF files, data from files is not accessible to the script, although to a limited extent the script may be able to

###### manipulate the data as a whole. For example, STL files can be rendered in OpenSCAD, translated, clipped, etc. But the internal data

###### that constitutes the STL file is inaccessible.

###### Getting a point is useful for reading an origin point in a 2D view in a technical drawing. The function dxf_cross reads the intersection

###### of two lines on a layer you specify and returns the intersection point. This means that the point must be given with two lines in the

###### DXF file, and not a point entity.

###### You can read dimensions from a technical drawing. This can be useful to read a rotation angle, an extrusion height, or spacing between

###### parts. In the drawing, create a dimension that does not show the dimension value, but an identifier. To read the value, you specify this

###### identifier from your program:

###### For a nice example of both functions, see Example009 and the image on the homepage of OpenSCAD (http://www.openscad.org/).

#### Getting input

##### Getting a point from a drawing

```
OriginPoint = dxf_cross(file="drawing.dxf", layer="SCAD.Origin",
origin=[ 0 , 0 ], scale= 1 );
```
##### Getting a dimension value

```
TotalWidth = dxf_dim(file="drawing.dxf", name="TotalWidth",
layer="SCAD.Origin", origin=[ 0 , 0 ], scale= 1 );
```

## Chapter 2 -- 3D Objects

##### OpenSCAD User Manual/The OpenSCAD Language

###### Creates a cube or rectangular prism (i.e., a "box") in the first octant. When center is true, the cube is centered on the origin. Argument

###### names are optional if given in the order shown here.

```
cube(size = [x,y,z], center = true/false);
cube(size = x , center = true/false);
```
###### parameters :

###### size

###### single value, cube with all sides this length

###### 3 value array [x,y,z], rectangular prism with dimensions x, y and z.

###### center

###### false (default), 1st (positive) octant, one corner at (0,0,0)

###### true , cube is centered at (0,0,0)

```
default values: cube(); yields: cube(size = [1, 1, 1], center = false);
```
###### examples :

```
equivalent scripts for this example
cube(size = 18);
cube(18);
cube([18,18,18]);
.
cube(18,false);
cube([18,18,18],false);
cube([18,18,18],center=false);
cube(size = [18,18,18], center = false);
cube(center = false,size = [18,18,18] );
```
```
equivalent scripts for this example
cube([18,28,8],true);
box=[18,28,8];cube(box,true);
```
#### Primitive Solids

##### cube

##### sphere


###### Creates a sphere at the origin of the coordinate system. The r argument name is optional. To use d instead of r, d must be named.

###### Parameters

###### r

###### Radius. This is the radius of the sphere.

###### d