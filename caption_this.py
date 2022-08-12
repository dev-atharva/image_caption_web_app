from numpy import argmax
from pickle import load
from keras_preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model
from keras_preprocessing.image import load_img
from keras_preprocessing.image import img_to_array
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input


# In[2]:


def extract_features1(filename):
  model = InceptionV3()
  model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
  print(model.summary)
  features = dict()
  image = load_img(filename, target_size=(299, 299))
  image = img_to_array(image)
  image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
  image = preprocess_input(image)
  feature = model.predict(image, verbose=0)
  
  return feature


# In[3]:


def word_for_id(integer, tokenizer):
	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word
	return None


# In[4]:


def generate_desc(model, tokenizer, photo, max_length):
    # seed the generation process
    in_text = 'startseq'
    # iterate over the whole length of the sequence
    for i in range(max_length):
        # integer encode input sequence
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        # pad input
        sequence = pad_sequences([sequence], maxlen=max_length)
        # predict next word
        yhat = model.predict([photo,sequence], verbose=0)
        # convert probability to integer
        yhat = argmax(yhat)
        # map integer to word
        word = word_for_id(yhat, tokenizer)
        # stop if we cannot map the word
        if word is None:
            break
        # append as input for generating the next word
        in_text += ' ' + word
        # stop if we predict the end of the sequence
        if word == 'endseq':
            break
    final = in_text.split()
    final = final[1:-1]
    final = ' '.join(final)
    return final


# In[5]:




# In[6]:


def caption_it(image):
    tokenizer = load(open('tokenizer.pkl', 'rb'))
    # pre-define the max sequence length (from training)
    max_length = 34
    # load the model
    model = load_model('model_10.h5')
    # load and prepare the photograph
    photo = extract_features1(image)
    # generate description
    description = generate_desc(model, tokenizer, photo, max_length)
    return description