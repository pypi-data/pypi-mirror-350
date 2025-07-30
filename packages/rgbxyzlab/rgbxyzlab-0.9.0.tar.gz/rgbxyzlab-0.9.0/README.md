

# Introduction

`Rgbxyzlab` is a Python C extension module for converting between color spaces. It got its name from the first three color conversions implemented, RGB, XYZ and `L*a*b*`, but since then more color space conversions has been added. So you can think of the name as a reference to an actual lab where experiments are taking place. So in fact his module is a lab for playing with colors in Python, at least that&rsquo;s what I use it for, and being compiled from C code it is lightning. Hopefully it&rsquo;s useful to others as well.

Most of the math used to implement the conversions is from Bruce Lindbloom&rsquo;s [awesome webpage](http://brucelindbloom.com/index.html?Math.html).


# Example: Converting RGB to XYZ color space

The API of the conversion routines are all the same. You pass a triplet sequence of numbers and the functions return a Python tuple. First, import the module, then all functions are available. We&rsquo;ll convert RGB = (0, 1, 1) (cyan) to HLS color mode:

    import rgbxyzlab as R
    
    rgb = (0, 1, 1)
    hls = R.rgb_to_hls(rgb)
    print(hls)
    (180.0, 0.5, 1.0)

All converstion functions are called something like `aaa_to_bbb()`, and they all take a parameter of a tuple.

We can also convert this cyan color to XYZ color space, more formally known as the [CIE 1931 color space](https://en.wikipedia.org/wiki/CIE_1931_color_space). The XYZ colorspace is linear in terms of human color perception, so it&rsquo;s suited for interpolating between colors or finding the &ldquo;distance&rdquo; between colors.

    xyz = R.rgb_to_xyz(rgb)
    print(xyz)
    (53.8013560910308, 78.73271485943779, 106.94961044176709)

For example, if you would like to make the cyan color lighter, you could interpolate a distance towards the white point. The white point used in `rgbxyzlab` is exposed as a tuple `D65_ref`:

    print(R.D65_ref)
    (0.95047, 1.0, 1.08883)


## Not every conversion is available

The main players in this module is the RGB and XYZ formats, and sometimes you need to go through these to get the conversion you want. Say you have a hexadecimal color code, and you want an HSV color code. First, you convert to RGB color space and from there you can convert to HSV:

    hexcod = "#abcdef"
    rgb = R.hex_to_rgb(hexcod)
    hsv = R.rgb_to_hsv(rgb)
    print(hsv)
    (210.0, 0.2845188284518829, 0.9372549019607843)

Incidentally, this is a light blue color called &ldquo;alphabetblue&rdquo; in my [collection of colors](https://bioxray.dk/color-hexcodes/) <sup><a id="fnr.1" class="footref" href="#fn.1" role="doc-backlink">1</a></sup>.


## Also works with numpy arrays

In the examples above, we saw the module work with Python tupes as input, by the functions in `rgbxyzlab` work with any Python sequence type, including numpy arrays. As we have access to the 8 primary colors (red, green, blue, yellow, magenta, cyan, white, black) in all color spaces, we might as well try that.

    import numpy as np
    from rgbxyzlab import primaries
    
    yellow = np.array(primaries.xyz_yellow)
    
    # print yellow and its type
    print(yellow, type(yellow))
    [77.00325167 92.78250067 13.85259215] <class 'numpy.ndarray'>
    
    lab = R.xyz_to_lab(yellow)
    print(lab)
    (97.1392634315565, -21.553728492653857, 94.47796332009793)

So in `L*a*b*` color space, also called CIELAB color space, the color yellow has a quite strange coordinate, far outside the normal [1:0] range.  It&rsquo;s quite a useful color space when working with perception. In short,

-   `L*` measures whether the sample is light (high `L*`) or dark (`low L*`)
-   `a*` and `b*` represent the chromaticity (hue and chroma) of the sample, where
    -   Negative `a*` gives colors in the *green* direction
    -   Positive `a*` gives colors in the *red* direction
    -   Negative `b*` gives colors in the *blue* direction
    -   Positive `b*` gives colors in the *yellow* direction

Using color values in the `L*a*b*` color space it is possible to compute the difference between colors.

So, lets see how well we did, we can compare our converted color stored in variable `lab` to the given lab color for yellow. We need to do this with numpy arrays so we can do arithmetic operations:

    print(np.array(lab) - np.array(primaries.lab_yellow))
    [-4.43506565e-10  3.46144446e-10  1.09793064e-09]

That is very close. In any case, the purpose of this example was to illustrate that `rgbxyzlab` works transparently with numpy.


# Reproducing the RGB to XYZ conversion in Python

The RGB to XYZ conversion is rather complex, you can check out [Bruce Lindbloom&rsquo;s site](http://brucelindbloom.com/index.html?Math.html) for the mathematical details. But here, lets reproduce what is going on inside `rgb_to_xyz` in Python.

The thing to realize is the that our well known and loved RGB color space *is not linear*. It was created to give a certain visual response on the monitors used in the childhood of computer graphics. For example, a red value of 100 would result in a certain voltage on the red electron cathode in the monitor that would provide a certain color brightness, but a value of 200 would not give of twice that voltage and brightness. The reason is that the human eye can distinguish better between different intensities of bright colors than dark colors, so the &ldquo;distance&rdquo; between RGB values is smaller at high RGBs than at low. Of course you already know that, we don&rsquo;t see well in the dark.

Therefore, when converting to the linear XYZ space, we first need to linearize (it&rsquo;s called *companding*) the RGB scale to the linear rgb scale. Fortunately this function is available in `rgbxyzlab`.

So following the notation of Lindbloom, as a first step, the companded RGB channels (denoted with upper case (`R`, `G`, `B`) are made linear with respect to energy (denoted with lower case (`r`, `g`, `b`).

Let&rsquo;s again use the color alphabetblue in this example. Furthermore, in the following you will see how we can juggle between numpy and Python tuples (and lists) returned by the various `rgbxyzlab` functions. It is advantageous to use numpy in situations where you want to do arithmetic computations on vectors.

    RGB = R.hex_to_rgb("#abcdef")
    print(RGB)
    (0.6705882352941176, 0.803921568627451, 0.9372549019607843)

The resulting type of `RGB` is a Python tuple object, containing the red, green and blue components of alphabetblue. Next convert to linear rgb space:

    rgb  = [ R.to_linear(i) for i in RGB ]
    print(rgb)
    [0.4072402119017367, 0.6104955708078648, 0.8631572134541023]

Type resulting type of `rgb` is a Python list object. It is obvious that the numbers of the non-linear `RGB` triplet and the linear `rgb` triplet are very different!

Next step is to convert the RGB to XYZ conversion matrix to a 3 x 3 numpy array, that can be used in further calculations. The matrix is exposed by `rgbxyzlab` as a tuple with 9 elements:

    M = R.mat_rgb_to_xyz
    (0.412456439089692, 0.357576077643909, 0.180437483266399, 0.212672851405623, 0.715152155287818, 0.07217499330656, 0.019333895582329, 0.119192025881303, 0.950304078536368)
    
    # Convert to 3x3 matrix
    M = np.array(R.mat_rgb_to_xyz).reshape(3,3)
    print(M)
    [[0.41245644 0.35757608 0.18043748]
     [0.21267285 0.71515216 0.07217499]
     [0.0193339  0.11919203 0.95030408]]

The final step is to left multiply the linearized `rgb` vector by the matrix `M`:

    XYZ = 100 * M.dot(rgb)
    print(XYZ)
    [54.20133745 58.55045264 90.0901564 ]

So, the XYZ color of alphabetblue in XYZ space is `[54.20, 58.55, 90.09]`,


### Checking results

Checking with the results from the function `rgb_to_xyz()`:

    alphabetblue = R.rgb_to_xyz(RGB)
    print(alphabetblue)
    (54.201337454247366, 58.55045264326424, 90.09015639735054)

Now what is the difference of this to the value `XYZ` we calculated above?

    print(XYZ - np.array(alphabetblue))
    [0. 0. 0.]


# How the matrix M is derived

As we saw about, this is what the RGB to XYZ conversion matrix looks like converted to numpy format:

    M = np.array(R.mat_rgb_to_xyz).reshape(3,3)
    print(M)
    
    [[0.41245644 0.35757608 0.18043748]
     [0.21267285 0.71515216 0.07217499]
     [0.0193339  0.11919203 0.95030408]]

But how is it derived?

If you want to follow along with the mathical notation, find the page on the [Lindbloom site](http://brucelindbloom.com/index.html?Math.html) where the RGB/XYZ matrices are explained.

We start with the chromaticity coordinates of an RGB system, called `(xr, yr)`, `(xg, yg)` and `(xb, yb)` for red, green and blue respectively.  The exact values of these differ depending on what standard is used. In `rgbxyzlab` the sRGB, the D65 standard is used.

    print(R.chrom_red, R.chrom_green, R.chrom_blue)
    (0.64, 0.33) (0.3, 0.6) (0.15, 0.06)
    xr, yr = R.chrom_red
    xg, yg = R.chrom_green
    xb, yb = R.chrom_blue

White point, D65 standard:

    print(R.D65_ref)
    (0.95047, 1.0, 1.08883)

Next we compute some intermediate variables, `Xr`, `Xg` and `Xb`:

    # Red
    Xr = xr / yr
    Yr = 1.0
    Zr = (1.0 - xr - yr) / yr
    
    # Green
    Xg = xg / yg
    Yg = 1.0
    Zg = (1.0 - xg - yg) / yg
    
    # BLue
    Xb = xb / yb
    Yb = 1.0
    Zb = (1.0 - xb - yb) / yb

From these components, form a 3x3 matrix:

    mat = (Xr, Xg, Xb, Yr, Yg, Yb, Zr, Zg, Zb )
    mat = np.array(Mi).reshape(3,3)

Invert the matrix `mat`:

    mat_inv = np.linalg.inv(mat)

And left multiply the vector of the White Point with the inverted matrix:

    Sr, Sg, Sb = mat_inv.dot(R.D65_ref)
    print(Sr, Sg, Sb)

Finally, compute the RGB to XYZ conversion matrix `M`:

    M = (Sr*Xr, Sg*Xg, Sb*Xb,
         Sr*Yr, Sg*Yg, Sb*Yb,
         Sr*Zr, Sg*Zg, Sb*Zb)
    M = np.array(M).reshape(3, 3)
    print(M)
    array([[0.41245644, 0.35757608, 0.18043748],
           [0.21267285, 0.71515216, 0.07217499],
           [0.0193339 , 0.11919203, 0.95030408]])

Compare to the RGB to XYZ matrix used in `rgbxyzlab`, exposed as a tuple of length 9 in `mat_rgb_to_xyz`:

    M_builtin = np.array(R.mat_rgb_to_xyz).reshape(3,3)
    print(M_builtin)
    [[0.41245644 0.35757608 0.18043748]
     [0.21267285 0.71515216 0.07217499]
     [0.0193339  0.11919203 0.95030408]]

They&rsquo;re identical.

So now you know how the function `rgb_to_xyz()` works, except it&rsquo;s programmed in C not in Python and numpy.


# Conversion function overview

<table>


<colgroup>
<col  class="org-left">

<col  class="org-left">

<col  class="org-left">

<col  class="org-left">

<col  class="org-left">

<col  class="org-left">

<col  class="org-left">

<col  class="org-left">

<col  class="org-left">
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">to</th>
<th scope="col" class="org-left">rgb</th>
<th scope="col" class="org-left">hls</th>
<th scope="col" class="org-left">hsv</th>
<th scope="col" class="org-left">xyz</th>
<th scope="col" class="org-left">xyy</th>
<th scope="col" class="org-left">lab</th>
<th scope="col" class="org-left">luv</th>
<th scope="col" class="org-left">hex</th>
</tr>
</thead>
<tbody>
<tr>
<td class="org-left">rgb</td>
<td class="org-left">-</td>
<td class="org-left">*</td>
<td class="org-left">*</td>
<td class="org-left">*</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">*</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">*</td>
</tr>

<tr>
<td class="org-left">hls</td>
<td class="org-left">*</td>
<td class="org-left">-</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">hsv</td>
<td class="org-left">*</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">-</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">xyz</td>
<td class="org-left">*</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">-</td>
<td class="org-left">*</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">*</td>
<td class="org-left">*</td>
</tr>

<tr>
<td class="org-left">xyy</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">*</td>
<td class="org-left">-</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">lab</td>
<td class="org-left">*</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">*</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">-</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">*</td>
</tr>

<tr>
<td class="org-left">luv</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">*</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">-</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">hex</td>
<td class="org-left">*</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">&#xa0;</td>
<td class="org-left">-</td>
</tr>
</tbody>
</table>


## RGB to various

-   `rgb_to_xyz()` Convert RGB triple to XYZ color space
-   `rgb_to_lab()` Convert RGB triple to Lab color space
-   `rgb_to_hex()` Convert RGB triple to hex code
-   `rgb_to_hls()` Convert RGB triple to HLS color space
-   `rgb_to_hsv()` Convert RGB triple to HSV color space


## Lab to various

-   `lab_to_rgb()` Convert Lab triple to RGB color space
-   `lab_to_xyz()` Convert Lab triple to XYZ color space


## Hexcode to various

-   `hex_to_rgb()` Convert hex code to RGB color space
-   `hex_to_xyz()` Convert hex code to XYZ color space
-   `hex_to_lab()` Convert hex code to Lab color space


## XYZ to various

-   `xyz_to_rgb()` Convert XYZ triple to RGB color space
-   `xyz_to_lab()` Convert XYZ triple to Lab color space
-   `xyz_to_xyy()` Convert XYZ triple to xyY color space
-   `xyz_to_luv()` Convert a XYZ triple to Luv color space


## To XYZ

-   `rgb_to_xyz()` Convert RGB triple to XYZ color space
-   `xyy_to_xyz()` Convert xyY triple to XYZ color space
-   `luv_to_xyz()` Convert a Luv triple to XYZ color space
-   `lab_to_xyz()` Convert Lab triple to XYZ color space


## To RGB

-   `hls_to_rgb()` Convert HLS triple to RGB color space
-   `hsv_to_rgb()` Convert HSV triple to RGB color space
-   `xyz_to_rgb()` Convert XYZ triple to RGB color space

-   `lab_to_rgb()` Convert Lab triple to RGB color space
-   `hex_to_rgb()` Convert hex code to RGB color space


## sRGB companding

-   `to_linear()`  Compand sRGB values to linear form
-   `from_linear()` Compand linear rgb values to sRGB form


## Luminance

-   `rgb_to_lum_sum()` Compute luminance using weighted sum.
-   `rgb_to_lum_sqr()` Compute luminance using weighted root sum squared.
-   `rgb_to_lum_wcag()` Compute luminance using [WCAG algorithm](https://www.w3.org/TR/WCAG20-TECHS/G18.html).
-   `contrast_ratio()` Calculate the contrast ratio of two RGB colors.

---


# Footnotes

<sup><a id="fn.1" href="#fnr.1">1</a></sup> Direct [link to the json file](https://codeberg.org/mok0/gist/raw/branch/main/color-hexcodes.json).
