$args = 'describe', '--tags', '--always'
$cmd = 'git'
$tag = & $cmd $args
$version = $tag.TrimStart('v')

$args =  "/DVERSION=$version", "installer.nsi"
$cmd = "$env:NSIS_HOME\makensis.exe"
& $cmd $args
