
# pleXpert - PLEX Image Renamer

![pleXpert Logo](src/pleXpertLogo.png)

### pleXpert - The Easiest To Use Image Renamer for the PLEX naming convention

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Usage](#usage)
4. [Why Create An Output Folder?](#why-create-an-output-folder)
   - [Will This Change?](#will-this-change)
5. [Contributing](#contributing)
6. [License](#license)
7. [Contact](#contact)
8. [Sections To Be Added](#sections-to-be-added)

## Overview

**`pleXpert`** is a sophisticated Python-based utility designed to streamline the renaming of image files for PLEX media server use. This tool automates the tedious process of renaming images to conform to PLEX's strict naming conventions, ensuring that your TV show posters and episode title cards are seamlessly recognized and displayed.

## Features

- **TV Season Posters**: Automatically renames season poster images to the standardized format required by PLEX.
- **Episode Title Cards**: Accurately renames episode title cards based on season and episode numbers to align with corresponding episode filenames.
- **Batch Processing**: Efficiently handles bulk file operations, making it ideal for large-scale media libraries.
- **Preview Mode**: Offers a detailed preview of renaming operations, allowing users to review changes before finalizing.
- **Dark Mode**: A modern, visually appealing dark mode interface for an enhanced user experience.
- **Cross-Platform Compatibility**: Designed to work seamlessly on Windows. With support for macOS and Linux platforms to come.

## Usage

1. **Load Image Folder**: Select the folder containing your TV show images via the "Browse" button.
	- Loading the Image Folder will load a preview list of the files found.
2. **Select Destination Folder**: Specify the destination folder where the renamed images will be saved.
	- Selecting the Destination Folder will populate the list with the matches found. E.g. An image file with "S1 E5" in it's name will be shown to be matched to the episode file which indicates it's also for Season 01 Episode 05.
3. **Choose Options**: Opt to rename TV Season Posters, Episode Title Cards, or both based on your needs.
	- This allows you to tell the program if you're after only adjusting TV Season Posters, Episode Title Cards or Both. The importance of this is it ensures the program runs your image files naming conventions against the plex standards correctly.
4. **Preview Changes**: Review the preview of the file renaming operations to ensure accuracy.
5. **Proceed with Renaming**: Once satisfied, click "Proceed" to execute the renaming and move the files to the output folder.
	- Note: Upon completion this will automatically open the folder above the Output folder allowing ease of copying.

## Why Create An Output Folder?
The program is designed to create an output folder in your image file location, with pre-created matching folders allowing a quick drag merge between the output files and your destination folder. The program however is currently designed to not complete this transfer for you.
The reason the program was designed with this limitation is simply because most users consider their destination location as their "Live Production Server" and as such, if an error was to occur during the file renaming or transfer there could be unforseen ramifications for the files within the destination folder.

### Will This Change?
Yes, in Version 2.0 one key addition to the software will be a selection toggle allowing a user to set if they want one of four things to happen with their files, these new options will be:

 1. **Standard Output Folder:** This setting will allow the same functionality as Version 1.0
 2. **Move Files Without Output Folder:** This will remove the output folder entirely after the files have been merged with their destination location.
 3. **Move Files With Output Folder:** This will copy the files into the destination but retain the output folder.
 4. **Move and Clean:** This setting will copy the files to the destination folder and totally remove the original images folder allowing a one click solution to cleaning the original files. 
 *I do **NOT** recommend this option, but it was requested by several pre production users.*

## Contributing

Contributions to `pleXpert` are welcome and encouraged in the form of feature requests and bug reports. To contribute:

1.  Go to the [Issues Tab](https://github.com/DatProGuy/pleXpert/issues).
2.  Create a issue and detail your request, concern, bug or feature suggestion using the appropriate tag. Also feel free to note here if you're interested in participating in the fix if it's a bug, or if you've got a snipit of code you'd like to directly contribute to the project.
3.  Your Issue will be reviewed.

If you're interested in working on this project directly and not simply contributing suggestions and bug reports please contact me prior.

## License

This project is licensed under the **GPL-3.0** License. See the [LICENSE](https://github.com/DatProGuy/pleXpert?tab=GPL-3.0-1-ov-file) file for more information.

## Contact

For inquiries, issues, or suggestions, feel free to open an issue on GitHub or reach out to the maintainer:

-   **GitHub**: [DatProGuy](https://github.com/DatProGuy)

## Sections To Be Added
- **Screenshots**: A section showcasing screenshots of the application in use.
- **Changelog**: A changelog is essential for tracking the history of changes and updates.
- **Future Plans**: Outlining future improvements or planned features.
