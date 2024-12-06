## Adding ONLY main executable here ~1.5mb.

I will copy the main executable from here to the container and download the model in the container itself. This way the build is not bloated. 
This executable is dynamically linked to some C++ libraries.

```
	ajafri@ajafri-GF75-Thin-9SC:~/Desktop/journaly/whisper$ ldd ./main
	linux-vdso.so.1 (0x00007ffcde5e1000)
    libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 		 (0x00007eb492200000)
	libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007eb49258f000)
	libgomp.so.1 => /lib/x86_64-linux-gnu/libgomp.so.1 (0x00007eb492538000)
	libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007eb49250b000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007eb491e00000)
	/lib64/ld-linux-x86-64.so.2 (0x00007eb49285e000)
```
Out of all these, we need to install libstdc++ and libgomp1 to run this executable as they aren't provided by default in python:3.12-slim base image
