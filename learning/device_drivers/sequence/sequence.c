// sequence.c : a simple module to print a sequence of integer when its proc file is read
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

// sequence_start
//    - start a session and take a position, pos, as an argument
//    - pos is either 0 or the most recent pos used in the previous session
//    - return an iterator which will start reading at that position
static void *sequence_start( struct seq_file *s, loff_t *pos ) {
   // the current position. In most cases, we have to check for a 'past end of file' condition
   // and return NULL if need be.
   loff_t *spos = kmalloc( sizeof( loff_t ), GFP_KERNEL );
   if ( !spos ) return NULL;
   *spos = *pos;
   return spos;
}

// sequence_next
//    - move the iterator to the next position. I guess v is the previous position.
//    - also need to move pos to the new position that start() can use to find the new
//      location in the sequence
static void *sequence_next( struct seq_file *s, void *v, loff_t *pos ) {
   loff_t *spos = v;
   *pos = ++*spos;
   return spos;
}

// sequence_stop
//    - a place to clean up e.g. freeing memory or releasing lock
//    - the value of *pos set by the last next() call before stop() is passed to the first
//      start() call of the next session unless lseek() has been called on the file
//    - We can assume that the seq_file code will not sleep or acquire any lock between
//      start() and stop(). So it is ok to hold a lock.
static void sequence_stop( struct seq_file *s, void *v ) {
   kfree( v );
}

// sequence_show
//    - format the current object currently pointed to by the iterator for output
static int sequence_show( struct seq_file *s, void *v ) {
   loff_t *spos = v;
   seq_printf( s, "%lld\n", (long long)*spos );
   return 0;
}

static const struct seq_operations seq_file_ops = {
   .start   = sequence_start,
   .next    = sequence_next,
   .stop    = sequence_stop,
   .show    = sequence_show
};

static int proc_file_open( struct inode *inode, struct file *file ) {
   return seq_open( file, &seq_file_ops );
}

static const struct proc_ops proc_file_ops = {
   .proc_open     = proc_file_open,
   .proc_read     = seq_read,
   .proc_lseek    = seq_lseek,
   .proc_release  = seq_release
};

static int sequence_init( void ) {
   proc_create( "sequence", 0, NULL, &proc_file_ops );
   return 0;
}

static void sequence_exit( void ) {
   remove_proc_entry( "sequence", NULL );
}

module_init( sequence_init );
module_exit( sequence_exit );
