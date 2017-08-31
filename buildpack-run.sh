install_dir=graphviz
mkdir -p /app/.heroku/vendor/bin

BASE_DIR=`pwd`
wget http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.40.1.tar.gz
tar -zxf graphviz-2.40.1.tar.gz
pushd graphviz-2.40.1
./configure
make
mkdir -p $BASE_DIR/tmpdestdir/usr/local/bin
make install DESTDIR=$BASE_DIR/tmpdestdir
dot -c
popd
cp -R "tmpdestdir" "$BUILD_DIR/$install_dir"

script=$BUILD_DIR/.profile.d/graphviz.sh
echo "PATH=/app/$install_dir/usr/local/bin:\$PATH" > "$script"
echo "export GRAPHVIZ_DOT=/app/$install_dir/usr/local/bin/dot" >> "$script"
echo "export LD_LIBRARY_PATH=/app/$install_dir/usr/local/lib:\$LD_LIBRARY_PATH" >> "$script"
