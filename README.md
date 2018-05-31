Convert-Invoke-Kerberoast
==========

Converts the output from Invoke-Kerberoast.ps1 into a hashcat format.

When using [Invoke-Kerberoast](https://github.com/EmpireProject/Empire/blob/master/data/module_source/credentials/Invoke-Kerberoast.ps1) and you output the hashes they aren't in the correct format to crack straight away with hashcat. You can manually handjam them, but if you get multiple hashes it can be trouble some. This script will output to the console or to a file to the right format.

Example:
```
python Convert-Invoke-Kerberoast.py -f tickets.txt -w hashes.txt
```


Hashcat:

```
hashcat hashes.txt -m 13100 -a 3
```
