/*
    This file is a part of libmox, a utility library.
    Copyright (C) 1995-2007 Morten Kjeldgaard

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public License
    as published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

/** @file hsv.c
   @brief Routines to manipulate hsv colors
   @author Morten Kjeldgaard
*/

#include "vector3.h"
#define EPS 10e-9

/**
   hsv_to_rgb_p()
  Translate a colour given in hue, saturation and value (intensity) as
  given by the PS300 into an (R,G,B) triplet.  See Foley & Van Dam
  p. 615.  First version, in Fortran, 11-May-1990 Morten Kjeldgaard
  - Converted from FORTRAN to to C 991104.
  - 2025-05-22 Conversion formula converted since PS300 HSV was 120 out of phase
    with current definition.
*/
void hsv_to_rgb_p (Vector3 *hsv, Vector3 *rgb)
{
  double r, g, b, hue, sat, val;

  r = g = b = 0.0;
  hue = hsv->x; sat = hsv->y; val = hsv->z;

  if (sat < EPS) {
   rgb->x = val;
   rgb->y = val;
   rgb->z = val;
   return;
  }

  if (hue < 0.0) hue = hue + 360.0;
  if (hue >= 360.0) hue = hue - 360.0;

  hue = hue / 60.0;

  int i = hue;
  double f = hue - (float)i;
  double p = val * (1.0 - sat);
  double q = val * (1.0 - (sat * f));
  double t = val * (1.0 - (sat * (1.0 - f)));

  switch (i) {
  case 0:
    r = val; g = t; b = p;
    break;
  case 1:
    r = q; g = val; b = p;
    break;
  case 2:
    r = p; g = val; b = t;
    break;
  case 3:
    r = p; g = q; b = val;
    break;
  case 4:
    r = t; g = p; b = val;
    break;
  case 5:
    r = val; g = p; b = q;
  }

  rgb->x = r;
  rgb->y = g;
  rgb->z = b;
  return;
}

/**
   rgb_to_hsv_p()
   Translate a colour given in the (R,G,B) triplet into hue, saturation,
  and value (intensity) as required by the PS300.  See Foley & Van Dam
  p. 615. 10-May-1990 Morten Kjeldgaard. Written in Dallas.
  - Converted from FORTRAN to C 991104.
  - 2025-05-22 Conversion formula converted since PS300 HSV was 120 out of phase
    with current definition.
*/
void rgb_to_hsv_p (Vector3 *rgb, Vector3 *hsv)
{
  double r, g, b;
  double rc, gc, bc;

  double hue = 0.0;
  double sat = 0.0;
  r = rgb->x; g = rgb->y; b = rgb->z;

  double rgbmax = (r > g ? r : g); rgbmax = (rgbmax > b ? rgbmax : b);
  double rgbmin = (r < g ? r : g); rgbmin = (rgbmin < b ? rgbmin : b);
  double delta = rgbmax - rgbmin;
  double val = rgbmax;

  /* All components are zero (black) */
  if (rgbmax < EPS) {
    hsv->x = 0.0;
    hsv->y = 0.0;
    hsv->z = 0.0;
    return;
  }

  sat = (rgbmax - rgbmin) / rgbmax;

  if (sat < EPS) {
    hsv->x = 0.0;
    hsv->y = 0.0;
    hsv->z = val;
    return;
  }

  /* rc measures the distance of color from red */
  rc = (rgbmax - r) / delta;
  gc = (rgbmax - g) / delta;
  bc = (rgbmax - b) / delta;

  if (r == rgbmax)
    /* resulting color between yellow and magenta */
    hue = bc - gc;
  else if (g == rgbmax)
    /* resulting color between cyan and yellow */
    hue = 2.0 + rc - bc;
  else if (b == rgbmax)
    /* resulting color between magenta and cyan */
    hue = 4.0 + gc - rc;

  /* convert to degrees */
  hue = hue * 60.0;; // + 120.0;
  if (hue < 0.0) hue = hue + 360.0;
  if (hue > 360.0) hue = hue - 360.0;

  hsv->x = hue;
  hsv->y = sat;
  hsv->z = val;
  return;
}
