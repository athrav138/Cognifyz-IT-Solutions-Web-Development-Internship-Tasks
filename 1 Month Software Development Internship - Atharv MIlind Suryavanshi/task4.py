def fahreTocelci(fahrenheit):
  return ((fahrenheit - 32) * 5/9)

def celciTofahre(celcius):
  return celcius * 9/5 + 32

while True:
  print("---Choose Task---")
  print("1. Covert Temperature Fahrenheit to Celcius.")
  print("2. Covert Temperature Celcius to Fahrenheit.")
  print("3. Exit")

  choice = int(input("Enter a Choice: "))

  
  if choice==1:
    fahre = float(input("Enter temperature in Fahreniet: "))
    print("The temerature in celcius: ",fahreTocelci(fahre)," celcius")
  elif choice==2:
    celci = float(input("Enter temperature in Fahreniet: "))
    print("The temerature in Fahreniet: ",celciTofahre(celci)," fahreniet")
  elif choice==3:
    print("Exiting..!!")
    break
  else:
    print("Invalid Choice Choose valid choice (1-3)")


    
