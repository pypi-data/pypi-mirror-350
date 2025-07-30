/*
  Copyright (C) 2025 Morten Kjeldgaard
*/

#include <Python.h>
#include "version.h"

#include "rgb.h"
#include "xyz.h"
#include "lab.h"
#include "hex.h"
#include "hls.h"
#include "hsv.h"
#include "luv.h"
#include "luminance.h"
#include "constants.h"

#define EPS 10e-9


/**
  convert_rgb_to_xyz(): This functions converts a color triple passed
  in a Python object to xyz color space.
*/
static PyObject *convert_rgb_to_xyz(PyObject *self, PyObject *args)
{
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }

  // Check range of data
  for (int i=0; i<3; i++){
    if (input.v[i] < 0) {
      PyErr_SetString(PyExc_ValueError, "r, g, b must be postive");
      return NULL;
    }
    if (input.v[i] > 1.0) {
      PyErr_SetString(PyExc_ValueError, "r, g, b must be in range [0:1]");
      return NULL;
    }
  }

  Vector3 result;
  rgb_to_xyz_p(&input, &result);

  return Py_BuildValue("(ddd)", result.x, result.y, result.z);
}

/**
  convert_rgb_to_lab(): This functions converts a color triple passed
  in a Python object to Lab color space.
*/
static PyObject *convert_rgb_to_lab(PyObject *self, PyObject *args)
{
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }

  // Check range of data
  for (int i=0; i<3; i++){
    if (input.v[i] < 0) {
      PyErr_SetString(PyExc_ValueError, "r, g, b must be postive");
      return NULL;
    }
    if (input.v[i] > 1.0) {
      PyErr_SetString(PyExc_ValueError, "r, g, b must be in range [0:1]");
      return NULL;
    }
  }

  Vector3 result;
  rgb_to_lab_p(&input, &result);

  return Py_BuildValue("(ddd)", result.x, result.y, result.z);
}


/**
  convert_rgb_to_hls(): This functions converts a color triple passed
  in a Python object to HLS color space.
*/
static PyObject *convert_rgb_to_hls(PyObject *self, PyObject *args)
{
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }

  // Check range of data
  for (int i=0; i<3; i++){
    if (input.v[i] < 0) {
      PyErr_SetString(PyExc_ValueError, "r, g, b must be postive");
      return NULL;
    }
    if (input.v[i] > 1.0) {
      PyErr_SetString(PyExc_ValueError, "r, g, b must be in range [0:1]");
      return NULL;
    }
  }

  Vector3 result;
  rgb_to_hls_p(&input, &result);

  return Py_BuildValue("(ddd)", result.x, result.y, result.z);
}


/**
  convert_hls_to_rgb(): This functions converts a color triple passed
  in a Python object to HLS color space.
*/
static PyObject *convert_hls_to_rgb(PyObject *self, PyObject *args)
{
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }


  // Check range of data
  if (input.v[0] < 0 || input.v[0] > 360.0) {
      PyErr_SetString(PyExc_ValueError, "hue must be in range [0:360]");
      return NULL;
    }

  if (input.v[1] > 1.0 || input.v[1] < -1.0) {
      PyErr_SetString(PyExc_ValueError, "lightness must be in range [-1:1]");
      return NULL;
    }

  if (input.v[2] > 1.0 || input.v[2] < 0.0) {
      PyErr_SetString(PyExc_ValueError, "saturation must be in range [0:1]");
      return NULL;
    }


  Vector3 result;
  hls_to_rgb_p(&input, &result);

  return Py_BuildValue("(ddd)", result.x, result.y, result.z);
}


/**
  convert_rgb_to_hsv(): This functions converts a color triple passed
  in a Python object to HSV color space.
*/
static PyObject *convert_rgb_to_hsv(PyObject *self, PyObject *args)
{
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }

  // Check range of data
  for (int i=0; i<3; i++){
    if (input.v[i] < 0) {
      PyErr_SetString(PyExc_ValueError, "r, g, b must be postive");
      return NULL;
    }
    if (input.v[i] > 1.0) {
      PyErr_SetString(PyExc_ValueError, "r, g, b must be in range [0:1]");
      return NULL;
    }
  }

  Vector3 result;
  rgb_to_hsv_p(&input, &result);

  return Py_BuildValue("(ddd)", result.x, result.y, result.z);
}


