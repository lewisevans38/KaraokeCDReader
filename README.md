# KaraokeCDReader

This project aims to to allow a user to search for a desired track over an ordered list of images, and find the disc number that the track pertains to.

An Example Image:
![image](https://github.com/lewisevans38/KaraokeCDReader/assets/143433180/57d25cdf-2da4-4f5e-80f0-25733af171ac)


The project uses PyTesseract and a host of OpenCV image pre-processing techniques to do the OCR, and then sorts through the text to extract the meaningful information. This text is put into a pandas database, that provides the track name and the disc number. Then, the project employs a fuzzy matching function that takes a user inputted string, and returns the closest matched track and the target disc number. This function was created as a way of dealing with the OCR's frequent spelling and misreading errors.

To interface with the database, the function is implemented into a TKinter GUI. The same GUI that was used in the OSRS-TraderAdvisor.

Example of use:

![image](https://github.com/lewisevans38/KaraokeCDReader/assets/143433180/ecc9ff59-fef9-465d-a7a9-7c054d02d02b)
