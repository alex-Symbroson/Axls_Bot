
    # use ast to prevent evil stuff
from ast import literal_eval

    # calculate int from string via literal_eval
def toInt(s):
        # convert to lower case to allow things like "Abs" or "SQRT"
    try: return ast.literal_eval(s.lower())
    except ZeroDivisionError:
        return 'Division by 0!'
    except: return 'Error!'
