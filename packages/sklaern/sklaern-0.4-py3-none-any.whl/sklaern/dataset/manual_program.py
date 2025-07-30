def mnist1():
    print('''

import numpy as np 
import tensorflow as tf 
from tensorflow.keras import layers, models 
from tensorflow.keras.datasets import mnist 
import matplotlib.pyplot as plt 
# Load and preprocess the MNIST dataset 
(x_train, _), (x_test, _) = mnist.load_data() 
x_train = x_train.astype('float32') / 255.0 
x_test = x_test.astype('float32') / 255.0 
 
x_train = x_train.reshape((x_train.shape[0], 28, 28, 1)) 
x_test = x_test.reshape((x_test.shape[0], 28, 28, 1)) 
# Define the autoencoder model 
input_img = layers.Input(shape=(28, 28, 1)) 
 
# Encoding layer 
x = layers.Conv2D(32, (3, 3), activation='relu', 
padding='same')(input_img) 
x = layers.MaxPooling2D((2, 2), padding='same')(x) 
x = layers.Conv2D(16, (3, 3), activation='relu', 
padding='same')(x) 
encoded = layers.MaxPooling2D((2, 2), padding='same')(x) 
 
# Decoding layer 
x = layers.Conv2D(16, (3, 3), activation='relu', 
padding='same')(encoded) 
x = layers.UpSampling2D((2, 2))(x) 
x = layers.Conv2D(32, (3, 3), activation='relu', 
padding='same')(x) 
x = layers.UpSampling2D((2, 2))(x)

decoded = layers.Conv2D(1, (3, 3), activation='sigmoid', 
padding='same')(x) 
 
# Build the autoencoder model 
autoencoder = models.Model(input_img, decoded) 
 
 
# Compile the model 
autoencoder.compile(optimizer='adam', 
loss='binary_crossentropy') 
# Train the model 
autoencoder.fit(x_train, x_train, 
                epochs=10, 
                batch_size=128, 
                shuffle=True, 
                validation_data=(x_test, x_test)) 
# Encode and decode some digits 
encoded_imgs = autoencoder.predict(x_test) 
 
# Display the results 
n = 10  # Display the first 10 images 
plt.figure(figsize=(20, 4)) 
for i in range(n): 
    # Display original 
    ax = plt.subplot(2, n, i + 1) 
    plt.imshow(x_test[i].reshape(28, 28), cmap='gray') 
    plt.gray() 
    ax.get_xaxis().set_visible(False) 
    ax.get_yaxis().set_visible(False) 
 
    # Display reconstruction 
    ax = plt.subplot(2, n, i + 1 + n) 
    plt.imshow(encoded_imgs[i].reshape(28, 28), cmap='gray') 
    plt.gray() 
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False) 
 
plt.show() 

''')
    

def mnist2():
    print('''


import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras

# Load the MNIST dataset
(x_train, _), (x_test, _) = keras.datasets.mnist.load_data()

# Normalize and reshape
x_train = x_train.astype('float32') / 255.
x_train = x_train.reshape((x_train.shape[0], -1))
x_test = x_test.astype('float32') / 255.
x_test = x_test.reshape((x_test.shape[0], -1))

# Dimensionality of encoding space
encoding_dim = 32

# Autoencoder architecture
input_img = keras.Input(shape=(784,))
encoded = keras.layers.Dense(encoding_dim, activation='relu')(input_img)
decoded = keras.layers.Dense(784, activation='sigmoid')(encoded)

# Models
autoencoder = keras.Model(input_img, decoded)
encoder = keras.Model(input_img, encoded)

decoder_input = keras.Input(shape=(encoding_dim,))
decoder_layer = autoencoder.layers[-1]
decoder = keras.Model(decoder_input, decoder_layer(decoder_input))

# Compile and train
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
history = autoencoder.fit(
    x_train, x_train,
    epochs=50,
    batch_size=256,
    shuffle=True,
    validation_data=(x_test, x_test)
)

# Plot training and validation loss
plt.figure(figsize=(8, 5))
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Autoencoder Loss over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Binary Crossentropy Loss')
plt.legend()
plt.grid(True)
plt.show()

# Encode and decode test images
encoded_imgs = encoder.predict(x_test)
decoded_imgs = decoder.predict(encoded_imgs)

# Display original and reconstructed images
n = 10  # how many digits to display
plt.figure(figsize=(20, 4))
for i in range(n):
    # Original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i].reshape(28, 28), cmap='gray')
    plt.title("Original")
    plt.axis('off')

    # Reconstruction
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_imgs[i].reshape(28, 28), cmap='gray')
    plt.title("Reconstructed")
    plt.axis('off')
plt.show()


''')
    

def mnist3():
    print('''
          

INSTALL DEPENDENCIES

!pip install tensorflow-probability

# to generate gifs
!pip install imageio
!pip install git+https://github.com/tensorflow/docs



from IPython import display

import glob
import imageio
import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf
import tensorflow_probability as tfp
import time

(train_images, _), (test_images, _) = tf.keras.datasets.mnist.load_data()

def preprocess_images(images):
  images = images.reshape((images.shape[0], 28, 28, 1)) / 255.
  return np.where(images > .5, 1.0, 0.0).astype('float32')

train_images = preprocess_images(train_images)
test_images = preprocess_images(test_images)

train_size = 60000
batch_size = 32
test_size = 10000

train_dataset = (tf.data.Dataset.from_tensor_slices(train_images)
                 .shuffle(train_size).batch(batch_size))
test_dataset = (tf.data.Dataset.from_tensor_slices(test_images)
                .shuffle(test_size).batch(batch_size))

class CVAE(tf.keras.Model):
  """Convolutional variational autoencoder."""

  def __init__(self, latent_dim):
    super(CVAE, self).__init__()
    self.latent_dim = latent_dim
    self.encoder = tf.keras.Sequential(
        [
            tf.keras.layers.InputLayer(input_shape=(28, 28, 1)),
            tf.keras.layers.Conv2D(
                filters=32, kernel_size=3, strides=(2, 2), activation='relu'),
            tf.keras.layers.Conv2D(
                filters=64, kernel_size=3, strides=(2, 2), activation='relu'),
            tf.keras.layers.Flatten(),
            # No activation
            tf.keras.layers.Dense(latent_dim + latent_dim),
        ]
    )

    self.decoder = tf.keras.Sequential(
        [
            tf.keras.layers.InputLayer(input_shape=(latent_dim,)),
            tf.keras.layers.Dense(units=7*7*32, activation=tf.nn.relu),
            tf.keras.layers.Reshape(target_shape=(7, 7, 32)),
            tf.keras.layers.Conv2DTranspose(
                filters=64, kernel_size=3, strides=2, padding='same',
                activation='relu'),
            tf.keras.layers.Conv2DTranspose(
                filters=32, kernel_size=3, strides=2, padding='same',
                activation='relu'),
            # No activation
            tf.keras.layers.Conv2DTranspose(
                filters=1, kernel_size=3, strides=1, padding='same'),
        ]
    )

  @tf.function
  def sample(self, eps=None):
    if eps is None:
      eps = tf.random.normal(shape=(100, self.latent_dim))
    return self.decode(eps, apply_sigmoid=True)

  def encode(self, x):
    mean, logvar = tf.split(self.encoder(x), num_or_size_splits=2, axis=1)
    return mean, logvar

  def reparameterize(self, mean, logvar):
    eps = tf.random.normal(shape=mean.shape)
    return eps * tf.exp(logvar * .5) + mean

  def decode(self, z, apply_sigmoid=False):
    logits = self.decoder(z)
    if apply_sigmoid:
      probs = tf.sigmoid(logits)
      return probs
    return logits


optimizer = tf.keras.optimizers.Adam(1e-4)


def log_normal_pdf(sample, mean, logvar, raxis=1):
  log2pi = tf.math.log(2. * np.pi)
  return tf.reduce_sum(
      -.5 * ((sample - mean) ** 2. * tf.exp(-logvar) + logvar + log2pi),
      axis=raxis)


def compute_loss(model, x):
  mean, logvar = model.encode(x)
  z = model.reparameterize(mean, logvar)
  x_logit = model.decode(z)
  cross_ent = tf.nn.sigmoid_cross_entropy_with_logits(logits=x_logit, labels=x)
  logpx_z = -tf.reduce_sum(cross_ent, axis=[1, 2, 3])
  logpz = log_normal_pdf(z, 0., 0.)
  logqz_x = log_normal_pdf(z, mean, logvar)
  return -tf.reduce_mean(logpx_z + logpz - logqz_x)


@tf.function
def train_step(model, x, optimizer):
  """Executes one training step and returns the loss.

  This function computes the loss and gradients, and uses the latter to
  update the model's parameters.
  """
  with tf.GradientTape() as tape:
    loss = compute_loss(model, x)
  gradients = tape.gradient(loss, model.trainable_variables)
  optimizer.apply_gradients(zip(gradients, model.trainable_variables))

epochs = 10
# set the dimensionality of the latent space to a plane for visualization later
latent_dim = 2
num_examples_to_generate = 16

# keeping the random vector constant for generation (prediction) so
# it will be easier to see the improvement.
random_vector_for_generation = tf.random.normal(
    shape=[num_examples_to_generate, latent_dim])
model = CVAE(latent_dim)

def generate_and_save_images(model, epoch, test_sample):
  mean, logvar = model.encode(test_sample)
  z = model.reparameterize(mean, logvar)
  predictions = model.sample(z)
  fig = plt.figure(figsize=(4, 4))

  for i in range(predictions.shape[0]):
    plt.subplot(4, 4, i + 1)
    plt.imshow(predictions[i, :, :, 0], cmap='gray')
    plt.axis('off')

  # tight_layout minimizes the overlap between 2 sub-plots
  plt.savefig('image_at_epoch_{:04d}.png'.format(epoch))
  plt.show()

# Pick a sample of the test set for generating output images
assert batch_size >= num_examples_to_generate
for test_batch in test_dataset.take(1):
  test_sample = test_batch[0:num_examples_to_generate, :, :, :]

generate_and_save_images(model, 0, test_sample)

for epoch in range(1, epochs + 1):
  start_time = time.time()
  for train_x in train_dataset:
    train_step(model, train_x, optimizer)
  end_time = time.time()

  loss = tf.keras.metrics.Mean()
  for test_x in test_dataset:
    loss(compute_loss(model, test_x))
  elbo = -loss.result()
  display.clear_output(wait=False)
  print('Epoch: {}, Test set ELBO: {}, time elapse for current epoch: {}'
        .format(epoch, elbo, end_time - start_time))
  generate_and_save_images(model, epoch, test_sample)

def display_image(epoch_no):
  return PIL.Image.open('image_at_epoch_{:04d}.png'.format(epoch_no))

plt.imshow(display_image(epoch))
plt.axis('off')  # Display images

anim_file = 'cvae.gif'

with imageio.get_writer(anim_file, mode='I') as writer:
  filenames = glob.glob('image*.png')
  filenames = sorted(filenames)
  for filename in filenames:
    image = imageio.imread(filename)
    writer.append_data(image)
  image = imageio.imread(filename)
  writer.append_data(image)

import tensorflow_docs.vis.embed as embed
embed.embed_file(anim_file)

def plot_latent_images(model, n, digit_size=28):
  """Plots n x n digit images decoded from the latent space."""

  norm = tfp.distributions.Normal(0, 1)
  grid_x = norm.quantile(np.linspace(0.05, 0.95, n))
  grid_y = norm.quantile(np.linspace(0.05, 0.95, n))
  image_width = digit_size*n
  image_height = image_width
  image = np.zeros((image_height, image_width))

  for i, yi in enumerate(grid_x):
    for j, xi in enumerate(grid_y):
      z = np.array([[xi, yi]])
      x_decoded = model.sample(z)
      digit = tf.reshape(x_decoded[0], (digit_size, digit_size))
      image[i * digit_size: (i + 1) * digit_size,
            j * digit_size: (j + 1) * digit_size] = digit.numpy()

  plt.figure(figsize=(10, 10))
  plt.imshow(image, cmap='Greys_r')
  plt.axis('Off')
  plt.show()

plot_latent_images(model, 20)





''')


