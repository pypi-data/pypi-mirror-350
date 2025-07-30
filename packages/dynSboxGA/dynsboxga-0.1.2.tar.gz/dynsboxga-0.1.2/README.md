# Dynamic S-Box Generator

`dynamic-sbox` is a Python package that generates AES S-boxes using a Genetic Algorithm (GA) approach. It evaluates each S-box candidate based on non-linearity and avalanche effect, evolving toward cryptographically secure substitution boxes.

---

## 📦 Features

- Random S-box generation with 256 unique values
- Fitness evaluation using:
  - **Non-linearity** (Differential uniformity)
  - **Avalanche effect**
- Genetic operations:
  - **Crossover**
  - **Mutation**
  - **Repair**
- Visualization of final S-box as a 16×16 hexadecimal matrix using `pandas`
- Exports the best S-box to a `.txt` file
- CLI support: `generate-sbox`

---

## 🔧 Requirements

- Python 3.6+
- numpy
- pandas

---

## 🚀 Installation

### ✅ From Source
```bash
pip install dynSboxGA
```

---

## 🔍 Usage

### As a Python Module
```python
from dynamic_sbox import DynamicAESSBoxGA, display_sbox_hex_table

sbox_gen = DynamicAESSBoxGA()
best_sbox = sbox_gen.apply_ga()
sbox_gen.export_sbox(best_sbox)
display_sbox_hex_table(best_sbox)
```

### As a CLI Tool
```bash
generate-sbox
```

- Generates best S-box using GA
- Saves result to `dynamic_sbox.txt`
- Displays 16×16 hex matrix

---

## 📄 Output

- `dynamic_sbox.txt`: Contains 256 comma-separated integers (final S-box)
- Visual S-box in terminal (if running in Jupyter or with pandas display support)

---

## 🧪 Future Enhancements

- Add unit tests
- Support other block sizes or substitution structures
- Integrate with AES encryption demos

---

## 📜 License

MIT License © 2025 Mohammad Luqman, Salman Ali

---

## ✨ Author

- **Mohammad Luqman** – [GitHub Profile](https://github.com/mohdluqman)
- **Salman Ali** – [GitHub Profile](https://github.com/salmanali)

---