/**
  convert_hsv_to_rgb(): This functions converts a color triple passed
  in a Python object to HSV color space.
*/
static PyObject *convert_hsv_to_rgb(PyObject *self, PyObject *args)
{
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }

  // Check range of data
  if (input.v[0] < 0 || input.v[0] > 360.0) {
      PyErr_SetString(PyExc_ValueError, "hue must be in range [0:360]");
      return NULL;
  }

  if (input.v[1] > 1.0 || input.v[1] < -1.0) {
      PyErr_SetString(PyExc_ValueError, "saturation must be in range [-1:1]");
      return NULL;
  }

  if (input.v[2] > 1.0 || input.v[2] < 0.0) {
      PyErr_SetString(PyExc_ValueError, "value must be in range [0:1]");
      return NULL;
  }

  Vector3 result;
  hsv_to_rgb_p(&input, &result);

  return Py_BuildValue("(ddd)", result.x, result.y, result.z);
}


/**
  convert_xyz_to_rgb(): This functions converts a color triple passed
  in a Python object to Lab color space.
*/
static PyObject *convert_xyz_to_rgb(PyObject *self, PyObject *args)
{
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }

  Vector3 result;
  xyz_to_rgb_p(&input, &result);

  return Py_BuildValue("(ddd)", result.x, result.y, result.z);
}


/**
  convert_xyz_to_lab(): This functions converts a color triple passed
  in a Python object to Lab color space.
*/
static PyObject *convert_xyz_to_lab(PyObject *self, PyObject *args)
{
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }

  Vector3 result;
  xyz_to_lab_p(&input, &result);

  return Py_BuildValue("(ddd)", result.x, result.y, result.z);
}


/**
  convert_lab_to_rgb(): This functions converts a Lab color triple passed
  in a Python object to RGB color space.
*/
static PyObject *convert_lab_to_rgb(PyObject *self, PyObject *args)
{
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }

  Vector3 result;
  lab_to_rgb_p(&input, &result);

  return Py_BuildValue("(ddd)", result.x, result.y, result.z);
}


/**
  convert_lab_to_xyz(): This functions converts a Lab color triple passed
  in a Python object to XYZ color space.
*/
static PyObject *convert_lab_to_xyz(PyObject *self, PyObject *args)
{
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }

  Vector3 result;
  lab_to_xyz_p(&input, &result);

  return Py_BuildValue("(ddd)", result.x, result.y, result.z);
}


/**
  convert_hex_to_rgb(): This functions converts a hex code to a Python RGB tuple.
*/

static PyObject *convert_hex_to_rgb(PyObject *self, PyObject *args) {

  char *hexstring;
  char result[8]; // recieves verified hexcode from check_hexstr()

  if (!PyArg_ParseTuple(args, "s", &hexstring)) {
      return NULL;
    }

  int status = check_hexstr(hexstring, result);

  switch (status) {
  case OK:
    break;

  case NO_HASH:
    PyErr_SetString(PyExc_ValueError, "Not a hexcode, must start with '#'");
    return NULL;

  case NOT_HEX:
    PyErr_SetString(PyExc_ValueError, "Not a hexcode");
    return NULL;

  case ERROR:
    PyErr_SetString(PyExc_ValueError, "Unspecified hexcode error");
    return NULL;

  default:
    PyErr_SetString(PyExc_ValueError, "Unspecified hexcode error");
    return NULL;
  }


  /* The checked and verified hex string is now in 'results'. Now
   we convert the r, g and b components to actual double values */

  Vector3 rgb;

  hexcode_to_rgb_triple(result, &rgb);

  return Py_BuildValue("(ddd)", rgb.x, rgb.y, rgb.z);
}


