wget http://www.graphviz.org/pub/graphviz/stable/SOURCES/graphviz-2.40.1.tar.gz
tar -zxf graphviz-2.40.1.tar.gz
cd graphviz-2.40.1
./configure --prefix=/app/graphviz
make
make install

