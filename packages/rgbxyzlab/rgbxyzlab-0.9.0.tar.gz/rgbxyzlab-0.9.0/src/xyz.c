#include <math.h>
#include "vector3.h"


#ifdef OFFICIAL_DEFINITION

// Official CIE defintions
double m_rgb_to_xyz[] = {
    0.4124, 0.3576, 0.1805,
    0.2126, 0.7152, 0.0722,
    0.0193, 0.1192, 0.9505};

double m_xyz_to_rgb[] = {
  3.2406255, -1.5372080, -0.4986286,
 -0.9689307,  1.8757561,  0.0415175,
  0.0557101, -0.2040211,  1.0569959};

#else

/*
  My exact computed matrices from D65 white point and chromaticity
  coordinates: RGB to XYZ conversion matrix:
*/

// RGB to XYZ conversion matrix:
double m_rgb_to_xyz[] = {
  0.412456439089692, 0.357576077643909, 0.180437483266399,
  0.212672851405623, 0.715152155287818, 0.072174993306560,
  0.019333895582329, 0.119192025881303, 0.950304078536368 };

// XYZ to RGB conversion matrix:
double m_xyz_to_rgb[] = {
  3.240454162114105, -1.537138512797716, -0.498531409556016,
  -0.969266030505187, 1.876010845446694, 0.041556017530350,
  0.055643430959115, -0.204025913516754, 1.057225188223179 };
#endif


/**
   to_linear() converts companded sRGB values to their linearized form.
 */
double to_linear(double v) {
  // from wikipedia
  double V = v <= 0.04045 ? v/12.92 : pow((v + 0.055)/1.055, 2.4);
  return V;
}


/**
   from_linear() compands linear rgb values to sRGB standard.
 */
double from_linear(double v) {
  // from wikipedia
  double V = v <= 0.0031308 ? 12.92 * v : 1.055 * pow(v, 1/2.4) - 0.055;
  return V;
}

/**
   Convert linear rgb color to XYZ

   The linear RGB channels (denoted with lower case (r,g,b), (or
   generically v, v ∈ {r,g,b}), are made nonlinear (denoted with upper
   case (R,G,B) (or generically V, V ∈ {R,G,B}).

   RGB to XYZ

   A companded RGB color [RGB], whose components are in the nominal
   range [0, 1], is converted to XYZ in two steps.

   1. First, the companded RGB channels (denoted with upper case
      (R,G,B)) are made linear with respect to energy (denoted with
      lower case (r,g,b)). This same operation is performed on all three
      channels, but the operation depends on the companding function
      associated with the RGB color system.
   2. Linear RGB to XYZ
 */
Vector3 rgb_to_xyz(double R, double G, double B) {

  double r = to_linear(R);
  double g = to_linear(G);
  double b = to_linear(B);

  double X = m_rgb_to_xyz[0] * r + m_rgb_to_xyz[1] * g + m_rgb_to_xyz[2] * b;
  double Y = m_rgb_to_xyz[3] * r + m_rgb_to_xyz[4] * g + m_rgb_to_xyz[5] * b;
  double Z = m_rgb_to_xyz[6] * r + m_rgb_to_xyz[7] * g + m_rgb_to_xyz[8] * b;

  Vector3 result;
  result.x = 100 * X;
  result.y = 100 * Y;
  result.z = 100 * Z;

  return result;
}


/**
   Convert XYZ color to linear rgb

   The linear RGB channels (denoted with lower case (r,g,b), (or
   generically v, v ∈ {r,g,b}), are made nonlinear (denoted with upper
   case (R,G,B) (or generically V, V ∈ {R,G,B}).

   XYZ to RGB

   Given an XYZ color whose components are in the nominal range [0.0,
   1.0] and whose reference white is the same as that of the RGB
   system, the conversion to companded RGB is done in two steps.

   1. Convert XYZ to Linear RGB
   2. Linear RGB channels (denoted with lower case (r,g,b), or
      generically v) are made nonlinear (denoted with upper case (R,G,B)
      or generically V). This operation is performed on all three
      channels, but the operation depends on the companding function (for
      example applying Gamma) associated with the RGB color system.
 */

Vector3 xyz_to_rgb(double X, double Y, double Z) {

  X /= 100;
  Y /= 100;
  Z /= 100;

  double R = m_xyz_to_rgb[0] * X + m_xyz_to_rgb[1] * Y + m_xyz_to_rgb[2] * Z;
  double G = m_xyz_to_rgb[3] * X + m_xyz_to_rgb[4] * Y + m_xyz_to_rgb[5] * Z;
  double B = m_xyz_to_rgb[6] * X + m_xyz_to_rgb[7] * Y + m_xyz_to_rgb[8] * Z;

  Vector3 result;
  result.v[0] = from_linear(R);
  result.v[1] = from_linear(G);
  result.v[2] = from_linear(B);
  return result;
}

/**
   rgb_to_xyz pointer version.
 */
void rgb_to_xyz_p(Vector3 *in, Vector3 *result) {

  double r = to_linear(in->x);
  double g = to_linear(in->y);
  double b = to_linear(in->z);

  double X = m_rgb_to_xyz[0] * r + m_rgb_to_xyz[1] * g + m_rgb_to_xyz[2] * b;
  double Y = m_rgb_to_xyz[3] * r + m_rgb_to_xyz[4] * g + m_rgb_to_xyz[5] * b;
  double Z = m_rgb_to_xyz[6] * r + m_rgb_to_xyz[7] * g + m_rgb_to_xyz[8] * b;

  result->x = 100 * X;
  result->y = 100 * Y;
  result->z = 100 * Z;
}

/**
   xyz_to_rgb pointer version.
 */
void xyz_to_rgb_p(Vector3 *in, Vector3 *result) {

  double X = in->x / 100;
  double Y = in->y / 100;
  double Z = in->z / 100;

  double R = m_xyz_to_rgb[0] * X + m_xyz_to_rgb[1] * Y + m_xyz_to_rgb[2] * Z;
  double G = m_xyz_to_rgb[3] * X + m_xyz_to_rgb[4] * Y + m_xyz_to_rgb[5] * Z;
  double B = m_xyz_to_rgb[6] * X + m_xyz_to_rgb[7] * Y + m_xyz_to_rgb[8] * Z;

  result->v[0] = from_linear(R);
  result->v[1] = from_linear(G);
  result->v[2] = from_linear(B);
}