/**
  convert_hex_to_xyz(): This functions converts a hex code to a Python
  XYZ tuple. The code is almost identical to convert_hex_to_rgb(),
  except we further convert the rgb triple to XYZ space.
*/
static PyObject *convert_hex_to_xyz(PyObject *self, PyObject *args) {

  char *hexstring;
  char result[8]; // recieves verified hexcode from check_hexstr()

  if (!PyArg_ParseTuple(args, "s", &hexstring)) {
      return NULL;
    }

  int status = check_hexstr(hexstring, result);

  switch (status) {
  case OK:
    break;

  case NO_HASH:
    PyErr_SetString(PyExc_ValueError, "Not a hexcode, must start with '#'");
    return NULL;

  case NOT_HEX:
    PyErr_SetString(PyExc_ValueError, "Not a hexcode");
    return NULL;

  case ERROR:
    PyErr_SetString(PyExc_ValueError, "Unspecified hexcode error");
    return NULL;

  default:
    PyErr_SetString(PyExc_ValueError, "Unspecified hexcode error");
    return NULL;
  }


  /* The checked and verified hex string is now in 'results'. Now
   we convert the r, g and b components to actual double values */

  Vector3 rgb, xyz;

  hexcode_to_rgb_triple(result, &rgb);

  // Convert further to XYZ
  rgb_to_xyz_p(&rgb, &xyz);

  return Py_BuildValue("(ddd)", xyz.x, xyz.y, xyz.z);
}


/**
  convert_hex_to_lab(): This functions converts a hex code to a Python
  XYZ tuple. The code is almost identical to convert_hex_to_rgb(),
  except we further convert the rgb triple to Lab space.
*/
static PyObject *convert_hex_to_lab(PyObject *self, PyObject *args) {

  char *hexstring;
  char result[8]; // recieves verified hexcode from check_hexstr()

  if (!PyArg_ParseTuple(args, "s", &hexstring)) {
      return NULL;
    }

  int status = check_hexstr(hexstring, result);

  switch (status) {
  case OK:
    break;

  case NO_HASH:
    PyErr_SetString(PyExc_ValueError, "Not a hexcode, must start with '#'");
    return NULL;

  case NOT_HEX:
    PyErr_SetString(PyExc_ValueError, "Not a hexcode");
    return NULL;

  case ERROR:
    PyErr_SetString(PyExc_ValueError, "Unspecified hexcode error");
    return NULL;

  default:
    PyErr_SetString(PyExc_ValueError, "Unspecified hexcode error");
    return NULL;
  }


  /* The checked and verified hex string is now in 'results'. Now
   we convert the r, g and b components to actual double values */

  Vector3 rgb, lab;

  hexcode_to_rgb_triple(result, &rgb);

  // Convert further to Lab space
  rgb_to_lab_p(&rgb, &lab);

  return Py_BuildValue("(ddd)", lab.x, lab.y, lab.z);
}


/**
  convert_xyz_to_xyy(): This functions converts an XYZ color triple
  passed in a Python object to xyY color space.
*/
static PyObject *convert_xyz_to_xyy(PyObject *self, PyObject *args)
{
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }

  Vector3 result;

  double sum = input.v[0] + input.v[1] + input.v[2];

  // if X = Y = Z = 0
  if (input.v[0] < EPS && input.v[1] < EPS && input.v[2] < EPS) {
    result.v[0] = D65_Xref;
    result.v[1] = D65_Yref;
  } else {
    result.v[0] = input.v[0] / sum;
    result.v[1] = input.v[1] / sum;
  }
  result.v[2] = input.v[1];

  return Py_BuildValue("(ddd)", result.x, result.y, result.z);
}


