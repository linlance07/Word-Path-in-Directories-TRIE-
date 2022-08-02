import os
from collections import defaultdict

search_res_count = []
search_res_lexi = []
search_file = []

class Node:
    def __init__(self):
        self.children = defaultdict(Node)
        self.eow = False
        self.file = defaultdict(lambda:[0,""])
        self.isfile = False
        self.folder = defaultdict(lambda:["",""])


class WordSearch:
    def __init__(self):
        self.root = Node()

    def insert(self,word,fname,path_link,isfile):
        temp = self.root
        for l in word:
            if l.isalpha() or isfile:
                if l not in temp.children:
                    temp.children[l] = Node()
                temp = temp.children[l]
        if not isfile:
            temp.eow = True
            temp.file[fname][0] += 1
            temp.file[fname][1] = path_link
        else:
            temp.isfile = isfile
            temp.folder[word][0] = path_link
            temp.folder[word][1] = fname

    def search(self,word):
        temp = self.root
        for l in word:
            if l not in temp.children:
                return
            temp = temp.children[l]

        def further_search(temp,new_word):
            if temp.isfile:
                search_file.append((temp.folder[new_word][1],temp.folder[new_word][0]))
            if temp.eow:
                for files in temp.file:
                    search_res_lexi.append(">> {} ({}) ---> {} ; Path: {}".format(new_word,temp.file[files][0],files,temp.file[files][1]))
                    search_res_count.append((temp.file[files][0],">> {} ({}) ---> {} ; Path: {}".format(new_word,temp.file[files][0],files,temp.file[files][1])))
            for nxt in temp.children:
                further_search(temp.children[nxt],new_word+nxt)
        further_search(temp,word)


path = "C:/Users/Colin Rolance D/PycharmProjects/wordsuggest"
os.chdir(path)

wordsuggestor = WordSearch()


def read_text_file(file_path):
    with open(file_path, 'r') as f:
        return f.read().split()


array = defaultdict(list)
for root, dirs, files in os.walk(path):
    # print(dirs,f"{root}\{dirs[0]}")
    for dirr in dirs:
        wordsuggestor.insert(dirr.lower(),dirr,f"{root}\{dirr}",1)
    for file in files:
        if file.endswith(".txt"):
            file_path = f"{root}\{file}"
            array[file] = (read_text_file(file_path),file_path)


for File in array:
    for word in array[File][0]:
        if word[-1].isalpha():
            n = len(word)
        else:
            n = len(word) - 1
        if n >= 6:
            wordsuggestor.insert(word.lower(),File,array[File][1],0)

string = input("Enter the word to be searched: ")
print()
print("***** WORD SEARCH BASED ON SORTING THE SUGGESTED WORDS *****")
print()
wordsuggestor.search(string)
if not search_res_lexi:
    print("Sorry there is no such word, Try Again!")
else:
    search_res_lexi.sort()
    for res in search_res_lexi:
        print(res)
print()
print("***** WORD SEARCH BASED ON COUNT & SUGGESTION *****")
print()
if not search_res_count:
    print("Sorry there is no such word, Try Again!")
else:
    search_res_count.sort(reverse = True)
    for res in search_res_count:
        print(res[1])
print()
print("***** FILE SEARCH *****")
for file in search_file:
    print(">> {} --> {}".format(file[0],file[1]))
print()
print("*******************************************************************")




