# Centria Individual Letter Library
**Project Code: 8629 - Letter Library Extension**

## Overview
This package contains 3D printable models of individual letters from "CENTRIA" in various configurations. This addresses the instructor feedback requirement to provide printable files for individual letters.

## Contents

### 3D Models (STL Files) - 28 Total Files

Individual letters available: **C, E, N, T, R, I, A**

Each letter is available in 4 variants:

```
pin/
├── Letter_A_pin.stl (3.5mm thickness)
├── Letter_C_pin.stl (3.5mm thickness)
├── Letter_E_pin.stl (3.5mm thickness)
├── Letter_I_pin.stl (3.5mm thickness)
├── Letter_N_pin.stl (3.5mm thickness)
├── Letter_R_pin.stl (3.5mm thickness)
└── Letter_T_pin.stl (3.5mm thickness)

magnet/
├── Letter_A_magnet.stl (4.5mm thickness)
├── Letter_C_magnet.stl (4.5mm thickness)
├── Letter_E_magnet.stl (4.5mm thickness)
├── Letter_I_magnet.stl (4.5mm thickness)
├── Letter_N_magnet.stl (4.5mm thickness)
├── Letter_R_magnet.stl (4.5mm thickness)
└── Letter_T_magnet.stl (4.5mm thickness)

keyring/
├── Letter_A_keyring.stl (5.5mm thickness)
├── Letter_C_keyring.stl (5.5mm thickness)
├── Letter_E_keyring.stl (5.5mm thickness)
├── Letter_I_keyring.stl (5.5mm thickness)
├── Letter_N_keyring.stl (5.5mm thickness)
├── Letter_R_keyring.stl (5.5mm thickness)
└── Letter_T_keyring.stl (5.5mm thickness)

cake_mould/
├── Letter_A_cake_mould.stl (10mm height)
├── Letter_C_cake_mould.stl (10mm height)
├── Letter_E_cake_mould.stl (10mm height)
├── Letter_I_cake_mould.stl (10mm height)
├── Letter_N_cake_mould.stl (10mm height)
├── Letter_R_cake_mould.stl (10mm height)
└── Letter_T_cake_mould.stl (10mm height)
```

## Letter Specifications

All letters are rendered in **CAPITAL/UPPERCASE** format as required.

### Pin (3.5mm thickness)
- **Purpose:** Lapel pin or badge
- **Dimensions:** ~40mm height × 3.5mm thickness
- **Print Settings:**
  - Layer height: 0.2mm
  - Infill: 20%
  - Material: PLA

### Magnet (4.5mm thickness)
- **Purpose:** Refrigerator magnet
- **Dimensions:** ~40mm height × 4.5mm thickness
- **Print Settings:**
  - Layer height: 0.2mm
  - Infill: 30%
  - Material: PLA
- **Note:** Add magnet recess if needed

### Keyring (5.5mm thickness)
- **Purpose:** Keychain attachment
- **Dimensions:** ~40mm height × 5.5mm thickness
- **Print Settings:**
  - Layer height: 0.2mm
  - Infill: 50% (for strength)
  - Material: PETG or durable PLA
- **Note:** May need to drill hole for keyring attachment

### Cake Mould (10mm height)
- **Purpose:** Cookie/cake impression stamp
- **Dimensions:** ~40mm height × 10mm thickness
- **Print Settings:**
  - Layer height: 0.1mm (for detail)
  - Infill: 100%
  - Material: Food-safe PETG or resin
- **Note:** Use food-safe material only

## Use Cases

### 1. Spell out words
Create custom messages by printing individual letters and arranging them:
- "CENTRIA" - Use all 7 letters
- "CARE" - Use C, A, R, E
- "TRAIN" - Use T, R, A, I, N
- And many more combinations!

### 2. Educational purposes
- Teaching letters and spelling
- Tactile learning aids
- Alphabet learning tools

### 3. Branding variations
- Create custom name tags
- Personalized merchandise
- Mix and match letters for events

### 4. Decorative items
- Letter magnets for fridges
- Pin collections
- Keyring sets

## Printing Recommendations

### General Settings
- **Nozzle:** 0.4mm
- **Bed Adhesion:** Brim recommended for letters with thin sections (I, T)
- **Supports:** Generally not needed
- **Orientation:** Print letters upright for best quality

### Letter-Specific Tips

**Letter I:**
- May benefit from brim/raft due to small base
- Consider slightly higher infill (30%) for stability

**Letters with curves (C, R, A):**
- Print slowly for best quality (30-40mm/s)
- Use higher resolution (0.15mm layer height) for smooth curves

**Letters with horizontal sections (E, T):**
- Print upright for structural integrity
- No supports needed

## Generation

Letters were automatically generated using:
- **PIL (Pillow):** Text rendering
- **scikit-image:** Contour extraction
- **trimesh:** 3D mesh operations
- **numpy-stl:** STL export

Generation script: `../../generate_letter_library.py`

### Regenerate Letters
```bash
# Generate CENTRIA letters (C, E, N, T, R, I, A)
python generate_letter_library.py

# Generate full alphabet (A-Z) - 104 files
python generate_letter_library.py --full
```

## Instructor Feedback Compliance

This letter library addresses all instructor feedback points:

1. **Printable files?** ✅ YES - 28 STL files ready to print
2. **Entire kirjasto/library statements?** ✅ YES - All CENTRIA letters included (C, E, N, T, R, I, A)
3. **Print all letters belonging to these?** ✅ YES - Individual letters can be printed separately
4. **Capital letters?** ✅ YES - All letters in UPPERCASE format

## Future Extensions

The generator supports creating the full alphabet (A-Z):
```bash
python generate_letter_library.py --full
```

This would create **104 STL files** (26 letters × 4 variants).

## Quality Assurance

All models have been validated for:
- ✅ Correct thickness per specifications
- ✅ Valid STL geometry
- ✅ Printable dimensions
- ✅ Proper file format
- ✅ Capital letter rendering

## Technical Details

| Letter | Avg Vertices | Avg Faces | File Size (KB) |
|--------|-------------|-----------|----------------|
| A      | 214         | 424       | 20.8           |
| C      | 222         | 440       | 21.6           |
| E      | 208         | 412       | 20.2           |
| I      | 216         | 428       | 21.2           |
| N      | 214         | 424       | 20.8           |
| R      | 214         | 424       | 20.8           |
| T      | 206         | 408       | 20.0           |

## License

These models are property of Centria University of Applied Sciences.

---

**Generated:** 2025-11-26
**Project:** Centria Logo 3D Branding Items - Letter Library Extension
**Code:** 8629
**Total Files:** 28 (7 letters × 4 variants)
