# TCQi Library

---

This library is intended to facilitate the modification of TCQi files,
unpacking and saving the tables in Excel and/or DataFrame format, and the resulting
compression and saved in TCQi format, when finished.

---

## Structure

To use this library, you must create "Data" and "Output" folders in the project directory:

```
project-tcqi/
-Data/
--file.tcqi
-Output/
--file.xlsx
-main.py
```

## Use

To install the library, use the package collected by the 'pip' command:

```
!pip install tcqi
```

Then, it should be imported into the Python file that requires it:

```
from tcqi import TCQi
```

And finally, you must initialize a TCQi object, in order to call the functions
containing the library:

```
tcqi = TCQi()
```

Example:

```
from tcqi import TCQi

# Initialize the TCQi object
tcqi = TCQi()
# Locate tcqi file to modify
file = 'filename.tcqi'
# Execute a function of the library with format 'tcqi.funcion_x()'
table_files = tcqi.read_and_split_TQQi_file(
    tcqi.unpack_file('.//Data//' + file)
)
```
