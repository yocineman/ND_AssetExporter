#coding:utf8

def main(file_path):
    shaped_lines = []
    with open(file_path) as f:
        lines = f.readlines()
    for line in lines:
        # line = line.replace('\n', '')
        if line.startswith(' u\''):line.replace(' u\'', '\'')
        if line.startswith(' u\''):line.replace(' u\'', '\'')
        # if line.startswith('Error: '): continue
        if line.startswith('Warning: '): continue
        if line.startswith('Read '): continue
        if line.startswith('the data object '): continue
        if line.startswith('File read '): continue
        if line.startswith('\'NoneType\' object'):continue
        if line.startswith('No attribute was specified.'):continue
        if line.startswith('no imp'):continue
        if 'AbcImport' in line:continue
        if 'has no attribute \"ai' in line:continue
        if 'No object matches name: .ai' in line:continue
        if '"mtoa", was not found' in line:continue
        if 'aov_' in line:continue
        if 'aovs' in line:continue
        if 'has no \'ai_' in line:continue
        if 'has no \'.ai_' in line:continue
        if 'UI commands can\'t be run' in line:continue
        if line.startswith('Error: line 1: Error reading'):continue
        if line.startswith('Failed to execute userSetup.py'):continue
        if line.startswith('Traceback (most recent call last):'):continue
        if line.startswith('  File '):continue
        if line.startswith('    if not cmds.commandPort'):continue
        if line.startswith('RuntimeError: Maya command error'):continue
        if line.startswith('list.remove(x)'):continue
        if line.startswith('Result: '):continue
        if line.startswith('get CurrentContext Error'):continue
        if line.startswith('The attribute is compound with mixed type elements.'):continue
        if line.startswith('Message attributes have no data values.'):continue
        if line == '\n': continue
        if line == '': continue
        if line == '\r': continue
        if line == ' ':continue
        if line == '\r\n': continue
        shaped_lines.append(line)
    with open(file_path, 'w+') as f:
        f.writelines(shaped_lines)
