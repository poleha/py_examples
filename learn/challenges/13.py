#http://www.pythonchallenge.com/pc/return/disproportional.html

from xmlrpc.client import ServerProxy

phonebook = ServerProxy('http://www.pythonchallenge.com/pc/phonebook.php')

print(phonebook.system.listMethods())
#['phone', 'system.listMethods', 'system.methodHelp', 'system.methodSignature', 'system.multicall', 'system.getCapabilities']
print(phonebook.system.methodHelp('phone'))
#Returns the phone of a person
print(phonebook.phone('Bert')) #???
# 555-ITALY