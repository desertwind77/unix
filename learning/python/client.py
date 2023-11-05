#!/usr/bin/env python3
# To run this program, we need to run two servers
# ./server -p 1234
# ./server -p 5678

import errno
import select
import socket
import time

def other_task() -> None:
    '''This task mimics a CPU-intensive task.'''
    i = 0
    while i < 30:
        i += 1
        print( i )
        time.sleep( 0.02 )
        yield

def send_data_task( port, data ):
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    sock.connect( ( 'localhost', port ) )
    # Make this socket non-blocking so it will never wait for the operation to
    # complete.
    sock.setblocking( 0 )

    # Prepare the data to be sent
    data = ( data + '\n' ) * 1024 * 1024
    print( f'Bytes to send: {len( data )}' )

    total_sent = 0
    while len( data ):
        try:
            # Encode the string into a byte format before sending
            sent = sock.send( data.encode( 'utf-8' ) )
            total_sent += sent
            data = data[ sent: ]
            print( f'Sent: current = {sent} bytes, total = {total_sent} bytes' )
        except socket.error as e:
            if e.errno != errno.EAGAIN:
                raise e
            # The write buffer becomes full and an exception is raised. We can
            # not send any more data. Let's yield and let other tasks proceed.
            yield ( 'w', sock )

def main():
    tasks = [
        # This task mimics a CPU-intensive task
        other_task(),
        # These two tasks send a lot of data to two different TCP servers.
        send_data_task( port=12345, data='foo' ),
        send_data_task( port=56789, data='bar' )
    ]

    # Create a dictionary with two keys, namely 'w' and 'r'
    fds = dict( w={}, r={} )
    #while len( tasks ) != 0 or len( fds[ 'w' ] ) != 0 or len( fds[ 'r' ] ) != 0:
    while tasks or fds[ 'w' ] or fds[ 'r' ]:
        new_tasks = []
        for task in tasks:
            try:
                # TODO: understand yield, next, iter in Python
                resp = next( task )
                try:
                    iter( resp )
                    fds[ resp[ 0 ] ][ resp[ 1 ] ] = task
                except TypeError:
                    # This case is for other_task() because it yields without any
                    # parameter. The assignment in fds above will cause the TypeError
                    # exception. Let's add in back to the new_tasks list.
                    new_tasks.append( task )
            except StopIteration:
                # funciton completed
                pass

        if len( fds[ 'w' ].keys() ) != 0 or len( fds[ 'r' ].keys() ) != 0:
            # Every socket (really, every file descriptor that can be
            # select()ed on) has a list of waiters that are currently waiting
            # for activity on that socket (struct wait_queue_head_t in Linux
            # terminology). Whenever something interesting happens on that
            # socket (new data is available, buffer space is free for writing,
            # or some kind of error), that socket will walk its list and notify
            # everyone waiting on it.
            #
            # select() works by looping over the list of file descriptors that
            # the user passed in. For every file descriptor, it calls that fd's
            # poll() method, which will add the caller to that fd's wait queue,
            # and return which events (readable, writeable, exception)
            # currently apply to that fd.
            #
            # If any file descriptor matches the condition that the user was
            # looking for, select() will simply return immediately, after
            # updating the appropriate fd_sets that the user passed.
            #
            # If not, however, select() will go to sleep, for up to the maximum
            # timeout the user specified.
            #
            # If, during that interval, an interesting event happens to any
            # file descriptor that select() is waiting on, that fd will notify
            # its wait queue. That will cause the thread sleeping inside
            # select() to wake up, at which point it will repeat the above loop
            # and see which of the fd's are now ready to be returned to the
            # user.
            #
            # select() also keeps track of all of the wait queues it has been
            # added to, and before returning (successfully or otherwise), must
            # go through and ensure it's been removed from all of them.)
            readable, writeable, exceptional = \
                    select.select( fds[ 'r' ].keys(), fds[ 'w' ].keys(), [], 0 )
            for readable_sock in readable:
                new_tasks.append( fds[ 'r' ][ readable_sock ] )
                del fds[ 'r' ][ readable_sock ]
            for writeable_sock in writeable:
                new_tasks.append( fds[ 'w' ][ writeable_sock ] )
                del fds[ 'w' ][ writeable_sock ]
            # Ignore exceptional for now

        tasks = new_tasks

if __name__ == '__main__':
    main()