def mnist4():
    print('''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load MNIST data
print("Loading MNIST dataset...")
mnist = fetch_openml('mnist_784', version=1)
X, y = mnist["data"], mnist["target"].astype(np.int32)

# Normalize the data to [0, 1]
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Create RBM model
rbm = BernoulliRBM(n_components=64, learning_rate=0.06, batch_size=100, n_iter=10, random_state=0, verbose=True)

# Logistic regression classifier
logistic = LogisticRegression(max_iter=1000, solver='lbfgs', multi_class='multinomial')

# Pipeline: RBM + Logistic Regression
rbm_classifier = Pipeline(steps=[('rbm', rbm), ('logistic', logistic)])

# Train the pipeline
print("Training RBM + Logistic Regression pipeline...")
rbm_classifier.fit(X_train, y_train)

# Predictions
y_pred = rbm_classifier.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\\n🔹 Accuracy: {accuracy:.4f}")

# Classification report
print("\\n🔹 Classification Report:")
print(classification_report(y_test, y_pred))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Plot confusion matrix
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=range(10), yticklabels=range(10))
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# Show RBM features
def plot_rbm_features(rbm, n_components=64):
    plt.figure(figsize=(8, 8))
    for i in range(n_components):
        plt.subplot(8, 8, i + 1)
        plt.imshow(rbm.components_[i].reshape((28, 28)), cmap='gray')
        plt.axis('off')
    plt.suptitle("Learned RBM Features (Hidden Units)")
    plt.show()

plot_rbm_features(rbm)

# Show original vs. RBM features (visual)
def show_original_vs_features(X_original, X_transformed, num=5):
    plt.figure(figsize=(10, 4))
    for i in range(num):
        # Original
        plt.subplot(2, num, i + 1)
        plt.imshow(X_original[i].reshape((28, 28)), cmap='gray')
        plt.title("Original")
        plt.axis('off')

        # RBM Feature Vector (reshaped to 8x8 for visual)
        plt.subplot(2, num, i + 1 + num)
        plt.imshow(X_transformed[i].reshape((8, 8)), cmap='viridis')
        plt.title("RBM Features")
        plt.axis('off')

    plt.suptitle("Original vs. RBM Feature Representation")
    plt.show()

# Transform to feature space using RBM
X_test_features = rbm.transform(X_test)
show_original_vs_features(X_test, X_test_features)


''')


def mnist5():
    print('''
          
from sklearn.datasets import load_digits 
from sklearn.neural_network import BernoulliRBM 
from sklearn.linear_model import LogisticRegression 
from sklearn.pipeline import Pipeline 
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report 
import numpy as np 
 
# Load digit dataset 
digits = load_digits() 
X, y = digits.data, digits.target 
 
# Normalize to [0, 1] 
X = X / 16.0 
 
# Split dataset 
X_train, X_test, y_train, y_test = train_test_split(X, y, 
test_size=0.2, random_state=42) 
 
# Define RBMs 
rbm1 = BernoulliRBM(n_components=64, learning_rate=0.06, 
n_iter=20, random_state=0) 
rbm2 = BernoulliRBM(n_components=32, learning_rate=0.06, 
n_iter=20, random_state=0) 
 
# Define classifier 
logistic = LogisticRegression(max_iter=1500) 
 
# Stack RBMs + classifier 
stacked_rbm = Pipeline(steps=[ 
    ('rbm1', rbm1), 
    ('rbm2', rbm2), 
    ('logistic', logistic) 
]) 
# Train the model 
stacked_rbm.fit(X_train, y_train) 
 
# Predict on test data 
y_pred = stacked_rbm.predict(X_test) 
 
# Print classification report 
print("\\n--- Classification Report ---") 
print(classification_report(y_test, y_pred)) 
 
# Print a comparison of actual vs predicted 
print("\\n--- Comparison of Actual vs Predicted (First 20 samples) ---") 
for i in range(20): 
  print(f"Sample {i+1}: Actual = {y_test[i]} | Predicted = {y_pred[i]}")

''')
    


def mnist6():
    print('''

import torch 
import torch.nn as nn 
import torch.nn.functional as F 
from torchvision import datasets, transforms 
from torch.utils.data import DataLoader 
import matplotlib.pyplot as plt 
 
# Load MNIST dataset 
transform = transforms.ToTensor() 
train_set = datasets.MNIST(root='./data', train=True, 
download=True, transform=transform) 
test_set = datasets.MNIST(root='./data', train=False, 
download=True, transform=transform) 
 
train_loader = DataLoader(train_set, batch_size=64, 
shuffle=True) 
test_loader = DataLoader(test_set, batch_size=1000) 
 
# Simple neural network (DBN-like structure) 
class SimpleDBN(nn.Module): 
    def __init__(self): 
        super().__init__() 
        self.fc1 = nn.Linear(28*28, 256) 
        self.fc2 = nn.Linear(256, 128) 
        self.fc3 = nn.Linear(128, 10) 
 
    def forward(self, x): 
        x = x.view(-1, 28*28)      # flatten the image 
        x = F.relu(self.fc1(x))    # first hidden layer 
        x = F.relu(self.fc2(x))    # second hidden layer 
        return self.fc3(x)         # output layer 
 
# Initialize model, loss function and optimizer 
model = SimpleDBN()
criterion = nn.CrossEntropyLoss() 
optimizer = torch.optim.Adam(model.parameters(), lr=0.001) 
 
# Train the model 
print("Training...") 
for epoch in range(5): 
    for images, labels in train_loader: 
        outputs = model(images) 
        loss = criterion(outputs, labels) 
 
        optimizer.zero_grad() 
        loss.backward() 
        optimizer.step() 
    print(f"Epoch {epoch+1} complete") 
 
# Test the model 
model.eval() 
correct = 0 
total = 0 
with torch.no_grad(): 
    for images, labels in test_loader: 
        outputs = model(images) 
        _, predicted = torch.max(outputs, 1) 
        total += labels.size(0) 
        correct += (predicted == labels).sum().item() 
 
print(f"Test Accuracy: {100 * correct / total:.2f}%") 
 
# Predict and display 5 test images 
dataiter = iter(test_loader) 
images, labels = next(dataiter) 
sample_images = images[:5] 
sample_labels = labels[:5]
with torch.no_grad(): 
    outputs = model(sample_images) 
    _, preds = torch.max(outputs, 1) 
 
# Plot predictions 
for i in range(5): 
    img = sample_images[i].squeeze().numpy() 
    plt.imshow(img, cmap='gray') 
    plt.title(f"Predicted: {preds[i].item()}, Actual: {sample_labels[i].item()}") 
    plt.axis('off') 
    plt.show() 


''')


