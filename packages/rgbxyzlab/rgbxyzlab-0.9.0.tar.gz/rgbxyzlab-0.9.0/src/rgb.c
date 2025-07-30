#include "vector3.h"
#include "lab.h"
#include "xyz.h"

void rgb_to_lab_p(Vector3 *in, Vector3 *result) {

  Vector3 tmp;

  rgb_to_xyz_p(in, &tmp);
  xyz_to_lab_p(&tmp, result);
}


void lab_to_rgb_p(Vector3 *in, Vector3 *result) {
  Vector3 tmp;

  lab_to_xyz_p(in, &tmp);
  xyz_to_rgb_p(&tmp, result);
}
