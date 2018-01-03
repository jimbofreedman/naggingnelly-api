install_dir=graphviz
mkdir -p /app/.heroku/vendor/bin

BASE_DIR=`pwd`
wget https://graphviz.gitlab.io/pub/graphviz/stable/SOURCES/graphviz.tar.gz
tar -zxf graphviz.tar.gz
pushd graphviz-2.40.1
./configure
make
mkdir -p $BASE_DIR/tmpdestdir/usr/local/bin
make install DESTDIR=$BASE_DIR/tmpdestdir
popd
cp -R "tmpdestdir" "$BUILD_DIR/$install_dir"

cd "$BUILD_DIR/$install_dir"
export LD_LIBRARY_PATH="$BUILD_DIR/$install_dir/usr/local/lib:\$LD_LIBRARY_PATH"
"$BUILD_DIR/$install_dir"/usr/local/bin/dot -c

script=$BUILD_DIR/.profile.d/graphviz.sh
echo "PATH=/app/$install_dir/usr/local/bin:\$PATH" > "$script"
echo "export GRAPHVIZ_DOT=/app/$install_dir/usr/local/bin/dot" >> "$script"
echo "export LD_LIBRARY_PATH=/app/$install_dir/usr/local/lib:\$LD_LIBRARY_PATH" >> "$script"
