#include <linux/cdev.h>       // character device
#include <linux/errno.h>
#include <linux/fs.h>         // struct file_operations
#include <linux/kernel.h>     // printk()
#include <linux/module.h>     // THIS_MODULE
#include <linux/uaccess.h>    // copy_to_user()

static int major_device_number = 0;
static const char device_name[] = "demo";
static const char message[] = "Demo Linux device driver\n\0";
static const ssize_t msg_size = sizeof( message );

static ssize_t demo_read( struct file *file_ptr, char __user *buffer,
                          size_t count, loff_t *pos ) {
   // file_ptr : the information about the file we are working with
   // buffer   : user space buffer to read to
   // count    : number of bytes to read to
   // pos      : the starting offset to start read from
   //
   // The goal of this function is to get the value of the string message.
   // But the user space cannot just access the string message because
   // this pointer is in the kernel space. Then we have to copy the value from
   // the kernel space to the user space using copy_to_user(). This function
   // return the number of bytes copied on success; otherwise, 0.
   //
   // long copy_to_user( void __user *to, const void * from, unsigned long n );
   printk( KERN_NOTICE "demo: %s offset: %i, count: %u\n", __func__,
           (int)*pos, (unsigned int)count );

   if ( *pos >= msg_size ) return 0;
   if ( *pos + count > msg_size ) {
      count = msg_size - *pos;
   }

   if ( copy_to_user( buffer, message + *pos, count ) != 0 ) {
      return -EFAULT;
   }

   *pos += count;
   return count;
}

static struct file_operations file_fops = {
   .owner = THIS_MODULE,
   .read = demo_read,
};

// register a character device
// return 0 if success
int register_device(void) {
   int rc = 0;

   // int register_chrdev( unsigned int major, const char *name,
   //                      const struct file_operations *fops );
   //    major = 0 means let the kernel select the major device number
   //    this function will return 0 on success otherwise an error code
   rc = register_chrdev( 0, device_name, &file_fops );
   if ( rc < 0 ) {
      // The printk function forms a string, which we add to the circular buffer.
      // From there the klog daemon reads it and sends it to the system log.
      // Implementing the printk allows us to call this function from any point in
      // the kernel. Use this function carefully, as it may cause overflow of the
      // circular buffer, meaning the oldest message will not be logged.
      //
      // options for printk are KERN_DEBUG, KERN_NOTICE, KERN_WARNING, KERN_EMERG 
      printk( KERN_WARNING "demo: %s unable to register char device, error: %i\n",
              __func__, rc );
      return rc;
   }

   major_device_number = rc;
   printk( KERN_NOTICE "demo: %s major_device_number: %i\n",
           __func__, major_device_number );

   return 0;
}

void unregister_device(void) {
   if ( major_device_number != 0 ) {
      printk( KERN_NOTICE "demo: %s major_device_number: %i\n",
              __func__, major_device_number );
      unregister_chrdev( major_device_number, device_name );
   }
}
