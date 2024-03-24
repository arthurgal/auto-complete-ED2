import PyPDF2 as pdf
import re
import re
import nltk
from PyPDF2 import PdfReader
from nltk.corpus import stopwords

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if node is None:
            return 0
        return node.height

    def balance(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def rotate_right(self, y):
      if y is None or y.left is None:
          return y  # Retorna o nó original se não puder ser rotacionado
      x = y.left
      T2 = x.right

      x.right = y
      y.left = T2

      y.height = 1 + max(self.height(y.left), self.height(y.right))
      x.height = 1 + max(self.height(x.left), self.height(x.right))

      return x

    def rotate_left(self, x):
      if x is None or x.right is None:
          return x  # Retorna o nó original se não puder ser rotacionado
      y = x.right
      T2 = y.left

      y.left = x
      x.right = T2

      x.height = 1 + max(self.height(x.left), self.height(x.right))
      y.height = 1 + max(self.height(y.left), self.height(y.right))

      return y


    def insert(self, node, key):
        if node is None:
            return AVLNode(key)
        if key < node.key:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)

        node.height = 1 + max(self.height(node.left), self.height(node.right))

        balance = self.balance(node)

        if balance > 1:
            if key < node.left.key:
                return self.rotate_right(node)
            else:
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        if balance < -1:
            if key > node.right.key:
                return self.rotate_left(node)
            else:
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node

    def insert_word(self, key):
        self.root = self.insert(self.root, key)

    def search(self, node, key):
        if node is None:
            return False
        if node.key == key:
            return True
        elif key < node.key:
            return self.search(node.left, key)
        else:
            return self.search(node.right, key)

    def autocomplete(self, prefix):
        suggestions = []
        self._autocomplete_helper(self.root, prefix, suggestions)
        return suggestions

    def _autocomplete_helper(self, node, prefix, suggestions):
        if node is None:
            return

        if node.key.startswith(prefix):
            suggestions.append(node.key)

        if prefix < node.key:
            self._autocomplete_helper(node.left, prefix, suggestions)
        elif prefix > node.key:
            self._autocomplete_helper(node.right, prefix, suggestions)
        else:
            self._autocomplete_helper(node.left, prefix, suggestions)
            self._autocomplete_helper(node.right, prefix, suggestions)
            


nltk.download('punkt')
nltk.download('stopwords')

def extract_words_from_pdf(pdf_file_path, remove_stopwords=True):
    words = set()
    stop_words = set(stopwords.words('portuguese'))
    with open(pdf_file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            text = text.lower()  # Convertendo para minúsculas
            text = re.sub(r'\s+', ' ', text)  # Substituindo espaços em branco múltiplos por um único espaço
            text = re.sub(r'[^\w\s]', '', text)  # Removendo pontuação e caracteres especiais
            tokens = nltk.word_tokenize(text)  # Dividindo o texto em palavras
            if remove_stopwords:
                tokens = [word for word in tokens if word not in stop_words]  # Removendo palavras de parada
            words.update(tokens)  # Atualizando o conjunto de palavras
    # print(words)
    return list(words)


def get_autocomplete_suggestions(text):
    pdf_file_path = "PlataoOBanquete.pdf"  # Caminho do arquivo PDF
    words = extract_words_from_pdf(pdf_file_path)
    avl_tree = AVLTree()
    for word in words:
        avl_tree.insert_word(word)

    suggestions = avl_tree.autocomplete(text)

    return suggestions
