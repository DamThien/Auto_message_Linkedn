credential = open('credentials.txt')
line = credential.readlines()
username = line[0]
password = line[1]
print(line)
message = open('message.txt')
customized_message = message.readlines()
print(customized_message)
