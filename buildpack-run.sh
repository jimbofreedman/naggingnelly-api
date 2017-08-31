install_dir=graphviz

wget http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.40.1.tar.gz
tar -zxf graphviz-2.40.1.tar.gz
cd graphviz-2.40.1
./configure --prefix=$BUILD_DIR/$install_dir
make
make install

echo "INSTALL COMPLETE"
echo "BUILD_DIR is $BUILD_DIR"
echo "INSTALL_DIR is $install_dir"

mkdir -p $BUILD_DIR/.profile.d
echo $BUILD_DIR
script=$BUILD_DIR/.profile.d/graphviz.sh
echo "SCRIPT is $script"
echo "PATH=$BUILD_DIR/$install_dir/usr/bin:\$PATH" >"$script"
# The variable GRAPHVIZ_DOT is needed by some applications (e.g. PlantUML)
echo "export GRAPHVIZ_DOT=$BUILD_DIR/$install_dir/usr/bin/dot" >>"$script"
# If shared libraries were installed (necessary on Heroku-16), set load path
echo "export LD_LIBRARY_PATH=$BUILD_DIR/$install_dir/usr/lib:\$LD_LIBRARY_PATH" >>"$script"

echo "Successfully installed Graphviz $graphviz_version"
echo "Verify installation with \"heroku run dot -V\""
echo
