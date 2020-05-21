# The ATE.org STDF library

## Introduction

#### This library is NOT intended to be the 'fastes in the world'! 

Often people are searching for 'the fastest' STDF parser. If this is what you are after, keep on looking and by all means, hit the wall later on, and at that point you might consider to return! 🤣

Ok, a `fast` parser is first of all writen in probably [C](https://en.wikipedia.org/wiki/C_(programming_language))/[++](https://en.wikipedia.org/wiki/C%2B%2B), and it has to dispence of a lot of the checking/correcting in order to become realy fast. However in real life STDF files are **far from perfect**, meaning that fast parsers will **FAIL** to do their intended job!

In any case, when you start parsing STDF's **at the moment** you want to interact with the data, you are, as they say *too little too late* ... you must still be living in the last century (not to say last milenium Millennium 🤪)

A `good` parser is written in a higher level language (like [Python](https://www.python.org/)) and it does an awefull lot of checking (and if needed correcting) to return with meaningfull and correct data. This of course makes it slower. One can optimize that a bit by using [Cython](https://cython.org/) or maybe [numba](http://numba.pydata.org/) but that is besides the point.

The point is that STDF data should be converted to a useable format like [pandas](https://pandas.pydata.org/) ([numpy](https://numpy.org/) alone will not do as plenty of data is not numerical) **WHILE** the data is generated!

Think of it like this: STDF is a very good format from the point of view of the ATE, because if a test program is crashing, we lost virtually no data! STDF is an un-usable format from the point of view of data analysis! Therefore we need to convert the data to a format that usable. (if now you are thinking '[SQL](https://en.wikipedia.org/wiki/SQL)', then I can confirm that either you are still living in last millennium or you are a die-hard masochist! 🧐)   

#### It is also <ins>not</ins> set up as just a parser!

In ATE.org we also need to **write** STDF files!


## Support
 - Endians: Little & Big
 - Versions & Extensions:
   - ~~V3~~
   - V4
     - [standard](/docs/standards/STDF/STDF-V4-spec.pdf)
     - [V4-2007](/docs/standards/STDF/STDF-V4-2007-spec.pdf)
     - [Memory:2010.1]()
 - Modes: read & write
 - compressions:
   - [gzip](https://www.gnu.org/software/gzip/)
   - [lzma](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Markov_chain_algorithm) (*.xz extension) → turns out to be the best to compress STDF files.
   - [bz2](https://www.sourceware.org/bzip2/)


