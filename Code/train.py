import music21
import numpy as np
from hmmlearn import hmm
import os
import pickle


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

n = 2
def trainhmm(data):
  midstr=[]
  midstrl=[]
  maxi=[]
  global n

  # Daten umwandeln
  for i in data:
    tmp=midi_to_string(i)
    midstrl.append(len(tmp))
    midstr+=[i for i in tmp]
  
  # mit zufälligen Parametern trainieren
  for idx in range(20):
      model = hmm.GaussianHMM(n_components=n,
      random_state=idx, n_iter=60)
      model.fit(midstr, midstrl)
      score=model.score(midstr, midstrl)
      maxi.append([score, idx])
  maxi.sort()
  maxi.reverse()

  scores = []
  models = []
  for i in range(5):
      model = hmm.GaussianHMM(n_components=n,
      random_state=maxi[i][1],n_iter=300)
      model.fit(midstr, midstrl)
      models.append(model)
      scores.append(model.score(midstr, midstrl))
  bestmodel = models[np.argmax(scores)]
  print(f'The best model had a score of {max(scores)}')
  print(sum(midstrl), max(scores), max(scores)/sum(midstrl))
  return bestmodel


f="E:\Seminararbeit\Code\midi\Kla"
arr = os.listdir(f)
data = [f+"\\"+i for i in arr]
model = trainhmm(data)
with open("kla" + str(n) + ".pkl", "wb") as file:
  pickle.dump(model, file)

f="E:\Seminararbeit\Code\midi\Rom"
arr = os.listdir(f)

data = [f+"\\"+i for i in arr]
model = trainhmm(data)
with open("rom" + str(n) + ".pkl", "wb") as file:
  pickle.dump(model, file)


f="E:\Seminararbeit\Code\midi\Imp"
arr = os.listdir(f)
data = [f+"\\"+i for i in arr]

model = trainhmm(data)

with open("imp" + str(n) + ".pkl", "wb") as file:
  pickle.dump(model, file)