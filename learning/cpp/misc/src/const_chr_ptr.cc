// const keyword applies to whatever is immediately to its left. If there is
// nothing to its left, it applies to whatever is immediately to its right.
//
// const char *ptr         : a non-constant ponter to a constant character
// char *const ptr         : a const pointer to a non-constant character
// const char *const ptr   : a const pointer to a const character
//
// https://www.geeksforgeeks.org/difference-const-char-p-char-const-p-const-char-const-p/
//
#include<stdio.h>
#include<stdlib.h>

int main() {
   char a ='A', b ='B';
   const char *ptr1 = &a;
   char *const ptr2 = &a;
   const char *const ptr3 = &a;

   printf( "ptr1 = %ul, *ptr1 = %c\n", ptr1, *ptr1 );
   // *ptr = b;   // illegal because ptr1 is a non-const pointer to a const char
   ptr1 = &b;     // legal because ptr1 is a non-const pointer to a const char
   printf( "ptr1 = %ul, *ptr1 = %c\n", ptr1, *ptr1 );

   printf( "ptr2 = %ul, *ptr2 = %c\n", ptr2, *ptr2 );
   // ptr2 = &b;  // illegal because ptr2 is a const pointer to a non-const char
   *ptr2 = b;     // legal because ptr2 is a const pointer to a non-const char
   printf( "ptr2 = %ul, *ptr2 = %c\n", ptr2, *ptr2 );

   printf( "ptr3 = %ul, *ptr3 = %c\n", ptr3, *ptr3 );
   // ptr3 = &b;  // illegal because ptr3 is a const pointer to a const char
   // *ptr3 = b;  // illegal because ptr3 is a const pointer to a const char

	return 0;
}
