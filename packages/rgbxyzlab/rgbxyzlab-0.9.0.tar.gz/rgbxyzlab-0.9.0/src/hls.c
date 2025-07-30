#include <math.h>
#include <sys/param.h>  // MAX, MIN
#include "vector3.h"
#define EPS 1e-9

/**
   rgb_to_hls_p() converts an RGB value to HLS color space.
 */
void rgb_to_hls_p(Vector3 *rgb, Vector3 *result) {

  double H, L, S;
  double tmp;

  double max = MAX(rgb->x, rgb->y);
  max = MAX(rgb->z, max);

  double min = MIN(rgb->x, rgb->y);
  min = MIN(rgb->z, min);

  double c = max - min;
  L = (max + min) / 2;

  if (max == min) {
    H = S = 0; // achromatic
    goto done;
  }

  if (c < EPS) { // Don't blow up here
    H = 0;
    goto calc_sat;
  }

  if (max == rgb->x) {
    // red is max

    H = fmod((rgb->y - rgb->z)/c, 6);
  } else if (max == rgb->y) {
    // green is max
    H = ((rgb->z - rgb->x) / c) + 2;

  } else if (max == rgb->z) {
    // blue is max

    H = ((rgb->x - rgb->y)/ c) + 4;
  } else {
    // should never happen
    H = 0;
  }

  H *= 60;
  H = H < 0 ? 360 + H : H;

 calc_sat:
  tmp = (1 - fabs(2 * L - 1));

  if (tmp < EPS) { // don't let this blow up
    S = 1.0;
  } else {
    S = c / tmp;
  }

 done:
  result->x = H;
  result->y = L;
  result->z = S;
}


/**
   hls_to_rgb_p() converts an HLS value to RGB color space.
 */
void hls_to_rgb_p(Vector3 *hls, Vector3 *result) {

  double H = hls->x;
  //double L = hls->y;
  //  double S = hls->z;

  double c = hls->z * (1 - fabs(2 * hls->y - 1));
  double m = (hls->y - 0.5 * c);
  double x = c * (1.0 - fabs(fmod(H / 60.0, 2) - 1.0));


  if (H >= 0.0 && H < 60.0) {
    result->x = c + m;
    result->y = x + m;
    result->z = m;

  } else if (H >= 60.0 && H < 120.0) {

    result->x = x + m;
    result->y = c + m;
    result->z = m;

  } else if (H >= 120.0 && H < 180.0) {

    result->x = m;
    result->y = c + m;
    result->z = x + m;

  } else if (H >= 180.0 && H < 240.0) {

    result->x = m;
    result->y = x + m;
    result->z = c + m;

  } else if (H >= 240.0 && H < 300.0) {

    result->x = x + m;
    result->y = m;
    result->z = c + m;

  } else if (H >= 300.0 && H < 360.0) {

    result->x = c + m;
    result->y = m;
    result->z = x + m;

  } else {

    result->x = m;
    result->y = m;
    result->z = m;
  }
}
