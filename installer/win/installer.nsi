!include MUI2.nsh

!define APP_NAME "Monitoring Module for HEC-DSSVue"
;!define VERSION "0.1.0" ; should be set by `makensis` argument e.g. `/DVERSION=0.0.0`

!define ORG_NAME "EnviroCentre"
!define ORG_URL "http://www.envirocentre.co.uk"

; Interface settings
!define MUI_WELCOMEPAGE_TITLE "${APP_NAME} ${VERSION} setup"
!define MUI_WELCOMEPAGE_TEXT "A set of scripts for managing environmental monitoring data within the HEC-DSSVue software.$\r$\n$\r$\nPlease close HEC-DSSVue before continuing."
!define MUI_COMPONENTSPAGE_NODESC

!define MUI_FINISHPAGE_LINK "${ORG_NAME} website"
!define MUI_FINISHPAGE_LINK_LOCATION "${ORG_URL}"
!define MUI_FINISHPAGE_SHOWREADME "https://envirocentre.github.com/monitoring-module"
!define MUI_FINISHPAGE_SHOWREADME_TEXT "Read the manual"

Name "${APP_NAME}"

!define OUTFILENAME "${APP_NAME}-${VERSION}-win32.exe"
OutFile "..\..\dist\${OUTFILENAME}"
InstallDir "$PROGRAMFILES\HEC\HEC-DSSVue"
RequestExecutionLevel highest

; Installer pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Language settings
!insertmacro MUI_LANGUAGE "English"

Section "Module scripts"
    SetOutPath "$APPDATA\HEC\HEC-DSSVue\scripts"
    File "..\..\src\*.py"

    SetOutPath "$APPDATA\HEC\HEC-DSSVue\scripts\monitoring"
    File "..\..\src\monitoring\*.py"

    SetOutPath "$APPDATA\HEC\HEC-DSSVue\scripts\toolbox"
    File "..\..\src\toolbox\*.py"
SectionEnd

Section "Python libraries"
    SetOutPath "$InstDir\jython\lib\site-packages"
    File /r "..\..\src\lib\*.py"
SectionEnd
