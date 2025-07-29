# BeautifulTerminal

**BeautifulTerminal** is a Python library that automatically beautifies terminal output by adding colors based on the content of the messages. This library improves the readability of your console applications and makes it easier to understand log outputs and messages. No additional setup is required after importing!

## Features

* **Automatic Colors**:

  * Errors are displayed in **red**.
  * Warnings are displayed in **yellow**.
  * Success messages are displayed in **green**.
  * Regular messages use the **terminal's default color** (no color override).

* **Easy Integration**:

  * Simply import the library, and it works immediately.

* **Customizable**:

  * You can easily change the color codes to suit your preferences.

## Installation

To install the library, use `pip`:

```bash
pip install beautiful-terminal
````

## Optional Version Check

**BeautifulTerminal** optionally checks if you are running the latest version by contacting PyPI when you import the library or run it as a script.

* This feature requires the external libraries `requests` and `setuptools`.
* These dependencies are **optional** and the library works perfectly without them.
* If these libraries are installed, **BeautifulTerminal** will notify you in the terminal if your installed version is outdated or up to date.
* If not installed, the version check silently skips without affecting normal usage.

To enable the version check dependencies, install with:

```bash
pip install beautiful-terminal[version_check]
```

If you want to disable the version check completely, simply uninstall or avoid installing these optional dependencies.

## Getting Started

After installation, you can quickly use the library in your Python scripts. Follow these simple steps:

1. **Import the library**:

```python
import beautiful_terminal
```

2. **Print messages**:

Use the `print` function as usual. The library automatically applies the appropriate colors based on the content of your messages.

## Usage

Here are some examples of how to use the library:

```python
import beautiful_terminal

# Examples of using the library
print("This is a regular message.")            # Default terminal color
print("Error: Something went wrong!")          # Error in Red
print("Warning: Be careful!")                  # Warning in Yellow
print("Success: Operation completed!")         # Success in Green
```

### Example Outputs

| Type            | Description                 |
| --------------- | --------------------------- |
| Regular message | Uses terminal default color |
| Warning         | 🟡 Yellow                   |
| Error           | 🔴 Red                      |
| Success         | 🟢 Green                    |

### Using the `color` Option

The `print` function in `BeautifulTerminal` supports an optional `color` parameter that lets you specify the color of the printed text directly. Example:

```python
import beautiful_terminal

print("This text is normal.")                         # Default terminal color
print("This text is red!", color="red")               # Red text
print("This text is yellow!", color="yellow")         # Yellow text
print("This text is green!", color="green")           # Green text
```

If you specify an invalid color, the default terminal color is used. This gives you flexibility to customize the text to your liking.

## Customization

You can change the color codes in the library to modify the appearance of the outputs. This allows you to tailor the library to your preferred terminal design or personal preferences. Simply modify the `COLORS` dictionary in the `BeautifulTerminal` class.

## Disabling

If you need to temporarily disable color output, you can do so:

```python
import beautiful_terminal as bt
bt.disable()  # Disable color output
```

To re-enable color output:

```python
bt.enable()  # Re-enable color output
```

## Compatibility

The `BeautifulTerminal` library is compatible with any terminal that supports ANSI escape codes, which includes most modern terminal emulators on **Windows, macOS, and Linux**. It automatically enables ANSI support on Windows terminals. However, it may not work correctly on older systems or environments that do not support ANSI codes.

## Cross-Platform Support

**BeautifulTerminal** works seamlessly across multiple operating systems, including:

* **Windows** (enables ANSI escape code support automatically)
* **macOS**
* **Linux**

This makes it a reliable choice for terminal beautification in cross-platform Python projects.

## Acknowledgments

* This library was inspired by the need for better readability of terminal outputs.
* Special thanks to the contributors and the open-source community for their continuous support and suggestions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributions

Contributions are welcome! If you have suggestions for improvements or additional features, feel free to open an issue or submit a pull request.

## Contact

For questions or feedback, please reach out to us through the [GitHub repository](https://github.com/StarByteGames/beautiful-terminal).