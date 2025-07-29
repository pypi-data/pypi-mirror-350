# na
Functions and script to peek into the callable/argument structure of a set of callables

To install:	```pip install na```

## Overview
The `na` package provides a suite of tools designed to analyze and visualize the structure of callables (functions, classes, methods) within Python modules, classes, or any iterable collection of callables. It enables users to inspect callable signatures, filter callables based on their type, and generate detailed reports and visualizations of argument usage and defaults across a collection of callables.

## Key Features
- **Filtering Callables**: Select callables based on type (functions, classes, methods, or any callable).
- **Signature Extraction**: Retrieve the argument names and default values from callables.
- **Visualization**: Generate heatmaps and bar graphs to visualize the usage and defaults of callable arguments.
- **Data Frame Conversion**: Convert callable signature data into pandas DataFrames for further analysis or reporting.

## Installation
To install the package, use the following pip command:
```bash
pip install na
```

## Usage Examples

### Getting Callable Signatures as DataFrame
To retrieve and display the signatures of callables within a module as a DataFrame:
```python
import na
import sys  # Example module

# Get DataFrame of callable signatures in the sys module
df_signatures = na.callables_signatures_df(sys.modules[__name__])
print(df_signatures)
```

### Visualizing Callable Signatures
To visualize the signatures of callables using a heatmap:
```python
import na
import sys  # Example module

# Visualize signatures as a heatmap
na.heatmap_of_signatures(sys.modules[__name__])
```

### Plotting Non-Null Counts of Signatures
To plot the count of non-null/default arguments for callables:
```python
import na
import sys  # Example module

# Plot non-null counts of signatures
na.plot_nonnull_counts_of_signatures(sys.modules[__name__])
```

## API Reference

### `callables_of_module(module, callable_filt='callable')`
Retrieve callables from a specified module.
- **module**: The module from which to retrieve callables.
- **callable_filt**: Filter criterion for what type of callables to retrieve (e.g., 'callable', 'class', 'function').

### `callables_of_class(cls, callable_filt='function')`
Retrieve callables from a specified class.
- **cls**: The class from which to retrieve callables.
- **callable_filt**: Filter criterion for what type of callables to retrieve.

### `get_callables_from(callables, callable_filt='callable')`
Get a generator of callable objects from various types of inputs like modules, classes, or lists of callables.
- **callables**: Input from which to extract callables.
- **callable_filt**: Filter criterion for what type of callables to retrieve.

### `SignatureExtractor(normalize_var_names=True)`
Class to extract and normalize parameter names and defaults from callables.
- **normalize_var_names**: Whether to normalize variable names like `*args` and `**kwargs`.

### `arg_default_dict_of_callables(callables, callable_filt='callable')`
Get a dictionary with callable names as keys and another dictionary of argument names and their default values as values.
- **callables**: Input from which to extract callables.
- **callable_filt**: Filter criterion for what type of callables to retrieve.

### `heatmap(...)`
Function to create a heatmap from a matrix or DataFrame.
- **X**: Data to plot as a heatmap.
- **other parameters**: Customization options for the heatmap appearance.

### `heatmap_of_signatures(callables, callable_filt='callable', ...)`
Visualize the argument structure of callables as a heatmap.
- **callables**: Input from which to extract callables.
- **callable_filt**: Filter criterion for what type of callables to retrieve.

### `plot_nonnull_counts_of_signatures(callables, callable_filt='callable', ...)`
Plot the count of non-null/default arguments for callables.
- **callables**: Input from which to extract callables.
- **callable_filt**: Filter criterion for what type of callables to retrieve.

## Contributing
Contributions to the `na` package are welcome! Please feel free to fork the repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see the LICENSE file for details.