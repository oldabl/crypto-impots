import time, sys, os, math

# Class: ProgressBar
# Role: print a progress bar with next to no
#  line of code required by user
class ProgressBar:

  # Role : assign arguments to internal values
  def __init__(self,
              pretext=r"", # Text to print before the bar
              progresschar=r"█", # Character of done part of the bar
              remainingbarchar=r" ", # Character to fill the remaining bar with
              loadingchars=r"█▓▒░▒▓", # Last character of bar moving as bar loads (moves even if no progress)
              startendchar=r"||", # The two characters going around the bar
              displaypercentage=True, # Show percentage as well or not
              displaycount=False, # Show count as well or not
              rightjustified=True, # Print the bar on the right hand side of the console
              consolewidthrate=3 # Print the bar on 1/3 of the width of console
              ):
    self.pretext = str(pretext)
    self.progresschar = str(progresschar)
    self.remainingbarchar = str(remainingbarchar)
    self.loadingchars = loadingchars
    self.startendchar = str(startendchar)
    self.displaypercentage = displaypercentage
    self.displaycount = displaycount
    self.rightjustified = rightjustified
    self.consolewidthrate = consolewidthrate

    # Private
    self.loadingcharsindex = 0
    self.firstprint = True

  
  # Role : prints the progress bar as an independent thread
  # Arguments:
  # - number: progress value (type multiprocessing.Value of int)
  # - max: value to reach (int)
  # - updateperiod: refresh period of progress bar in seconds
  def inThread(self, number, max, updateperiod=0.1):
    while(number.value < max):
      self.print(number.value,max)
      time.sleep(float(updateperiod))
    self.print(max,max)

  
  # Role : prints the progress bar inline
  # Arguments:
  # - number: progress value (int)
  # - max: maximum value (int)
  def print(self,number,max):
    actuallyjustifyright = True
    consolewidth = os.get_terminal_size().columns

    prebarstring = barstring = ""

    # No carriage return on first print
    if not self.firstprint:
      prebarstring += "\r"
    self.firstprint = False

    ### Pre progress bar
    if self.pretext:
      compatiblepretext = self.pretext
      limitsizepretext = math.floor( (1-1/self.consolewidthrate)*consolewidth )
      if self.displaycount: limitsizepretext = limitsizepretext - 4 - len(str(max))*2
      if self.displaypercentage: limitsizepretext = limitsizepretext - 5
      limitsizepretext = limitsizepretext - len(self.startendchar) - 2
      limitsizepretext = limitsizepretext - 1
      if len(compatiblepretext) >= limitsizepretext:
        # If pretext is too long
        compatiblepretext = compatiblepretext[:limitsizepretext]+"..."
        actuallyjustifyright = False
      prebarstring += compatiblepretext + " "

    ### Progress bar

    # Start char
    if self.startendchar:
      barstring += self.startendchar[0]

    # Current state of affairs
    barwidth=int(os.get_terminal_size().columns/self.consolewidthrate) # Calculated from terminal size
    sofarbar = int( (number/max)*barwidth )
    remainingbar = barwidth - sofarbar

    # Add progress chars
    barstring += sofarbar*self.progresschar

    # If loading chars, print loading chars and go to next one (unless 100%)
    if self.loadingchars != "" and number != max:
      barstring += self.loadingchars[self.loadingcharsindex]
      self.loadingcharsindex = (self.loadingcharsindex+1) % len(self.loadingchars)
      remainingbar -= 1

    # Add remaining gap
    barstring += remainingbar*self.remainingbarchar

    # End char
    if self.startendchar:
      if len(self.startendchar) >= 2:
        barstring += self.startendchar[1]
      else:
        barstring += self.startendchar[0]

    ### Post progress bar
    if self.displaypercentage:
      per = " %d%%" % int(number*100/max)
      barstring += " "*(5 - len(per)) + per
    if self.displaycount:
      count = " (%d/%d)" % (number,max)
      barstring += " "*(len(str(max))-len(str(number))) + count

    # Print the bar out
    if self.rightjustified and actuallyjustifyright:
      fillthevoid = " "*(consolewidth-len(prebarstring)-len(barstring)-1)
      sys.stdout.write(prebarstring + fillthevoid + barstring + " ")
      sys.stdout.flush()
    else:
      sys.stdout.write(prebarstring + barstring)
      sys.stdout.flush()

    # Add new line if bar is finished
    if number == max:
      print()