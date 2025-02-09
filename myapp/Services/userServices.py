from myapp.Dal.userDal import UserDao
from myapp.Models.userModel import User


class UserManage:
    def __init__(self)->None:
        self.userDao=UserDao()
        
    def listUsers(self)->list[User]:
        return self.userDao.getusers()
    
    def auth(self,login:str,password:str)->User|None:
        return self.userDao.auth(login,password)    

    def register(self,email:str,username:str,password:str)->bool:
        return self.userDao.register(email,username,password)
