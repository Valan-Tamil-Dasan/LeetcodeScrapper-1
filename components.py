import requests
from bs4 import BeautifulSoup
from pandas import Series, DataFrame
import time

class User:
    """
        Simulates one LeetCode User
    """
    def __init__(self, username='/'):
        """
            Constructor function that takes in the arguement 'username' and detects if 
            such a LeetCode username exists
        """

        if username == '/':
            print('Pass Username in the User Constructor to START...')
            return
        
        self.username = username
        self.url = f'https://www.leetcode.com/{username}'

        test_response = requests.get(self.url)
        
        if test_response.status_code == 200:
            print(f'User Sucessfully Created... Username \'{self.username}\' is detected...')
            self.exists = True

        elif test_response.status_code == 404:
            print(f'Username \'{self.username}\' doesnot exist...')
            self.exists = False
            return
        elif test_response.status_code == 429:
            print(f'Username \'{self.username}\' cannot be fetched, due to too many requests')
            self.exists = False
            return
        
        self.setProblemsByDifficulty()

        return
    
    def setProblemsByDifficulty(self):

        html_text = requests.get(self.url).content

        soup = BeautifulSoup(html_text, 'lxml')


        categories = soup.find_all('span', class_='mr-[5px] text-base font-medium leading-[20px] text-label-1 dark:text-dark-label-1')

        self.easy = int(categories[0].text)
        self.medium = int(categories[1].text)
        self.hard = int(categories[2].text)
        self.score = self.easy + self.medium * 2 + self.hard * 3
        self.total = self.easy + self.medium + self.hard

        self.ProblemsByDifficultyString = f'{self.username} has solved {self.total} problems of which {self.easy} are EASY, {self.medium} are MEDIUM and {self.hard} are HARD.'

        return

    def getProblemsByDifficulty(self, easy=True, medium=True, hard=True, outputString=True, score=True):
        result = {}

        if easy:
            result['easy'] = self.easy
        if medium:
            result['medium'] = self.medium
        if hard:
            result['hard'] = self.hard
        if outputString:
            result['outputString'] = self.ProblemsByDifficultyString
        if score:
            result['score'] = self.score

        return result
    
    def __str__(self):
        """
            Overloads print( ) function, i.e when an User( ) object is 
            passed through the print( ) function the following return values will be printed.
        """

        if self.exists:
            return self.ProblemsByDifficultyString
        else:
            return f'User Details cannot be printed as Username \'{self.username}\' doesnot exist... '
        
    def __eq__(self, other):
        if self.username == other.username:
            return True
        return False
    
    def __lt__(self, other):
        return self.score < other.score
    
    def __gt__(self, other):
        return self.score > other.score
        

class UserList:
    """
    Used to iterate through a list of users
    """

    def __init__(self, usernames=[]):
        self.users = []
        self.errors = []

        for username in usernames:
            user = User(username)
            time.sleep(3)
            
            if user.exists:
                self.users.append(user)

            else:
                self.errors.append(username)

        self.usernames = usernames

        return
    
    def __str__(self):
        for user in self.users:
            print(user)
            print('\n')

    def __iter__(self):
        return iter(self.users)
    
    def __getitem__(self, index):
        if index < len(self.users) and index >= -len(self.users):
            return self.users[index]
        
        return f'Index is out of range: The index of this UserList object must be between [{-len(self.users)},{len(self.users)-1}]'
    

class Report:
    def __init__(self, userlist=UserList()):
        data = []
        for user in userlist:
            data.append({'Username' : user.username ,'Easy' : user.easy, 'Medium' : user.medium, 'Hard' : user.hard, 'Score' : user.score, 'Total Problems solved' : user.total})
        
        data = DataFrame(data)
        self.data = data
    
    def to_csv(self, path='report.csv'):
        self.data.to_csv(path, index=False)
        return
                                                                                
