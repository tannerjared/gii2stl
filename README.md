# gii2stl
Python script to convert GIfTI surface files to STL. It specifically takes two cerebral hemisphere files, combines them, and does Scale Dependant Laplacian Smoothing of them using the accompanying .mlx file. This can be used for 3D printing or displaying the 3D model in 3D software.

GIfTI files are used by several MRI analysis software packages: https://www.nitrc.org/projects/gifti/

You can use the FreeSurfer tool mris_convert to convert .pial files to GIfTI: https://surfer.nmr.mgh.harvard.edu/fswiki/GIfTI
