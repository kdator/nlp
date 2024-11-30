from typing import List

class PrefixTreeNode:
    def __init__(self):
        # словарь с буквами, которые могут идти после данной вершины
        self.children: dict[str, PrefixTreeNode] = {}
        self.is_end_of_word = False

class PrefixTree:
    def __init__(self, vocabulary: List[str]):
        """
        vocabulary: список всех уникальных токенов в корпусе
        """
        self.root = PrefixTreeNode()
        
        for word in vocabulary:
            self._insert(word)

    def search_prefix(self, prefix) -> List[str]:
        """
        Возвращает все слова, начинающиеся на prefix
        prefix: str – префикс слова
        """

        node = self._find_node(prefix)

        if node is None:
            return []
        
        words = []
        self._find_words(node, prefix, words)
        return words

    def _insert(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = PrefixTreeNode()
            node = node.children[char]
        node.is_end_of_word = True

    def _find_node(self, prefix: str) -> PrefixTreeNode:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _find_words(self, node: PrefixTreeNode, prefix: str, words: List[str]):
        if node.is_end_of_word:
            words.append(prefix)

        for char, child_node in node.children.items():
            self._find_words(child_node, prefix + char, words)
