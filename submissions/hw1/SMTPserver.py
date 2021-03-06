import re
def process_input():
    try:
        text = input()
        print(text) # echo the response
        return text
    except EOFError:
        quit()

def message250():
    print("250 OK",end="\r\n")
    
def message354():
    print("354 Start mail input; end with . on a line by itself",end="\r\n")
    
def message500():
    print("500 Syntax error: command unrecognized",end="\r\n")

def message501():
    print("501 Syntax error in parameters or arguments",end="\r\n")
    
def message503():
    print("503 Bad sequence of commands",end="\r\n")
    
def regularExpression(text,mail):
    mailFrom = re.match('MAIL\s+FROM:\s*<(\w+@(?:(?:[a-zA-Z0-9])+\.)+\w+)>\s*$', text)
    rcptto = re.match('RCPT\s+TO:\s*<(\w+@(?:(?:[a-zA-Z0-9])+\.)+\w+)>\s*$', text)
    data = re.match('(DATA\s*$)', text)
    
    # append to mail if no error exists
    if mailFrom:
        mail.append(mailFrom.group(0))
        return True
    elif rcptto:
        mail.append(rcptto.group(0))
        mail.append(rcptto.group(1))
        return True
    elif data:
        mail.append(data.group(1))
        return True
    else:
        return False


def check501Error(text,token,mail):
    if(token != 'mailFromToken' and token != 'dataToken' and token != 'rcptToken' ):
        return True
    if(token == 'mailFromToken'):
        if regularExpression(text,mail):
            message250()
            return False
        else:
            message501()
            return True
    elif(token == 'rcptToken'):
        if regularExpression(text,mail):
            message250()
            return False
        else:
            message501()
            return True
    elif(token == 'dataToken'):
        if regularExpression(text,mail):
            message354()
            return False
        else:
            message501()
            return True



# this function checks for 500 error and 503 error----whether token is spelled right and sequence right
#checkToken has to be used before check501Error
def checkToken(token, text):
    if(token != 'mailFromToken' and token != 'dataToken' and token != 'rcptToken' ):
        print('wrong token string')
        return False

    rcptToken = re.match('RCPT\s+TO:\s*', text)
    dataToken = re.match('DATA\s*', text)
    mailFromToken = re.match('MAIL\s+FROM:\s*', text)

    if(token == 'mailFromToken'):
        if(rcptToken or dataToken):
            message503()
            return False
        elif(mailFromToken):
            return True


    elif(token == 'dataToken'):
        if(rcptToken or mailFromToken):
            message503()
            return False
        elif(dataToken):
            return True

    elif(token == 'rcptToken'):
        if(mailFromToken or dataToken):
            message503()
            return False
        elif(rcptToken):
            return True

    message500()
    return False
    
def parseMAIL(mail):
    while(True):
        text = process_input()
        #check if token is out of order
        status = checkToken('mailFromToken', text)
        if(status == False):# if the token is not right, 500 or 503
            continue
        else:
            ErrorStatus501 = check501Error(text, 'mailFromToken',mail) # false if error free
            if (ErrorStatus501 == False):
                return True
            else:
                continue

def parseRCPT(mail):# check for RCPT
    while(True):
        text = process_input()
        #check if token is out of order
        status = checkToken('rcptToken', text)
        if(status == False):# if the token is not right, 500 or 503
            continue
        else:
            ErrorStatus501 = check501Error(text, 'rcptToken',mail) # false if error free
            if (ErrorStatus501 == False):
                return True
            else:
                continue

def parseDATA(mail):
    while(True):
        text =process_input()
        status = checkToken('dataToken', text)
        if(status == False):            # if the token is not right, 500 or 503
            continue
        else:
            ErrorStatus501 = check501Error(text,'dataToken',mail)
            if (ErrorStatus501 == False):
                content=[]
                while(True):
                    inputData = process_input()
                    content.append(inputData)
                    if (inputData.find('.') == 0):
                        j = 0
                        message250()
                        break
                mail.append(content)
                return True
            else:
                continue


def writeEmail(mail):
    fileName = "forward/"+'<'+mail[2]+'>'
    fileWriter = open((fileName), "a+")
    fileWriter.write(mail[0]+ "\r\n")     #mail
    fileWriter.write(mail[1]+ "\r\n")     #rcpt
    fileWriter.write(mail[3]+ "\r\n")     #data
    for i in range(len(mail[4])):
        receiver = mail[4][i]
        fileWriter.write(receiver+ "\r\n")


mailRecord = []

while(True):
    mail = []
    #mail[0] mail, mail[1], rcpt, mail[2] data
    mailFromstatus = parseMAIL(mail)
    if mailFromstatus == True:          # check for RCPT
        rcptStatus = parseRCPT(mail)
        if rcptStatus == True:
            parseDATA(mail)
            mailRecord.append(mail)
            writeEmail(mail)
    else:
        continue
