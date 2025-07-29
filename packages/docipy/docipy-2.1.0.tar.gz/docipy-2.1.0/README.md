# DociPy v2.1.0

**Project**: DociPy
<br>**Version**: 2.1.0
<br>**OS**: OS Independent
<br>**Author**: Irakli Gzirishvili
<br>**Mail**: gziraklirex@gmail.com

**DociPy** is a Python command-line interface application. DociPy is designed to easily generate impressive static HTML documentations

## Installation

To use DociPy, follow these steps:

1. Run this CLI command to install the Python module `pip install docipy`
2. Navigate to any directory containing markdown `folder/files.md`
3. Open the CLI in the selected directory and run this command `docipy render`
4. Update the documentation logo at `assets/logo.ico` and the author image at `assets/author.png`
5. Run `docipy version` to upgrade the version number, or `docipy version (number)` to set it manually

> Do not change the file names in the `assets` folder, but feel free to update the files if needed

## Output

The output will consist of **2** folders and **3** files in the root directory by default:

- **assets**: A folder containing all required resources
- **version**: A folder reserving previous versions
- **index.html**: The generated static HTML file
- **menu.yaml**: The generated menu file, which you can adjust
- **robots.txt**: File that controls the behavior of search engines

The menu is mapped according to the directory tree. After adjusting your menu, don't forget to run this CLI command again `docipy render` to update your documentation
Change the `*circle` to any Bootstrap icon `*name` in the `menu.yaml` file that you think fits the topic

> To reset the menu, simply run the following CLI command: `docipy render -r`

## Config

If you want to update any configuration parameters that were defined during the initial generation of the documentation:

1. Run this CLI command to start updating configuration parameters `docipy reform`
2. Skip parameters by pressing `Enter` to leave their values unchanged
3. Enter new values for any desired parameter and press `Enter`

> Config parameters will be updated as you finish filling out the required fields

These are the configuration parameters requested during the initial generation of the documentation:

- **Project**: Name of the project `required`
- **Version**: Version of the project `required`
- **Slogan**: Slogan of the project
- **Description**: Description of the project
- **Keywords**: Keywords for search engines
- **Documentation URL**: URL of the live documentation domain
- **Author**: Author of the project `required`
- **Position**: Author's position
- **Email**: Author's email address `required`
- **LinkedIn**: Author's LinkedIn profile URL
- **X**: Author's X account URL
- **Button 1 Name**: Name of the first main button
- **Button 1 Link**: URL for the first main button
- **Button 2 Name**: Name of the second main button
- **Button 2 Link**: URL for the second main button
- **Main Color**: Main color for the documentation
- **Dark Color**: Darker variant of the main color for the documentation
- **Google Tag (script)**: Google tag script for analytics
- **Copyright Verification (meta)**: Meta tag for copyright verification
- **Copyright Badge (a, script)**: Link and script for the copyright badge

## Publish

Don't forget to update the `Documentation URL` before publishing:

1. Run this CLI command to start updating configuration parameters `docipy reform`
2. Skip other parameters by pressing `Enter` to leave their values unchanged
3. Enter `Documentation URL` value `e.g https://example.com` and press `Enter`

> For local versions, the `Documentation URL` must be specified as a dot `.`