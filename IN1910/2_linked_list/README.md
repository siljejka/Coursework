# [H19_project2_jrevense_siljejka](https://github.uio.no/IN1910/H19_project2_jrevense_siljejka)

Assignment for IN1910 Fall 2019.

## Compilation commands used on the IFI machines:

### Part 1:

`g++ -std=c++11 -o al array_list.cpp`

### Part 2:

`g++ -std=c++11 -o ll linked_list.cpp`

### Part 3:

Singly linked circular list:

`g++ -std=c++11 -o cll circular_linked_list.cpp`

Doubly linked circular list:

`g++ -std=c++11 -o -cdll circular_doubly_linked_list.cpp`

## Part 1

Compiled and ran all excercises with tests.

While we were not asked to make a test function for this, we felt it was good practice in general, and for ourselves to do so. This test function tests all methods except print, the tests are done with preset numbers, we would have implemented them with random numbers if we had the time. We had to add a `cap()` method that returns the current `capacity` to test `resize()` and `shrink_to_fit()`.

## Part 2

Compiled and ran all excercises with tests.

We ran all the same tests as in Part 1, except the ones that had to do with resizing up or down.

## Part 3

### Get element *i* by index

##### `ArrayList`

The `if` check costs 3 boolean operations, and the fetching of the element is a single fetch of the *i*th element, from an array with *n* elements.

This means that it should execute in the same time, regardles off the value of *i*, thus this is an *&#x1D4AA;(1)* operation.

##### `LinkedList`

The `if` check costs 3 boolean operations, but the fetching of the element requires us to iterate through the elements until we reach the *i*th element.

This means that the fetch operation will have to execute *i* "jumps" from element to element, and then return the actual value of the element. This is an *&#x1D4AA;(N)* function, where the time it takes to execute is dependent on how deep into the linked list the element we wish to fetch is located.

### Insert

#### At front

##### `ArrayList`

Inserting at the front in an array with *n* elements requires us to move all the elements back one step, which means that this is an *&#x1D4AA;(N)* operation.

The `len` value is also increased by 1.

##### `LinkedList`

Inserting at the front of a linked list requires a heap memory assignment for the new node, the initialisation of the new node, the reassignment of the old `head`'s `last` value and finally reassigning the `head` to the new `head`. The `len` value is also increased by 1.


This makes it an *&#x1D4AA;(1)* operation.

#### At back

##### `ArrayList`

Inserting at the back of the arraylist is significantly easier, given that the array has enough space.

If the array has enough space it only has to increase the length of the list by 1, and assign a value to the new last element of the list, making this an *&#x1D4AA;(1)* operation.

If the array does not have enough space, it has to resize itself, meaning a new memory allocation on the heap, moving all the old values to the new memory addresses, deleting the old memory allocation, and finally increasing the list by 1 and assigning a value to the last element of the list.

Since moving each value from the old memory allocation to the new memory addresses takes at least one operation, the amount of operations required depends on however many values are stored in the arraylist, making this an *&#x1D4AA;(N)* operation.

Given that this can be both an *&#x1D4AA;(1)* operation, and an *&#x1D4AA;(N)* operation, it is important to point out when it will be either. It will be an *&#x1D4AA;(1)* operation far more often than it will be an *&#x1D4AA;(N)* operation, the *&#x1D4AA;(N)* operations only take place when the arraylist needs more space. The arraylist will need more space more often when it is smaller, but given it's growth factor of 2 this will drop significantly of as size grows.

The `len` value is also increased by 1.

##### `LinkedList`

Same as for the front of the list, but with the tail instead.

#### In middle

##### `ArrayList`

Inserting in the middle of the arraylist is similar to inserting at the front, except we don't have to move all the values of the array back, we only have to move the ones after the index we want to insert the value into.

This still makes it an *&#x1D4AA;(N)* operation though, as it will have to perform however many operations it requires to move all the values after the index we wish to insert into. The `len` value is also increased by 1.

##### `LinkedList`

Inserting into the middle of the linked list is similar to inserting at the front/back, except we don't have to reassign the `head`/tail.

