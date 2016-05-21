import subprocess

def external_cmd(cmd, msg_in=''):
    try:
        proc = subprocess.Popen(cmd,
                   shell=True,
                   stdin=subprocess.PIPE,
                   stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,
                  )
        stdout_value, stderr_value = proc.communicate(msg_in)
        return stdout_value, stderr_value
    except ValueError as err:
        raise err
    except IOError as err:
        raise err

if __name__ == '__main__':
    stdout_val, stderr_val = external_cmd('dir')
    print 'Standard Output: %s' % stdout_val
    print 'Standard Error: %s' % stderr_val