/**
  convert_xyy_to_xyz(): This functions converts an xyY color triple
  passed in a Python object to XYZ color space.
*/
static PyObject *convert_xyy_to_xyz(PyObject *self, PyObject *args)
{
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }

  Vector3 result;

  // if  y = 0
  if (input.v[1] < EPS) {
    result.v[0] = 0;
    result.v[1] = 0;
    result.v[2] = 0;
  } else {
    // X                x              Y            y
    result.v[0] = input.v[0] * input.v[2] / input.v[1];
    // Y               Y
    result.v[1] = input.v[2];
    // Z                     x             y               Y             y
    result.v[2] = (1 - input.v[0] - input.v[1]) * input.v[2] / input.v[1];
  }

  return Py_BuildValue("(ddd)", result.v[0], result.v[1], result.v[2]);
}


/**
   convert_rgb_to_hex() converts an RGB triple to hexcode.
 */
static PyObject *convert_rgb_to_hex(PyObject *self, PyObject *args) {

  Vector3 input;
  char result[8];

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }

  // Make sure user is not passing something weird
  for (int i=0; i<3; i++) {
    if (input.v[i] < 0 || input.v[i] > 1) {
      PyErr_SetString(PyExc_ValueError, "RGB triple must have values in [0:1]");
      return NULL;
    }
  }

  rgb_triple_to_hexcode(&input, result);

  return Py_BuildValue("s", result);
}


/**
   convert_xyz_to_luv() converts an XYZ triple to LUV color space.
 */
static PyObject *convert_xyz_to_luv(PyObject *self, PyObject *args)
{
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }

  Vector3 result;
  xyz_to_luv_p(&input, &result);
  return Py_BuildValue("(ddd)", result.x, result.y, result.z);
}


/**
   convert_luv_to_xyz() converts an LUV triple to XYZ color space.
 */
static PyObject *convert_luv_to_xyz(PyObject *self, PyObject *args)
{
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }

  Vector3 result;
  luv_to_xyz_p(&input, &result);
  return Py_BuildValue("(ddd)", result.x, result.y, result.z);
}


// --- RGB companding functions ---

/**
   call_to_linear() exposes the to_linear() function to Python.
 */
static PyObject *call_to_linear(PyObject *self, PyObject *args)
{
  double input;

  if (!PyArg_ParseTuple(args, "d", &input)) {
    return NULL;
  }
    return Py_BuildValue("d", to_linear(input));
}


/**
   call_from_linear() exposes the from_linear() function to Python.
 */
static PyObject *call_from_linear(PyObject *self, PyObject *args)
{
  double input;

  if (!PyArg_ParseTuple(args, "d", &input)) {
    return NULL;
  }
    return Py_BuildValue("d", from_linear(input));
}

// --- Luminocity calculations ---

/**
   convert_rgb_to_lum_sqr(), exposes the rgb_to_lum_sqr function to Python.
   Compute luminance using weighted root sum squared.
*/
static PyObject *convert_rgb_to_lum_sqr(PyObject *self, PyObject *args) {
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }
  return Py_BuildValue("d", rgb_to_luminance_sqr(&input));
}


/**
   convert_rgb_to_lum_sum() exposes the rgb_to_lum_sum function to Python.
   Compute luminance using weighted sum.
*/
static PyObject *convert_rgb_to_lum_sum(PyObject *self, PyObject *args) {
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }
  return Py_BuildValue("d", rgb_to_luminance_sum(&input));
}


/**
   convert_rgb_to_lum_wcag() exposes the rgb_to_lum_wcag function to Python.
   Compute luminance using WCAG algorithm.
*/
static PyObject *convert_rgb_to_lum_wcag(PyObject *self, PyObject *args) {
  Vector3 input;

  if (!PyArg_ParseTuple(args, "(ddd)", &input.v[0], &input.v[1], &input.v[2])) {
    return NULL;
  }
  return Py_BuildValue("d", rgb_to_luminance_wcag(&input));
}


/**
   compute_contrast_ratio() exposes the contrast_ratio to Python.
   Calculate the contrast ratio of two colors.
*/
static PyObject *compute_contrast_ratio(PyObject *self, PyObject *args) {
  Vector3 input1, input2;

  if (!PyArg_ParseTuple(args, "(ddd)(ddd)",
                        &input1.v[0], &input1.v[1], &input1.v[2],
                        &input2.v[0], &input2.v[1], &input2.v[2])) {
    return NULL;
  }
  return Py_BuildValue("d", contrast_ratio(&input1, &input2));
}

