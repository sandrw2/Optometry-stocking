Part 1: OCR reader for reading contact lense paramters and brands 
Part 2: Visual manual stocking
Part 3: Database for live stocking

Packages downloaded:
Opencv 
pillow

1. Navigate to dependency folder and run conda env create -f environment.yml


Issues:
1. Parameters are being matched properly for a few labels. For some contacts such as test 33 "precision 1 Sphere -7.50" contact. X coordinates of "-7.50" is less than "PWR". Might be because of slight tilt? I dunno 

