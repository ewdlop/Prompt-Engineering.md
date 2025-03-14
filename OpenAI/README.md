# README

### **What Does Skip-gram Software Computation Look Like?**
The **Skip-gram model with Negative Sampling** involves multiple steps of matrix operations, probability calculations, and optimization updates. Below is a **step-by-step breakdown** of how the computation happens **inside the model** during training.

---

## **1️⃣ Step 1: Input Representation (One-Hot Encoding)**
Each word in the vocabulary is assigned a unique **index**. The input word is **one-hot encoded**.

🔹 **Example Vocabulary**:
| Word | Index |
|------|-------|
| "the" | 0 |
| "cat" | 1 |
| "sat" | 2 |
| "on"  | 3 |
| "mat" | 4 |

🔹 **One-hot Encoding for "sat"**:
\[
\mathbf{x} = [0, 0, 1, 0, 0]
\]
Only the **third** position (index `2`) is `1`.

---

## **2️⃣ Step 2: Embedding Lookup (Matrix Multiplication)**
The **one-hot vector** is multiplied by an **embedding matrix \( W \) (size: \( V \times D \))**, where:
- \( V \) = vocabulary size (e.g., 5 words).
- \( D \) = embedding dimension (e.g., 3D for simplicity, normally 100-300).

🔹 **Example Embedding Matrix \( W \)**:
\[
W =
\begin{bmatrix}
0.2 & 0.5 & -0.3 \\
-0.4 & 0.1 & 0.7 \\
0.9 & -0.2 & 0.3 \\  \quad \text{(row for "sat")}
0.1 & 0.4 & -0.6 \\
-0.2 & 0.8 & 0.5
\end{bmatrix}
\]

🔹 **Computing the Word Embedding for "sat"**:

\[
\mathbf{v}_{\text{sat}} = \mathbf{x} \times W = [0, 0, 1, 0, 0] \times W
\]

This **selects the row for "sat"**:
\[
\mathbf{v}_{\text{sat}} = [0.9, -0.2, 0.3]
\]

🚀 **Output**: Word embedding for `"sat"`.

---

