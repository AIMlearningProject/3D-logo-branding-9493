"""
Centria Individual Letter STL Generator
Generates 3D printable models for individual letters (A-Z)
Project Code: 8629 - Letter Library Extension

Addresses instructor feedback:
- Creates individual letter files for the entire alphabet
- Supports all 4 variants (pin, magnet, keyring, cake_mould)
- All letters in CAPITAL format
"""

import numpy as np
from stl import mesh
import trimesh
import os
from pathlib import Path as FilePath
from PIL import Image, ImageDraw, ImageFont

class LetterSTLGenerator:
    """Generate 3D printable STL files for individual letters"""

    # Specifications matching the main project
    VARIANTS = {
        'pin': {
            'thickness': 3.5,
            'description': 'Pin with mounting post'
        },
        'magnet': {
            'thickness': 4.5,
            'description': 'Magnet with recess'
        },
        'keyring': {
            'thickness': 5.5,
            'description': 'Keyring with reinforced loop'
        },
        'cake_mould': {
            'thickness': 10.0,
            'description': 'Cake mould (inverted relief)'
        }
    }

    # CENTRIA letters + full alphabet option
    CENTRIA_LETTERS = ['C', 'E', 'N', 'T', 'R', 'I', 'A']
    FULL_ALPHABET = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def __init__(self, output_dir='Centria_3D_Models/Letters_Library', font_size=200):
        self.output_dir = FilePath(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.font_size = font_size

        # Create subdirectories for each variant
        for variant in self.VARIANTS.keys():
            (self.output_dir / variant).mkdir(exist_ok=True)

    def create_letter_mesh(self, letter, thickness):
        """Create 3D mesh from a letter using PIL text rendering"""

        # Create image with letter
        img_size = 300
        image = Image.new('L', (img_size, img_size), 0)
        draw = ImageDraw.Draw(image)

        # Try to use a bold, clean font
        try:
            # Try different font options
            font_options = [
                'arial.ttf',
                'Arial Bold.ttf',
                'arialbd.ttf',
                'C:/Windows/Fonts/arialbd.ttf',
                'C:/Windows/Fonts/arial.ttf',
            ]
            font = None
            for font_path in font_options:
                try:
                    font = ImageFont.truetype(font_path, self.font_size)
                    break
                except:
                    continue

            if font is None:
                # Fallback to default
                font = ImageFont.load_default()
        except Exception as e:
            font = ImageFont.load_default()

        # Get text bounding box and center it
        bbox = draw.textbbox((0, 0), letter, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (img_size - text_width) // 2 - bbox[0]
        y = (img_size - text_height) // 2 - bbox[1]

        # Draw letter
        draw.text((x, y), letter, fill=255, font=font)

        # Convert to numpy array
        img_array = np.array(image)

        # Create binary mask (threshold)
        mask = img_array > 128

        # Find contour points
        contour_points = self._extract_contour(mask)

        if len(contour_points) < 3:
            print(f"  Warning: Insufficient points for letter {letter}")
            return None

        # Create 3D mesh by extruding the contour
        mesh_obj = self._extrude_contour(contour_points, thickness)

        return mesh_obj

    def _extract_contour(self, mask):
        """Extract contour points from binary mask"""
        from scipy import ndimage
        from skimage import measure

        # Find contours
        contours = measure.find_contours(mask, 0.5)

        if not contours:
            return []

        # Use the longest contour (main letter outline)
        main_contour = max(contours, key=len)

        # Simplify contour to reduce polygon complexity
        # Sample every nth point
        step = max(1, len(main_contour) // 100)
        simplified = main_contour[::step]

        return simplified

    def _extrude_contour(self, contour_points, height):
        """Extrude 2D contour to create 3D mesh"""

        # Convert to numpy array and normalize
        coords = np.array(contour_points)

        # Center and scale
        center = coords.mean(axis=0)
        coords -= center

        # Scale to reasonable size (40mm width)
        max_extent = np.max(np.abs(coords))
        if max_extent > 0:
            coords = coords * (40.0 / max_extent)

        # Flip Y axis (image coordinates to 3D coordinates)
        coords[:, 1] = -coords[:, 1]

        # Create bottom and top faces
        n_points = len(coords)
        bottom = np.column_stack([coords, np.zeros(n_points)])
        top = np.column_stack([coords, np.full(n_points, height)])

        # Create vertices and faces
        vertices = []
        faces = []

        # Add bottom and top vertices
        vertices.extend(bottom)
        vertices.extend(top)

        # Create side faces
        for i in range(n_points - 1):
            # Two triangles per side quad
            faces.append([i, i + 1, i + 1 + n_points])
            faces.append([i, i + 1 + n_points, i + n_points])

        # Close the loop
        faces.append([n_points - 1, 0, n_points])
        faces.append([n_points - 1, n_points, 2 * n_points - 1])

        # Create bottom face (fan triangulation)
        for i in range(1, n_points - 1):
            faces.append([0, i + 1, i])

        # Create top face
        for i in range(1, n_points - 1):
            faces.append([n_points, n_points + i, n_points + i + 1])

        vertices = np.array(vertices)
        faces = np.array(faces)

        # Create trimesh object
        mesh_obj = trimesh.Trimesh(vertices=vertices, faces=faces)

        # Fix normals and make watertight
        mesh_obj.fix_normals()
        trimesh.repair.fill_holes(mesh_obj)

        return mesh_obj

    def generate_letter_variants(self, letter):
        """Generate all 4 variants for a single letter"""

        print(f"\nProcessing Letter: {letter}")
        print("-" * 50)

        for variant_name, specs in self.VARIANTS.items():
            print(f"  Creating {variant_name} ({specs['thickness']}mm)... ", end='')

            try:
                # Create mesh
                letter_mesh = self.create_letter_mesh(letter, specs['thickness'])

                if letter_mesh is None:
                    print("FAILED - Could not create mesh")
                    continue

                # Output filename
                output_file = self.output_dir / variant_name / f"Letter_{letter}_{variant_name}.stl"

                # Export as STL
                letter_mesh.export(str(output_file))

                # Verify file
                file_size = output_file.stat().st_size / 1024  # KB

                print(f"OK ({file_size:.1f} KB, {len(letter_mesh.vertices)} vertices)")

            except Exception as e:
                print(f"ERROR: {e}")
                import traceback
                traceback.print_exc()

    def generate_centria_letters(self):
        """Generate STL files for CENTRIA letters (C, E, N, T, R, I, A)"""
        print("\n" + "=" * 60)
        print("CENTRIA LETTER LIBRARY GENERATOR")
        print("Project Code: 8629 - Letter Library Extension")
        print("=" * 60)
        print("\nGenerating CENTRIA letters: C, E, N, T, R, I, A")
        print("Variants: pin, magnet, keyring, cake_mould")
        print("=" * 60)

        for letter in self.CENTRIA_LETTERS:
            self.generate_letter_variants(letter)

        self._print_summary(self.CENTRIA_LETTERS)

    def generate_full_alphabet(self):
        """Generate STL files for the complete alphabet (A-Z)"""
        print("\n" + "=" * 60)
        print("FULL ALPHABET LIBRARY GENERATOR")
        print("Project Code: 8629 - Complete Letter Library")
        print("=" * 60)
        print("\nGenerating all letters: A-Z")
        print("Variants: pin, magnet, keyring, cake_mould")
        print("=" * 60)

        for letter in self.FULL_ALPHABET:
            self.generate_letter_variants(letter)

        self._print_summary(self.FULL_ALPHABET)

    def _print_summary(self, letters):
        """Print generation summary"""
        print("\n" + "=" * 60)
        print("GENERATION COMPLETE")
        print("=" * 60)
        print(f"\nOutput directory: {self.output_dir.absolute()}")
        print(f"Letters generated: {', '.join(letters)}")
        print(f"Total files: {len(letters) * len(self.VARIANTS)}")

        # List files by variant
        print("\nGenerated files by variant:")
        for variant_name in self.VARIANTS.keys():
            variant_dir = self.output_dir / variant_name
            stl_files = sorted(variant_dir.glob('*.stl'))
            print(f"\n{variant_name}/ ({len(stl_files)} files)")
            for f in stl_files:
                size = f.stat().st_size / 1024
                print(f"  - {f.name} ({size:.1f} KB)")


def main():
    import sys

    print("Centria Letter Library Generator")
    print("=" * 60)

    # Check if dependencies are installed
    try:
        from scipy import ndimage
        from skimage import measure
    except ImportError:
        print("\nERROR: Missing required dependencies")
        print("\nPlease install:")
        print("  pip install scipy scikit-image pillow")
        return

    if len(sys.argv) > 1 and sys.argv[1] == '--full':
        # Generate full alphabet
        generator = LetterSTLGenerator()
        generator.generate_full_alphabet()
    else:
        # Generate just CENTRIA letters
        generator = LetterSTLGenerator()
        generator.generate_centria_letters()

        print("\n" + "=" * 60)
        print("TIP: Run with --full flag to generate complete alphabet (A-Z)")
        print("  python generate_letter_library.py --full")
        print("=" * 60)


if __name__ == '__main__':
    main()
