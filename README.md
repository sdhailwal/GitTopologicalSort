# Git Topological Sort

The goal of this project is to read a git repository and list all of the commits in topological order.
This is done through using the directed acyclic graph that these commits always form. The program focuses 
on first reading the contents of the .git directory using the zlib library. Secondly, the program will get a 
list of all the local branch names. After this, a commit graph will be created; creating a parent-child relationship
between the commits. The commits are finally topologically sorted and printed to the user. 


To run this program

`python3 sort.py`

inside of a git repository. '


## Note:
Since we are dealing with graphs that will contain various different branches, there exists many different 
possible topological sorts. The program is designed to be determinsitic; therefore, the same results will always 
be viewed. 