def mnist7():
    print('''

import numpy as np 
 
# Sigmoid activation 
def sigmoid(x): 
    return 1 / (1 + np.exp(-x)) 
 
# Sampling binary units based on probabilities 
def sample(prob): 
    return np.random.binomial(1, prob) 
 
# Sampling function for a layer 
def sample_layer(input_data, weights, bias): 
    activation = np.dot(input_data, weights) + bias 
    prob = sigmoid(activation) 
    return sample(prob), prob 
 
# One training step for a simplified DBM 
def dbm_step(v0, W1, b1, W2, b2, lr=0.01): 
    # ======== UPWARD PASS ======== 
    h1, h1_prob = sample_layer(v0, W1, b1)     # From visible to hidden1 
    h2, h2_prob = sample_layer(h1, W2, b2)     # From hidden1 to hidden2 
 
    # ======== DOWNWARD PASS (Reconstruction) ======== 
    h1_down, _ = sample_layer(h2, W2.T, np.zeros_like(b1))   # Reconstruct hidden1 
    v1, _ = sample_layer(h1_down, W1.T, np.zeros_like(v0))   # Reconstruct visible 
 

    pos_W1 = np.outer(v0, h1) 
    pos_W2 = np.outer(h1, h2) 
 
    # Negative phase 
    neg_W1 = np.outer(v1, h1_down) 
    neg_W2 = np.outer(h1_down, h2) 
 
    # Update weights and biases 
    W1 += lr * (pos_W1 - neg_W1) 
    W2 += lr * (pos_W2 - neg_W2) 
    b1 += lr * (h1 - h1_down) 
    b2 += lr * (h2 - h2_prob) 
 
    return W1, b1, W2, b2 
 
# ======== INITIALIZATION ======== 
np.random.seed(42)  # For reproducibility 
 
v0 = np.array([1, 0, 1, 0])           # 4 visible units (input) 
W1 = np. random. randn(4, 3) * 0.1      # 4 ↔ 3 weights (visible ↔ hidden1) 
b1 = np.zeros(3) 
 
W2 = np.random.randn(3, 2) * 0.1      # 3 ↔ 2 weights (hidden1 ↔ hidden2) 
b2 = np.zeros(2) 
 
# ======== TRAINING STEP ======== 
W1, b1, W2, b2 = dbm_step(v0, W1, b1, W2, b2) 
 
# ======== OUTPUT ======== 
print ("Updated W1 (v ↔ h1): \\n", W1) 
print("Updated b1 (h1):", b1) 
print ("Updated W2 (h1 ↔ h2): \\n", W2) 
print("Updated b2 (h2):", b2)

''')
    

def mnist8():
    print('''

#importing library 
import numpy as np 
import matplotlib.pyplot as plt 
from keras import Sequential 
from keras.layers import Dense, Conv2D, MaxPooling2D, UpSampling2D 
from keras.datasets import mnist 
 
#Loading the dataset 
(x_train, _), (x_test, _) = mnist.load_data() 
x_train = x_train.astype('float32') / 255 
x_test = x_test.astype('float32') / 255 
 
 
# reshape in the input data for the model 
x_train = x_train.reshape(len(x_train), 28, 28, 1) 
x_test = x_test.reshape(len(x_test), 28, 28, 1) 
x_test.shape 
 
#model implementation 
model = Sequential([
                    Conv2D(32, 3, activation='relu', padding='same', input_shape=(28, 28, 1)), 
                    MaxPooling2D(2, padding='same'), 
                    Conv2D(16, 3, activation='relu', padding='same'), 
                    MaxPooling2D(2, padding='same'), 
                    # decoder network 
                    Conv2D(16, 3, activation='relu', padding='same'), 
                    UpSampling2D(2), 
                    Conv2D(32, 3, activation='relu', padding='same'), 
                    UpSampling2D(2), 
                    # output layer 
                    Conv2D(1, 3, activation='sigmoid', padding='same') 
]) 
 
model.compile(optimizer='adam', loss='binary_crossentropy') 
model.fit(x_train, x_train, epochs=20, batch_size=256, 
validation_data=(x_test, x_test)) 
 
#storing the predected output here and visualizing the result 
pred = model.predict(x_test) 
#Visual Representation 
index = np.random.randint(len(x_test)) 
plt.figure(figsize=(10, 4)) 
# display original image 
ax = plt.subplot(1, 2, 1) 
plt.title("Original Image") 
plt.imshow(x_test[index].reshape(28,28)) 
plt.gray() 
 
# display compressed image 
ax = plt.subplot(1, 2, 2) 
plt.title("compressed Image") 
plt.imshow(pred[index].reshape(28,28)) 
plt.gray() 
plt.show() 
 
from sklearn.metrics import mean_squared_error 
 
# Get original and predicted images 
original = x_test[index].reshape(28, 28) 
reconstructed = pred[index].reshape(28, 28) 
 
# Compute Mean Squared Error 
mse = mean_squared_error(original, reconstructed) 
print(f"Mean Squared Error (MSE) between original and reconstructed image: {mse}")

''')
    

def mnist9():
    print('''

import numpy as np 
import matplotlib.pyplot as plt 
from tensorflow.keras.datasets import mnist 
from tensorflow.keras.models import Model 
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D 
 
# Load and normalize MNIST 
(x_train, _), (x_test, _) = mnist.load_data() 
x_train = x_train.astype("float32") / 255. 
x_test = x_test.astype("float32") / 255. 
x_train = np.reshape(x_train, (len(x_train), 28, 28, 1)) 
x_test = np.reshape(x_test, (len(x_test), 28, 28, 1)) 
 
# Define encoder 
input_img = Input(shape=(28, 28, 1)) 
x = Conv2D(16, (3, 3), activation='relu', 
padding='same')(input_img) 
x = MaxPooling2D((2, 2), padding='same')(x) 
x = Conv2D(8, (3, 3), activation='relu', padding='same')(x) 
encoded = MaxPooling2D((2, 2), padding='same')(x) 
 
# Define decoder 
x = Conv2D(8, (3, 3), activation='relu', 
padding='same')(encoded) 
x = UpSampling2D((2, 2))(x) 
x = Conv2D(16, (3, 3), activation='relu', padding='same')(x) 
x = UpSampling2D((2, 2))(x) 
decoded = Conv2D(1, (3, 3), activation='sigmoid', 
padding='same')(x) 
 
# Build autoencoder 
autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adam', 
loss='binary_crossentropy') 
 
# Train the model 
autoencoder.fit(x_train, x_train, 
                epochs=5, 
                batch_size=128, 
                shuffle=True, 
                validation_data=(x_test, x_test)) 
 
# Predict on test set 
decoded_imgs = autoencoder.predict(x_test) 
n = 10  # Number of digits to display 
plt.figure(figsize=(20, 4)) 
for i in range(n): 
    # Original 
    ax = plt.subplot(2, n, i + 1) 
    plt.imshow(x_test[i].reshape(28, 28), cmap='gray') 
    plt.title("Original") 
    plt.axis('off') 
 
    # Reconstructed 
    ax = plt.subplot(2, n, i + 1 + n) 
    plt.imshow(decoded_imgs[i].reshape(28, 28), cmap='gray') 
    plt.title("Reconstructed") 
    plt.axis('off') 
plt.tight_layout() 
plt.show()

''')
    

def mnist10():
    print('''

import torch, torch.nn as nn, torch.optim as optim 
from torchvision import datasets, transforms 
from torch.utils.data import DataLoader 
import matplotlib.pyplot as plt 
 
# Data 
data = DataLoader(datasets.MNIST('.', train=True, download=True, 
               
transform=transforms.Compose([transforms.ToTensor(), 
transforms.Normalize((0.5,), (0.5,))])), 
               batch_size=64, shuffle=True) 
 
# Generator & Discriminator 
G = nn.Sequential(nn.Linear(100, 256), nn.ReLU(), nn.Linear(256, 784), nn.Tanh()) 
D = nn.Sequential(nn.Linear(784, 256), nn.LeakyReLU(0.2), nn.Linear(256, 1), nn.Sigmoid()) 
opt_G = optim.Adam(G.parameters(), lr=0.0002) 
opt_D = optim.Adam(D.parameters(), lr=0.0002) 
loss = nn.BCELoss() 
 
# Train 
for epoch in range(100):  # few epochs for quick training 
    for real, _ in data: 
        real = real.view(-1, 784) 
        z = torch.randn(real.size(0), 100) 
        fake = G(z) 
 
        # Discriminator 
        D_real = D(real) 
        D_fake = D(fake.detach()) 
        loss_D = loss(D_real, torch.ones_like(D_real)) + loss(D_fake, torch.zeros_like(D_fake)) 
        opt_D.zero_grad(); loss_D.backward(); opt_D.step()

 
        # Generator 
        D_fake = D(fake) 
        loss_G = loss(D_fake, torch.ones_like(D_fake)) 
        opt_G.zero_grad(); loss_G.backward(); opt_G.step() 
 
    print(f"Epoch {epoch+1}: D_loss={loss_D.item():.3f}, G_loss={loss_G.item():.3f}") 
 
# Generate sample 
z = torch.randn(1, 100) 
img = G(z).view(28, 28).detach() 
plt.imshow(img, cmap='gray'); plt.axis('off'); plt.show()

''')
    



def cifar1():
    print('''

import tensorflow as tf
import matplotlib.pyplot as plt

# Load and preprocess MNIST
(x_train, _), (x_test, _) = tf.keras.datasets.mnist.load_data()
x_train = x_train[..., None]/255.0
x_test = x_test[..., None]/255.0

# Define CNN autoencoder
inp = tf.keras.Input(shape=(28,28,1))
x = tf.keras.layers.Conv2D(16, 3, activation='relu', padding='same')(inp)
x = tf.keras.layers.MaxPooling2D(2, padding='same')(x)
x = tf.keras.layers.Conv2D(8, 3, activation='relu', padding='same')(x)
encoded = tf.keras.layers.MaxPooling2D(2, padding='same')(x)

x = tf.keras.layers.Conv2DTranspose(8, 3, strides=2, activation='relu', padding='same')(encoded)
x = tf.keras.layers.Conv2DTranspose(16, 3, strides=2, activation='relu', padding='same')(x)
decoded = tf.keras.layers.Conv2D(1, 3, activation='sigmoid', padding='same')(x)

autoencoder = tf.keras.Model(inp, decoded)
autoencoder.compile(optimizer='adam', loss='mse')
autoencoder.fit(x_train, x_train, epochs=5, batch_size=128, validation_data=(x_test, x_test))

# Predict and display input vs output
decoded_imgs = autoencoder.predict(x_test[:10])

plt.figure(figsize=(20, 4))
for i in range(10):
    # Original
    ax = plt.subplot(2, 10, i + 1)
    plt.imshow(x_test[i].squeeze(), cmap='gray')
    plt.axis("off")

    # Reconstructed
    ax = plt.subplot(2, 10, i + 11)
    plt.imshow(decoded_imgs[i].squeeze(), cmap='gray')
    plt.axis("off")
plt.show()


''')