// --------------------------------

/**
  The PyMethodDef struct holds information about the methods in the
  module, this is the interface of the above functions with Python.
*/
static PyMethodDef RGBXYZLABMethods[]=
  {
    {"rgb_to_xyz", convert_rgb_to_xyz, METH_VARARGS, "Convert RGB triple to XYZ color space"},
    {"rgb_to_lab", convert_rgb_to_lab, METH_VARARGS, "Convert RGB triple to Lab color space"},
    {"rgb_to_hex", convert_rgb_to_hex, METH_VARARGS, "Convert RGB triple to hex code"},
    {"rgb_to_hls", convert_rgb_to_hls, METH_VARARGS, "Convert RGB triple to HLS color space"},
    {"hls_to_rgb", convert_hls_to_rgb, METH_VARARGS, "Convert HLS triple to RGB color space"},
    {"rgb_to_hsv", convert_rgb_to_hsv, METH_VARARGS, "Convert RGB triple to HSV color space"},
    {"hsv_to_rgb", convert_hsv_to_rgb, METH_VARARGS, "Convert HSV triple to RGB color space"},
    {"xyz_to_rgb", convert_xyz_to_rgb, METH_VARARGS, "Convert XYZ triple to RGB color space"},
    {"xyz_to_lab", convert_xyz_to_lab, METH_VARARGS, "Convert XYZ triple to Lab color space"},
    {"lab_to_rgb", convert_lab_to_rgb, METH_VARARGS, "Convert Lab triple to RGB color space"},
    {"lab_to_xyz", convert_lab_to_xyz, METH_VARARGS, "Convert Lab triple to XYZ color space"},
    {"hex_to_rgb", convert_hex_to_rgb, METH_VARARGS, "Convert hex code to RGB color space"},
    {"hex_to_xyz", convert_hex_to_xyz, METH_VARARGS, "Convert hex code to XYZ color space"},
    {"hex_to_lab", convert_hex_to_lab, METH_VARARGS, "Convert hex code to Lab color space"},
    {"xyz_to_xyy", convert_xyz_to_xyy, METH_VARARGS, "Convert XYZ triple to xyY color space"},
    {"xyy_to_xyz", convert_xyy_to_xyz, METH_VARARGS, "Convert xyY triple to XYZ color space"},
    {"xyz_to_xyy", convert_xyz_to_xyy, METH_VARARGS, "Convert XYZ triple to xyY color space"},
    {"xyz_to_luv", convert_xyz_to_luv, METH_VARARGS, "Convert XYZ triple to LUV color space"},
    {"luv_to_xyz", convert_luv_to_xyz, METH_VARARGS, "Convert LUV triple to XYZ color space"},
    {"to_linear",  call_to_linear, METH_VARARGS, "Compand sRGB values to linear form"},
    {"from_linear", call_from_linear, METH_VARARGS, "Compand linear rgb values to sRGB form"},
    {"rgb_to_lum_sqr", convert_rgb_to_lum_sqr, METH_VARARGS,"Compute luminance using weighted root sum squared"},
    {"rgb_to_lum_sum", convert_rgb_to_lum_sum, METH_VARARGS, "Compute luminance using weighted sum"},
    {"rgb_to_lum_wcag", convert_rgb_to_lum_wcag, METH_VARARGS,"Compute luminance using WCAG algorithm"},
    {"contrast_ratio", compute_contrast_ratio, METH_VARARGS, "Calculate the contrast ratio of two colors."},
    {NULL, NULL, 0, NULL}  /* Sentinel */
  };


/* PyModuleDef struct holds information about your module itself. It
   is not an array of structures, but rather a single structure that’s
   used for module definition:
*/
static struct PyModuleDef _rgbxyzlabmodule = {
  PyModuleDef_HEAD_INIT,
  "_rgbxyzlab",
  "Python module for converting colors between color spaces",
  -1,
  RGBXYZLABMethods
};

