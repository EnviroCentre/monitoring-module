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
!define MUI_FINISHPAGE_RUN $INSTDIR\HEC-DSSVue.exe
!define MUI_FINISHPAGE_RUN_TEXT "Open HEC-DSSVue"

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

Section "Install module scripts"
    SetOutPath "$APPDATA\HEC\HEC-DSSVue\scripts"
    File /r "..\..\src\*.py"
SectionEnd

Section "Example tool configuration files"
    SetOutPath "$DOCUMENTS\Monitoring Module"
    File "..\..\src\*.yml"
SectionEnd
