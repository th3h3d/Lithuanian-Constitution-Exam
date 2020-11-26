import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
from datetime import datetime
import time
import hashlib

class WebDriverPythonBasics(unittest.TestCase):


    def setUp(self):
        #self.browser = webdriver.Chrome()
        self.browser = webdriver.Chrome(executable_path='./chromedriver')


    def test_saucelabs_homepage_header_displayed(self):
        file_name = "output"
        file_num = 0
        file_ext = '.txt'   

        for idx in range(5000):

            self.browser.get("http://konstitucijosegzaminas.lt/bandomasis-egzaminas/")

            # ---------------------------------------------------------------------------->
            # Get questions and their answers

            all_questions_answers = []


            
            for i in range(15):
                question_answer = dict()
                now = datetime.now()
                dt_string = now.strftime("%Y%m%d%H%M%S%f")[:-3]
                question_answer['id'] = ''
                question_answer['date'] = dt_string
                
                try:
                    question = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div/section/div/div/form/div['+str(i+1)+']/div/p[2]');
                    question_answer['question'] = question.text
                except:
                    try:
                        question = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div/section/div/div/form/div['+str(i+1)+']/div/p');
                        question_answer['question'] = question.text
                    except:
                        try:
                            question = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div/section/div/div/form/div['+str(i+1)+']/div/p/strong');
                            question_answer['question'] = question.text
                        except:
                            pass
                
                hash_id = hashlib.md5(question_answer['question'].encode())
                question_answer['id'] = hash_id.hexdigest()

                option1_read = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div/section/div/div/form/div['+str(i+1)+']/div/table/tbody/tr[1]/td[2]/label');
                question_answer['A'] = option1_read.text
                option2_read = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div/section/div/div/form/div['+str(i+1)+']/div/table/tbody/tr[2]/td[2]/label');
                question_answer['B'] = option2_read.text
                option3_read = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div/section/div/div/form/div['+str(i+1)+']/div/table/tbody/tr[3]/td[2]/label');
                question_answer['C'] = option3_read.text
                option4_read = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div/section/div/div/form/div['+str(i+1)+']/div/table/tbody/tr[4]/td[2]/label');
                question_answer['D'] = option4_read.text
                all_questions_answers.append(question_answer)
            # ---------------------------------------------------------------------------->



            #  Always select first options
            for i in range(len(all_questions_answers)):
                option1_click = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div/section/div/div/form/div['+str(i+1)+']/div/table/tbody/tr[1]/td[1]/input');
                option1_click.click();


            # submit your questions
            button_click = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div/section/div/div/form/div[16]/input')
            button_click.click();

            for i in range(len(all_questions_answers)):            
                answer = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div/section/div/div/div['+str(i+1)+']/div/span'); # correct or incorrect
                if answer.text == 'Incorrect':
                    correct_answer = self.browser.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div/div/section/div/div/div['+str(i+1)+']/div/div/p')
                    all_questions_answers[i]['answer'] = (correct_answer.text)
                else:
                    all_questions_answers[i]['answer'] = all_questions_answers[i]['A']


            if (idx%1000) == 0:
                file_num = file_num + 1
                                    
            with open(file_name+str(file_num)+file_ext, 'a') as my_file:
                my_file.write(str(all_questions_answers))
            
            print(idx)


    def tearDown(self):
        self.browser.close()
        pass


if __name__ == '__main__':
        unittest.main()