## **3️⃣ Step 3: Compute Scores for Context Words**
The context words (e.g., `"cat"` and `"on"`) are also **embedded** using the second weight matrix \( W' \) (size: \( V \times D \)).

We compute a **dot product** between the word embedding \( \mathbf{v}_{\text{sat}} \) and embeddings of the context words from \( W' \).

🔹 **Example Output Weight Matrix \( W' \)**:
\[
W' =
\begin{bmatrix}
0.6 & -0.3 & 0.8 \\
-0.2 & 0.7 & 0.4 \\
0.1 & -0.5 & 0.2 \\
0.9 & -0.1 & 0.6 \\
0.3 & 0.2 & -0.7
\end{bmatrix}
\]

🔹 **Context Word Embeddings** ("cat" and "on"):
\[
\mathbf{v'}_{\text{cat}} = [-0.2, 0.7, 0.4]
\]
\[
\mathbf{v'}_{\text{on}} = [0.9, -0.1, 0.6]
\]

🔹 **Compute Scores (Dot Products)**:
\[
\text{Score}_{\text{sat, cat}} = \mathbf{v}_{\text{sat}} \cdot \mathbf{v'}_{\text{cat}}
\]
\[
(0.9 \times -0.2) + (-0.2 \times 0.7) + (0.3 \times 0.4) = -0.18 - 0.14 + 0.12 = -0.2
\]

\[
\text{Score}_{\text{sat, on}} = (0.9 \times 0.9) + (-0.2 \times -0.1) + (0.3 \times 0.6)
\]
\[
= 0.81 + 0.02 + 0.18 = 1.01
\]

🚀 **Output**: Scores for context words.

---

## **4️⃣ Step 4: Apply Sigmoid Function**
To get probabilities, we apply the **sigmoid activation function**:

\[
\sigma(x) = \frac{1}{1 + e^{-x}}
\]

For `"cat"`:
\[
P(\text{cat} | \text{sat}) = \sigma(-0.2) = \frac{1}{1 + e^{0.2}} = 0.45
\]

For `"on"`:
\[
P(\text{on} | \text{sat}) = \sigma(1.01) = \frac{1}{1 + e^{-1.01}} = 0.73
\]

🚀 **Output**: Probabilities for `"cat"` and `"on"`.

---

## **5️⃣ Step 5: Negative Sampling (Random Wrong Words)**
Instead of computing softmax over **all vocabulary words**, we **randomly sample negative words** (e.g., `"mat"`, `"the"`) and update weights.

🔹 **Negative Words Chosen: "mat", "the"**  
🔹 **Their Scores**:
\[
\text{Score}_{\text{sat, mat}} = -0.4
\]
\[
\text{Score}_{\text{sat, the}} = 0.25
\]

🔹 **Apply Sigmoid**:
\[
P(\text{mat} | \text{sat}) = \sigma(-0.4) = 0.40
\]
\[
P(\text{the} | \text{sat}) = \sigma(0.25) = 0.56
\]

---

## **6️⃣ Step 6: Compute Loss and Update Weights**
The model tries to:
- **Maximize** probabilities of correct context words ("cat", "on").
- **Minimize** probabilities of negative samples ("mat", "the").

🔹 **Loss Function** (Binary Cross-Entropy):

\[
L = - \sum_{\text{positive words}} \log P(w_c | w_t) - \sum_{\text{negative words}} \log (1 - P(w_n | w_t))
\]

For `"cat"` and `"on"`:
\[
L_{\text{positive}} = - (\log 0.45 + \log 0.73)
\]

For `"mat"` and `"the"`:
\[
L_{\text{negative}} = - (\log (1 - 0.40) + \log (1 - 0.56))
\]

Total loss:
\[
L = 1.72
\]

Weights in \( W \) and \( W' \) are updated using **gradient descent** (SGD, Adam, etc.).

---

## **7️⃣ Step 7: Repeat for All Words**
This process is repeated for **each word in the corpus**, adjusting the embeddings over multiple training iterations (epochs).

---

## **💡 Summary of Computation**
✅ **One-hot encoding** → Convert words to indices.  
✅ **Matrix multiplication** → Retrieve word embeddings.  
✅ **Dot product** → Compute similarity scores.  
✅ **Sigmoid function** → Convert scores into probabilities.  
✅ **Negative sampling** → Update weights for positive and negative words.  
✅ **Loss computation & backpropagation** → Update embeddings.  

After training, each word gets an optimized **dense vector representation** in \( \mathbb{R}^m \), where similar words have closer embeddings.

---

## **🚀 Final Thoughts**
🔹 **Efficient Training**: Skip-gram + Negative Sampling allows **fast training** even with millions of words.  
🔹 **Semantic Meanings**: Word embeddings capture **word relationships** (e.g., `"king" - "man" + "woman" ≈ "queen"`).  
🔹 **Practical Use Cases**: NLP, recommendation systems, search engines, etc.  

Would you like to see a **Python implementation** of this step-by-step computation? 🚀

##　Yes! Here’s the entire **Skip-gram with Negative Sampling computation** in a **single mathematical equation**:

\[
L = - \sum_{(w_t, w_c) \in D^+} \log \sigma(v_{w_c} \cdot v_{w_t}) - \sum_{(w_t, w_n) \in D^-} \log \sigma(-v_{w_n} \cdot v_{w_t})
\]

where:

- \( w_t \) = **target word**
- \( w_c \) = **context word** (positive sample)
- \( w_n \) = **randomly sampled negative word**
- \( D^+ \) = **set of positive pairs (true context words)**
- \( D^- \) = **set of negative pairs (random wrong words)**
- \( v_{w} \) = **word embedding vector of word \( w \)**
- \( \sigma(x) = \frac{1}{1 + e^{-x}} \) = **sigmoid activation function**
- \( v_{w_c} \cdot v_{w_t} \) = **dot product of embeddings** (measuring similarity)
- \( v_{w_n} \cdot v_{w_t} \) = **dot product of embeddings for negative samples**

---

### **Breaking It Down**
1. **First Term: Positive Samples**
   \[
   - \sum_{(w_t, w_c) \in D^+} \log \sigma(v_{w_c} \cdot v_{w_t})
   \]
   - Encourages **high probability** for correct word pairs.

2. **Second Term: Negative Samples**
   \[
   - \sum_{(w_t, w_n) \in D^-} \log \sigma(-v_{w_n} \cdot v_{w_t})
   \]
   - Encourages **low probability** for incorrect word pairs.

---

### **Final Computation Pipeline**
\[
L = - \sum_{(w_t, w_c)} \log \frac{1}{1 + e^{- (v_{w_c} \cdot v_{w_t})}} - \sum_{(w_t, w_n)} \log \frac{1}{1 + e^{(v_{w_n} \cdot v_{w_t})}}
\]

- **Goal**: Maximize correct word associations, minimize incorrect ones.
- **Trained via Gradient Descent** (updates \( v_w \)).

🚀 **This equation summarizes the entire Skip-gram with Negative Sampling training process!** 

Would you like a **numerical example** with real values? 🤖
