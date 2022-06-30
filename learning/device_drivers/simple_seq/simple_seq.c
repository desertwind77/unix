// simple_seq.c : a simple module to print a sequence of integer when its proc file is read
//
// Reference:
// https://www.kernel.org/doc/html/latest/filesystems/seq_file.html
// https://habr.com/en/post/444620/
// https://tldp.org/LDP/lkmpg/2.6/html/x861.html
#include <linux/init.h>
#include <linux/module.h>
#include <linux/proc_fs.h>       // for struct proc_dir_entry
#include <linux/seq_file.h>      // for struct seq_operations
#include <linux/slab.h>          // for kmalloc

MODULE_DESCRIPTION( "Demo of sequence file" );
MODULE_LICENSE( "GPL" );
MODULE_AUTHOR( "Athichart Tangpong" );

static int simple_proc_show( struct seq_file *m, void *v ) {
   seq_printf( m, "Hello World!\n" );
   return 0;
}

static int proc_file_open( struct inode *inode, struct file *file ) {
   return single_open( file, simple_proc_show, NULL );
}

static const struct proc_ops proc_file_ops = {
   .proc_open     = proc_file_open,
   .proc_read     = seq_read,
   .proc_lseek    = seq_lseek,
   .proc_release  = seq_release
};

static int sequence_init( void ) {
   proc_create( "simple_sequence", 0, NULL, &proc_file_ops );
   return 0;
}

static void sequence_exit( void ) {
   remove_proc_entry( "simple_sequence", NULL );
}

module_init( sequence_init );
module_exit( sequence_exit );
