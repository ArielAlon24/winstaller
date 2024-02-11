# Winstaller

A script to automatically install various software for Windows.

## Usage

1. Clone this repo or download it.

2. Open PowerShell as an Administrator, this can be done by right clicking the Windows icon and the clicking on the PowerShell(Admin) option.

3. Navigate to the repo's folder.

4. Use the command `Set-ExecutionPolicy Unrestricted` (this allows PowerShell to install software), then answer the popped up dialog with `A` - Yes To All.

5. Now you are ready to go - use the command `.\winstaller.ps1` to execute winstaller and after couple of minutes you'll be set!.

## In The Future

- [ ] Multiple processes simultaneously.
- [ ] Using a temp folder instead of manually removing installers.
- [ ] Removing the need to provide a installer path in the `Program` constructor.
- [ ] Using the `pathlib` module instead of bare strings.
- [ ] Creating a logger for each `Program` instance.
