# TreeCrypt

## Basic Info
- Creates a random structure of nodes pointing to one another and converts them into an array.
- Maps each letter into a set of directions to a node which contains the equivalent letter inside it.
- During decryption, the directions can be used to find a node and extract the letter inside it.


## Detailed Working
- A tree of nodes is generated based on a set of rules.
- The process starts with a default root node.
- Nodes are recursively and randomly attached to existing nodes, beginning from the root.
- Each node attempts to connect to up to three other nodes, making several attempts to find valid positions.
- Node and edge placement avoids any intersections with other nodes or edges. If a suitable position can't be found after several tries, the process skips that attempt and continues elsewhere, increasing randomness.
- The final structure is a non-intersecting tree where each node contains a randomly selected character from a predefined character set.
- A dictionary is built, mapping each character in the character set to a list of pointers referencing all nodes containing that character.
- To encode a message:
  - The algorithm uses the dictionary to randomly select a node corresponding to each character.
  - From each selected node, it backtracks to the root to generate a path (a sequence of directions).
  - Each character in the input is replaced by its corresponding path, with paths separated by dots "`.`".
- The special character "`|`" is used to represent whitespace.
  - Regardless of the number of spaces in the input, all contiguous whitespace is encoded as a single "`|`".



# How to use

## 1. Import
Download the `TreeCrypt.py` file from the repository into your workspace.

Inside your python code add the line
```python
from TreeCrypt import KeyMaker, Crypter
```

This will import the key generator and the crypt-maker as classes and these can be used to do the encryption

## 2. Create a key
If you already have the key and dictionary, then skip to step 4

First of all you need a charset.

The charset used must be a list of characters which are exactly one letter and are eligible to be a python dictionary's  key

```python
customCharset = ['A' , 'B', 'C', ....]
myKeyMaker = KeyMaker(customCharset)
```

Then generate the key using

```python
myKeyMaker.GenerateKey(20, 10, 5)

# Note the format of the parameters
def GenerateKey(self, Depth, MaxDistance, MinDistance = 0):

# You can ignore the last parameter since it has a default value
```

The parameters are the depth of the tree and the maximum & minimum distance between connected nodes.

## 3. Export the key
Now you can export the key as a .txt file

```python
myKeyMaker.Export("KEY1.txt", "DICT1.txt")

# Note the format of the parameters
def Export(self, keyFile="key.txt", dictFile="dict.txt"):
# You can ignore the parameters as they have defaults
```

The parameters are the filenames of the exported key and dictionary.

## 4. Create a crypter and Import the key
Using the Crypter class, create an object that will encrypt and decrypt text using the previously exported key. If you already have a key then you can skip to over here.

Remember that a text can only be decrypted using the same key with which it was encrypted.

```python
myCrypter = Crypter()
myCrypter.Import("KEY1.txt", "DICT1.txt")

# Make sure that you are using the correct file names for import

def Import(self, keyFile="key.txt", dictFile="dict.txt"):
# Import uses same format as Export of KeyMaker
# You can ignore the parameters if the inputs have the default file names
```

## 5. Start Crypting!!
Now you can encrypt and decrypt as you wish. However make sure the input doesn't contain anything outside of the custom charset used by the KeyMaker

```python
cipher = myCrypter.Encrypt("TreeCrypt is AMAZING")
doubleCheck = myCrypter.Decrypt(cipher)

print(cipher)
print(doubleCheck)
```

## Additional Function
Both classes have a `DarwKey()` function which displays a graphical version of the key
```python
myCrypter.DrawKey()
```

# Why to use??

Don't want to save your passwords online? Save them locally as a .txt file and use TreeCrypt to encrypt them.

<br class="big-spacer">