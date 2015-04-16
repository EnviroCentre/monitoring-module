$appdataFolder = "$env:APPDATA\HEC\HEC-DSSVue"

Copy-Item .\src\*.py -destination "$appdataFolder\scripts"

$packages = "monitoring", "yaml"

ForEach ($package in $packages) {
    New-Item -type directory -force "$appdataFolder\lib\$package"
    Remove-Item "$appdataFolder\lib\$package\*$py.class"
    Copy-Item .\src\$package\* -destination "$appdataFolder\lib\$package" -recurse
}
