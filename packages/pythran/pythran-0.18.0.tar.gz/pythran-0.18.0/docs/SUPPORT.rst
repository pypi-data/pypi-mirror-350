===============================
Supported Modules and Functions
===============================

bisect
******

bisect
bisect_left
bisect_right

builtins
********

ArithmeticError
AssertionError
AttributeError
BaseException
BufferError
BytesWarning
DeprecationWarning
EOFError
EnvironmentError
False
FloatingPointError
FutureWarning
GeneratorExit
IOError
ImportError
ImportWarning
IndentationError
IndexError
KeyError
KeyboardInterrupt
LookupError
MemoryError
NameError
None
NotImplementedError
OSError
OverflowError
PendingDeprecationWarning
ReferenceError
RuntimeError
RuntimeWarning
StopIteration
SyntaxError
SyntaxWarning
SystemError
SystemExit
TabError
True
TypeError
UnboundLocalError
UnicodeError
UnicodeWarning
UserWarning
ValueError
Warning
ZeroDivisionError
abs
all
any
bin
bool
chr
divmod
enumerate
filter
getattr
hex
id
int
isinstance
iter
len
map
max
min
next
oct
open
ord
pow
print
range
reduce
reversed
round
sorted
sum
tuple
type
zip

Exception
---------

args
errno
filename
strerror


complex
-------

conjugate
imag
real


dict
----

clear
copy
fromkeys
get
items
keys
pop
popitem
setdefault
update
values


float
-----

is_integer


list
----

append
clear
count
extend
insert
pop
remove
reverse
sort


pythran
-------

StaticIfBreak
StaticIfCont
StaticIfNoReturn
StaticIfReturn
abssqr
is_none
kwonly
len_set
make_shape
static_if
static_list


set
---

add
clear
copy
difference
difference_update
discard
intersection
intersection_update
isdisjoint
issubset
issuperset
remove
symmetric_difference
symmetric_difference_update
union
update


slice
-----

start
step
stop


str
---

__mod__
capitalize
count
endswith
find
isalpha
isdigit
join
lower
lstrip
replace
rstrip
split
startswith
strip
upper


cmath
*****

cos
e
exp
isnan
log10
pi
sin
sqrt

functools
*********

partial
reduce

io
**


_io
---


TextIOWrapper
+++++++++++++

close
closed
fileno
flush
isatty
mode
name
newlines
next
read
readline
readlines
seek
tell
truncate
write
writelines



itertools
*********

combinations
count
islice
permutations
product
repeat

math
****

acos
acosh
asin
asinh
atan
atan2
atanh
ceil
cos
cosh
degrees
e
erf
erfc
exp
expm1
fabs
factorial
floor
fmod
frexp
gamma
hypot
isinf
isnan
ldexp
lgamma
log
log10
log1p
modf
pi
pow
radians
sin
sinh
sqrt
tan
tanh
trunc

copysign
--------

accumulate


numpy
*****

Inf
NINF
abs
absolute
all
allclose
alltrue
amax
amin
angle
any
append
arange
arccos
arccosh
arcsin
arcsinh
arctan
arctanh
argmax
argmin
argsort
argwhere
around
array
array2string
array_equal
array_equiv
array_split
array_str
asarray
asarray_chkfinite
ascontiguousarray
asfarray
atleast_1d
atleast_2d
atleast_3d
average
base_repr
binary_repr
bincount
bitwise_not
bool
broadcast_to
byte
cbrt
ceil
clip
complex128
complex256
complex64
concatenate
conj
conjugate
convolve
copy
copyto
correlate
cos
cosh
count_nonzero
cross
cumprod
cumproduct
cumsum
deg2rad
degrees
delete
diag
diagflat
diagonal
diff
digitize
dot
double
e
ediff1d
empty
empty_like
exp
expand_dims
expm1
eye
fabs
fill_diagonal
fix
flatnonzero
flip
fliplr
flipud
float128
float32
float64
floor
frexp
fromfile
fromfunction
fromiter
fromstring
full
full_like
hstack
identity
imag
indices
inf
inner
insert
int16
int32
int64
int8
intc
interp
intersect1d
intp
invert
isclose
iscomplex
isfinite
isinf
isnan
isneginf
isposinf
isreal
isrealobj
isscalar
issctype
lexsort
linspace
log
log10
log1p
log2
logical_not
logspace
longlong
max
mean
median
min
nan
nan_to_num
nanargmax
nanargmin
nanmax
nanmin
nansum
ndenumerate
ndim
ndindex
negative
newaxis
nonzero
ones
ones_like
outer
pi
place
prod
product
ptp
put
putmask
rad2deg
radians
ravel
real
reciprocal
repeat
resize
rint
roll
rollaxis
rot90
round
round
searchsorted
select
setdiff1d
shape
short
sign
signbit
sin
sinh
size
sometrue
sort
sort_complex
spacing
split
sqrt
square
stack
std
sum
swapaxes
take
tan
tanh
tile
trace
transpose
tri
tril
trim_zeros
triu
trunc
ubyte
uint16
uint32
uint64
uint8
uintc
uintp
ulonglong
union1d
unique
unravel_index
unwrap
ushort
var
vdot
vectorize
vstack
where
zeros
zeros_like

