#!/usr/bin/env python
# --------------------------------------------------------------
# Script used to write commit time for each file
# --------------------------------------------------------------
from commands import getstatusoutput


def find_change_dates(current_dir):
    status, path_sct = getstatusoutput('echo $SCT_DIR')
    path = str(current_dir)+'/scripts'
    print path
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [ f for f in listdir(path) if isfile(join(path,f)) ]
    modif_list = {}

    for file in onlyfiles:
        print file
        print os.getcwd()
        if file.startswith("sct") and ".pyc" not in file:
            change_found = False
            tatus, output = getstatusoutput("git --git-dir ../.git --work-tree .. log "+path+"/"+file)
            print output
            output_list = output.split("\n")

            for line in output_list:
                if "Date:" in line and change_found is False:
                    date = line.split(":   ")
                    change_found = True
                    modif_list[file] = date[-1]
                    print modif_list[file]

    return modif_list


# This change is a test
def find_staged_files():

    status, output = getstatusoutput("git diff --cached")

    output_list = output.split("\n")

    staged_files = []
    a = iter(output_list)

    for line in a:
        if line.startswith("index"):
            line_next = ""
            try :
                line_next = next(a)
            except StopIteration, e:
                print e.message
            if line_next.startswith("---"):
                target_list = line_next.split("/")
                for substr in target_list:
                    if "." in substr:
                        staged_files.append(substr)
                        # modify/add to modifs.txt
    return staged_files


def save_changed_files(staged_files, sct_dir):
    status, path_sct = getstatusoutput('echo $SCT_DIR')
    modif_fname = str(sct_dir)+'/bin/modif.txt'
    print modif_fname
    f = open(modif_fname, "w+")
    for script_name, date in staged_files.iteritems():
        date_split = date.split("-")[0]
        date_without_time_zone = date_split
        f.write(script_name + " = " + date_without_time_zone+"\n")
    f.close()
    # status, path_sct = getstatusoutput('cp '+modif_fname+" "+path_sct+"/dev/modif_backup.txt")

    # add
    status, output = getstatusoutput("git add "+modif_fname)


def save_changed_files_and_date(staged_files):
    # Test change
    pass

if __name__ == "__main__":

    # call main function
    import os
    current_dir = os.getcwd()
    status, path_sct = getstatusoutput('echo $SCT_DIR')
    path = str(current_dir)+'/scripts'
    os.chdir(path)
    try:
        changed_files = find_change_dates(current_dir)
        save_changed_files(changed_files, current_dir)
    except Exception, e:
        print e.message
    os.chdir(current_dir)
