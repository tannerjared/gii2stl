import argparse
import os

# Check if the required packages are installed
try:
    import nibabel as nib
    import numpy as np
    from stl import mesh
    import pymeshlab
except ImportError as e:
    print(f"Error: {e}")
    print("Please install the required packages using:")
    print("pip install nibabel numpy numpy-stl pymeshlab")
    exit()

def convert_gii_to_stl(gii_filename, stl_filename):
    gii = nib.load(gii_filename)
    vertices = gii.darrays[0].data
    faces = gii.darrays[1].data
    stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, face in enumerate(faces):
        for j in range(3):
            stl_mesh.vectors[i][j] = vertices[face[j]]
    stl_mesh.save(stl_filename)
    print(f"STL file saved to {stl_filename}")

def combine_stl_files(mesh1_filename, mesh2_filename, output_filename):
    mesh1 = mesh.Mesh.from_file(mesh1_filename)
    mesh2 = mesh.Mesh.from_file(mesh2_filename)
    combined_vertices = np.vstack([mesh1.vectors, mesh2.vectors])
    combined_normals = np.vstack([mesh1.normals, mesh2.normals])
    combined_mesh = mesh.Mesh(np.zeros(combined_vertices.shape[0], dtype=mesh.Mesh.dtype))
    combined_mesh.vectors = combined_vertices
    combined_mesh.normals = combined_normals
    combined_mesh.save(output_filename)
    print(f"Combined mesh saved to {output_filename}")

def smooth_stl_file(input_filename, output_filename, smoothing_script):
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(input_filename)
    ms.load_filter_script(smoothing_script)
    ms.apply_filter_script()
    ms.save_current_mesh(output_filename)

def determine_hemisphere(filename):
    if 'lh.' in filename:
        return '_lh'
    elif 'rh.' in filename:
        return '_rh'
    else:
        return ''

def main():
    parser = argparse.ArgumentParser(description='Convert GIfTI files to STL, combine them, and apply smoothing.')
    parser.add_argument('-i', '--input', nargs='+', required=True, help='Input GIfTI file names')
    parser.add_argument('-o', '--output', required=True, help='Output combined and smoothed STL file name')
    parser.add_argument('-s', '--smoothing-script', required=True, help='Path to the MeshLab XML script for smoothing')

    args = parser.parse_args()

    if len(args.input) != 2:
        print("Please provide exactly two input GIfTI surface files created by the CAT12 toolbox or other software.")
        exit()

    gii1_filename, gii2_filename = args.input
    output_filename = args.output

    # Determine hemisphere from the input filenames
    hemisphere1 = determine_hemisphere(gii1_filename)
    hemisphere2 = determine_hemisphere(gii2_filename)

    # Convert GIfTI files to STL
    convert_gii_to_stl(gii1_filename, os.path.splitext(output_filename)[0] + hemisphere1 + ".stl")
    convert_gii_to_stl(gii2_filename, os.path.splitext(output_filename)[0] + hemisphere2 + ".stl")

    # Combine STL files
    combine_stl_files(
        os.path.splitext(output_filename)[0] + hemisphere1 + ".stl",
        os.path.splitext(output_filename)[0] + hemisphere2 + ".stl",
        output_filename
    )

    # Smooth combined STL file
    smooth_stl_file(output_filename, os.path.splitext(output_filename)[0] + '_smoothed.stl', args.smoothing_script)

if __name__ == "__main__":
    main()
