$appdataFolder = "$env:APPDATA\HEC\HEC-DSSVue"

Copy-Item .\src\*.py -destination "$appdataFolder\scripts"

$packages = "monitoring", "yaml", "toolbox"

ForEach ($package in $packages) {
    New-Item -type directory -force "$appdataFolder\scripts\$package"
    Remove-Item "$appdataFolder\scripts\$package\*$py.class"
    Copy-Item .\src\$package\* -destination "$appdataFolder\scripts\$package" -recurse
}
