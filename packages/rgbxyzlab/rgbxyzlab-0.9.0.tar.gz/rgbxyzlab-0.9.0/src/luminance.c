#include <math.h>
#include <string.h>
#include <sys/param.h>  // for MAX and MIN
#include "vector3.h"

#define SQR(x) ((x)*(x))

/**
   rgb_to_luminance_sqr()
   Compute luminance = sqrt( 0.299 * R^2 + 0.587 *G^2 + 0.114*B^2 )
*/
double rgb_to_luminance_sqr(Vector3 *rgb) {
  return 0.299 * SQR(rgb->x) + 0.587 * SQR(rgb->y) + 0.114 * SQR(rgb->z);
}

/**
   rgb_to_luminance_sum()
   Compute luminance = 0.299 * R + 0.587 *G + 0.114*B
   A bit darker than rgb_to_luminance()
 */
double rgb_to_luminance_sum(Vector3 *rgb) {
  return 0.299 * rgb->x + 0.587 * rgb->y + 0.114 * rgb->z;
}

/**
   rgb_to_luminance_wcag()
   This calculation is used in contrast determination, see
   https://www.w3.org/TR/WCAG20-TECHS/G18.html
 */
double rgb_to_luminance_wcag(Vector3 *inp) {

  Vector3 rgb;
  memcpy(&rgb, inp, sizeof(Vector3));   /* Make a copy to work on */

  for(int i=0; i<3; i++) {
    if(rgb.v[i] <= 0.03928) {
      rgb.v[i] /= 12.92;
    } else {
      rgb.v[i] = pow((rgb.v[i] + 0.055) / 1.055, 2.4);
    }
  }
    return 0.2126 * rgb.x + 0.7152 * rgb.y + 0.0722 * rgb.z;
}

/**
   contrast_ratio()
   Calculate the contrast ratio of two colors.
   To properly distinguish two colors the contrast ratio should be
   equal to or greater than 4.5:1
*/
double contrast_ratio(Vector3 *lighter, Vector3 *darker) {
  // L1 is the relative luminance of the lighter of the two colors:
  double lum1 = rgb_to_luminance_wcag(lighter);
  // L2 is the relative luminance of the darker of the two colors:
  double lum2 = rgb_to_luminance_wcag(darker);
  double L1 = MAX(lum1, lum2);
  double L2 = MIN(lum1, lum2);
  return  (L1 + 0.05) / (L2 + 0.05);
}