def cifar2():
    print('''


import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import cifar10

(x_train, _), (x_test, _) = cifar10.load_data()

x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.

def add_noise(images, noise_factor=0.15):
    noisy_images = images + noise_factor * np.random.randn(*images.shape)
    noisy_images = np.clip(noisy_images, 0., 1.)
    return noisy_images

x_train_noisy = add_noise(x_train)
x_test_noisy = add_noise(x_test)
def build_denoising_autoencoder(input_shape):
    model = models.Sequential()

    model.add(layers.InputLayer(input_shape=input_shape))
    model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(layers.MaxPooling2D((2, 2), padding='same'))
    model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(layers.MaxPooling2D((2, 2), padding='same'))

    model.add(layers.Conv2DTranspose(64, (3, 3), activation='relu', padding='same'))
    model.add(layers.UpSampling2D((2, 2)))
    model.add(layers.Conv2DTranspose(32, (3, 3), activation='relu', padding='same'))
    model.add(layers.UpSampling2D((2, 2)))
    model.add(layers.Conv2D(3, (3, 3), activation='sigmoid', padding='same'))  # Final layer with sigmoid

    return model

autoencoder = build_denoising_autoencoder(x_train.shape[1:])
autoencoder.compile(optimizer='adam', loss='mse')
autoencoder.summary()
history = autoencoder.fit(
    x_train_noisy, x_train,
    epochs=10,
    batch_size=128,
    validation_data=(x_test_noisy, x_test)
)


# Plot training and validation loss curves
plt.figure(figsize=(8, 5))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss Curve')
plt.xlabel('Epoch')
plt.ylabel('MSE Loss')
plt.legend()
plt.grid(True)
plt.show()


reconstructed_images = autoencoder.predict(x_test_noisy)

def display_comparison(noisy, reconstructed, original, n=5):
    plt.figure(figsize=(10, 4))
    for i in range(n):
        ax = plt.subplot(3, n, i + 1)
        plt.imshow(noisy[i])
        plt.title("Noisy")
        plt.axis('off')

        ax = plt.subplot(3, n, i + 1 + n)
        plt.imshow(reconstructed[i])
        plt.title("Reconstructed")
        plt.axis('off')

        ax = plt.subplot(3, n, i + 1 + 2 * n)
        plt.imshow(original[i])
        plt.title("Original")
        plt.axis('off')
    plt.show()

display_comparison(x_test_noisy, reconstructed_images, x_test)

          




import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist

# Load MNIST dataset
(x_train, _), (x_test, _) = mnist.load_data()

# Normalize and reshape to (28, 28, 1)
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = np.expand_dims(x_train, axis=-1)
x_test = np.expand_dims(x_test, axis=-1)

# Add noise
def add_noise(images, noise_factor=0.5):
    noisy = images + noise_factor * np.random.randn(*images.shape)
    noisy = np.clip(noisy, 0., 1.)
    return noisy

x_train_noisy = add_noise(x_train)
x_test_noisy = add_noise(x_test)

# Denoising autoencoder model
def build_denoising_autoencoder(input_shape):
    model = models.Sequential()
    model.add(layers.InputLayer(input_shape=input_shape))

    # Encoder
    model.add(layers.Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(layers.MaxPooling2D((2, 2), padding='same'))  # 14x14
    model.add(layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(layers.MaxPooling2D((2, 2), padding='same'))  # 7x7

    # Decoder
    model.add(layers.Conv2DTranspose(64, (3, 3), strides=2, activation='relu', padding='same'))  # 14x14
    model.add(layers.Conv2DTranspose(32, (3, 3), strides=2, activation='relu', padding='same'))  # 28x28
    model.add(layers.Conv2D(1, (3, 3), activation='sigmoid', padding='same'))  # 28x28x1 output

    return model


# Build and train the model
autoencoder = build_denoising_autoencoder(x_train.shape[1:])
autoencoder.compile(optimizer='adam', loss='mse')
autoencoder.summary()

history = autoencoder.fit(
    x_train_noisy, x_train,
    epochs=10,
    batch_size=128,
    validation_data=(x_test_noisy, x_test)
)

# Plot loss curve
plt.figure(figsize=(8, 5))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss Curve')
plt.xlabel('Epoch')
plt.ylabel('MSE Loss')
plt.legend()
plt.grid(True)
plt.show()

# Reconstruct images
reconstructed_images = autoencoder.predict(x_test_noisy)

# Display comparison
def display_comparison(noisy, reconstructed, original, n=5):
    plt.figure(figsize=(10, 4))
    for i in range(n):
        ax = plt.subplot(3, n, i + 1)
        plt.imshow(noisy[i].squeeze(), cmap='gray')
        plt.title("Noisy")
        plt.axis('off')

        ax = plt.subplot(3, n, i + 1 + n)
        plt.imshow(reconstructed[i].squeeze(), cmap='gray')
        plt.title("Reconstructed")
        plt.axis('off')

        ax = plt.subplot(3, n, i + 1 + 2 * n)
        plt.imshow(original[i].squeeze(), cmap='gray')
        plt.title("Original")
        plt.axis('off')
    plt.show()

display_comparison(x_test_noisy, reconstructed_images, x_test)


''')
    

