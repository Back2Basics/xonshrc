###
# my .xonshrc file
# rename this to .xonshrc and put in your home directory
###
import pandas as pd

$PATH=["/Users/jlangley/miniconda3/envs/py3k/bin","/Users/jlangley/miniconda3/bin","/usr/local/bin","/usr/bin","/bin","/usr/sbin","/sbin"]
source-bash activate py3k
def reformat_line(line):
    """ 'mounted on' is misparsed if volume or column name has spaces"""
    data = line[:8]
    mounted = ' '.join(line[8:])
    data.append(mounted)
    return data

def diskfree():
    diskfree_output = $(df -l).split('\n')[:-1] #take out extra carrage return
    diskfree_data = [line.split() for line in diskfree_output]
    diskfree_data = list(map(reformat_line, diskfree_data))
    titles = pd.Series(diskfree_data[0]) #"Mounted on" is misparsed
    diskfree_data = pd.DataFrame(diskfree_data[1:], columns=titles.values)
    diskfree_data.Capacity = diskfree_data.Capacity.str.strip('%').astype(float)

    output = ''
    for x in diskfree_data[['Mounted on', 'Capacity']][diskfree_data.Capacity>=97].values:
        output+='{color}{0}={1:.2f}% full '.format(x[0], x[1], color="{BOLD_RED}")
    for x in diskfree_data[['Mounted on', 'Capacity']][diskfree_data.Capacity<97].values:
        output+='{color}{0}={1:.2f}% full '.format(x[0], x[1], color="{BOLD_GREEN}")
    return output

def get_current_environment():
    """ changing current environements doesn't work currently"""
    current_env = $(conda info --envs)
    for line in current_env:
        if '*' in line:
            return line.split()[0]

$PROMPT = '{BOLD_GREEN}'+$(uptime)+diskfree()+'\n'
$PROMPT += '{WHITE}('+get_current_environment()+') {BOLD_BLUE}{cwd}{branch_color}{curr_branch} {BOLD_BLUE}:{NO_COLOR} '


