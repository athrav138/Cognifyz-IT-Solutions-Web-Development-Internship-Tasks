
; Inno Setup Script for WebScraper Pro
; To use this:
; 1. Install Inno Setup (https://jrsoftware.org/isdl.php)
; 2. Open this file in Inno Setup
; 3. Click "Compile"

[Setup]
AppId={{C6B1B1B1-E1E1-4B1B-B1B1-B1B1B1B1B1B1}
AppName=WebScraper Pro
AppVersion=1.0
AppPublisher=WebScraper Pro Team
DefaultDirName={autopf}\WebScraper Pro
DefaultGroupName=WebScraper Pro
AllowNoIcons=yes
; Output file name
OutputBaseFilename=WebScraperPro_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; The executable created by PyInstaller
Source: "D:\Web Scrapper\dist\WebScraperPro.exe"; DestDir: "{app}"; Flags: ignoreversion
; Note: We don't need to add assets separately if they were bundled with --onefile/--add-data in build.py

[Icons]
Name: "{group}\WebScraper Pro"; Filename: "{app}\WebScraperPro.exe"
Name: "{autodesktop}\WebScraper Pro"; Filename: "{app}\WebScraperPro.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\WebScraperPro.exe"; Description: "{cm:LaunchProgram,WebScraper Pro}"; Flags: nowait postinstall skipifsilent
