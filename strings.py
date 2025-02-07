class StringManipulator:
    
    def getString(self):
        self.user_string = input("Enter a string: ")

    def printString(self):
        print(self.user_string.upper())

manipulator = StringManipulator()
manipulator.getString()  
manipulator.printString() 
