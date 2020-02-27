#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 10:16:35 2020

@author: leonardo
"""

import os
import shutil
from git import Repo
import matplotlib.pyplot as plt

def list_file_tex(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".tex"):
                print(os.path.join(root, file))

def create_dir(dirName):
    # dirName = 'tempDir2/temp2/temp'
    # Create target directory & all intermediate directories if don't exists
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print("Directory " , dirName ,  " Created ")
    else:    
        print("Directory " , dirName ,  " already exists")
        
def delete_temp_dir(dirName):
    # Delete target directory & all intermediate directories if exists
    if os.path.exists(dirName):
        shutil.rmtree(dirName)
        print("Directory " , dirName ,  " Deleted ")
    else:    
        print("Directory " , dirName ,  " does not exist")
        
def count_diff_between_commit(input_file):
    cnt_added_lines = 0
    cnt_sub_lines = 0
    cnt_added_letters = 0
    cnt_sub_letters = 0
    with open(input_file) as fp:
        lines = fp.readlines()
        cnt_added_lines = 0
        cnt_sub_lines = 0
        for line in lines:
            if line[0] == "+" and line[1] != "+":
                cnt_added_lines = cnt_added_lines + 1
                cnt_added_letters = cnt_added_letters + len(line) - 1
            if line[0] == "-" and line[1] != "-":
                cnt_sub_lines = cnt_sub_lines + 1
                cnt_sub_letters = cnt_sub_letters + len(line) - 1
    return cnt_added_lines, cnt_sub_lines, cnt_added_letters, cnt_sub_letters

if __name__ == "__main__":
    # os.system("pwd")
    dirName = "_analysis_evolution_tmp"
    print("starting analysis tex")
    #list_file_tex("./Template02")
    create_dir(dirName)
    folder_name = "/path/to/your/git_repo"
    repo = Repo(folder_name)
    assert not repo.bare
    assert not repo.is_dirty() 
    heads = repo.heads
    master = heads.master       # lists can be accessed by name for convenience
    # log_obj = master.log()
    # fifty_first_commits = list(repo.iter_commits('master', max_count=50))
    all_commits = list(repo.iter_commits('master'))
    number_commits = len(all_commits)
    number_commits = len(all_commits)
    """
    all_commits[0].hexsha
    all_commits[0].parents
    all_commits[0].author
    all_commits[0].author.name
    all_commits[0].committer<.name>
    all_commits[0].message
    """
    # hcommit = repo.head.commit 
    headcommit = repo.head.commit
    print("0/" + str(number_commits-1) + " ---> " + headcommit.hexsha)
    git = repo.git
    string=git.diff('HEAD~1')
    f=open(dirName + "/difference.diff","w")
    f.write(string)
    f.close()

    # to read carefully https://stackabuse.com/read-a-file-line-by-line-in-python/
    output = [None] * number_commits
    
    output[0] = count_diff_between_commit(dirName + "/difference.diff")
    
    for i in range(1, number_commits-1):
        repo.head.reference = repo.commit('HEAD~1')
        headcommit = repo.head.commit
        print(str(i) + "/" + str(number_commits-1) + " ---> " + headcommit.hexsha)
        git = repo.git
        try:
            string=git.diff('HEAD~1')
        except:
            number_commits = i
            break
        f=open(dirName + "/difference.diff","w")
        f.write(string.encode('utf-8', 'surrogateescape').decode('ISO-8859-1'))
        f.close()
        output[i] = count_diff_between_commit(dirName + "/difference.diff")
    
    repo.head.reference = master
    delete_temp_dir(dirName)
    output = output[:number_commits]
    added_lines = [None] * len(output)
    sub_lines = [None] * len(output)
    added_letters = [None] * len(output)
    sub_letters = [None] * len(output)
    for i in range(len(output) - 1):
        added_lines[i] = output[i][0]
        sub_lines[i] = output[i][1]
        added_letters[i] = output[i][2]
        sub_letters[i] = output[i][3]
    figObject1 = plt.figure();
    
    ax1 = figObject1.add_subplot(111)    
    plt.plot(added_lines, label='line added')
    plt.plot(sub_lines, label='line deleted')
    # plt.plot(added_letters)
    # plt.plot(sub_letters, label='letters deleted')
    ax1.set_xlabel('Commit')
    ax1.set_ylabel('Number of #')
    plt.title("Work Evolution with Git")
    ax1.legend()
