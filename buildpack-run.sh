# install_dir=graphviz
mkdir -p /app/.heroku/vendor/bin

BASE_DIR=`pwd`
wget http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.40.1.tar.gz
tar -zxf graphviz-2.40.1.tar.gz
cd graphviz-2.40.1
./configure --prefix=/app/graphviz --disable-shared
make
make install DESTDIR=$BASE_DIR/tmpdestdir
cd $BASE_DIR
cp -R "tempdestdir" "$BUILD_DIR/graphviz"