It requires a heap memory assignment for the new node, the initialisation of the new node(with pointers to the elements at either end of it's insertion location), reassigning the preceding element's `next` pointer to the new element, and lastly the proceeding element's `last` pointer to the new element. The `len` value is also increased by 1.

### Remove element

#### From front

##### `ArrayList`

This is very similar to inserting an element in the front of an array, but simply in reverse. Remove the first element, and move every element after up 1 index. The `len` value is also reduced by 1.

Thus this is also an *&#x1D4AA;(N)* operation.

In the case that the `len` of our current list is reduced below 25% of the `capacity`, we automatically do a shrinking operation on the arraylist. This means we find the lowest possible value for `capacity` where `capacity`= `growth_factor`<sup>*N* </sup>, that will fit the `len` of our current arraylist, and move the elements into a new array of that capacity.

##### `LinkedList`

Removing an element from the front of the linked list means setting the `head` to be the second element of the list, setting the (now new) `head`'s `last` value to a `nullptr`, and finally deleting the "old" `head`. The `len` value is also reduced by 1.

This makes it an *&#x1D4AA;(1)* operation.

#### From back

##### `ArrayList`

Removing an element from the back of the arraylist is very simple, the `len` value is just reduced by 1.<sup>[1](#footnote1)</sup>

This will make it an *&#x1D4AA;(1)* operation, however if the shrinking operation mentioned earlier is incurred it can be an *&#x1D4AA;(N)* operation, since it will take however many moves of the elements the shrinking requires.


##### `LinkedList`

This is the same as removing from the front, but using the tail instead, and setting the "new" `tail`'s `next` to a `nullptr`. The `len` value is also reduced by 1.

Like removing from the front, this is an *&#x1D4AA;(1)* operation.

#### From middle

##### `ArrayList`

Removing from the middle of an arraylist is actually very similar to inserting in the middle, but instead of moving all the elements after<sup>[2](#footnote2)</sup> the index we're moving into up one index, we just move every element after the index we're removing from, down one index.
The `len` value is also reduced by 1.<sup>[3](#footnote3)</sup>

This is an *&#x1D4AA;(N)* operation.

##### `LinkedList`

Removing from the middle of a linked list is quite simple, if we're going to delete element *n*, we set element *n-1*'s `next` to element *n+1*, and element *n+1*'s `last` to element *n-1*, delete element *n*, and reduce the `len` value by 1.

At first glance this might seem like an *&#x1D4AA;(1)* operation, but it isn't. To get to element *n*, we have to traverse the list from the `head` to element *n*, making it an *&#x1D4AA;(N)* operation.

### Print

##### `ArrayList`

Printing an arraylist goes through the values from *0* to *n*, and outputs them to the terminal, thus it is an *&#x1D4AA;(N)* operation.

##### `LinkedList`

To print a linked list it has to be traversed from `head` to `tail`, and the node values output to terminal during traversal, making it an *&#x1D4AA;(N)* operation.


## Part 4

Compiled and ran all excercises with tests.

We implemented this in two different ways, first with a singly linked circular list in `circular_linked_list`, as this seemed to match what the task asked. We also implemented a doubly linked circular list in `circular_doubly_linked_list`, this was done mostly out of curiosity.

In the Numberphile video they always kill the person to the left, we wanted to implement a way to change this direction, and to see if we could make this work.

In both implementations we ended up with several interesting issues as we implemented the `josephus_sequence`.

Firstly we had to add an `if` statement in the destructor for the case `len==1`, since our early implementations of `josephus_sequence` deleted every node but the survivor node, but this caused our `while` loop in the destructor to run forever since the link between the `head` and `tail` nodes had been disconnected and our `while` loop runs while `index != tail`.

Later we changed it so that we had an `if (len==0)` statement too, since we changed our `josephus_sequence` to also delete the survivor node. This was just a `return` statement, to ensure none of the other cases ran. We also added a `return` statement to `if (len==1)` for the same reason.

When we had a functioning `josephus_sequence` implementation, we decided to test it to make sure we got the right answers. We used [this calculator](http://webspace.ship.edu/deensley/mathdl/Joseph.html) we found online, and found our implementation to be returning the wrong survivor. This caused us to examine how we counted with *k*, but until not after we had spent quite some time looking for the problem elsewhere in our code. We found the right way to count with *k* when we saw that the online calculator killed every second person for *k=2*, while we had assumed that this would be the case with *k=1*.

We used the online calculator to make a list of expected winners for different values of *n* and *k*, then we made a test function `expected_values_test`, that checked our implementation for these values.

In the doubly linked implementation, we had to manually solve some cases of the *Josephus problem* to ensure our implementation was correct, in these cases we printed out the victims as they were brutally murdered by their comrades, and compared it to our manual calculation.

In the Numberphile video, they give us an algebraic solution for *Josephus(n,2)*, which we chose to make a test out of. Firstly we made a function implementing this algebraic solution called `josephus_expected(n)`, then we made a test called `randomised_values_test(N)` which compared the results of `josephus_expected(n)` and `last_man_standing(n,2)`, for random values *n* between *1* and *200*, *N* times. We made sure that we had different random values for *n* each run, by setting our `srand` seed with the current UNIX timestamp.



#### Task 4g)

In the case of *Josephus(68,7)* you'd want to stand in the last position, position 68, to survive.

### Footnotes
<a name="footnote1">1</a>: This might seem like we're not removing the value, but for all intents and purposes it is in this case. This is easier to see through an example:

Say we have an arraylist with a capacity of 8, we don't really care what values we put in, so we're going to use red apples &#x1F34E;, to illustrate which memory locations we are not currently allowed to access:

[&#x1F34E;,&#x1F34E;,&#x1F34E;,&#x1F34E;,&#x1F34E;,&#x1F34E;,&#x1F34E;,&#x1F34E;]

We fill this array by appending 6 green apples &#x1F34F;, which we can access and have designated a value to:

[&#x1F34F;,&#x1F34F;,&#x1F34F;,&#x1F34F;,&#x1F34F;,&#x1F34F;,&#x1F34E;,&#x1F34E;]

The way we have designed our class, the `len` value decides how many apples we can access, in this case `len` is 6, since we appended 6 &#x1F34F;.

Now if we decide to reduce `len` to 5, the last &#x1F34F; will turn into a &#x1F351;, the &#x1F351; is a value we have set with a &#x1F34F; but which we can no longer access due to the value of `len`, which gives us:

[&#x1F34F;,&#x1F34F;,&#x1F34F;,&#x1F34F;,&#x1F34F;,&#x1F351;,&#x1F34E;,&#x1F34E;]

While the actual value we stored in the last position before removing it is still written to that memory location, we do not need to spend operations on deleting or overwriting it, as it is for all intents and purposes inaccessible to us, and does not consume any extra memory.

(I could not find an easy way to colour text in Github Markdown, so emojis.)


<a name="footnote2">2</a>: And including the index we're inserting into, in the case of insertion.

<a name="footnote3">3</a>: See removing from the front, and it's footnote (<sup>[1](#footnote1)</sup>), if you're concerned about what happens to the last element of the list.
