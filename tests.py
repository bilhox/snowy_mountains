class Burger:
     
     class BigMac:
          
          def __init__(self):
               pass
     
     def __init__(self):
          self.name = "Burger"
          self.author = "MacDonald"
     
     def gift(self , name):
          print(f"{self.author} a donné un {self.name} à {name}")

burger = Burger()
burger.gift("Jean claude")