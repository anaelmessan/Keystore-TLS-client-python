# OpenSSL
## Note on TLS_AES_128_CCM_SHA256
`TLS_AES_128_CCM_SHA256` does not appear as a valid cipher using `openssl ciphers ALL` or any other command, though it can be used. Python `ssl` module relies on the list of cipher given by the ssl library, which `TLS_AES_128_CCM_SHA256` isn't part of. We will fix that.  

### Find where to add TLS_AES_128_CCM_SHA256
Where does TLS_AES_256_GCM_SHA384 (a TLS 1.3 ciphersuite considered valid and default by the library) vs TLS_AES_128_CCM_SHA256 appear in the code?  
>`grep -rnw './' -e 'TLS_AES_256_GCM_SHA384'`  
>`grep -rnw './' -e 'TLS_AES_128_CCM_SHA256'`  

In OpenSSL 3.5.2, omitting documentation code and test, we find 2 places where TLS_AES_128_CCM_SHA256 doesn't appear but `TLS_AES_256_GCM_SHA384` does :
>`include/openssl/ssl.h.in:202:#  define TLS_DEFAULT_CIPHERSUITES "TLS_AES_256_GCM_SHA384:"`  
>`ssl/ssl_ciph.c:2249:    return "TLS_AES_256_GCM_SHA384:"`

### What to edit ?
In both files, we replace the list of ciphers by `TLS_AES_128_CCM_SHA256` to force python `ssl` to use it, since as of python 3.13, the selection of ciphersuite is not implemented.  

The displayed version can be edited in `VERSION.dat`, useful for testing.

### How to compile

>./Configure
>make clean && make


### How to run
>LD_LIBRARY_PATH=<.so files directory path> apps/openssl version  
>LD_LIBRARY_PATH=<.so files directory path> python App.py  

Note: the default path is the source code path.

