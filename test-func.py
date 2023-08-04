member = "Thien Dam"

message = open('content.txt')
with open('content.txt', encoding='utf-8') as message_file:
    customized_message = message_file.read()
    send_message = "Hi " + \
        member.split()[0] + ",\n" + customized_message
print(send_message)


[]