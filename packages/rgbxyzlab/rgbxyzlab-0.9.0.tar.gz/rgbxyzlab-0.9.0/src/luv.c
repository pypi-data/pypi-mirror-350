#include <math.h>
#include "vector3.h"
#include "constants.h"

#define DENOM (D65_Xref + 15 * D65_Yref + 3 * D65_Zref)
#define UR_PRIME (4 * D65_Xref / DENOM)
#define VR_PRIME (9 * D65_Yref / DENOM)

#define EPS 10e-9

/**
   xyz_to_luv() converts an XYZ triple to LUV color space.
   See http://www.brucelindbloom.com/index.html?LContinuity.html
 */
void xyz_to_luv_p(Vector3 *input, Vector3 *result) {

  double X = input->x / 100;
  double Y = input->y / 100;
  double Z = input->z / 100;

  if (X < EPS && Y < EPS && Z < EPS) {  // we divide by sum later
    result->x = 0;
    result->y = 0;
    result->z = 0;
    return;
  }

  double yr = Y / D65_Yref;
  double L = yr > epsilon ? 116 * cbrt(yr) - 16 : kappa * yr;

  double d = X + 15 * Y + 3 * Z;
  double u_prime = 4 * X / d;
  double v_prime = 9 * Y / d;

  result->x = L;
  result->y = 13 * L * (u_prime - UR_PRIME);
  result->z = 13 * L * (v_prime - VR_PRIME);
  return;
}


#define U0 (4 * D65_Xref / DENOM)
#define V0 (9 * D65_Yref / DENOM)
#define MINUS_ONE_THIRD (-1.0/3)

/**
   luv_to_xyz() converts an LUV triple to XYZ color space.
   See http://www.brucelindbloom.com/index.html?LContinuity.html
 */
void luv_to_xyz_p(Vector3 *input, Vector3 *result) {

  //double X = 0, Y = 0, a = 0, b = 0, d = 0;

  double L = input->x ;
  double u = input->y ;
  double v = input->z ;

  if (L < EPS) {  // we divide by L later
    result->x = 0;
    result->y = 0;
    result->z = 0;
    return;
  }

  double Y = L > kappa * epsilon ? pow((L + 16)/ 116, 3) : L / kappa;
  double a = ((52 * L / (u + 13 * L * U0)) - 1) / 3;
  double b = -5 * Y;
  double d = Y * ((39 * L /(v + 13 * L * V0)) - 5);
  double X = (d - b)/ (a - MINUS_ONE_THIRD);

  result->x = 100 * X;
  result->y = 100 * Y;
  result->z = 100 * (X * a + b);
  return;
}
