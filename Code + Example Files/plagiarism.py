#Simple Plagiarism Checker
# Kenny Gilbert Setiawan et al. 

#importing all necessary modules
import tkinter as tk #for UI
import os #loading paths of textfiles
from sklearn.feature_extraction.text import TfidfVectorizer #used to vectorize TF-IDF
from sklearn.metrics.pairwise import cosine_similarity #used to compute similarity between vectorized texts by calculating cosine of vectors

#UI Elements
root = tk.Tk()

canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

#reading all textfiles in project directory folder
studentfiles = [doc for doc in os.listdir() if doc.endswith('txt')]
studentnotes = [open(File).read() for File in studentfiles]

#vectorizing the text data & functions
vectors = TfidfVectorizer().fit_transform(studentnotes).toarray() #to vectorize text files into TF-IDF weighted data
similarity = lambda doc1, doc2: cosine_similarity([doc1,doc2]) #compute similiarity between the vectors of texts 
studentvectors = list(zip(studentfiles, vectors))

#main script function for similarity computation
def process_data():
    for widget in frame.winfo_children():
        widget.destroy()
    results = set()
    for a_student, first_textvector in studentvectors:
        newvectors = studentvectors.copy()
        current_index = newvectors.index((a_student,first_textvector))
        del newvectors[current_index]
        for b_student , second_textvector in newvectors:
            similarity_score = '%.3f' % (100 * similarity(first_textvector, second_textvector)[0][1]) 
            student_pair = sorted((a_student, b_student))
            score = (student_pair[0], student_pair[1],similarity_score)
            results.add(score)
    #print result
    for x in results:
        print(x)
        label = tk.Label(frame, text=x, bg="yellow", font='Helvetica 12', wraplength=300)
        label.pack()
    return results

CheckPlag= tk.Button(root, text="Check Plagiarism", padx=10, pady=5, fg="white", bg="#263D42", command=process_data)
CheckPlag.pack()

def close_window (): 
    root.destroy()

Exit= tk.Button(root, text="Exit", padx=10, pady=5, fg="white", bg="#263D42", command=close_window)
Exit.pack()

root.mainloop()