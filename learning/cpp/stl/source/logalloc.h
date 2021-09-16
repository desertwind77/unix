
#line 404 "ch24.w"
// Define an allocator adaptor that logs memory allocation and deallocation.

#line 407 "ch24.w"
#include <memory>
#include <iostream>
using namespace std; 

template <typename T, typename Allocator = allocator<T> >
class logging_allocator
{
private:
  Allocator alloc;

public:
  typedef typename Allocator::size_type size_type;
  typedef typename Allocator::difference_type difference_type;
  typedef typename Allocator::pointer pointer;
  typedef typename Allocator::const_pointer const_pointer;
  typedef typename Allocator::reference reference;
  typedef typename Allocator::const_reference const_reference;
  typedef typename Allocator::value_type value_type;
  template <typename U> struct rebind {
    typedef logging_allocator<U, 
          typename Allocator::template rebind<U>::other> other;
  };

  logging_allocator() {}
  logging_allocator(const logging_allocator& x)
    : alloc(x.alloc) {}
  template <typename U>
  logging_allocator(const logging_allocator<U, 
          typename Allocator::template rebind<U>::other>& x)
    : alloc(x.alloc) {}
  ~logging_allocator() {}
  
  pointer address(reference x) const {
    return alloc.address(x); 
  }
  const_pointer address(const_reference x) const { 
    return alloc.address(x); 
  }
  size_type max_size() const  { return alloc.max_size(); }
  void construct(pointer p, const value_type& val) { 
    alloc.construct(p, val);
  }
  void destroy(pointer p) { alloc.destroy(p); }
  
  pointer allocate(size_type n, const void* hint = 0) {
    ios::fmtflags flags = cerr.flags();

    cerr << "allocate(" << n << ", " 
         << hex << hint << dec << ") = ";
    pointer result = alloc.allocate(n, hint);
    cerr << hex << result << dec << endl;

    cerr.setf(flags);
    return result;
  }

  void deallocate(pointer p, size_type n) {
    ios::fmtflags flags = cerr.flags();

    cerr << "deallocate(" << hex << p << dec << ", "
         << n << ")" << endl;
    alloc.deallocate(p, n);

    cerr.setf(flags);
  }
};

template <typename T, typename Allocator1, 
          typename U, typename Allocator2>
bool operator==(const logging_allocator<T, Allocator1>& x,
                const logging_allocator<U, Allocator2>& y) {
  return x.alloc == y.alloc; 
}

template <typename T, typename Allocator1, 
          typename U, typename Allocator2>
bool operator!=(const logging_allocator<T, Allocator1>& x,
                const logging_allocator<U, Allocator2>& y) {
  return x.alloc != y.alloc; 
}
