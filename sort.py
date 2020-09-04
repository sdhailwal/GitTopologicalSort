#!/usr/bin/python3
#Simran Dhaliwal
#UID 905361068
import sys, os, zlib, os.path
from os import path
class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.associated_branches = []
        self.children = set()



def checkDir():
    curr_dir = os.getcwd()
    if os.path.exists(curr_dir+"/.git") and os.path.isdir(curr_dir+"/.git"):
        return curr_dir  #return immediately from function because .git was found
    count = 0
    #to find number of parent directories
    for i in curr_dir:
        if i == '/':
            count += 1
   
    for x in range(0, count-1): # check all parent directories
        curr_dir = os.path.dirname(curr_dir)
        if os.path.exists(curr_dir+"/.git") and os.path.isdir(curr_dir+"/.git"):
            return curr_dir #return immediately from function because .git was found
    sys.stderr.write("Not inside a Git repository\n")
    exit(1)

def getBranchHash(branch_dir, branches, branch_list):

    for i in branch_list:
        with open(branch_dir+"/"+i, 'r') as f:
            hash_num = f.read();
            hash_num = hash_num[:-1]
            if hash_num not in branches:
                branches[hash_num] = []
                branches[hash_num].append(i)
            else:
                branches[hash_num].append(i)


def getNodes(curr_dir, all_nodes, branches):
    #create nodes for branches first
    stack = []
    all_nodes = {}
    for i in branches:
        node = CommitNode(i)
        node.associated_branches = branches[i]
        all_nodes[i] = node
    for curr_hash in sorted(branches.keys()):
        stack.append(curr_hash)
    while stack:
        print("Hello")
        curr_hash = stack.pop()
        getParents(all_nodes, curr_hash, curr_dir, stack)


#get parents of a child node        
def getParents(all_nodes, i, curr_dir, stack):
    filename =  curr_dir + "/" + i[:2] + "/" + i[2:]
    compressed_contents = open(filename, 'rb').read()
    decompressed_contents = zlib.decompress(compressed_contents)
    decompressed_contents = decompressed_contents.decode('utf-8')
    numberOfParents = decompressed_contents.count('parent')
    j = decompressed_contents.find('parent')

    while j != -1:
        hash_val = decompressed_contents[j+7:j+47]
        if hash_val in all_nodes:
            parent_node = all_nodes[hash_val]
        else:
            parent_node = CommitNode(hash_val)
            all_nodes[hash_val] = parent_node

        parent_node.children.add(i)
        all_nodes[i].parents.add(hash_val)
        stack.append(hash_val)
        j = decompressed_contents[j+6].find('parent')


def DFS_topo(all_nodes, root_commits):
    order = []
    visited = set()
    stack = list(root_commits)

    while stack:
        v = stack[-1]
        children_to_go = []
        for c in all_nodes[v].children:
            if c not in visited:
                children_to_go.append(c)
        if children_to_go:
            stack.append(children_to_go[0])
        else:
            stack.pop()
            order.append(v)
            visited.add(v)
    return order
            


def getChildren(all_nodes):
    for i in all_nodes:
        for j in sorted(all_nodes[i].parents):
            all_nodes[j].children.add(i)

def topo_order_commits():
    curr_dir = checkDir()
    curr_dir = curr_dir+"/.git"
    #retriving all local branches into a list
    branch_list = os.listdir(curr_dir+"/refs/heads")
    branch_dir = curr_dir+"/refs/heads"
    #fill dictionary with intial branches and their hashs
    all_nodes = {}
    branches = {}
    getBranchHash(branch_dir, branches, branch_list)

    curr_dir += "/objects"
    getNodes(curr_dir, all_nodes, branches)
    root_commits = []

    for i in all_nodes:
        print(i)
    
    for i in sorted (all_nodes):
        if len(all_nodes[i].parents) == 0:
            root_commits.append(i)
    order = DFS_topo(all_nodes, root_commits)
    
    stickyEnd = False
    stickyStart = False
    for i in range(0, len(order)):
        curr_hash = order[i]
        next_hash = "-1"
        if i != len(order)-1:
            next_hash = order[i+1]
        if next_hash not in all_nodes[curr_hash].parents and next_hash != "-1":
            stickyEnd = True
        else:
             stickyEnd = False

        if stickyStart:     
            child_commits = ""
            for i in all_nodes[curr_hash].children:
                child_commits += i + " "
            if(len(child_commits) != 0):
                child_commits = "=" + child_commits[1:]
            else:
                child_commits = "="
            stickyStart = False
            print(child_commits)
        #print current regardless
        bs = ""
        for i in sorted(all_nodes[curr_hash].associated_branches):
            bs += " "+i
        print(curr_hash + bs)

        if stickyEnd:
            parent_commits = ""
            for i in all_nodes[curr_hash].parents:
                parent_commits += " " + i
            parent_commits += "="
            if len(parent_commits) == 1:
                print("=")
            else:
                print(parent_commits[1:])
            print()
            stickyStart = True
            
if __name__=="__main__":
    topo_order_commits()

