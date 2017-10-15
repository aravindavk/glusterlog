dev:
	mkdir -p build
	g++ src/main.cpp -o build/gluster-log

install:
	mkdir -p build
	g++ -O3 src/main.cpp -o build/gluster-log
	sudo cp build/gluster-log /usr/bin/gluster-log

uninstall:
	sudo rm /usr/bin/gluster-log

clean:
	rm -rf build
