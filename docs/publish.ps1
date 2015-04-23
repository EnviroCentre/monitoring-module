git checkout gh-pages
git read-tree master:docs/build
git commit -m'gh-pages documentation'
git push origin gh-pages
git checkout master
