
- **Goal:** Suggest unique gift ideas for a colleague.
- **Context:** My colleague works in software development, enjoys hiking, and is celebrating their 30th birthday next month.
- **Warning:** Avoid generic gifts like gift cards or anything too expensive.
- **Format:** List 3-5 specific gift ideas with a brief explanation for each.


goal: create a powershell script that looks for new .m4a files in a folder. running at certain time

context: create a powershell script that looks for new .m4a files in folder "C:\Users\JasonU\Recordings". the powershell script finds a new file and the calls the following program 'transcribe-anything "filename.m4a" --device cpu --language en'
the powershell script will look for the new .m4a file by created date.
the script will take the new file name and add it to the program syntax and into the 'transcribe-anything "%filename%.m4a" --device cpu --language en'

warning: use best practice where possible. feel free to research from the web to solve the powershell script

format: output will be into a powershell script that can be run periodically by a windows task scheduler

