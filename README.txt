== Sugar
== Bringing the pleasure back to JavaScript !

Sugar is a _new programming language_ designed to replace JavaScript
for client-side (and server-side) web development. Sugar is inspired by
languages such as Python, Smalltalk, Pascal, Eiffel and Lisp. Sugar can compile
to JavaScript, ActionScript and Python.

For the impatient, here is an example of Sugar's syntax:

>   @module helloworld
>   
>   @class HelloWorld
>   | This is a docstring for my hello world
>   
>       @property message
>   
>       @constructor
>           message = "Hello, World !"
>       @end
>   
>       @method say
>           alert ( message )
>       @end
>   
>   @end

Design goals
============

Sugar was designed with *software engineering in mind*, which means the core
values are _readability_, _maintainability_ and _expressivity_. While Sugar does
no forces you to use objects everywhere, it encourages you to use classes (yes,
sugar also has class-based inheritance) and focus on your program architecture.

Sugar design goals include:

 - Can be learned in a couple of days by average developers
 - Abstract from common JavaScript pitfalls
 - Minimize the differences in the code produced by different coders
 - Capture more information than other languages (be explicit)

Sugar owes the following languages in different areas:

 - Python, for the simplicity and cleanliness of the syntax
 - Eiffel, for the design by contract support
 - Smalltalk, for blocks
 - Io, for the message sending syntax
 - ML, for the pattern-matching syntax
 - Lisp, for the map/reduce/filter support
 
Installing sugar
================

Sugar is implemented in Python uses the [DParser](http://dparser.sf.net), and
relies on the [LambdaFactory](http://www.ivy.fr/lambdafactory) lirbary.

If you don't already have _dparser_, you should do the following:

>   cd Dependencies ; bash make-dparser.sh

and then copy the 'Dependencies/dparser' directory to somewhere in your
'PYTHONPATH'.

We're slowly getting away from DParser, as it has problems with 64 bits, and is
not flexible enough for the future of Sugar. In the meantime, please bear with
it ;)

Once you have DParser and LambdaFactory installed, simply type:

>   python setup.py install

And you'll have sugar install, and will have the 'sugar' command available in
your path.


# EOF - vim: syn=kiwi ts=2 sw=2 et
