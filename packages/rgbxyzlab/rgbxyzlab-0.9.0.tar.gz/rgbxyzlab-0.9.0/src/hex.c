#include <string.h>
#include <stdlib.h>
#include "vector3.h"
#include "hex.h"

/**
   check_hexstr() is a function to check the validity of a hexcode string.
   Accepts 6 or 3 digit codes of the form '#abcdef' or '#abc'. Three
   digit codes are expanded to six digit ones before return.
   */
int check_hexstr(const char *s, char result[8]) {
  static char *valid_hex = "0123456789abcdefABCDEF";


  if (s[0] != '#') {
    result[0] = '\0';
    return NO_HASH;
  }

  size_t n = strspn(s+1, valid_hex);

  switch (n) {

  case 3:
    // 3 digit hexcode, expand to six
    result[0] = '#';
    result[1] = result[2] = *(s+1);
    result[3] = result[4] = *(s+2);
    result[5] = result[6] = *(s+3);
    return OK;

  case 6:
    // 6 digit hexcode
    strncpy(result, s, 7);
    return OK;

  default:
    // not a hexcode
      result[0] = '\0';
      return NOT_HEX;

  }

  // some other error, catch-all
  result[0] = '\0';
  return ERROR;
}


/**
   char_to_dec() converts a single hexadecimal digit to an integer
   value.
  */
static int char_to_dec(char c) {
  if (c>='0' && c<='9') return c-'0';
  if (c>='a' && c<='f') return c-'a'+10;
  if (c>='A' && c<='F') return c-'A'+10;
  return 0;
}


/**
   two_hex_2_digits_to_int() converts a two character input string of
   the type 'ff' or '03' to integer value. It *must* receive exactly
   two digits, but that is also the case for the hex codes we are
   working with, they are of the form '#abcdef'.
    */
static int two_hex_digits_to_int(const char input[2]) {
  // requires exactly 2 characters

  int d = 0;

  d = char_to_dec(input[1]);
  d = d + char_to_dec(input[0]) * 16;

  return d;
  }

/**
   hexcode_to_rgb_triple() takes a hexcode of the form
   '#abcdef' and returns and rgb triple with components in range
   [0:1].
 */

void hexcode_to_rgb_triple(char input[8], Vector3 *rgb) {
  char digits[2];

  digits[0] = input[1];
  digits[1] = input[2];
  rgb->x = (double)two_hex_digits_to_int(digits) / 255.0;
  digits[0] = input[3];
  digits[1] = input[4];
  rgb->y = (double)two_hex_digits_to_int(digits) / 255.0;
  digits[0] = input[5];
  digits[1] = input[6];
  rgb->z = (double)two_hex_digits_to_int(digits) / 255.0;
}


/**
   int_to_hexstr() converts a positive decimal number to a string with
   its hexadecimal representation. Be careful that there is enough
   space in result, it has to fit the number of digits in the
   hexadecimal number. Supply a result array of size no larger than 16
   which is the size of the internal array hex_str[].
*/
static void int_to_hexstr(int num, char *result, size_t siz)
{
  char hexstr[16];  // temp storage of (reversed) hex number

  int k = 0;
  int n = num;

  // Initialize hexstr because memory location may be reused between
  // function calls, and this function doesn't work if it isn't.
  memset(hexstr, '0', 16);

  while (n != 0) {

    int rem = 0;
    char ch;
    rem = n % 16;

    if (rem < 10) {
      ch = rem + 48;
    }
    else {
      ch = rem + 87;
    }

    hexstr[k]= ch;
    k++;
    n = n / 16;
  }

  // If number < 16 set leading '0'
  if (num < 16) {
    hexstr[++k] = '0';
  }

  // If number is zero set leading '0'
  if (num == 0) {
    result[1] = '0';
  }

  // Reverse hexstr and save in result
  int i = 0, j = k-1;
  while( j >= 0) {
      result[i++] = hexstr[j--];
  }
}


/**
   convert_rgb_triple_to_hexcode() converts an RGB triple to hexcode.
 */
void rgb_triple_to_hexcode(Vector3 *rgb, char result[8]) {

  int R = 255 * rgb->x;
  int G = 255 * rgb->y;
  int B = 255 * rgb->z;
  result[0] = '#';
  int_to_hexstr(abs(R), &result[1], 2); // 1, 2
  int_to_hexstr(abs(G), &result[3], 2); // 3, 4
  int_to_hexstr(abs(B), &result[5], 2); // 5, 6
  result[7] = '\0';

}