def cifar3():
    print('''

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt

# Set random seeds for reproducibility
tf.random.set_seed(42)
np.random.seed(42)

class VAE(keras.Model):
    def __init__(self, latent_dim=2, **kwargs):
        super(VAE, self).__init__(**kwargs)
        self.latent_dim = latent_dim
        
        # Encoder
        self.encoder = keras.Sequential([
            layers.InputLayer(input_shape=(28, 28, 1)),
            layers.Conv2D(32, 3, activation="relu", strides=2, padding="same"),
            layers.Conv2D(64, 3, activation="relu", strides=2, padding="same"),
            layers.Flatten(),
            layers.Dense(16, activation="relu"),
        ])
        
        # Latent space parameters
        self.z_mean = layers.Dense(latent_dim)
        self.z_log_var = layers.Dense(latent_dim)
        
        # Decoder
        self.decoder = keras.Sequential([
            layers.InputLayer(input_shape=(latent_dim,)),
            layers.Dense(7 * 7 * 32, activation="relu"),
            layers.Reshape((7, 7, 32)),
            layers.Conv2DTranspose(64, 3, activation="relu", strides=2, padding="same"),
            layers.Conv2DTranspose(32, 3, activation="relu", strides=2, padding="same"),
            layers.Conv2DTranspose(1, 3, activation="sigmoid", padding="same"),
        ])
    
    def encode(self, x):
        """Encode input to latent parameters"""
        h = self.encoder(x)
        z_mean = self.z_mean(h)
        z_log_var = self.z_log_var(h)
        return z_mean, z_log_var
    
    def reparameterize(self, z_mean, z_log_var):
        """Reparameterization trick"""
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon
    
    def decode(self, z):
        """Decode latent vector to image"""
        return self.decoder(z)
    
    def call(self, inputs):
        """Forward pass"""
        z_mean, z_log_var = self.encode(inputs)
        z = self.reparameterize(z_mean, z_log_var)
        reconstructed = self.decode(z)
        
        # Add KL divergence loss
        kl_loss = -0.5 * tf.reduce_mean(
            z_log_var - tf.square(z_mean) - tf.exp(z_log_var) + 1
        )
        self.add_loss(kl_loss)
        
        return reconstructed

def load_and_preprocess_data():
    """Load and preprocess MNIST data"""
    (x_train, _), (x_test, _) = keras.datasets.mnist.load_data()
    
    # Normalize to [0, 1] range
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0
    
    # Add channel dimension
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)
    
    return x_train, x_test

def train_vae(vae, x_train, x_test, epochs=50, batch_size=128):
    """Train the VAE"""
    # Compile model
    vae.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    # Train model
    history = vae.fit(
        x_train, x_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(x_test, x_test),
        verbose=1
    )
    
    return history

def plot_latent_space(vae, x_test, y_test=None, n_samples=5000):
    """Plot the latent space representation"""
    # Encode test data
    z_mean, _ = vae.encode(x_test[:n_samples])
    
    plt.figure(figsize=(10, 8))
    if y_test is not None:
        scatter = plt.scatter(z_mean[:, 0], z_mean[:, 1], c=y_test[:n_samples], 
                            cmap='tab10', alpha=0.6)
        plt.colorbar(scatter)
    else:
        plt.scatter(z_mean[:, 0], z_mean[:, 1], alpha=0.6)
    
    plt.xlabel('Latent Dimension 1')
    plt.ylabel('Latent Dimension 2')
    plt.title('Latent Space Representation')
    plt.show()

def generate_images(vae, n_samples=16):
    """Generate new images by sampling from latent space"""
    # Sample from standard normal distribution
    z_samples = tf.random.normal(shape=(n_samples, vae.latent_dim))
    
    # Decode to generate images
    generated_images = vae.decode(z_samples)
    
    # Plot generated images
    fig, axes = plt.subplots(4, 4, figsize=(10, 10))
    for i, ax in enumerate(axes.flat):
        ax.imshow(generated_images[i, :, :, 0], cmap='gray')
        ax.axis('off')
    
    plt.suptitle('Generated Images')
    plt.tight_layout()
    plt.show()

def plot_reconstructions(vae, x_test, n_samples=8):
    """Plot original vs reconstructed images"""
    reconstructions = vae(x_test[:n_samples])
    
    fig, axes = plt.subplots(2, n_samples, figsize=(15, 4))
    
    for i in range(n_samples):
        # Original images
        axes[0, i].imshow(x_test[i, :, :, 0], cmap='gray')
        axes[0, i].set_title('Original')
        axes[0, i].axis('off')
        
        # Reconstructed images
        axes[1, i].imshow(reconstructions[i, :, :, 0], cmap='gray')
        axes[1, i].set_title('Reconstructed')
        axes[1, i].axis('off')
    
    plt.tight_layout()
    plt.show()

def interpolate_images(vae, x1, x2, n_steps=10):
    """Interpolate between two images in latent space"""
    # Encode the two images
    z1_mean, _ = vae.encode(x1[np.newaxis, :])
    z2_mean, _ = vae.encode(x2[np.newaxis, :])
    
    # Create interpolation path
    alphas = np.linspace(0, 1, n_steps)
    interpolated_images = []
    
    for alpha in alphas:
        z_interp = (1 - alpha) * z1_mean + alpha * z2_mean
        img = vae.decode(z_interp)
        interpolated_images.append(img[0])
    
    # Plot interpolation
    fig, axes = plt.subplots(1, n_steps, figsize=(15, 2))
    for i, ax in enumerate(axes):
        ax.imshow(interpolated_images[i][:, :, 0], cmap='gray')
        ax.axis('off')
    
    plt.suptitle('Latent Space Interpolation')
    plt.tight_layout()
    plt.show()

def main():
    """Main training and evaluation function"""
    print("Loading and preprocessing MNIST data...")
    x_train, x_test = load_and_preprocess_data()
    
    print(f"Training data shape: {x_train.shape}")
    print(f"Test data shape: {x_test.shape}")
    
    # Create VAE model
    latent_dim = 2  # 2D for easy visualization
    vae = VAE(latent_dim=latent_dim)
    
    print(f"\\nTraining VAE with latent dimension: {latent_dim}")
    
    # Train the model
    history = train_vae(vae, x_train, x_test, epochs=30, batch_size=128)
    
    # Plot training history
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Training Accuracy') 
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    print("\\nEvaluating VAE...")
    
    # Load labels for latent space visualization
    (_, y_train), (_, y_test) = keras.datasets.mnist.load_data()
    
    # Visualize latent space
    plot_latent_space(vae, x_test, y_test)
    
    # Show reconstructions
    plot_reconstructions(vae, x_test)
    
    # Generate new images
    generate_images(vae, n_samples=16)
    
    # Show interpolation between two test images
    interpolate_images(vae, x_test[0], x_test[100])
    
    print("VAE training and evaluation complete!")

if __name__ == "__main__":
    main()

          







OR
          







import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import numpy as np

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")

class VAE(nn.Module):
    def __init__(self, input_dim=784, hidden_dim=400, latent_dim=20):
        super(VAE, self).__init__()
        
        # Encoder
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU()
        )
        
        # Latent space parameters
        self.fc_mu = nn.Linear(hidden_dim, latent_dim)
        self.fc_logvar = nn.Linear(hidden_dim, latent_dim)
        
        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim),
            nn.Sigmoid()  # Output probabilities for binary cross-entropy
        )
        
        self.latent_dim = latent_dim
    
    def encode(self, x):
        """Encode input to latent space parameters"""
        h = self.encoder(x)
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar
    
    def reparameterize(self, mu, logvar):
        """Reparameterization trick for backpropagation through sampling"""
        if self.training:
            std = torch.exp(0.5 * logvar)
            eps = torch.randn_like(std)
            return mu + eps * std
        else:
            return mu
    
    def decode(self, z):
        """Decode latent variables to reconstruction"""
        return self.decoder(z)
    
    def forward(self, x):
        """Full forward pass"""
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        reconstruction = self.decode(z)
        return reconstruction, mu, logvar

def vae_loss(recon_x, x, mu, logvar, beta=1.0):
    """
    VAE loss function with proper numerical stability
    
    Args:
        recon_x: Reconstructed data
        x: Original data
        mu: Mean of latent distribution
        logvar: Log variance of latent distribution
        beta: Beta parameter for beta-VAE (controls KL weight)
    """
    # Reconstruction loss (Binary Cross Entropy)
    # Use reduction='sum' to match original VAE paper
    BCE = F.binary_cross_entropy(recon_x, x, reduction='sum')
    
    # KL divergence loss
    # KL(q(z|x) || p(z)) where p(z) = N(0,I)
    # = -0.5 * sum(1 + log(sigma^2) - mu^2 - sigma^2)
    KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    
    return BCE + beta * KLD, BCE, KLD

def train_vae(model, train_loader, optimizer, epoch, beta=1.0):
    """Train VAE for one epoch"""
    model.train()
    train_loss = 0
    train_bce = 0
    train_kld = 0
    
    for batch_idx, (data, _) in enumerate(train_loader):
        data = data.view(-1, 784).to(device)
        
        optimizer.zero_grad()
        
        # Forward pass
        recon_batch, mu, logvar = model(data)
        
        # Calculate loss
        loss, bce, kld = vae_loss(recon_batch, data, mu, logvar, beta)
        
        # Backward pass
        loss.backward()
        
        # Gradient clipping to prevent exploding gradients
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        
        optimizer.step()
        
        train_loss += loss.item()
        train_bce += bce.item()
        train_kld += kld.item()
        
        if batch_idx % 100 == 0:
            print(f'Train Epoch: {epoch} [{batch_idx * len(data)}/{len(train_loader.dataset)} '
                  f'({100. * batch_idx / len(train_loader):.0f}%)]\t'
                  f'Loss: {loss.item() / len(data):.6f} '
                  f'BCE: {bce.item() / len(data):.6f} '
                  f'KLD: {kld.item() / len(data):.6f}')
    
    avg_loss = train_loss / len(train_loader.dataset)
    avg_bce = train_bce / len(train_loader.dataset)
    avg_kld = train_kld / len(train_loader.dataset)
    
    print(f'====> Epoch: {epoch} Average loss: {avg_loss:.4f} '
          f'BCE: {avg_bce:.4f} KLD: {avg_kld:.4f}')
    
    return avg_loss, avg_bce, avg_kld

def test_vae(model, test_loader, beta=1.0):
    """Test VAE"""
    model.eval()
    test_loss = 0
    test_bce = 0
    test_kld = 0
    
    with torch.no_grad():
        for data, _ in test_loader:
            data = data.view(-1, 784).to(device)
            recon_batch, mu, logvar = model(data)
            
            loss, bce, kld = vae_loss(recon_batch, data, mu, logvar, beta)
            test_loss += loss.item()
            test_bce += bce.item()
            test_kld += kld.item()
    
    avg_loss = test_loss / len(test_loader.dataset)
    avg_bce = test_bce / len(test_loader.dataset)
    avg_kld = test_kld / len(test_loader.dataset)
    
    print(f'====> Test set loss: {avg_loss:.4f} '
          f'BCE: {avg_bce:.4f} KLD: {avg_kld:.4f}')
    
    return avg_loss, avg_bce, avg_kld

def generate_samples(model, num_samples=16):
    """Generate new samples from the trained VAE"""
    model.eval()
    with torch.no_grad():
        # Sample from prior distribution
        z = torch.randn(num_samples, model.latent_dim).to(device)
        samples = model.decode(z)
        return samples

def visualize_reconstruction(model, test_loader, num_images=8):
    """Visualize original vs reconstructed images"""
    model.eval()
    with torch.no_grad():
        data, _ = next(iter(test_loader))
        data = data[:num_images].to(device)
        data_flat = data.view(-1, 784)
        
        recon_batch, _, _ = model(data_flat)
        
        # Plot original and reconstructed images
        fig, axes = plt.subplots(2, num_images, figsize=(num_images * 2, 4))
        
        for i in range(num_images):
            # Original images
            axes[0, i].imshow(data[i].cpu().squeeze(), cmap='gray')
            axes[0, i].set_title('Original')
            axes[0, i].axis('off')
            
            # Reconstructed images
            axes[1, i].imshow(recon_batch[i].cpu().view(28, 28), cmap='gray')
            axes[1, i].set_title('Reconstructed')
            axes[1, i].axis('off')
        
        plt.tight_layout()
        plt.show()

def visualize_latent_space(model, test_loader, num_batches=10):
    """Visualize the learned latent space (for 2D latent space)"""
    if model.latent_dim != 2:
        print("Latent space visualization only available for 2D latent space")
        return
    
    model.eval()
    latents = []
    labels = []
    
    with torch.no_grad():
        for batch_idx, (data, label) in enumerate(test_loader):
            if batch_idx >= num_batches:
                break
            
            data = data.view(-1, 784).to(device)
            mu, _ = model.encode(data)
            latents.append(mu.cpu().numpy())
            labels.append(label.numpy())
    
    latents = np.concatenate(latents, axis=0)
    labels = np.concatenate(labels, axis=0)
    
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(latents[:, 0], latents[:, 1], c=labels, cmap='tab10')
    plt.colorbar(scatter)
    plt.title('Latent Space Visualization')
    plt.xlabel('Latent Dimension 1')
    plt.ylabel('Latent Dimension 2')
    plt.show()

def visualize_latent_space_generation(model, epoch, grid_size=10, latent_range=3):
    """
    Generate images by sampling from a grid in the latent space
    Works best with 2D latent space but can work with higher dimensions too
    """
    model.eval()
    
    if model.latent_dim == 2:
        # For 2D latent space, create a 2D grid
        x = np.linspace(-latent_range, latent_range, grid_size)
        y = np.linspace(-latent_range, latent_range, grid_size)
        
        figure = np.zeros((grid_size * 28, grid_size * 28))
        
        with torch.no_grad():
            for i, xi in enumerate(x):
                for j, yi in enumerate(y):
                    z_sample = torch.tensor([[xi, yi]], dtype=torch.float32).to(device)
                    x_decoded = model.decode(z_sample)
                    digit = x_decoded[0].cpu().view(28, 28).numpy()
                    figure[i * 28: (i + 1) * 28, j * 28: (j + 1) * 28] = digit
        
        plt.figure(figsize=(10, 10))
        plt.imshow(figure, cmap='gray')
        plt.title(f'Latent Space Generation Grid - Epoch {epoch}')
        plt.axis('off')
        plt.show()
    
    else:
        # For higher dimensional latent space, show interpolations
        visualize_latent_interpolation(model, epoch)

def visualize_latent_interpolation(model, epoch, num_interpolations=10):
    """
    Visualize interpolations in latent space between random points
    """
    model.eval()
    
    with torch.no_grad():
        # Sample two random points in latent space
        z1 = torch.randn(1, model.latent_dim).to(device)
        z2 = torch.randn(1, model.latent_dim).to(device)
        
        # Create interpolation steps
        alpha = torch.linspace(0, 1, num_interpolations).to(device)
        
        interpolated_images = []
        for a in alpha:
            z_interp = (1 - a) * z1 + a * z2
            x_decoded = model.decode(z_interp)
            interpolated_images.append(x_decoded[0].cpu().view(28, 28).numpy())
        
        # Plot interpolation
        fig, axes = plt.subplots(1, num_interpolations, figsize=(num_interpolations * 2, 2))
        for i, img in enumerate(interpolated_images):
            axes[i].imshow(img, cmap='gray')
            axes[i].axis('off')
            axes[i].set_title(f'{i/(num_interpolations-1):.1f}')
        
        plt.suptitle(f'Latent Space Interpolation - Epoch {epoch}')
        plt.tight_layout()
        plt.show()

def visualize_digit_morphing(model, test_loader, epoch):
    """
    Show morphing between different digits by interpolating in latent space
    """
    model.eval()
    
    with torch.no_grad():
        # Get samples of different digits
        digit_samples = {}
        for data, labels in test_loader:
            for i, label in enumerate(labels):
                digit = label.item()
                if digit not in digit_samples:
                    sample_data = data[i:i+1].view(-1, 784).to(device)
                    mu, _ = model.encode(sample_data)
                    digit_samples[digit] = mu[0]
                    
                if len(digit_samples) >= 10:  # Got all digits
                    break
            if len(digit_samples) >= 10:
                break
        
        # Show morphing between digits 0 and 9
        if 0 in digit_samples and 9 in digit_samples:
            z_start = digit_samples[0].unsqueeze(0)
            z_end = digit_samples[9].unsqueeze(0)
            
            num_steps = 10
            alpha = torch.linspace(0, 1, num_steps).to(device)
            
            morphed_images = []
            for a in alpha:
                z_morph = (1 - a) * z_start + a * z_end
                x_decoded = model.decode(z_morph)
                morphed_images.append(x_decoded[0].cpu().view(28, 28).numpy())
            
            # Plot morphing sequence
            fig, axes = plt.subplots(1, num_steps, figsize=(num_steps * 1.5, 2))
            for i, img in enumerate(morphed_images):
                axes[i].imshow(img, cmap='gray')
                axes[i].axis('off')
                if i == 0:
                    axes[i].set_title('0')
                elif i == num_steps - 1:
                    axes[i].set_title('9')
                else:
                    axes[i].set_title(f'{i/(num_steps-1):.1f}')
            
            plt.suptitle(f'Digit Morphing (0→9) - Epoch {epoch}')
            plt.tight_layout()
            plt.show()

def plot_generated_samples(model, num_samples=16):
    """Plot generated samples"""
    samples = generate_samples(model, num_samples)
    
    fig, axes = plt.subplots(4, 4, figsize=(8, 8))
    for i, ax in enumerate(axes.flat):
        ax.imshow(samples[i].cpu().view(28, 28), cmap='gray')
        ax.axis('off')
    
    plt.suptitle('Generated Samples')
    plt.tight_layout()
    plt.show()

# Main training script
def main():
    # Hyperparameters
    batch_size = 128
    learning_rate = 1e-3
    num_epochs = 50
    latent_dim = 20  # Change to 2 for latent space visualization
    beta = 1.0  # Beta parameter for beta-VAE
    
    # Data loading
    transform = transforms.Compose([
        transforms.ToTensor(),
        # Note: We don't normalize to [-1,1] since we use sigmoid output and BCE loss
    ])
    
    train_dataset = datasets.MNIST('data', train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST('data', train=False, transform=transform)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    # Model initialization
    model = VAE(input_dim=784, hidden_dim=400, latent_dim=latent_dim).to(device)
    
    # Optimizer
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Learning rate scheduler
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=20, gamma=0.8)
    
    # Training loop
    train_losses = []
    test_losses = []
    
    print("Starting training...")
    for epoch in range(1, num_epochs + 1):
        train_loss, train_bce, train_kld = train_vae(model, train_loader, optimizer, epoch, beta)
        test_loss, test_bce, test_kld = test_vae(model, test_loader, beta)
        
        train_losses.append(train_loss)
        test_losses.append(test_loss)
        
        # Step the scheduler
        scheduler.step()
        
        # Visualize progress every 10 epochs
        if epoch % 10 == 0:
            print(f"\\nEpoch {epoch} - Generating samples and reconstructions...")
            visualize_reconstruction(model, test_loader)
            plot_generated_samples(model)
            
            # Show latent space visualizations
            print(f"Visualizing latent space at epoch {epoch}...")
            if latent_dim == 2:
                visualize_latent_space(model, test_loader)
                visualize_latent_space_generation(model, epoch)
            else:
                visualize_latent_space_generation(model, epoch)
            
            # Show digit morphing
            visualize_digit_morphing(model, test_loader, epoch)
    
    # Plot training curves
    plt.figure(figsize=(10, 5))
    plt.plot(train_losses, label='Train Loss')
    plt.plot(test_losses, label='Test Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.title('VAE Training Curves')
    plt.show()
    
    # Final evaluation
    print("\\nFinal evaluation:")
    test_vae(model, test_loader, beta)
    
    # Generate final samples
    print("Generating final samples...")
    plot_generated_samples(model, 16)
    
    # Save the model
    torch.save(model.state_dict(), 'vae_mnist.pth')
    print("Model saved as 'vae_mnist.pth'")
    
    return model

if __name__ == "__main__":
    # Set random seeds for reproducibility
    torch.manual_seed(42)
    np.random.seed(42)
    
    model = main()








''')
    

