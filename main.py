import functions, sys

if sys.argv[1] == 'HELP':
    print('HOW TO USE:'
          '\n    FIRST: (NON OPTIONAL) ENTER NAME OF FILE TO COMPILE (example.dml)'
          '\n    SECOND: (OPTIONAL) COMPILE INTO RAW DML (True or False)')

elif (sys.argv[1]).upper() == 'COMPILE':

    if len(sys.argv) > 2:
        path = sys.argv[2]
    else:
        path = None
    if len(sys.argv) > 3:
        compileIntoRaw = sys.argv[2]
        compileIntoRaw = compileIntoRaw.upper()
    else:
        compileIntoRaw = 'F'

    if compileIntoRaw == 'T' or compileIntoRaw == 'TRUE':
        compileIntoRaw = True
    elif compileIntoRaw == 'F' or compileIntoRaw == 'FALSE':
        compileIntoRaw = False
    else:
        raise Exception("PLEASE ENTER A VALID COMMAND\n >> (T, TRUE, FALSE, OR F)")

    if path is not None:
        validFile = False
        try:
            open('DML_Files/'+path, 'r')
            validFile = True
        except FileNotFoundError:
            raise Exception('PLEASE ENTER A REAL DML FILE')
    else:
        validFile = True

    if validFile and path is not None:
        functions.Compile_DML_file(path, compileIntoRaw)
    elif path is None:
        functions.Compile_DML_file(intoRaw=compileIntoRaw)
