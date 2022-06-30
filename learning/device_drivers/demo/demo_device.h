#ifndef __DEMO_DEVICE_H__
#define __DEMO_DEVICE_H__
#include <linux/compiler.h>         // __must_check

// #define __must_check __attribute__((warn_unused_result))
//
// The warn_unused_result attribute causes a warning to be emitted
// if a caller of the function with this attribute does not use its
// return value. This is useful for functions where not checking
// the result is either a security problem or always a bug,
// such as realloc.
__must_check int register_device(void);
void unregister_device(void);

#endif
