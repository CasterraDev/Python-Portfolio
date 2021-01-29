import pygame
import random
import sys
import time

class Session:
    def __init__(self):
        self.w = 750
        self.h = 500
        self.correct_words = ''
        self.word = ''
        self.user_input = ''
        self.timer = 0
        self.time_start = 0
        self.finished = False
        self.active = False
        self.accuracy = '0'
        self.wpm = 0
        self.results = 'Time: 0  Accuracy: 0%  WPM: 0'
        self.active = False
        self.input_box = None
        self.reset_box = None
        self.resultsY = 100
        self.main_C = (255,213,102)
        self.white_C = (250,250,250)
        self.black_C = (0,0,0)

        pygame.init()
        self.screen = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption("Speed Typer")

    def draw_text_centered(self,screen,message,y,fsize,color):
        font = pygame.font.Font(None,fsize)
        text = font.render(message,1,color)
        text_pos = text.get_rect(center=(self.w/2,y))
        screen.blit(text,text_pos)
        pygame.display.update()

    def get_sentence(self):
        s = open('sentences.txt').read()
        all_sentences = s.split('\n')
        sentence = random.choice(all_sentences)
        return sentence
    
    def show_results(self,screen):
        print(self.results)
        self.draw_text_centered(self.screen,self.results,self.resultsY,24,self.main_C)
    
    def calculate_results(self):
        if (not self.finished):
            #Calculate the Time
            self.timer = time.time() - self.time_start
            #Calculate Accuracy
            count = 0
            for i,c in enumerate(self.word):
                try:
                    if (self.user_input[i] == c):
                        count += 1
                except:
                    pass
            self.accuracy = count/len(self.word)*100

            #Calculate WPM
            #60 Seconds in a minute and a word has an average of 5 characters
            self.wpm = len(self.user_input)*60/(self.timer*5)
            self.finished = True

            #Assign it to self.results
            self.results = "Time: " + str(round(self.timer)) + " Accuracy: " + str(round(self.accuracy)) + "%" + " WPM: " + str(round(self.wpm))
            
            self.show_results(self.screen)

    def restart_session(self):
        pygame.display.update()
        time.sleep(1)
        self.restart = False
        self.finished = False

        self.user_input=''
        self.word = ''
        self.time_start = 0
        self.timer = 0
        self.wpm = 0
        
        self.word = self.get_sentence()
        if (not self.word): self.restart_session()
        self.screen.fill(self.black_C)
        
        mess = "Speed Typing Test"
        self.draw_text_centered(self.screen,mess,150,34,(255,192,25))

        # draw the rectangle for input box
        pygame.draw.rect(self.screen,(255,192,25), (50,250,650,50), 2)
        # draw the sentence string
        self.draw_text_centered(self.screen, self.word,200, 28,self.white_C)
        #draw a rectange for the input text to go into
        self.input_box = pygame.draw.rect(self.screen,self.main_C, (50,250,650,50), 2)
        #draw the text inside user_input
        self.draw_text_centered(self.screen, self.user_input, 274, 26,self.white_C)
        #draw Submit text
        self.draw_text_centered(self.screen,"Press Enter to Submit",350,24,self.main_C)
        #draw Reset Button
        self.reset_box = pygame.draw.rect(self.screen,(255,150,50), ((self.w/2)-50,400,100,50), 2)
        #draw text Reset
        self.draw_text_centered(self.screen,"Reset",425, 26,(255,150,50))
        pygame.display.update()

    def run(self):
        self.restart_session()
        self.running = True
        while(self.running):
            clock = pygame.time.Clock()
            #draw over input box
            self.screen.fill(self.black_C, (50,250,750,50))
            #draw a rectange for the input text to go into
            self.input_box = pygame.draw.rect(self.screen,self.main_C, (50,250,650,50), 2)
            #update the text inside input box
            self.draw_text_centered(self.screen, self.user_input, 274, 26,self.white_C)
            pygame.display.update()
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    print("QUITTING PROGRAM")
                    self.running = False
                    sys.exit()
                elif (event.type == pygame.MOUSEBUTTONDOWN):
                    #see if Input Box is clicked
                    if (self.input_box.collidepoint(event.pos)):
                        #input box is active
                        self.active = True
                        #reset user input
                        self.user_input = ''
                        #start the timer
                        self.time_start = time.time()
                    else:
                        self.active = False
                    #See if Reset button is clicked
                    if (self.reset_box.collidepoint(event.pos)):
                        self.restart_session()
                    print("MOUSE CLICKED")
                elif (event.type == pygame.KEYDOWN):
                    #if input_box is active and the session is not finished get keyboard events
                    if (self.active and not self.finished):
                        #If return is pressed stop the session
                        if (event.key == pygame.K_RETURN):
                            self.input_box = ''
                            self.calculate_results()
                            self.finished = True
                        elif(event.key == pygame.K_BACKSPACE):
                            self.user_input = self.user_input[:-1]
                        else:
                            try:
                                self.user_input += event.unicode
                            except:
                                pass
            pygame.display.update()
        clock.tick(60)

Session().run()