def cifar4():
    print('''



import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import BernoulliRBM
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.datasets import fetch_openml
from sklearn.metrics import accuracy_score

mnist = fetch_openml('mnist_784', version=1)
X, y = mnist.data.astype(np.float32), mnist.target.astype(int)

scaler = MinMaxScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rbm = BernoulliRBM(n_components=100, learning_rate=0.06, n_iter=10, random_state=42)
rbm.fit(X_train)

X_train_rbm = rbm.transform(X_train)
X_test_rbm = rbm.transform(X_test)

classifier = LogisticRegression(max_iter=200, solver='lbfgs', multi_class='multinomial', random_state=42)
classifier.fit(X_train_rbm, y_train)

y_pred = classifier.predict(X_test_rbm)

accuracy = accuracy_score(y_test, y_pred)
print(f"Classification Accuracy: {accuracy:.4f}")

num_samples = 10
fig, axes = plt.subplots(1, num_samples, figsize=(15, 3))

for i in range(num_samples):
    ax = axes[i]
    ax.imshow(X_test[i].reshape(28, 28), cmap='gray')
    ax.set_title(f"Pred: {y_pred[i]}")
    ax.axis("off")

plt.show()

          

''')
    
def cifar5():
    print('''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import BernoulliRBM
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load and preprocess MNIST
print("Loading MNIST dataset...")
mnist = fetch_openml('mnist_784', version=1)
X, y = mnist["data"], mnist["target"].astype(np.int32)

# Normalize the data to [0, 1]
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Define two stacked RBMs
rbm1 = BernoulliRBM(n_components=100, learning_rate=0.05, n_iter=10, verbose=True, random_state=0)
rbm2 = BernoulliRBM(n_components=100, learning_rate=0.05, n_iter=10, verbose=True, random_state=0)

# Train first RBM on raw input
print("\\nTraining RBM Layer 1...")
X_train_rbm1 = rbm1.fit_transform(X_train)

# Train second RBM on output of first
print("\\nTraining RBM Layer 2...")
X_train_rbm2 = rbm2.fit_transform(X_train_rbm1)

# Train logistic regression classifier on final RBM output
print("\\nTraining classifier on RBM2 features...")
clf = LogisticRegression(max_iter=1000, solver='lbfgs', multi_class='multinomial')
clf.fit(X_train_rbm2, y_train)

# Transform test data through both RBMs
X_test_rbm1 = rbm1.transform(X_test)
X_test_rbm2 = rbm2.transform(X_test_rbm1)

# Predict and evaluate
y_pred = clf.predict(X_test_rbm2)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\\n🔹 Accuracy: {accuracy:.4f}")

# Classification report
print("\\n🔹 Classification Report:")
print(classification_report(y_test, y_pred))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=range(10), yticklabels=range(10))
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()


''')
    
