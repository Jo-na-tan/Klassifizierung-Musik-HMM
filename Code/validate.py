import pickle
from hmmlearn import hmm
import music21
import os


def midi_to_string(midi_path):
  score = music21.converter.parse(midi_path,
    quantizePost=True,
    quarterLengthDivisors=(4,3))
  s = []
  last_offset = 0
  for n in score.flat.notes:
    delta = n.offset - last_offset
    duration = n.duration.components[0].type
    last_offset = n.offset
    if isinstance(n, music21.note.Note):
      notes = [n]
    else:
      notes = n.notes
    m=0
    for i in notes:
      if i.pitch.midi>m: m=i.pitch.midi
    s.append(m)
  z=[]
  for i in range(len(s)-1):
    tmp=s[i+1]-s[i]
    if tmp>12 or tmp<-12:
        continue
    if tmp>=0:
        z.append([tmp+12])
    elif tmp<0:
        z.append([12+tmp])
  return z

# hier fuer Klassik
f="E:\Seminararbeit\Code\midi\\Validation\Kla"
arr = os.listdir(f)
data = [f+"\\"+i for i in arr]
num="2"

with open("kla"+num+".pkl", "rb") as file:
  model1 = pickle.load(file)
with open("rom"+num+".pkl", "rb") as file:
  model2 = pickle.load(file)
with open("imp"+num+".pkl", "rb") as file:
  model3 = pickle.load(file)

a=0
b=0
c=0
for i in data:
  x=midi_to_string(i)
  # hier Divisor fuer n=2
  m1 = round(model1.score(x)/(2.7923130674275147), 2) 
  m2 = round(model2.score(x)/(2.8102016683967603), 2)
  m3 = round(model3.score(x)/(2.803844613578279), 2)
  print(i[42:], m1, m2, m3)
  if m1>m2 and m1>m3: a+=1
  elif m2>m1 and m2>m3: b+=1
  elif m3>m1 and m3>m2: c+=1
print("Gesamt(%):", round(a/len(data)*100, 2),
round(b/len(data)*100, 2) , round(c/len(data)*100, 2))
print("Gesamt(anz):",a, b, c)

# 2
  # m1 = round(model1.score(x)/(2.7923130674275147), 2) 
  # m2 = round(model2.score(x)/(2.8102016683967603), 2)
  # m3 = round(model3.score(x)/(2.803844613578279), 2)

# 4
  # m1 = round(model1.score(x)/(2.7495722981802815), 2) 
  # m2 = round(model2.score(x)/(1.803345984072812), 2)
  # m3 = round(model3.score(x)/(2.821344755791713), 2)

# 6
#   m1 = round(model1.score(x)/(1.8117294359966646), 2) 
#   m2 = round(model2.score(x)/(1.9918386764883595), 2)
#   m3 = round(model3.score(x)/(2.7594453349643515), 2)

# 8
  # m1 = round(model1.score(x)/(1.9833552469773407), 2) 
  # m2 = round(model2.score(x)/(1.1333369819393446), 2)
  # m3 = round(model3.score(x)/(1.864247857719344), 2)

# 10
  # m1 = round(model1.score(x)/(-1.0830928461356184), 2) 
  # m2 = round(model2.score(x)/(1.095462903604709), 2)
  # m3 = round(model3.score(x)/(2.015869711094486), 2)
