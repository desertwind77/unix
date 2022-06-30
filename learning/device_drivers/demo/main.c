#include <linux/init.h>       // module_init, module_exit
#include <linux/module.h>     // version info, MODULE_LICENSE, MODULE_AUTHOR, printk()
#include "demo_device.h"

MODULE_DESCRIPTION("Demo Linux device driver");
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Athichart Tangpong");

static int demo_init( void ) {
   int rc = 0;

   printk( KERN_NOTICE "%s\n", __func__ );
   rc = register_device();
   if( rc ) {
      printk( KERN_NOTICE "%s failed, error: %d\n", __func__, rc );
   }

   return rc;
}

static void demo_exit( void ) {
   printk( KERN_NOTICE "%s\n", __func__ );
   unregister_device();
}

module_init( demo_init );
module_exit( demo_exit );
