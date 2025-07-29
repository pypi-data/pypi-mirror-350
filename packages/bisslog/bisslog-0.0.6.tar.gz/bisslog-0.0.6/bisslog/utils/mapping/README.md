# Mapping

The function of a mapper is to redirect the information to different key values or to combine this
information to create new fields.


## Objectives

- Reduce code volume in cases where data mapping is necessary.
- Create objects in a standardized way that is well known to developers.
- Perform mapping as efficiently as possible so as not to leave this responsibility on the
  developer.

## Usage

It is provided with a name to obtain an exact trace and a dictionary for the `base` which is what we
call **data map**.

~~~python
from bisslog.utils.mapping import Mapper

EXAMPLE_MAPPER = Mapper(name="Get identification information",
                        base={"field_1": "username", "field_3": "password"})

EXAMPLE_MAPPER.map({"field_1": "i_want_to_be_mapped", "field_2": "Carlos", "field_3": "123:3"})
~~~

It is also possible to gather several maps in a group that act as a single map.

~~~python
from bisslog.utils.mapping import MappingGroup

MappingGroup([EXAMPLE_MAPPER, ANOTHER_EXAMPLE_MAPPER])
~~~