def cifar6():
    print('''

import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load MNIST data
print("Loading MNIST...")
mnist = fetch_openml('mnist_784', version=1)
X, y = mnist.data / 255.0, mnist.target.astype(np.int32)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------------------------------
# Helper: build and train an autoencoder
# ---------------------------------------
def build_autoencoder(input_dim, encoding_dim):
    input_img = tf.keras.Input(shape=(input_dim,))
    encoded = layers.Dense(encoding_dim, activation='relu')(input_img)
    decoded = layers.Dense(input_dim, activation='sigmoid')(encoded)
    autoencoder = models.Model(input_img, decoded)
    encoder = models.Model(input_img, encoded)
    autoencoder.compile(optimizer='adam', loss='mse')
    return autoencoder, encoder

# Layer 1 Autoencoder
print("Training Encoder 1...")
ae1, enc1 = build_autoencoder(784, 512)
ae1.fit(X_train, X_train, epochs=10, batch_size=256, shuffle=True, verbose=1)

# Layer 2 Autoencoder
X_train_enc1 = enc1.predict(X_train)
print("Training Encoder 2...")
ae2, enc2 = build_autoencoder(512, 256)
ae2.fit(X_train_enc1, X_train_enc1, epochs=10, batch_size=256, shuffle=True, verbose=1)

# Encode the test set
X_test_enc1 = enc1.predict(X_test)
X_test_enc2 = enc2.predict(X_test_enc1)

# ---------------------------------------
# Stack encoders + classifier (DBN-style)
# ---------------------------------------
print("Training final classifier...")
final_model = tf.keras.Sequential()
final_model.add(tf.keras.Input(shape=(784,)))

# Add first dense layer and set weights from AE1
dense1 = tf.keras.layers.Dense(512, activation='relu')
final_model.add(dense1)

dense1.set_weights(ae1.layers[1].get_weights())

# Add second dense layer and set weights from AE2
dense2 = tf.keras.layers.Dense(256, activation='relu')
final_model.add(dense2)
dense2.set_weights(ae2.layers[1].get_weights())

# Add final output layer
final_model.add(tf.keras.layers.Dense(10, activation='softmax'))

# Compile and train
final_model.compile(optimizer='adam',
                    loss='sparse_categorical_crossentropy',
                    metrics=['accuracy'])
final_model.fit(X_train, y_train, epochs=10, batch_size=256, validation_split=0.1)

# ---------------------------------------
# Evaluation
# ---------------------------------------
y_pred_probs = final_model.predict(X_test)
y_pred = np.argmax(y_pred_probs, axis=1)

acc = accuracy_score(y_test, y_pred)
print(f"\\n🔹 Accuracy: {acc:.4f}")
print("\\n🔹 Classification Report:\\n", classification_report(y_test, y_pred))

# Confusion Matrix
plt.figure(figsize=(10, 8))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues', xticklabels=range(10), yticklabels=range(10))
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()


          



OR 
          

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neural_network import BernoulliRBM
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Step 1: Load and Preprocess MNIST
print("Loading MNIST...")
mnist = fetch_openml('mnist_784', version=1)
X, y = mnist["data"], mnist["target"].astype(int)

# Normalize the data
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Step 2: Stack RBMs for Deep Belief Network (DBN-like)
print("Training stacked RBMs...")

rbm1 = BernoulliRBM(n_components=100, learning_rate=0.05, n_iter=10, random_state=0, verbose=True)
rbm2 = BernoulliRBM(n_components=100, learning_rate=0.05, n_iter=10, random_state=0, verbose=True)

# Transformations through RBM1 and RBM2
X_train_rbm1 = rbm1.fit_transform(X_train)
X_train_rbm2 = rbm2.fit_transform(X_train_rbm1)

X_test_rbm1 = rbm1.transform(X_test)
X_test_rbm2 = rbm2.transform(X_test_rbm1)

# Step 3: Train a Classifier (fine-tuning step)
print("Training classifier...")
clf = LogisticRegression(max_iter=1000, solver='lbfgs', multi_class='multinomial')
clf.fit(X_train_rbm2, y_train)

# Predict
y_pred = clf.predict(X_test_rbm2)

# Step 4: Evaluation
print("\\n🔹 Accuracy:", accuracy_score(y_test, y_pred))
print("\\n🔹 Classification Report:\\n", classification_report(y_test, y_pred))

# Step 5: Confusion Matrix
plt.figure(figsize=(10, 8))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues', xticklabels=range(10), yticklabels=range(10))
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()




''')
    
def cifar7():
    print('''

import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from sklearn.preprocessing import binarize
import matplotlib.pyplot as plt

# Set random seed
np.random.seed(42)
tf.random.set_seed(42)

# Load and preprocess MNIST data
(x_train, _), (_, _) = mnist.load_data()
x_train = x_train.reshape(-1, 784).astype(np.float32) / 255.0
x_train = binarize(x_train, threshold=0.5).astype(np.float32)



# Define RBM class
class RBM:
    def __init__(self, n_visible, n_hidden, learning_rate=0.01):
        self.n_visible = n_visible
        self.n_hidden = n_hidden
        self.learning_rate = learning_rate

        self.W = tf.Variable(tf.random.normal([n_visible, n_hidden], mean=0.0, stddev=0.01), name="weights")
        self.bv = tf.Variable(tf.zeros([n_visible]), name="visible_bias")
        self.bh = tf.Variable(tf.zeros([n_hidden]), name="hidden_bias")

    def sample_prob(self, probs):
        return tf.nn.relu(tf.sign(probs - tf.random.uniform(tf.shape(probs))))

    def gibbs_step(self, v):
        h_prob = tf.nn.sigmoid(tf.matmul(v, self.W) + self.bh)
        h_sample = self.sample_prob(h_prob)
        v_prob = tf.nn.sigmoid(tf.matmul(h_sample, tf.transpose(self.W)) + self.bv)
        v_sample = self.sample_prob(v_prob)
        return v_sample, h_sample

    def contrastive_divergence(self, v_input):
        h_prob = tf.nn.sigmoid(tf.matmul(v_input, self.W) + self.bh)
        h_sample = self.sample_prob(h_prob)

        v_recon_prob = tf.nn.sigmoid(tf.matmul(h_sample, tf.transpose(self.W)) + self.bv)
        h_recon_prob = tf.nn.sigmoid(tf.matmul(v_recon_prob, self.W) + self.bh)

        positive_grad = tf.matmul(tf.transpose(v_input), h_prob)
        negative_grad = tf.matmul(tf.transpose(v_recon_prob), h_recon_prob)

        self.W.assign_add(self.learning_rate * (positive_grad - negative_grad) / tf.cast(tf.shape(v_input)[0], tf.float32))
        self.bv.assign_add(self.learning_rate * tf.reduce_mean(v_input - v_recon_prob, axis=0))
        self.bh.assign_add(self.learning_rate * tf.reduce_mean(h_prob - h_recon_prob, axis=0))

    def get_hidden(self, v):
        return tf.nn.sigmoid(tf.matmul(v, self.W) + self.bh)

    def reconstruct(self, v):
        h = self.get_hidden(v)
        v_recon = tf.nn.sigmoid(tf.matmul(h, tf.transpose(self.W)) + self.bv)
        return v_recon

# Train RBMs layer-wise
def train_rbm(rbm, data, epochs=10, batch_size=64):
    for epoch in range(epochs):
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]
            rbm.contrastive_divergence(batch)
        recon = rbm.reconstruct(data).numpy()
        loss = np.mean(np.square(data - recon))
        print(f"Epoch {epoch+1}, Reconstruction Loss: {loss:.4f}")

# Define DBM architecture (784-500-200)
rbm1 = RBM(n_visible=784, n_hidden=500, learning_rate=0.01)
rbm2 = RBM(n_visible=500, n_hidden=200, learning_rate=0.01)

# Train first RBM
print("\\nTraining RBM 1 (784 -> 500)...")
train_rbm(rbm1, x_train, epochs=10)

# Get transformed data for second RBM
h1_train = rbm1.get_hidden(x_train).numpy()

# Train second RBM
print("\\nTraining RBM 2 (500 -> 200)...")
train_rbm(rbm2, h1_train, epochs=10)

# Sampling from the DBM (up-down pass)
def sample_dbm(rbm1, rbm2, steps=1):
    v = tf.random.uniform([1, 784])
    for _ in range(steps):
        h1 = rbm1.sample_prob(tf.nn.sigmoid(tf.matmul(v, rbm1.W) + rbm1.bh))
        h2 = rbm2.sample_prob(tf.nn.sigmoid(tf.matmul(h1, rbm2.W) + rbm2.bh))
        h1_down = rbm2.sample_prob(tf.nn.sigmoid(tf.matmul(h2, tf.transpose(rbm2.W)) + rbm2.bv))
        v = rbm1.sample_prob(tf.nn.sigmoid(tf.matmul(h1_down, tf.transpose(rbm1.W)) + rbm1.bv))
    return v

# Generate a sample
generated = sample_dbm(rbm1, rbm2, steps=50).numpy().reshape(28, 28)
plt.imshow(generated, cmap='gray')
plt.title("Sampled Image from DBM")
plt.axis('off')
plt.show()


''')
    
def cifar8():
    print('''

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist

# Load and normalize MNIST
(x_train, _), (x_test, _) = mnist.load_data()
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

# Reshape to add channel dimension
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)

# Define Convolutional Autoencoder
def build_autoencoder():
    input_img = layers.Input(shape=(28, 28, 1))

    # Encoder
    x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(input_img)
    x = layers.MaxPooling2D((2, 2), padding='same')(x)  # 14x14
    x = layers.Conv2D(16, (3, 3), activation='relu', padding='same')(x)
    encoded = layers.MaxPooling2D((2, 2), padding='same')(x)  # 7x7

    # Decoder
    x = layers.Conv2D(16, (3, 3), activation='relu', padding='same')(encoded)
    x = layers.UpSampling2D((2, 2))(x)  # 14x14
    x = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(x)
    x = layers.UpSampling2D((2, 2))(x)  # 28x28
    decoded = layers.Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)

    autoencoder = models.Model(input_img, decoded)
    return autoencoder

autoencoder = build_autoencoder()
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
autoencoder.summary()

# Train the model
autoencoder.fit(
    x_train, x_train,
    epochs=10,
    batch_size=128,
    shuffle=True,
    validation_data=(x_test, x_test)
)

# Reconstruct test images
decoded_imgs = autoencoder.predict(x_test)

# Display original vs reconstructed
n = 10
plt.figure(figsize=(20, 4))
for i in range(n):
    # Original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i].squeeze(), cmap="gray")
    plt.title("Original")
    plt.axis("off")

    # Reconstructed
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_imgs[i].squeeze(), cmap="gray")
    plt.title("Reconstructed")
    plt.axis("off")
plt.tight_layout()
plt.show()


''')
    
