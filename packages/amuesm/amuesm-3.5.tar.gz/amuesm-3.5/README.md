amuesm let's you not only create passwords with custom requirements, it can also encode and decode strings in your own custom charset! amuesm stand for:

- Annie's 
- Multi
- Use
- Encryption
- Security
- Module


___

**DISCLAIMER**

It is recommended that amuesm should only be used in your own custom databases/servers, amuesm is not secure to use when creating passwords for products like Google. We are also not responsible for any harm according to the MIT license.
___

createpass: (Creates a random password of your liking!)
```python
import amuesm

print(amuesm.createpass(['a', 'b'], 5))
```
Output: (EXAMPLE, RESULTS WILL VARY)
baaba

___

en: (Encodes text of your choice with your own custom charset!)
```python
import amuesm

print(amuesm.en('abc', ['a', 'b', 'c']))
```
Output:
```
- -- ---
```
___

de: (Decodes text of your choice with your own custom charset!)
```python
import amuesm

print(amuesm.de('- -- ---', ['a', 'b', 'c']))
```
Output:
```
abc
```
___

Extra features:

If you would like to use amuesm as a standalone tool, run in your terminal:
```
amuesm
```
and you'll be able to select all three of our features!

If you would like to add credits to your project, just do:

```python
import amuesm

amuesmcredits()
```
___

Thanks for reading, and enjoy amuesm! :)
