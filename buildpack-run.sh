# install_dir=graphviz
mkdir -p /app/.heroku/vendor/bin

BASE_DIR=`pwd`
wget http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.40.1.tar.gz
tar -zxf graphviz-2.40.1.tar.gz
pushd graphviz-2.40.1
./configure --prefix=/app/graphviz --disable-shared
make
make install DESTDIR=$BASE_DIR/tmpdestdir
popd
cp -R "tmpdestdir" "$BUILD_DIR/graphviz"