def cifar9():
    print('''

import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# Load MNIST dataset
(x_train, _), (x_test, _) = tf.keras.datasets.mnist.load_data()

# Normalize and reshape
x_train = x_train.astype("float32") / 255.
x_test = x_test.astype("float32") / 255.
x_train = x_train[..., tf.newaxis]  # Shape: (60000, 28, 28, 1)
x_test = x_test[..., tf.newaxis]

# Encoder
encoder = models.Sequential([
    layers.Input(shape=(28, 28, 1)),
    layers.Conv2D(32, (3, 3), activation='relu', padding='same', strides=2),
    layers.Conv2D(64, (3, 3), activation='relu', padding='same', strides=2),
])

# Decoder
decoder = models.Sequential([
    layers.Conv2DTranspose(64, (3, 3), strides=2, activation='relu', padding='same'),
    layers.Conv2DTranspose(32, (3, 3), strides=2, activation='relu', padding='same'),
    layers.Conv2D(1, (3, 3), activation='sigmoid', padding='same'),
])

# Autoencoder
autoencoder = models.Sequential([encoder, decoder])
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
autoencoder.summary()


autoencoder.fit(x_train, x_train,
                epochs=10,
                batch_size=128,
                validation_data=(x_test, x_test))


decoded_imgs = autoencoder.predict(x_test[:10])

plt.figure(figsize=(20, 4))
for i in range(10):
    # Original
    ax = plt.subplot(2, 10, i + 1)
    plt.imshow(x_test[i].squeeze(), cmap='gray')
    ax.axis('off')

    # Reconstructed
    ax = plt.subplot(2, 10, i + 11)
    plt.imshow(decoded_imgs[i].squeeze(), cmap='gray')
    ax.axis('off')
plt.show()


''')
    
def cifar10():
    print('''

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, utils
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

batch_size  = 128
lr          = 2e-4
latent_dim  = 100
epochs      = 30
image_size  = 28
device      = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

transform = transforms.Compose([
    transforms.Resize(image_size),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])
dataset = datasets.MNIST('.', train=True, download=True, transform=transform)
loader  = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=2)

class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.ConvTranspose2d(latent_dim, 128, 7, 1, 0, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(True),
            nn.ConvTranspose2d(128, 64, 4, 2, 1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(True),
            nn.ConvTranspose2d(64, 1, 4, 2, 1, bias=False),
            nn.Tanh()
        )

    def forward(self, z):
        return self.net(z)

class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(

            nn.Conv2d(1, 64, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(64, 128, 4, 2, 1, bias=False),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Flatten(),
            nn.Linear(128*7*7, 1)

        )

    def forward(self, img):
        return self.net(img).view(-1)

G = Generator().to(device)
D = Discriminator().to(device)

criterion = nn.BCEWithLogitsLoss()
optG = optim.Adam(G.parameters(), lr=lr, betas=(0.5, 0.999))
optD = optim.Adam(D.parameters(), lr=lr, betas=(0.5, 0.999))

fixed_noise = torch.randn(64, latent_dim, 1, 1, device=device)

for epoch in range(1, epochs+1):
    for real_imgs, _ in loader:
        bsz = real_imgs.size(0)
        real_imgs = real_imgs.to(device)

        real_labels = torch.ones(bsz, device=device)
        fake_labels = torch.zeros(bsz, device=device)

        D.zero_grad()

        logits_real = D(real_imgs)
        loss_real  = criterion(logits_real, real_labels)

        noise    = torch.randn(bsz, latent_dim, 1, 1, device=device)
        fake_imgs = G(noise)
        logits_fake = D(fake_imgs.detach())
        loss_fake  = criterion(logits_fake, fake_labels)
        lossD = (loss_real + loss_fake) * 0.5
        lossD.backward()
        optD.step()

        G.zero_grad()
        logits = D(fake_imgs)

        lossG = criterion(logits, real_labels)
        lossG.backward()
        optG.step()

    print(f"Epoch [{epoch}/{epochs}]  Loss_D: {lossD.item():.4f}  Loss_G: {lossG.item():.4f}")

G.eval()
with torch.no_grad():
    samples = G(fixed_noise).cpu()

real_batch, _ = next(iter(loader))

grid_real = utils.make_grid(real_batch[:64], nrow=8, normalize=True, value_range=(-1,1))
grid_fake = utils.make_grid(samples,      nrow=8, normalize=True, value_range=(-1,1))

fig, axes = plt.subplots(2,1, figsize=(8,4))
axes[0].imshow(grid_real.permute(1,2,0), cmap='gray')
axes[0].set_title("Real MNIST")
axes[0].axis('off')
axes[1].imshow(grid_fake.permute(1,2,0), cmap='gray')
axes[1].set_title("Generated MNIST")
axes[1].axis('off')
plt.tight_layout()
plt.show()

          




OR
          



import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt

# Load MNIST and normalize to [-1, 1]
(x_train, _), _ = tf.keras.datasets.mnist.load_data()
x_train = (x_train.astype(np.float32) - 127.5) / 127.5
x_train = np.expand_dims(x_train, axis=-1)  # Shape: (60000, 28, 28, 1)

BUFFER_SIZE = 60000
BATCH_SIZE = 128

train_dataset = tf.data.Dataset.from_tensor_slices(x_train).shuffle(BUFFER_SIZE).batch(BATCH_SIZE)
# Generator: Input is random noise (latent vector)
def make_generator():
    model = tf.keras.Sequential([
        layers.Dense(7*7*256, use_bias=False, input_shape=(100,)),
        layers.BatchNormalization(),
        layers.LeakyReLU(),

        layers.Reshape((7, 7, 256)),
        layers.Conv2DTranspose(128, (5, 5), strides=1, padding='same', use_bias=False),
        layers.BatchNormalization(),
        layers.LeakyReLU(),

        layers.Conv2DTranspose(64, (5, 5), strides=2, padding='same', use_bias=False),
        layers.BatchNormalization(),
        layers.LeakyReLU(),

        layers.Conv2DTranspose(1, (5, 5), strides=2, padding='same', use_bias=False, activation='tanh')
    ])
    return model

# Discriminator: Input is an image
def make_discriminator():
    model = tf.keras.Sequential([
        layers.Conv2D(64, (5, 5), strides=2, padding='same', input_shape=[28, 28, 1]),
        layers.LeakyReLU(),
        layers.Dropout(0.3),

        layers.Conv2D(128, (5, 5), strides=2, padding='same'),
        layers.LeakyReLU(),
        layers.Dropout(0.3),

        layers.Flatten(),
        layers.Dense(1)
    ])
    return model
cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)

def discriminator_loss(real_output, fake_output):
    real_loss = cross_entropy(tf.ones_like(real_output), real_output)
    fake_loss = cross_entropy(tf.zeros_like(fake_output), fake_output)
    return real_loss + fake_loss

def generator_loss(fake_output):
    return cross_entropy(tf.ones_like(fake_output), fake_output)

generator = make_generator()
discriminator = make_discriminator()

generator_optimizer = tf.keras.optimizers.Adam(1e-4)
discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)
EPOCHS = 50
noise_dim = 100
num_examples_to_generate = 16

# Seed for consistent visualization
seed = tf.random.normal([num_examples_to_generate, noise_dim])

@tf.function
def train_step(images):
    noise = tf.random.normal([BATCH_SIZE, noise_dim])

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        generated_images = generator(noise, training=True)

        real_output = discriminator(images, training=True)
        fake_output = discriminator(generated_images, training=True)

        gen_loss = generator_loss(fake_output)
        disc_loss = discriminator_loss(real_output, fake_output)

    gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)
    gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    generator_optimizer.apply_gradients(zip(gradients_of_generator, generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, discriminator.trainable_variables))

    return gen_loss, disc_loss

def train(dataset, epochs):
    for epoch in range(epochs):
        for image_batch in dataset:
            g_loss, d_loss = train_step(image_batch)

        print(f"Epoch {epoch+1}, Generator Loss: {g_loss:.4f}, Discriminator Loss: {d_loss:.4f}")
        generate_and_plot_images(generator, seed, epoch+1)

def generate_and_plot_images(model, test_input, epoch):
    predictions = model(test_input, training=False)
    predictions = (predictions + 1) / 2.0  # Rescale to [0,1]

    plt.figure(figsize=(4, 4))
    for i in range(predictions.shape[0]):
        plt.subplot(4, 4, i+1)
        plt.imshow(predictions[i, :, :, 0], cmap='gray')
        plt.axis('off')
    plt.suptitle(f'Generated Digits - Epoch {epoch}')
    plt.tight_layout()
    plt.show()
train(train_dataset, EPOCHS)
def compare_real_and_fake():
    real_imgs = x_train[:16]
    noise = tf.random.normal([16, noise_dim])
    fake_imgs = generator(noise, training=False)

    fake_imgs = (fake_imgs + 1) / 2.0  # Rescale to [0, 1]

    plt.figure(figsize=(8, 4))

    for i in range(8):
        plt.subplot(2, 8, i + 1)
        plt.imshow(real_imgs[i, :, :, 0], cmap='gray')
        plt.title("Real")
        plt.axis('off')

        plt.subplot(2, 8, i + 9)
        plt.imshow(fake_imgs[i, :, :, 0], cmap='gray')
        plt.title("Fake")
        plt.axis('off')

    plt.suptitle("Real vs Generated Digits")
    plt.tight_layout()
    plt.show()

compare_real_and_fake()


''')