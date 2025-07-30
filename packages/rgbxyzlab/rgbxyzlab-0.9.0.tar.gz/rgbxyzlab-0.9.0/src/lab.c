#include <math.h>
#include "vector3.h"
#include "lab.h"
#include "constants.h"


/**
   Convert XYZ color to Lab
 */
Vector3 xyz_to_lab(double X, double Y, double Z) {

  // This conversion requires a reference white (Xr,Yr,Zr)

  double xr = X / D65_Xref / 100;
  double yr = Y / D65_Yref / 100;
  double zr = Z / D65_Zref / 100;

  double fy = yr > epsilon ? cbrt(yr) : (kappa * yr + 16.0) / 116.0;
  double fx = xr > epsilon ? cbrt(xr) : (kappa * xr + 16.0) / 116.0;
  double fz = zr > epsilon ? cbrt(zr) : (kappa * zr + 16.0) / 116.0;

  Vector3 result;
  result.v[0] = 116.0 *  fy - 16.0;
  result.v[1] = 500.0 * (fx - fy);
  result.v[2] = 200.0 * (fy - fz);

  return result;
}

/**
   Convert Lab color to XYZ
*/
Vector3 lab_to_xyz(double L, double a, double b) {

  double fy = (L + 16.0) / 116.0;
  double fx = a / 500.0 + fy;
  double fz = fy - b / 200.0;

  double fx3 = pow(fx, 3);
  double xr = fx3 > epsilon ? fx3 : (116.0 * fx - 16.0) / kappa;

  double yr = L > kappa * epsilon ? pow((L + 16)/116, 3) : L / kappa;

  double fz3 = pow(fz, 3);
  double zr = fz3 > epsilon ? fz3 : (116.0 * fz - 16.0) / kappa;

  Vector3 result;

  result.v[0] = xr * D65_Xref * 100 ;
  result.v[1] = yr * D65_Yref * 100;
  result.v[2] = zr * D65_Zref * 100;

  return result;

}


/**
   Convert XYZ color to Lab
 */
void xyz_to_lab_p(Vector3 *in, Vector3 *result) {

  // This conversion requires a reference white (Xr,Yr,Zr)

  double xr = in->x/D65_Xref/100;
  double yr = in->y/D65_Yref/100;
  double zr = in->z/D65_Zref/100;

  double fy = yr > epsilon ? cbrt(yr) : (kappa * yr + 16.0) / 116.0;
  double fx = xr > epsilon ? cbrt(xr) : (kappa * xr + 16.0) / 116.0;
  double fz = zr > epsilon ? cbrt(zr) : (kappa * zr + 16.0) / 116.0;

  result->v[0] = 116.0 *  fy - 16.0;
  result->v[1] = 500.0 * (fx - fy);
  result->v[2] = 200.0 * (fy - fz);
}

/**
   Convert Lab color to XYZ
*/
void lab_to_xyz_p(Vector3 *in, Vector3 *result) {

  double fy = (in->x + 16.0) / 116.0;
  double fx = in->y / 500.0 + fy;
  double fz = fy - in->z / 200.0;

  double fx3 = pow(fx, 3);
  double xr = fx3 > epsilon ? fx3 : (116.0 * fx - 16.0) / kappa;
  double yr = in->x > kappa * epsilon ? pow((in->x + 16)/116, 3) : in->x / kappa;
  double fz3 = pow(fz, 3);
  double zr = fz3 > epsilon ? fz3 : (116.0 * fz - 16.0) / kappa;

  result->v[0] = xr * D65_Xref * 100 ;
  result->v[1] = yr * D65_Yref * 100;
  result->v[2] = zr * D65_Zref * 100;
}
