# THIS IS AN EXTENSION NETWORK OF THE SKILLS OF THE HURNET ARTIFICIAL NEURAL NETWORK
# Semantic Comparison Network (SCN) is a new artificial neural network architecture based on the HurNet network. The semantic comparison network architecture also utilizes semantic comparison calculations and Euclidean distance for feature expansion.
# The SCN focuses on language model development and employs a significantly faster training approach compared to traditional transformer-based architectures. This algorithm was created, designed, and developed by Sapiens Technology®️, and any sharing, disclosure,          
# or public commentary on the logic involved in this code without our prior authorization is strictly prohibited and subject to legal action by our team of attorneys. All copyright rights to this algorithm are under the guardianship of Sapiens Technology®️,
# and we do not permit any modification, customization, or enhancement of the original code.
# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
class SemanticComparisonNetwork():
    def __init__(self):
        try:
            from os import path, makedirs, listdir
            from tiktoken import get_encoding, encoding_for_model
            from numpy import ndarray
            from re import findall, sub, match, search
            from unicodedata import normalize, category
            from tqdm import tqdm
            from functools import partialmethod
            from pickle import dump, load
            from json import dump as json_dump
            from random import shuffle
            from time import sleep
            self.__path = path
            self.__get_encoding = get_encoding
            self.__ndarray = ndarray
            self.__findall = findall
            self.__encoding_for_model = encoding_for_model
            self.__sub = sub
            self.__normalize = normalize
            self.__category = category
            self.__match = match
            self.__search = search
            self.__tqdm = tqdm
            self.__partialmethod = partialmethod
            self.__makedirs = makedirs
            self.__dump = dump
            self.__json_dump = json_dump
            self.__load = load
            self.__shuffle = shuffle
            self.__listdir = listdir
            self.__sleep = sleep
            self.__vocabulary_index = 0
            self.__outputs = []
            self.__embedding_size = 50
            self.__method = 'semantic'
            self.__fx = False
            self.tokens_amount = 128000
            self.__tokenizer = 'gpt'
            self.__precision = 1
            self.__hidden_layers = []
            self.__input_list = []
            self.__inputs = []
            self.__hurnet_neural_network = None
            self.prediction_score = 0.0
        except Exception as error: print('ERROR in __init__: '+str(error))
    def __boolValidation(self, boolean=False): return bool(boolean) if type(boolean) in (bool, int, float) else False
    def __integerValidation(self, integer=0): return int(integer) if type(integer) in (bool, int, float) else 0     
    def __stringValidation(self, string=''): return string.strip() if type(string) == str else str(string).strip()
    def __getFilenameWithoutExtension(self, model_path=''):
        directory, filename = self.__path.split(model_path)
        filename_without_extension = self.__path.splitext(filename)[0]
        return self.__path.join(directory, filename_without_extension)
    def __loadJSON(self, string_content=''):
        try:
            json_content = {}
            string_content = str(string_content)
            try:
                from json import loads
                json_content = loads(string_content)
            except:
                from ast import literal_eval
                json_content = literal_eval(string_content)
            return json_content
        except Exception as error:
            print('ERROR in __loadJSON: ' + str(error))
            return {}
    def __floatValidation(self, floating=0.0): return float(floating) if type(floating) in (bool, int, float) else 0.0
    def __textForEmbeddingGPT(self, text='', length=50, quantization=0):
        encoding = self.__get_encoding('gpt2')
        embedding = encoding.encode(text)
        if length > 0:
            if len(embedding) < length: embedding += [0] * (length - len(embedding))
            else: embedding = embedding[:length]
        if quantization != 0: embedding = [round(token / (10 ** quantization), quantization) for token in embedding]
        return embedding
    def __textForEmbeddingSAPI(self, text='', length=50, quantization=0):
        embedding = [ord(char) for char in text]
        if length > 0:
            if len(embedding) < length: embedding.extend([32] * (length - len(embedding)))
            else: embedding = embedding[:length]
        if quantization != 0: embedding = [round(token / (10 ** quantization), quantization) for token in embedding]
        return embedding
    def __listValidation(self, array=[]):
        if type(array) in (tuple, list): array = list(array)
        elif type(array) == self.__ndarray: array = array.tolist()
        else: array = [array]
        return array
    def __outputAdaptedToInputYIELD(self, Input='', Output='', hot=True):
        try:
            if not hot:
                outputs = self.__findall(r'\S+|\n', Output)
                outputs_limit = len(outputs)-1
                for index, token in enumerate(outputs):
                    space = ' ' if index < outputs_limit else ''
                    yield token+space
                return ''
            def removePunctuation(word=''): return self.__sub(r'^[^\w]+|[^\w]+$', '', word)
            def normalizeWord(word=''): return removePunctuation(word).lower()
            def getWordCase(word=''):
                if word.isupper(): return 'upper'
                elif word.islower(): return 'lower'
                elif word.istitle(): return 'title'
                else: return 'mixed'
            def applyCase(word='', case_type=''):
                if case_type == 'upper': return word.upper()
                elif case_type == 'lower': return word.lower()
                elif case_type == 'title': return word.title()
                else: return word
            def transferAccents(source='', target=''):
                def stripAccents(text=''): return ''.join(character for character in self.__normalize('NFD', text) if self.__category(character) != 'Mn')
                source_stripped = stripAccents(source)
                target_stripped = stripAccents(target)
                if source_stripped != target_stripped or len(source) != len(target): return target
                result = ''
                for source_character, target_character in zip(source, target):
                    decomposed = self.__normalize('NFD', target_character)
                    accents = ''.join(character for character in decomposed if self.__category(character) == 'Mn')
                    if accents:
                        base = stripAccents(source_character)
                        result += self.__normalize('NFC', base + accents)
                    else: result += target_character
                return result
            input_words_with_punctuation = Input.split()
            output_words_with_punctuation = self.__findall(r'\S+|\n', Output)
            input_words = [normalizeWord(word) for word in input_words_with_punctuation]
            output_words = [normalizeWord(word) for word in output_words_with_punctuation]
            modified_output = output_words_with_punctuation[:]
            def internalSubstitution(index=0):
                left_output = output_words[index - 1]
                right_output = output_words[index + 1]
                for position in range(len(input_words) - 2):
                    if input_words[position] == left_output and input_words[position + 2] == right_output: return input_words_with_punctuation[position + 1]
                if left_output in input_words and len(input_words) >= 2 and input_words[-2] == left_output: return input_words_with_punctuation[-1]
                return None
            def firstSubstitution():
                right_output = output_words[1]
                if len(input_words) >= 2 and right_output == input_words[1]: return input_words_with_punctuation[0]
                return None
            def lastSubstitution():
                left_output = output_words[-2]
                if len(input_words) >= 2 and left_output == input_words[-2]: return input_words_with_punctuation[-1]
                return None
            output_words_limit = len(output_words)-1
            for index, token_normalized in enumerate(output_words):
                space = ' ' if index < output_words_limit else ''
                if token_normalized in input_words:
                    yield modified_output[index] + space
                    continue
                replacement_candidate = None
                if 0 < index < len(output_words) - 1: replacement_candidate = internalSubstitution(index)
                elif index == 0 and len(output_words) > 1: replacement_candidate = firstSubstitution()
                elif index == len(output_words) - 1 and len(output_words) > 1: replacement_candidate = lastSubstitution()
                if replacement_candidate:
                    word_case = getWordCase(output_words_with_punctuation[index])
                    candidate_core = removePunctuation(replacement_candidate)
                    candidate_with_case = applyCase(candidate_core, word_case)
                    candidate_final = transferAccents(output_words_with_punctuation[index], candidate_with_case)
                    core = removePunctuation(output_words_with_punctuation[index])
                    if core == '': modified_output[index] = candidate_final
                    else:
                        prefix_match = self.__match(r'^[^\w]+', output_words_with_punctuation[index])
                        suffix_match = self.__search(r'[^\w]+$', output_words_with_punctuation[index])
                        prefix = prefix_match.group(0) if prefix_match else ''
                        suffix = suffix_match.group(0) if suffix_match else ''
                        old = modified_output[index]
                        new = prefix + candidate_final + suffix
                        if old.isdigit() or new.isdigit(): modified_output = [new if output == old else output for output in modified_output]
                        else: modified_output[index] = new
                yield modified_output[index] + space
        except Exception as error:
            print('ERROR in __outputAdaptedToInputYIELD: ' + str(error))
            return Output
    def __outputAdaptedToInputRETURN(self, Input='', Output='', hot=True):
        try:
            if not hot: return Output
            def removePunctuation(word=''): return self.__sub(r'^[^\w]+|[^\w]+$', '', word)
            def normalizeWord(word=''): return removePunctuation(word).lower()
            def getWordCase(word=''):
                if word.isupper(): return 'upper'
                elif word.islower(): return 'lower'
                elif word.istitle(): return 'title'
                else: return 'mixed'
            def applyCase(word='', case_type=''):
                if case_type == 'upper': return word.upper()
                elif case_type == 'lower': return word.lower()
                elif case_type == 'title': return word.title()
                else: return word
            def transferAccents(source='', target=''):
                def stripAccents(text=''): return ''.join(character for character in self.__normalize('NFD', text) if self.__category(character) != 'Mn')
                source_stripped = stripAccents(source)
                target_stripped = stripAccents(target)
                if source_stripped != target_stripped or len(source) != len(target): return target
                result = ''
                for source_character, target_character in zip(source, target):
                    decomposed = self.__normalize('NFD', target_character)
                    accents = ''.join(character for character in decomposed if self.__category(character) == 'Mn')
                    if accents:
                        base = stripAccents(source_character)
                        result += self.__normalize('NFC', base + accents)
                    else: result += target_character
                return result
            input_words_with_punctuation = Input.split()
            output_words_with_punctuation = self.__findall(r'\S+|\n', Output)
            input_words = [normalizeWord(word) for word in input_words_with_punctuation]
            output_words = [normalizeWord(word) for word in output_words_with_punctuation]
            modified_output = output_words_with_punctuation[:]
            def internalSubstitution(index=0):
                left_output = output_words[index - 1]
                right_output = output_words[index + 1]
                for position in range(len(input_words) - 2):
                    if input_words[position] == left_output and input_words[position + 2] == right_output: return input_words_with_punctuation[position + 1]
                if left_output in input_words and len(input_words) >= 2 and input_words[-2] == left_output: return input_words_with_punctuation[-1]
                return None
            def firstSubstitution():
                right_output = output_words[1]
                if len(input_words) >= 2 and right_output == input_words[1]: return input_words_with_punctuation[0]
                return None
            def lastSubstitution():
                left_output = output_words[-2]
                if len(input_words) >= 2 and left_output == input_words[-2]: return input_words_with_punctuation[-1]
                return None
            for index, token_normalized in enumerate(output_words):
                if token_normalized in input_words: continue
                replacement_candidate = None
                if 0 < index < len(output_words) - 1: replacement_candidate = internalSubstitution(index)
                elif index == 0 and len(output_words) > 1: replacement_candidate = firstSubstitution()
                elif index == len(output_words) - 1 and len(output_words) > 1: replacement_candidate = lastSubstitution()
                if replacement_candidate:
                    word_case = getWordCase(output_words_with_punctuation[index])
                    candidate_core = removePunctuation(replacement_candidate)
                    candidate_with_case = applyCase(candidate_core, word_case)
                    candidate_final = transferAccents(output_words_with_punctuation[index], candidate_with_case)
                    core = removePunctuation(output_words_with_punctuation[index])
                    if core == '': modified_output[index] = candidate_final
                    else:
                        prefix_match = self.__match(r'^[^\w]+', output_words_with_punctuation[index])
                        suffix_match = self.__search(r'[^\w]+$', output_words_with_punctuation[index])
                        prefix = prefix_match.group(0) if prefix_match else ''
                        suffix = suffix_match.group(0) if suffix_match else ''
                        old = modified_output[index]
                        new = prefix + candidate_final + suffix
                        if old.isdigit() or new.isdigit(): modified_output = [new if output == old else output for output in modified_output]
                        else: modified_output[index] = new
            return str(' '.join(modified_output)).strip()
        except Exception as error:
            print('ERROR in __outputAdaptedToInputRETURN: ' + str(error))
            return Output
    def __embeddingForTextGPT(self, embedding=[]):
        if not embedding: return ''
        tokens = max((len(f'{token:.10f}'.split('.')[1].rstrip('0')) for token in embedding if token != 0), default=0)
        factor = 10 ** tokens
        tokens = [int(round(token * factor)) for token in embedding if token != 0]
        encoding = self.__get_encoding('gpt2')
        return encoding.decode(tokens).strip()
    def __embeddingForTextSAPI(self, embedding=[]):
        if not embedding: return ''
        tokens = max((len(f'{token:.10f}'.split('.')[1].rstrip('0')) for token in embedding if token != 0), default=0)
        text = ''.join(chr(int(round(token * (10 ** tokens)))) for token in embedding)
        return text.strip()
    def __set_tqdm(self, disable=True):
        try:
            disable = self.__boolValidation(boolean=disable)
            self.__tqdm.__init__ = self.__partialmethod(self.__tqdm.__init__, disable=disable)
            return True
        except: return False
    def __update_tqdm(self, total=1, description=''):
        try:
            total = self.__integerValidation(integer=total)
            description = description.strip() if type(description) == str else str(description).strip()
            progress_bar = self.__tqdm(total=total, desc=description, position=0, leave=True)
            return progress_bar
        except: return False
    def __getVocabularyIndex(self):
        vocabulary_index = self.__vocabulary_index
        self.__vocabulary_index += 1
        return vocabulary_index 
    def __saveVocabulary(self, model_path=''):
        try:
            model_path = self.__stringValidation(string=model_path)
            model_path = file_path = self.__getFilenameWithoutExtension(model_path=model_path)
            if model_path.count('/') > 1:
                def getDirectory(path=''):
                    result = self.__match(r"(.*/)", path) or self.__match(r"(.*\\)", path)
                    return result.group(1) if result else path
                path = getDirectory(path=model_path)
                if not self.__path.isdir(path): self.__makedirs(path, exist_ok=True)
            if len(model_path) < 1: model_path = 'model.vocabu'
            if not model_path.lower().endswith('.vocabu'): model_path += '.vocabu'
            with open(model_path, 'wb') as file: self.__dump(self.__outputs, file)
            scconf = {'_name_or_path': 'Sapiens', 'architectures': ['semantic_comparison_network'], 'max_position_embeddings': self.__embedding_size, 'model_type': self.__method, 'features_expansion': int(self.__fx), 'tokens_amount': self.tokens_amount}
            with open(file_path+'.scconf', 'w', encoding='utf-8') as file: self.__json_dump(scconf, file, ensure_ascii=False, indent=4)
            return True
        except Exception as error:
            print('ERROR in __saveVocabulary: ' + str(error))
            return False
    def __loadVocabulary(self, model_path=''):
        try:
            model_path, data = self.__stringValidation(string=model_path), ''
            model_path = file_path = self.__getFilenameWithoutExtension(model_path=model_path)
            if len(model_path) < 1: model_path = 'model.vocabu'
            if not model_path.lower().endswith('.vocabu'): model_path += '.vocabu'
            if not self.__path.isfile(model_path):
                print('Non-existent path: '+model_path)
                print('The path to the referenced VOCABU model does not exist.')
                return False
            with open(model_path, 'rb') as file: data = self.__load(file)
            data = self.__loadJSON(string_content=data)
            try: self.__outputs = list(data)
            except: self.__outputs = []
            file_path = file_path+'.scconf'
            if not self.__path.isfile(file_path):
                print('Non-existent path: '+file_path)
                print('The path to the referenced SCCONF model does not exist.')
                return False
            with open(file_path, 'r', encoding='utf-8') as file: data = str(file.read()).strip()
            data = self.__loadJSON(string_content=data)
            try: self.__embedding_size = int(data['max_position_embeddings'])
            except: self.__embedding_size = 50
            try: self.__method = str(data['model_type']).lower().strip()
            except: self.__method = 'euclidean'
            try: self.__fx = bool(data['features_expansion'])
            except: self.__fx = False
            try: self.tokens_amount = int(data['tokens_amount'])
            except: self.tokens_amount = 128000
            return True
        except Exception as error:
            print('ERROR in __loadVocabulary: ' + str(error))
            return False
    def __shuffleText(self, text=''):
        words = str(text).split()
        self.__shuffle(words)
        return ' '.join(words)
    def countTokens(self, text='', model='gpt-4'):
        try:
            text, model = self.__stringValidation(string=text), self.__stringValidation(string=model).lower()
            return len(self.__encoding_for_model(model).encode(str(text)))
        except Exception as error:
            print('ERROR in countTokens: ' + str(error))
            return len(str(text))
    def truncateTokens(self, text='', precision=1.0, minimum_length=3):
        try:
            truncate_text = ''
            text = self.__stringValidation(string=text)
            precision = self.__floatValidation(floating=precision)
            minimum_length = max((1, self.__integerValidation(integer=minimum_length)))
            if precision <= 0 or precision >= 1: return text
            words, truncated_words = text.split(), []
            for word in words:
                if len(word) > minimum_length: truncated_words.append(word[:int(len(word) * precision)])
                else: truncated_words.append(word)
            truncate_text = ' '.join(truncated_words)
            return truncate_text.strip()
        except Exception as error:
            print('ERROR in truncateTokens: ' + str(error))
            return str(text).lower()
    def normalization(self, text=''):
        try: return self.__sub(r'[^a-z0-9\s+\-*/%&@<>$]', '', self.__normalize('NFD', str(text).lower()).encode('ascii', 'ignore').decode('ascii')).strip()
        except Exception as error:
            print('ERROR in normalization: ' + str(error))
            return str(text).lower()
    def textForEmbedding(self, text='', length=50, quantization=0, tokenizer='sapi'):
        try:
            embedding = []
            text = self.__stringValidation(string=text)
            length = self.__integerValidation(integer=length)
            quantization = max((0, self.__integerValidation(integer=quantization)))
            tokenizer = self.__stringValidation(string=tokenizer).lower()
            if tokenizer == 'gpt': embedding = self.__textForEmbeddingGPT(text=text, length=length, quantization=quantization)
            else: embedding = self.__textForEmbeddingSAPI(text=text, length=length, quantization=quantization)
            return embedding
        except Exception as error:
            print('ERROR in textForEmbedding: '+str(error))
            return []
    def searchMethod(self, text='', text_vector=[], minimum_instruction_score=0.5):
        try:
            result_dictionary = {'response': [], 'best_index': 0, 'score': 0.0}
            text, text_vector = self.__stringValidation(string=text), self.__listValidation(array=text_vector)
            minimum_instruction_score = self.__floatValidation(floating=minimum_instruction_score)
            input_tokens = self.truncateTokens(text=self.normalization(text), precision=self.__precision, minimum_length=3).split()
            input_token_length = max((1, len(input_tokens)))
            best_score, best_index, response = 0, -1, ''
            for index, output_text in enumerate(text_vector):
                output_tokens, score = self.truncateTokens(text=self.normalization(str(output_text)), precision=self.__precision, minimum_length=3).split(), 0
                for input_token in input_tokens: score += (1 if input_token in output_tokens else 0)
                score /= input_token_length
                if score > best_score: best_score, best_index = score, index
            result_dictionary['best_index'], result_dictionary['score'] = best_index, best_score
            response, infinite = str(text_vector[best_index]).strip(), float('inf')
            def removeLeftNumbers(text=''):
                text = str(text).strip()
                return self.__sub(r'^\d+', '', text) if text.split()[0].strip().isdigit() else text
            if response.endswith('?'):
                try: result_dictionary['response'] = removeLeftNumbers(text=text_vector[best_index+1]).strip()
                except: result_dictionary['response'] = removeLeftNumbers(text=response)
                return result_dictionary
            separators, best_find, final_index, has_instruction = ('?', '.', ':', ';', '!'), infinite, 0, False
            for separator_index, separator in enumerate(separators):
                index = response.find(separator)
                if index > 1 and index < best_find: best_find, final_index = index, separator_index
            if best_find != infinite:
                separator = separators[final_index]
                response_split = response.split(separator)
                if 0 not in [1 if len(part.strip()) > 0 else 0 for part in response_split]:
                    instruction = response_split[0]
                    output_tokens = self.truncateTokens(text=self.normalization(instruction), precision=self.__precision, minimum_length=3).split()
                    if input_tokens == output_tokens: has_instruction = True
                    else:
                        inner_score = 0
                        for input_token in input_tokens: inner_score += (1 if input_token in output_tokens else 0)
                        inner_score /= input_token_length
                        if inner_score >= minimum_instruction_score: has_instruction = True
                    if has_instruction: response = separator.join(response_split[1:])
            result_dictionary['response'] = removeLeftNumbers(text=response).strip()
            return result_dictionary
        except Exception as error:
            print('ERROR in searchMethod: '+str(error))
            try: response = text_vector[-1]
            except: response = []
            return {'response': response, 'best_index': 0, 'score': 0.0}
    def semanticMethod(self, vector=[], matrix=[], removes_completeness=True):
        try:
            result_dictionary = {'response': [], 'best_index': 0, 'score': 0.0}
            vector, matrix = self.__listValidation(array=vector), self.__listValidation(array=matrix)
            removes_completeness = self.__boolValidation(boolean=removes_completeness)
            completeness = 32 if self.__tokenizer == 'sapi' else 0
            def removeZerosAndThirtyTwo(vector=[], removes_completeness=True, completeness=0): return [element for element in vector if element != completeness] if removes_completeness else vector
            def inTheVector(vector1=[], vector2=[]):
                str_vector1 = str(vector1).replace(' ', '').replace('[', '').replace(']', '')
                str_vector2 = str(vector2).replace(' ', '').replace('[', '').replace(']', '')
                return str_vector1 in str_vector2
            def closestNumber(target=0, numbers=[0]): return min(numbers, key=lambda number: abs(number - target))
            vector = removeZerosAndThirtyTwo(vector=vector, removes_completeness=removes_completeness, completeness=completeness)
            vector_length, best_index, best_score = len(vector), 0, 0
            for index, row in enumerate(matrix):
                row = removeZerosAndThirtyTwo(vector=row, removes_completeness=removes_completeness, completeness=completeness)
                if vector == row or inTheVector(vector1=vector, vector2=row) or inTheVector(vector1=row, vector2=vector):
                    response, best_index, best_score = matrix[index], index, 1.0
                    result_dictionary = {'response': response, 'best_index': best_index, 'score': best_score}
                    break
                current_score1 = 0
                for element in vector:
                    if element in row: current_score1 += 1
                    else:
                        closest_number = closestNumber(target=element, numbers=row)
                        current_score1 += (1-(abs(closest_number-element)/max((closest_number, element))))
                current_score1 = current_score1 / max((1, vector_length))
                current_score2, row_length = 0, len(row)
                for element in row:
                    if element in vector: current_score2 += 1
                    else:
                        closest_number = closestNumber(target=element, numbers=vector)
                        current_score2 += (1-(abs(closest_number-element)/max((closest_number, element))))
                current_score2 = current_score2 / max((1, row_length))
                current_score = max(current_score1, current_score2)
                if current_score > best_score: best_index, best_score = index, current_score
            response = matrix[best_index]
            result_dictionary = {'response': response, 'best_index': best_index, 'score': best_score}
            return result_dictionary
        except Exception as error:
            print('ERROR in semanticMethod: ' + str(error))
            try: response = matrix[0]
            except: response = []
            return {'response': response, 'best_index': 0, 'score': 0.0}
    def euclideanMethod(self, vector=[], matrix=[], removes_completeness=True):
        try:
            result_dictionary = {'response': [], 'best_index': 0, 'score': 0.0}
            vector, matrix = self.__listValidation(array=vector), self.__listValidation(array=matrix)
            removes_completeness = self.__boolValidation(boolean=removes_completeness)
            completeness = 32 if self.__tokenizer == 'sapi' else 0
            from math import inf
            def removeTrailing(input_list=[], removes_completeness=True, completeness=0):
                if not removes_completeness: return input_list
                output_list = input_list[:]
                while output_list and (output_list[-1] == completeness): output_list = output_list[:-1]
                return output_list
            def isSubsequence(sequence=[], subsequence=[]):
                index_sub = 0
                for element in sequence:
                    if index_sub < len(subsequence) and element == subsequence[index_sub]: index_sub += 1
                return index_sub == len(subsequence)
            def computeCost(list_one=[], list_two=[]):
                sorted_one, sorted_two = sorted(list_one), sorted(list_two)
                minimum_length = min(len(sorted_one), len(sorted_two))
                total_cost = sum(abs(sorted_one[index] - sorted_two[index]) for index in range(minimum_length))
                if len(sorted_one) > minimum_length: total_cost += sum(sorted_one[minimum_length:])
                elif len(sorted_two) > minimum_length: total_cost += sum(sorted_two[minimum_length:])
                return total_cost
            normalized_vector = removeTrailing(input_list=vector, removes_completeness=removes_completeness, completeness=completeness)
            best_score, best_index, best_candidate = -inf, -1, None
            for current_index, candidate in enumerate(matrix):
                if candidate == vector:
                    best_candidate, best_index, best_score = candidate, current_index, 1.0
                    break
                normalized_candidate = removeTrailing(input_list=candidate, removes_completeness=removes_completeness, completeness=completeness)
                if normalized_candidate == normalized_vector:
                    best_candidate, best_index, best_score = candidate, current_index, 1.0
                    break
                if isSubsequence(sequence=normalized_candidate, subsequence=normalized_vector) or isSubsequence(sequence=normalized_vector, subsequence=normalized_candidate): similarity = 1.0
                else:
                    def calculateDifference(vector1=[], vector2=[]):    
                        differences = []
                        for element1, element2 in zip(vector1, vector2):
                            if element1 != element2:
                                maximum_array = max(element1, element2)
                                difference = abs(element1 - element2) / (maximum_array if maximum_array > 0 else 1)
                                differences.append(difference)
                        differences_length = len(differences)
                        score = 1 - (sum(differences) / differences_length) if differences_length > 0 else 1
                        return score
                    cost = computeCost(list_one=normalized_vector, list_two=normalized_candidate)
                    score = calculateDifference(vector1=normalized_vector, vector2=normalized_candidate)
                    similarity = 1 / (1 + cost)
                    similarity = max(similarity, score)
                if similarity > best_score: best_score, best_index, best_candidate = similarity, current_index, candidate
            best_score = min((1.0, max((0.0, best_score))))
            result_dictionary = {'response': best_candidate, 'best_index': best_index, 'score': best_score}
            return result_dictionary
        except Exception as error:
            print('ERROR in euclideanMethod: ' + str(error))
            try: response = matrix[0]
            except: response = []
            return {'response': response, 'best_index': 0, 'score': 0.0}
    def semanticComparison(self, string1='', string2=''):
        try:
            score = 0.0
            prompt, answer = self.__stringValidation(string=string1), self.__stringValidation(string=string2)
            if len(prompt) < 1 or len(answer) < 1: return 0.0
            prompt = self.truncateTokens(text=self.normalization(prompt), precision=self.__precision, minimum_length=3)
            answer = self.truncateTokens(text=self.normalization(answer), precision=self.__precision, minimum_length=3)
            prompt_tokens, answer_tokens = prompt.split(), answer.split()
            prompt_length, answer_length = len(prompt_tokens), len(answer_tokens)
            tokens, targets = (prompt_tokens, answer_tokens) if prompt_length < answer_length else (answer_tokens, prompt_tokens)
            for token in tokens:
                had_hits = sum([int((token == target) or ((len(token) > 3 and len(target) > 3) and (token in target or target in token))) for target in targets]) > 0
                if had_hits: score += 1.0
            score = score / len(tokens)
            return score
        except Exception as error:
            print('ERROR in semanticComparison: ' + str(error))
            return 0.0  
    def outputAdaptedToInput(self, Input='', Output='', hot=True, stream=False):
        try:
            Input = self.__stringValidation(string=Input)
            Output = self.__stringValidation(string=Output)
            hot = self.__boolValidation(boolean=hot)
            stream = self.__boolValidation(boolean=stream)
            if stream: return self.__outputAdaptedToInputYIELD(Input=Input, Output=Output, hot=hot)
            else: return self.__outputAdaptedToInputRETURN(Input=Input, Output=Output, hot=hot)
        except Exception as error:
            print('ERROR in outputAdaptedToInput: ' + str(error))
            return ''   
    def embeddingForText(self, embedding=[], tokenizer='sapi'):
        try:
            text = ''
            embedding = self.__listValidation(array=embedding)
            tokenizer = self.__stringValidation(string=tokenizer).lower()
            if tokenizer == 'gpt': text = self.__embeddingForTextGPT(embedding=embedding)
            else: text = self.__embeddingForTextSAPI(embedding=embedding)
            return text
        except Exception as error:
            print('ERROR in embeddingForText: '+str(error))
            return ''
    def addHiddenLayer(self, num_neurons=0):
        try:
            self.__hidden_layers.append(num_neurons)
            return True
        except Exception as error:
            print('ERROR in addHiddenLayer: ' + str(error))
            return False
    def train(self, dataset_path='', string='', precision=1.0, tokenizer='gpt', method='semantic', interaction=True, activation_function='linear', bias=0.0, learning_rate=1.0, stochastic_factor=False, fx=False, progress=True):
        try:
            training_result = True
            progress = self.__boolValidation(boolean=progress)
            if not progress: self.__set_tqdm(disable=True)
            method = self.__stringValidation(string=method).lower()
            if len(self.__hidden_layers) > 0: method = 'hurnet'
            progress_bar_1 = self.__update_tqdm(total=7, description=method.title()+' model training')
            progress_bar_1.update(1)
            dataset_path = self.__stringValidation(string=dataset_path)
            string = self.__stringValidation(string=string)
            precision = min((1, max((0, self.__floatValidation(floating=precision)))))
            tokenizer = self.__stringValidation(string=tokenizer).lower()
            interaction = self.__boolValidation(boolean=interaction)
            activation_function = self.__stringValidation(string=activation_function).lower()
            bias = self.__floatValidation(floating=bias)
            learning_rate = self.__floatValidation(floating=learning_rate)
            stochastic_factor = self.__boolValidation(boolean=stochastic_factor)
            fx = self.__boolValidation(boolean=fx)
            its_json_file, json_content, general_text = dataset_path.endswith('.json'), '', string
            with_dataset_path, with_string = len(dataset_path) > 0, len(string) > 0
            progress_bar_1.update(1)
            if with_dataset_path or with_string:
                def isWEBAddress(url_path=''):
                    url_path = str(url_path).lower().strip()
                    return url_path.startswith('https://') or url_path.startswith('http://') or url_path.startswith('www.')
                is_web_address = isWEBAddress(url_path=dataset_path)
                if not is_web_address and not self.__path.isfile(dataset_path) and not with_string:
                    print('Non-existent path: '+dataset_path)
                    print('The dataset file does not exist at the specified path!')
                    return False
                if with_dataset_path:
                    if is_web_address:
                        def readRemoteFile(url=''):
                            from urllib.request import urlopen
                            with urlopen(url) as response: return str(response.read().decode('utf-8', errors='replace').replace('\r\n', '\n').replace('\r', '\n')).strip()
                        if its_json_file: json_content = readRemoteFile(url=dataset_path)
                        else: general_text = string+'\n\n'+readRemoteFile(url=dataset_path)
                    else:
                        with open(dataset_path, 'r', encoding='utf-8') as file:
                            if its_json_file: json_content = str(file.read()).strip()
                            else: general_text = string+'\n\n'+str(file.read()).strip()
                tokens_amount = str(json_content)+'\n\n'+general_text
                self.tokens_amount = self.countTokens(text=tokens_amount, model='gpt-4')
            else:
                print('The dataset file is empty!')
                return False
            progress_bar_1.update(1)    
            data, general_text = [], general_text.strip()
            if its_json_file:
                data = self.__loadJSON(string_content=json_content)
                if type(data) == dict:
                    key0 = list(data.keys())[0]
                    data = data[key0]
            data_length = len(data)
            if method == 'automatic':
                more_than_one_million = data_length > 1000000
                if its_json_file and not more_than_one_million: method = 'semantic'
                elif its_json_file and precision <= 0.5: method = 'euclidean'
                elif its_json_file and more_than_one_million: method = 'hurnet'
                else: method = 'search'
            if method == 'search':
                progress_bar_x = self.__update_tqdm(total=4, description='Converting data file')
                progress_bar_x.update(1)
                if its_json_file:
                    general_text += '\n\n'
                    for input_output in data:
                        keys = list(input_output.keys())
                        for key in keys: general_text += input_output[key]+'\n'
                        general_text += '\n'
                progress_bar_x.update(1)
                general_text = general_text.strip()
                def normalizeNewLines(text=''): return self.__sub(r'\n+', '\n', str(text).strip())
                bar_n, bar_nn, point, separator = '\n', '\n\n', '.', ' '
                count_bar_n = normalizeNewLines(text=general_text).count(bar_n)
                count_bar_nn = general_text.count(bar_nn)
                count_point = general_text.count(point)
                progress_bar_x.update(1)
                if max((count_bar_n, count_bar_nn)) > (count_point//4): separator = bar_nn if count_bar_nn > (count_bar_n//4) else bar_n
                else:
                    separators, maximum_count, maximum_index = ('.', '?', ';', '!', '\n'), 0, 0
                    for index, separator in enumerate(separators):
                        separator_count = general_text.count(separator)
                        if separator_count > maximum_count: maximum_count, maximum_index = separator_count, index
                    separator = separators[maximum_index]
                self.__outputs, self.__method, self.__precision = general_text.split(separator), method, precision
                progress_bar_x.update(1)
                progress_bar_1.update(4)
                return True
            embedding_size, vocabulary_indexes = 10, []
            if its_json_file:
                progress_bar_2 = self.__update_tqdm(total=data_length, description='Converting JSON file')
                for input_output in data:
                    keys = list(input_output.keys())
                    Input, Output = '', ''
                    if 'input' in keys: Input = input_output['input']
                    elif 'Input' in keys: Input = input_output['Input']
                    elif 'INPUT' in keys: Input = input_output['INPUT']
                    elif 'question' in keys: Input = input_output['question']
                    elif 'Question' in keys: Input = input_output['Question']
                    elif 'QUESTION' in keys: Input = input_output['QUESTION']
                    elif 'prompt' in keys: Input = input_output['prompt']
                    elif 'Prompt' in keys: Input = input_output['Prompt']
                    elif 'PROMPT' in keys: Input = input_output['PROMPT']
                    else: Input = input_output[keys[0]]
                    if 'output' in keys: Output = input_output['output']
                    elif 'Output' in keys: Output = input_output['Output']
                    elif 'OUTPUT' in keys: Output = input_output['OUTPUT']
                    elif 'answer' in keys: Output = input_output['answer']
                    elif 'Answer' in keys: Output = input_output['Answer']
                    elif 'ANSWER' in keys: Output = input_output['ANSWER']
                    else: Output = input_output[keys[-1]]
                    input_data = self.truncateTokens(text=self.normalization(Input), precision=precision, minimum_length=3)
                    input_length = len(input_data)
                    if input_length > embedding_size: embedding_size = input_length
                    self.__input_list.append(input_data)
                    self.__outputs.append(Output.strip())
                    vocabulary_indexes.append([self.__getVocabularyIndex()])
                    progress_bar_2.update(1)
            progress_bar_1.update(1)
            if len(general_text) > 0:
                def splitText(text=''):
                    def extractCodeBlocks(text=''):
                        result = []
                        lines, index = text.split('\n'), 0
                        lines_length = len(lines)
                        progress_bar_3 = self.__update_tqdm(total=lines_length, description='Converting code blocks')
                        while index < lines_length:
                            if '```' in lines[index]:
                                code_block = []
                                line_before_backticks = lines[index].split('```')[0].strip()
                                if index > 0 and lines[index-1].strip().endswith(':'):
                                    code_block.append(lines[index-1])
                                    new_index = index - 2
                                    while new_index >= 0:
                                        if lines[new_index].strip() != '':
                                            result.append(lines[new_index])
                                            break
                                        new_index -= 1
                                if line_before_backticks: result.append(line_before_backticks)
                                code_block.append(lines[index])
                                index += 1
                                while index < len(lines) and '```' not in lines[index]:
                                    code_block.append(lines[index])
                                    index += 1
                                if index < len(lines):
                                    code_block.append(lines[index])
                                    index += 1
                                result.append('\n'.join(code_block))
                            else: index += 1
                            progress_bar_3.update(1)
                        return result
                    code_blocks = []
                    if '```' in text:
                        code_blocks = extractCodeBlocks(text=text)
                        for block in code_blocks: text = text.replace(block, '')
                    result_list, list_index, odd_index = [], -1, False
                    text = str(text).strip()
                    sentence, separator, code_block, text_length = '', '', [], len(text)
                    progress_bar_4 = self.__update_tqdm(total=len(text), description='Converting text')
                    for index, char in enumerate(text):
                        sentence += char
                        if char == ':': separator = '\n\n'
                        if sentence.endswith('```'): code_block.append('```')
                        is_code_block0, is_code_block1 = len(code_block) > 0, len(code_block) > 1
                        odd_index = (list_index % 2) != 0
                        if not separator and not is_code_block0 and char in ('?', '!', '.', ';'):
                            sentence = sentence.strip()
                            if len(sentence) > 0:
                                result_list.append(sentence)
                                list_index += 1
                                odd_index = (list_index % 2) != 0
                            if list_index >= 2 and odd_index and sentence.endswith('?'):
                                result_list[list_index - 2] += ' '+result_list[list_index - 1]
                                result_list.pop(list_index - 1)
                                list_index -= 1
                                odd_index = (list_index % 2) != 0
                            sentence = ''
                        if separator and not is_code_block0:
                            next_separator = text[index + 1] if index + 1 < text_length else ''
                            if char+next_separator == separator:
                                sentence = sentence.strip()
                                if len(sentence) > 0:
                                    result_list.append(sentence)
                                    list_index += 1
                                    odd_index = (list_index % 2) != 0
                                sentence, separator = '', ''
                        if is_code_block1:
                            if len(sentence) > 0:
                                result_list.append(sentence)
                                list_index += 1
                                odd_index = (list_index % 2) != 0      
                            sentence, code_block, is_code_block0, is_code_block1 = '', [], False, False
                        progress_bar_4.update(1)
                    return result_list+code_blocks
                def createInputOutput(text_parts=[], embedding_size=10):
                    vocabulary_indexes = []
                    text_parts_length = len([x for x in range(0, len(text_parts), 2)])
                    progress_bar_5 = self.__update_tqdm(total=text_parts_length, description='Structuring data')
                    for vocabulary_index in range(0, len(text_parts), 2):
                        input_value = text_parts[vocabulary_index].strip()
                        if vocabulary_index + 1 < len(text_parts): output_value = text_parts[vocabulary_index + 1].strip()
                        else: output_value = input_value
                        if len(input_value) < 1: input_value = output_value
                        if len(output_value) < 1: output_value = input_value
                        input_data = self.truncateTokens(text=self.normalization(input_value), precision=precision, minimum_length=3)
                        input_length = len(input_data)
                        if input_length > embedding_size: embedding_size = input_length
                        self.__input_list.append(input_data)
                        self.__outputs.append(output_value)
                        vocabulary_indexes.append([self.__getVocabularyIndex()])
                        progress_bar_5.update(1)
                    return (vocabulary_indexes, embedding_size)
                text_parts = splitText(text=general_text)
                if len(text_parts) > 0:
                    _vocabulary_indexes, embedding_size = createInputOutput(text_parts=text_parts, embedding_size=embedding_size)
                    vocabulary_indexes += _vocabulary_indexes
            if len(vocabulary_indexes) < 1:
                print('There is no data for training!')
                return False
            progress_bar_1.update(1)
            progress_bar_6 = self.__update_tqdm(total=len(self.__input_list), description='Tokenizing data')
            for input_data in self.__input_list:
                input_data = self.textForEmbedding(text=input_data, length=embedding_size, quantization=0, tokenizer=tokenizer)
                self.__inputs.append(input_data)
                progress_bar_6.update(1)
            self.__input_list = []              
            progress_bar_1.update(1)
            if method == 'hurnet':
                from hurnet import HurNet
                self.__hurnet_neural_network = HurNet(architecture='multi_layer', fx=fx)
                if len(self.__hidden_layers) > 0:
                    for hidden_layer in self.__hidden_layers: self.__hurnet_neural_network.addHiddenLayer(num_neurons=hidden_layer)
                training_result = self.__hurnet_neural_network.train(input_layer=self.__inputs, output_layer=vocabulary_indexes, interaction=interaction, activation_function=activation_function, bias=bias, learning_rate=learning_rate, stochastic_factor=stochastic_factor)
            self.__embedding_size, self.__precision, self.__tokenizer, self.__method, self.__fx = embedding_size, precision, tokenizer, method, fx
            progress_bar_1.update(1)
            self.__set_tqdm(disable=False)
            return training_result
        except Exception as error:
            print('ERROR in train: '+str(error))
            self.__set_tqdm(disable=False)
            return False
    def saveModel(self, model_path='', progress=True):
        try:
            progress = self.__boolValidation(boolean=progress)
            if not progress: self.__set_tqdm(disable=True)
            progress_bar = self.__update_tqdm(total=7, description=f'Saving {self.__method} model')
            progress_bar.update(1)
            if len(model_path) < 1: model_path = './model'
            if not model_path.startswith('./'): model_path = './'+model_path
            directory = self.__path.split(model_path)[0]
            if directory not in ('.', './') and not self.__path.isdir(directory): self.__makedirs(directory, exist_ok=True)
            if self.__path.isdir(model_path):
                file_name = 'model.hurnet' if self.__method == 'hurnet' else 'model.scnnet'
                model_path = self.__path.join(model_path, file_name)
            save_vocabulary = self.__saveVocabulary(model_path=model_path)
            progress_bar.update(1)
            def replaceExtension(path='', old='', new=''):
                if path.lower().endswith('.'+old):
                    model_path_split = path.split('.')
                    model_path_split[-1] = new
                    return '.'.join(model_path_split)
                else: return path
            if self.__method == 'hurnet':
                model_path = replaceExtension(path=model_path, old='scnnet', new='hurnet')
                progress_bar.update(5)
                self.__set_tqdm(disable=False)
                return self.__hurnet_neural_network.saveModel(model_path=model_path)
            progress_bar.update(1)
            model_path = self.__stringValidation(string=model_path)
            if len(model_path) < 1: model_path = 'model.scnnet'
            progress_bar.update(1)
            model_path = replaceExtension(path=model_path, old='hurnet', new='scnnet')
            if not model_path.lower().endswith('.scnnet'): model_path += '.scnnet'
            progress_bar.update(1)
            data = {'inputs': self.__inputs, 'precision': self.__precision, 'tokenizer': self.__tokenizer}
            progress_bar.update(1)
            with open(model_path, 'wb') as file: self.__dump(data, file)
            progress_bar.update(1)
            self.__set_tqdm(disable=False)
            return save_vocabulary
        except Exception as error:
            print('ERROR in saveModel: ' + str(error))
            self.__set_tqdm(disable=False)
            return False
    def loadModel(self, model_path='', progress=True):
        try:
            progress = self.__boolValidation(boolean=progress)
            if not progress: self.__set_tqdm(disable=True)
            progress_bar = self.__update_tqdm(total=7, description=f'Loading {self.__method} model')
            progress_bar.update(1)
            if len(model_path) < 1: model_path = './model'
            if not model_path.startswith('./'): model_path = './'+model_path
            def findFile(directory=''):
                if not self.__path.isdir(directory): return directory
                files = self.__listdir(directory)
                for extension in ('.scnnet', '.hurnet'):
                    for file in files:
                        if file.endswith(extension): return self.__path.join(directory, file)
                return directory
            if self.__path.isdir(model_path): model_path = findFile(directory=model_path)
            load_vocabulary = self.__loadVocabulary(model_path=model_path)
            progress_bar.update(1)
            if self.__method == 'hurnet':
                if self.__hurnet_neural_network is None:
                    from hurnet import HurNet
                    self.__hurnet_neural_network = HurNet(architecture='multi_layer', fx=self.__fx)
                hurnet_neural_network = self.__hurnet_neural_network.loadModel(model_path=model_path)
                if not hurnet_neural_network:
                    print('Path: '+str(model_path))
                    print('The path to the referenced HURNET model does not exist or there was an error loading it.')
                progress_bar.update(5)
                self.__set_tqdm(disable=False)
                return hurnet_neural_network
            progress_bar.update(1)
            model_path, data = self.__stringValidation(string=model_path), ''
            if len(model_path) < 1: model_path = 'model.scnnet'
            if not model_path.lower().endswith('.scnnet'): model_path += '.scnnet'
            if not self.__path.isfile(model_path):
                print('Non-existent path: '+model_path)
                print('The path to the referenced SCNNET model does not exist.')
                return False
            progress_bar.update(1)
            with open(model_path, 'rb') as file: data = self.__load(file)
            progress_bar.update(1)
            data = self.__loadJSON(string_content=data)
            progress_bar.update(1)
            try: self.__inputs = list(data['inputs'])
            except: self.__inputs = []
            try: self.__precision = float(data['precision'])
            except: self.__precision = 1
            try: self.__tokenizer = str(data['tokenizer']).lower().strip()
            except: self.__tokenizer = 'sapi'
            progress_bar.update(1)
            self.__set_tqdm(disable=False)
            return load_vocabulary
        except Exception as error:
            print('ERROR in loadModel: ' + str(error))
            self.__set_tqdm(disable=False)
            return False
    def getTrainingText(self):
        try:
            text = ''
            if len(self.__inputs) == len(self.__outputs):
                for embedding, output in zip(self.__inputs, self.__outputs):
                    input_text = self.embeddingForText(embedding=embedding, tokenizer=self.__tokenizer).strip()
                    text += input_text+'\n'+output+'\n\n'
            else:
                for output in self.__outputs: text += output+'\n\n'
            return text.strip()
        except Exception as error:
            print('ERROR in getTrainingText: '+str(error))
            return ''
    def addFit(self, prompt='', answer=''):
        try:
            if self.__method == 'hurnet': return False
            prompt, answer = self.__stringValidation(string=prompt), self.__stringValidation(string=answer)
            if self.__method == 'search': self.__outputs.append(prompt+' '+answer)
            else:
                input_data = self.truncateTokens(text=self.normalization(prompt), precision=self.__precision, minimum_length=3)
                input_layer = self.textForEmbedding(text=input_data, length=self.__embedding_size, quantization=0, tokenizer=self.__tokenizer)
                self.__inputs.append(input_layer)
                self.__outputs.append(answer)
            return True
        except Exception as error:
            print('ERROR in addFit: ' + str(error))
            return False
    def predict(self, prompt='', minimum_score=0.5, hot=False, stream=False):
        try:
            answer = ''
            prompt = original_prompt = self.__stringValidation(string=prompt)
            minimum_score = min((1, max((0, self.__floatValidation(floating=minimum_score)))))
            hot = self.__boolValidation(boolean=hot)
            stream = self.__boolValidation(boolean=stream)
            if self.__method == 'search':
                method_result = self.searchMethod(text=original_prompt, text_vector=self.__outputs, minimum_instruction_score=0.5)
                output, best_index, score = method_result['response'], method_result['best_index'], method_result['score']
                if score >= minimum_score: answer = output
                self.prediction_score = score
                answer = self.outputAdaptedToInput(Input=original_prompt, Output=answer, hot=hot, stream=stream)
                return answer
            hurnet = self.__method == 'hurnet'
            if hot and hurnet: prompt = self.__shuffleText(text=prompt)
            input_data = self.truncateTokens(text=self.normalization(prompt), precision=self.__precision, minimum_length=3)
            input_layer = self.textForEmbedding(text=input_data, length=self.__embedding_size, quantization=0, tokenizer=self.__tokenizer)
            method_result = {'response': [], 'best_index': -1, 'score': 1.0}
            if hurnet:
                if self.__hurnet_neural_network is None:
                    from hurnet import HurNet
                    self.__hurnet_neural_network = HurNet(architecture='multi_layer', fx=self.__fx)
                vocabulary_index = self.__hurnet_neural_network.predict(input_layer=[input_layer], decimal_places=0)[0][0]
                minimum_index, maximum_index = 0, len(self.__outputs)-1
                vocabulary_index = min((maximum_index, max((minimum_index, vocabulary_index))))
                method_result['best_index'] = vocabulary_index
            elif self.__method == 'semantic': method_result = self.semanticMethod(vector=input_layer, matrix=self.__inputs, removes_completeness=True)
            elif self.__method == 'euclidean': method_result = self.euclideanMethod(vector=input_layer, matrix=self.__inputs, removes_completeness=True)
            best_index, score = method_result['best_index'], method_result['score']
            output = self.__outputs[best_index]
            if hurnet: score = self.semanticComparison(string1=original_prompt, string2=output)
            if score >= minimum_score: answer = output
            self.prediction_score = score
            answer = self.outputAdaptedToInput(Input=original_prompt, Output=answer, hot=hot, stream=stream)
            return answer
        except Exception as error:
            print('ERROR in predict: ' + str(error))
            return ''
    def print_predict(self, prompt='', minimum_score=0.5, hot=False, stream=False):
        try:
            answer = self.predict(prompt=prompt, minimum_score=minimum_score, hot=hot, stream=stream)
            if stream:
                for token in answer:
                    print(token, end='', flush=True)
                    self.__sleep(0.005)
                print()
            else: print(answer)
        except Exception as error:
            print('ERROR in print_predict: ' + str(error))
            return ''
# THIS IS AN EXTENSION NETWORK OF THE SKILLS OF THE HURNET ARTIFICIAL NEURAL NETWORK
# Semantic Comparison Network (SCN) is a new artificial neural network architecture based on the HurNet network. The semantic comparison network architecture also utilizes semantic comparison calculations and Euclidean distance for feature expansion.
# The SCN focuses on language model development and employs a significantly faster training approach compared to traditional transformer-based architectures. This algorithm was created, designed, and developed by Sapiens Technology®️, and any sharing, disclosure,          
# or public commentary on the logic involved in this code without our prior authorization is strictly prohibited and subject to legal action by our team of attorneys. All copyright rights to this algorithm are under the guardianship of Sapiens Technology®️,
# and we do not permit any modification, customization, or enhancement of the original code.
# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