/*
  When a Python program imports your module for the first time, it
  will call PyInit__rgbxyzlab():
*/
PyMODINIT_FUNC PyInit__rgbxyzlab()
{
  PyObject *module = PyModule_Create(&_rgbxyzlabmodule);

  /*
    Add lexer constants by name, some of these are never returned by
    parser but eaten in this module
  */

  /* These compile time constants are from version.h (autogenerated) */
#ifdef GIT_COMMIT
  PyModule_AddObjectRef(module, "GIT_COMMIT", PyUnicode_FromString(GIT_COMMIT));
#endif
#ifdef GIT_BRANCH
  PyModule_AddObjectRef(module, "GIT_BRANCH", PyUnicode_FromString(GIT_BRANCH));
#endif
#ifdef COMPILE_TIME
  PyModule_AddObjectRef(module, "COMPILE_TIME", PyUnicode_FromString(COMPILE_TIME));
#endif
#ifdef VERSION
  PyModule_AddObjectRef(module, "VERSION", PyUnicode_FromString(VERSION));
#endif

  // Expose the rgb to xyz conversion matrices

  PyObject* mat = PyTuple_New(9);
  for (int i=0; i < 9; i++) {
    PyTuple_SetItem(mat, i, PyFloat_FromDouble(m_rgb_to_xyz[i]));
  }

  PyModule_AddObjectRef(module, "mat_rgb_to_xyz", mat);
  Py_DECREF(mat);

  mat = PyTuple_New(9);
  for (int i=0; i < 9; i++) {
    PyTuple_SetItem(mat, i, PyFloat_FromDouble(m_xyz_to_rgb[i]));
  }

  PyModule_AddObjectRef(module, "mat_xyz_to_rgb", mat);
  Py_DECREF(mat);


  /*
    Chromaticity coordinates of an RGB system (xr, yr), (xg, yg) and
     (xb, yb). Here sRGB, D65 standard. Macros are defined in xyz.h
   */
  PyObject* vec = PyTuple_New(2);
  PyTuple_SetItem(vec, 0, PyFloat_FromDouble(CHROM_XR));
  PyTuple_SetItem(vec, 1, PyFloat_FromDouble(CHROM_YR));
  PyModule_AddObjectRef(module, "chrom_red", vec);
  Py_DECREF(vec);

  vec = PyTuple_New(2);
  PyTuple_SetItem(vec, 0, PyFloat_FromDouble(CHROM_XG));
  PyTuple_SetItem(vec, 1, PyFloat_FromDouble(CHROM_YG));
  PyModule_AddObjectRef(module, "chrom_green", vec);
  Py_DECREF(vec);

  vec = PyTuple_New(2);
  PyTuple_SetItem(vec, 0, PyFloat_FromDouble(CHROM_XB));
  PyTuple_SetItem(vec, 1, PyFloat_FromDouble(CHROM_YB));
  PyModule_AddObjectRef(module, "chrom_blue", vec);
  Py_DECREF(vec);

  /*
    D65 White reference point D65_ref = ()
  */
  vec = PyTuple_New(3);
  PyTuple_SetItem(vec, 0, PyFloat_FromDouble(D65_Xref));
  PyTuple_SetItem(vec, 1, PyFloat_FromDouble(D65_Yref));
  PyTuple_SetItem(vec, 2, PyFloat_FromDouble(D65_Zref));
  PyModule_AddObjectRef(module, "D65_ref", vec);
  Py_DECREF(vec);


  /*
    Expose constants kappa and epsilon.
   */
  PyObject *f = PyFloat_FromDouble(epsilon);
  PyModule_AddObjectRef(module, "epsilon", f);
  Py_DECREF(f);

  f = PyFloat_FromDouble(kappa);
  PyModule_AddObjectRef(module, "kappa", f);
  Py_DECREF(f);


  return module;
}
