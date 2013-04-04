## import bson
## from bson import _element_to_dict


## def _patched_elements_to_dict(data, as_class, tz_aware, uuid_subtype):
##     result = as_class()
##     position = 0
##     end = len(data) - 1
##     while position < end:
##         (key, value, position) = _element_to_dict(data, position, as_class,
##                                                   tz_aware, uuid_subtype)
##         result[key] = value

##     # IMPORTANT: we use below patch to deserialize each document after fetch
##     print "><><><>> ", type(result), hasattr(result, "deserialize")
##     if hasattr(result, "deserialize"):
##         print "!11111" * 100
##         result.deserialize()
##     return result

## print "here"
## _patched_elements_to_dict.color = True
## bson._elements_to_dict = _patched_elements_to_dict
