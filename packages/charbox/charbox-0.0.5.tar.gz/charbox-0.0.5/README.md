# CharBox

![CharBox Logo](https://tairerullc.vercel.app/images/logo.png)  
*A powerful character attribute generator for Python.*

## Overview
CharBox is a Python library that generates random character attributes, including names, hair colors, and eye colors. It supports multiple name origins and offers standard and fancy variations for hair and eye colors.

### Latest Features
- **Manager:** Added three new functions to 'CharBox' class, allowing users add new hair colors, eye colors, and names.

### Features
- Generate **realistic** or **fantasy-inspired** names.
- Choose names based on **gender** and **origin** (American, Japanese, Korean, German, Russian).
- Generate **standard** or **fancy** hair and eye colors.
- Translate fancy color names (ex. 'Ebony') into more recognizable formats (ex. 'Ebony' becomes 'Black').
- Simple initialization and usage.

## Installation
Install CharBox via pip:

```sh
pip install charbox
```

## Usage
### Initializing the Library
Before using CharBox, you must initialize it:

```python
import charbox
charbox.init()
```

### Generating Names
```python
from charbox import Name

# Generate a first name
first_name = Name.generate_first_name(gender="male", origin="Japanese")
print(first_name)  # Example Output: Haruto

# Generate a last name
last_name = Name.generate_last_name(origin="American")
print(last_name)  # Example Output: Smith

# Generate a full name
full_name = Name.generate_name(gender="female", origin="Russian")
print(full_name)  # Example Output: Anastasia Ivanova
```

### Adding Names (session-based)
```python
from charbox import CharBox

CharBox.add_name(new_value="Tyrell", origin="American", is_surname=False, gender="male")
CharBox.add_name(new_value="Arkham", origin="American", is_surname=True, gender="male")
```

### Generating Hair Colors
```python
from charbox import HairColor

# Generate a standard hair color
hair_color = HairColor.generate_hair_color(wording="standard")
print(hair_color)  # Example Output: Chestnut

# Generate a fancy hair color
fancy_hair_color = HairColor.generate_hair_color(wording="fancy")
print(fancy_hair_color)  # Example Output: Sapphire

# Translate a fancy hair color to a readable format
translated_hair_color = HairColor.translate("Sapphire")
print(translated_hair_color)  # Example Output: Blue
```

### Adding Hair Colors (session-based)
```python
from charbox import CharBox

CharBox.add_hair_color(new_value="321", wording="standard", translation="123")
```

### Generating Eye Colors
```python
from charbox import EyeColor

# Generate a standard eye color
eye_color = EyeColor.generate_eye_color(wording="standard")
print(eye_color)  # Example Output: Green

# Generate a fancy eye color
fancy_eye_color = EyeColor.generate_eye_color(wording="fancy")
print(fancy_eye_color)  # Example Output: Amethyst

# Translate a fancy eye color to a readable format
translated_eye_color = EyeColor.translate("Amethyst")
print(translated_eye_color)  # Example Output: Purple
```

### Adding Eye Colors (session-based)
```python
from charbox import CharBox

CharBox.add_eye_color(new_value="123", wording="standard", translation="321")
```

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author
Developed by **Taireru LLC**. Check out our other projects at [https://tairerullc.com/pages/products](https://tairerullc.vercel.app/pages/products).

## Contributing
Contributions are welcome! Feel free to submit a pull request or report issues in the repository.

## Support
For support, please contact us via email or visit our website.

---

⭐ *Enjoy using CharBox? Give us a star on GitHub!*