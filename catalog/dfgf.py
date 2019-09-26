class register:
    def _init_(self,name,des):
        self.name=name
        self.des=des
    def login(self):
        print("Login completed "+self.name)
object=register("gani","student")

print(object.name)
object.login()