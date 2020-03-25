# cpei35775_config_pack
Configuration packing and unpacking utility for the Motorola CPEi 35775 written in Python3. No external dependencies.

Thanks to [this covertbay.com article](https://rootshell.covertbay.com/2011/08/motorola-wimax-cpei-35775-configuration.html)[^1]
for providing tools to dowloand and re-upload the packed config files from the divce, and for pointing out the header layout of the file. However that page fails to mention that what it calls "checksum" is actually generated using the `cksum` unix utility. See [this page](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/cksum.html) for the method, which I included in config_pack.py

I successfully unpacked, patched, re-packed and uploaded a config to my device. Sadly no SSH access for far, but I'll keep trying.

[^1]: http://archive.is/TuNge In case it goes down. The download and upload utilities both make a POST request to `http://<device>/cgi-bin/firmwarecfg` with form name `dwnconfig` and `impConfiguration`, respectively.
