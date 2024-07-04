# RPA Challenge Using Python and RPAFramework

This project aims to exercise the practices of automating functions that usually require significant manual effort. The project's goal is to access the page https://www.latimes.com/ and perform a search using any keyword provided at the system's input. From there, based on filters and a specific time period, the system will extract some of the information found in the generated results, such as title, description, and more. Once this is done, the system will analyze the collected data, download images, and save all the information in an .xlsx file.
# RPA Challenge Using Python and RPAFramework

This project aims to exercise the practices of automating functions that usually require significant manual effort. The project's goal is to access the page https://www.latimes.com/ and perform a search using any keyword provided at the system's input. From there, based on filters and a specific time period, the system will extract some of the information found in the generated results, such as title, description, and more. Once this is done, the system will analyze the collected data, download images, and save all the information in an .xlsx file.

## Running

#### VS Code
1. Get [Robocorp Code](https://robocorp.com/docs/developer-tools/visual-studio-code/extension-features) -extension for VS Code.
1. You'll get an easy-to-use side panel and powerful command-palette commands for running, debugging, code completion, docs, etc.

#### Command line

1. [Get RCC](https://github.com/robocorp/rcc?tab=readme-ov-file#getting-started)
1. Use the command: `rcc run`

## Results

🚀 After running the bot, check out the `log.html` under the `output` -folder. To facilitate the process, you can install the Open in Browser plugin to accelerate the viewing of the log.html file generated. The log.html file centralizes all the information related to the execution of the bot, such as variable values, errors, execution sequence, and more.

## Dependencies

I recommend you getting familiar with adding your dependencies in [conda.yaml](conda.yaml) to control your Python dependencies and the whole Python environment for your automation.

<br/>

> The full power of [rpaframework](https://robocorp.com/docs/python/rpa-framework) -libraries is also available on Python as a backup while we implement the new Python libraries.

## What now?

### config
This directory contains configuration files used by the bot. These settings include information on browser configuration, selectors, access url and data related to the resulting excel file
### enums
All enumeration classes are defined here

Start writing Python and remember that the AI/LLM's out there are getting really good and creating Python code specifically.

👉 Try out [Robocorp ReMark 💬](https://chat.robocorp.com)

For more information, do not forget to check out the following:
- [Robocorp Documentation -site](https://robocorp.com/docs)
- [Portal for more examples](https://robocorp.com/portal)
- Follow our main [robocorp -repository](https://github.com/robocorp/robocorp) as it is the main location where we developed the libraries and the framework.
