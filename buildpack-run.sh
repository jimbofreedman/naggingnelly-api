install_dir=graphviz

wget http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.40.1.tar.gz
tar -zxf graphviz-2.40.1.tar.gz
cd graphviz-2.40.1
./configure --prefix=/app/$install_dir
make
make install

mkdir -p $1/.profile.d
script=$1/.profile.d/graphviz.sh
echo "PATH=/app/$install_dir/usr/bin:\$PATH" >"$script"
# The variable GRAPHVIZ_DOT is needed by some applications (e.g. PlantUML)
echo "export GRAPHVIZ_DOT=/app/$install_dir/usr/bin/dot" >>"$script"
# If shared libraries were installed (necessary on Heroku-16), set load path
((${#packages[@]} > 1)) &&
  echo "export LD_LIBRARY_PATH=/app/$install_dir/usr/lib:\$LD_LIBRARY_PATH" >>"$script"

echo "Successfully installed Graphviz $graphviz_version" | a
echo "Verify installation with \"heroku run dot -V\"" | i
echo
