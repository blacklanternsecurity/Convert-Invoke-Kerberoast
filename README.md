Convert-Invoke-Kerberoast
==========

Converts the output from Invoke-Kerberoast.ps1 into a hashcat format.

When using [Invoke-Kerberoast](https://gist.github.com/HarmJ0y/cc1004307157e372fc5bd3f89e553059) and you output the hashes they aren't in the correct format to crack straight away with hashcat. You can manually handjam them, but if you get multiple hashes it can be trouble some. This script will output to the console or to a file to the right format.

Example:
```
python Convert-Invoke-Kerberoast.py -f tickets.txt -w hashes.txt
```


Hashcat:

```
hashcat hashes.txt -m 13100 -a 3
```