add
---

accumulate
reduce


arctan2
-------

accumulate


bitwise_and
-----------

accumulate
reduce


bitwise_or
----------

accumulate
reduce


bitwise_xor
-----------

accumulate
reduce


copysign
--------

accumulate


ctypeslib
---------

as_array


divide
------

accumulate


dtype
-----

type


equal
-----

accumulate


fft
---

fft
fftn
hfft
ifft
ihfft
irfft
rfft


finfo
-----

eps


floor_divide
------------

accumulate


fmax
----

accumulate
reduce


fmin
----

accumulate
reduce


fmod
----

accumulate


greater
-------

accumulate


greater_equal
-------------

accumulate


heaviside
---------

accumulate


hypot
-----

accumulate


ldexp
-----

accumulate


left_shift
----------

accumulate


less
----

accumulate


less_equal
----------

accumulate


linalg
------

matrix_power
norm


logaddexp
---------

accumulate


logaddexp2
----------

accumulate


logical_and
-----------

accumulate


logical_or
----------

accumulate


logical_xor
-----------

accumulate


maximum
-------

accumulate
reduce


minimum
-------

accumulate
reduce


mod
---

accumulate


multiply
--------

accumulate
reduce


ndarray
-------

T
astype
dtype
fill
flat
flatten
item
itemsize
nbytes
ndim
reshape
shape
size
sort
strides
tofile
tolist
tostring
view


nextafter
---------

accumulate


not_equal
---------

accumulate


power
-----

accumulate


random
------

binomial
bytes
chisquare
choice
dirichlet
exponential
f
gamma
geometric
gumbel
laplace
logistic
lognormal
logseries
negative_binomial
normal
pareto
poisson
power
rand
randint
randn
random
random_integers
random_sample
ranf
rayleigh
sample
seed
shuffle
standard_exponential
standard_gamma
standard_normal
uniform
weibull


remainder
---------

accumulate


right_shift
-----------

accumulate


subtract
--------

accumulate


true_divide
-----------

accumulate


omp
***

destroy_lock
destroy_nest_lock
get_active_level
get_ancestor_thread_num
get_dynamic
get_level
get_max_active_levels
get_max_threads
get_nested
get_num_procs
get_num_threads
get_schedule
get_team_size
get_thread_limit
get_thread_num
get_wtick
get_wtime
in_final
in_parallel
init_lock
init_nest_lock
set_dynamic
set_lock
set_max_active_levels
set_nest_lock
set_nested
set_num_threads
set_schedule
test_lock
test_nest_lock
unset_lock
unset_nest_lock

operator
********

__abs__
__add__
__and__
__concat__
__contains__
__delitem__
__eq__
__floordiv__
__ge__
__getitem__
__gt__
__iadd__
__iand__
__iconcat__
__ifloordiv__
__ilshift__
__imatmul__
__imod__
__imul__
__inv__
__invert__
__ior__
__ipow__
__irshift__
__isub__
__itruediv__
__ixor__
__le__
__lshift__
__lt__
__matmul__
__mod__
__mul__
__ne__
__neg__
__not__
__or__
__pos__
__rshift__
__sub__
__theitemgetter__
__truediv__
__xor__
abs
add
and
concat
contains
countOf
delitem
eq
floordiv
ge
getitem
gt
iadd
iand
iconcat
ifloordiv
ilshift
imatmul
imod
imul
indexOf
inv
invert
ior
ipow
irshift
is
is_not
isub
itemgetter
itruediv
ixor
le
lshift
lt
matmul
mod
mul
ne
neg
not
or
pos
rshift
sub
truediv
truth
xor

os
**


path
----

join


random
******

choice
expovariate
gauss
randint
random
randrange
sample
seed
shuffle
uniform

scipy
*****


special
-------

binom
gamma
gammaln
i0
i0e
ndtr
ndtri

gammaincinv
+++++++++++

accumulate


hankel1
+++++++

accumulate


hankel2
+++++++

accumulate


iv
++

accumulate


ivp
+++

accumulate


jv
++

accumulate


jvp
+++

accumulate


kv
++

accumulate


kvp
+++

accumulate


spherical_jn
++++++++++++

accumulate


spherical_yn
++++++++++++

accumulate


yv
++

accumulate


yvp
+++

accumulate



string
******

ascii_letters
ascii_lowercase
ascii_uppercase
digits
hexdigits
octdigits

time
****

sleep
time
