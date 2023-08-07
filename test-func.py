# member = "Thien Dam"

didntsent = ["Gokula Kandaswamy",
             "JONATHAN ARNOLD~ACA 🇱🇰, FCCA 🇬🇧, CPA 🇦🇺🇨🇦, (Triple Chartered Accountant and KPMG SoQM Manager) BSc. (Hons)🎓l Award-winning Auditor🏆l Musician🎸",
             "Tal Cohen",
             ]
member_names = ["Gokula Kandaswamy",
                "JONATHAN ARNOLD~ACA 🇱🇰, FCCA 🇬🇧, CPA 🇦🇺🇨🇦, (Triple Chartered Accountant and KPMG SoQM Manager) BSc. (Hons)🎓l Award-winning Auditor🏆l Musician🎸",
                "Tal Cohen", "CPE Ian Lashley", "Eng. Marcel Scheel", "Md. Mannat Sharma",
                "MSC CPA Nishchay Munot", "CPA, FMVA Norhan Mohamed Fawzy", "Kyra Alcivar"]
for member in member_names:
    # Skip sending a message to didn't send account
    if member in didntsent:
        continue
    try:
        message = open('content.txt')
        # firstname = ""
        prefixes = ["CPE","Eng.","Md.","CMA","MSC CPA","CPA","FCCA","CA","CPA, FMVA"]
        for prefix in prefixes:
            if member.startswith(prefix):
                firstname = member[len(prefix):].strip()
                break
            else:
                firstname = member
        # print(member)
        # print("Name after change:",firstname)
        with open('content.txt', encoding='utf-8') as message_file:
            customized_message = message_file.read()
            firstname = firstname.split()[0]
        send_message = str("Hi " + \
            firstname.capitalize() + ",\n" + customized_message)
        print(send_message)
    except Exception as e:
        print(f"Error sending message to {member}: {e}")
        exception_occurred = False
        continue
    # finally:
    #     print("OK")
b = 2
a = 2

b+=1
a=a+1
print(b,a)