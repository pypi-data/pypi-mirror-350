## repeat_cons_n Function

## Overview
The repeat_cons_n function processes a given string s and arranges it into a matrix format based on the number of rows specified by numRows. The function then formats the matrix into a string with custom delimiters and separators, repeating the final output a specified number of times (epoch).


## Function Signature
```
def repeat_cons_n(s: str, numRows: int, delimiter: str, epoch: int, separator: str) -> str: 
```


## Parameters
•	s (str): The input string that will be arranged in the matrix.
•	numRows (int): The number of rows in the matrix.
•	delimiter (str): The string to be added between each row in the final result.
•	epoch (int): The number of times the final result string should be repeated.
•	separator (str): A string that will be appended at the end of the final result.


## Calling: 
```
import repcosn
from repcosn import repeat_cons_n as rpn 
```

## Functionality

# 1. Matrix Initialization:
o	Creates a matrix with numRows rows and columns based on the length of the string s.

# 2. Matrix Population:
o	Fills the matrix based on the provided string. Characters are distributed across rows, with special handling for the center row if numRows is odd, and for alternating rows if numRows is even.

# 3. Matrix to String Conversion:
o	Converts the matrix back into a string, joining the rows with the specified delimiter.

# 4. Final Output:
o	The result is repeated epoch times and appended with the separator.


## Example Usage
```
rpn(“Hello World”, 2, “->>”, 9, “”) ```

## Example Output
The function will output the processed string repeated 9 times, separated by the specified delimiter ("->>"), and appended with the separator at the end.


## Notes
•	Ensure that numRows is a positive integer. The function assumes valid inputs for simplicity.
•	The behavior for matrix filling and character placement varies depending on whether numRows is odd or even.
•	The function prints the result directly, it does not return it.


## Implementation Details
•	The function uses a matrix to arrange characters of the input string s.
•	Special handling is included for matrix rows based on the value of numRows.
•	Results are concatenated into a final string and printed.


## License
Free to use.

