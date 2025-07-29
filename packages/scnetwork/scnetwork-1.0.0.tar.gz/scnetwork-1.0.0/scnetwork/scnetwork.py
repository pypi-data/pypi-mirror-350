"""
This code was architected, developed, and programmed by Ben-Hur Varriano for Sapiens Technology®️ (as well as all other AI algorithms of the company),
and any unauthorized alteration, adaptation, and/or distribution, as well as public comments and/or postings regarding the operation and/or mathematics involved in the algorithm, are strictly prohibited.
Failure to comply with these rules may result in legal action against the author by our team of attorneys.

The module in question comprises a sophisticated mathematical algorithm operated by a set of advanced applied mathematics functions, equations,
and calculations that collaboratively develop large language models (LLMs) with a novel approach and a revolutionary concept.
It differentiates itself from other architectures due to its ease of construction and efficiency in model training and inference.
The parameterization, training, and inference processes are significantly faster and require computational resources several orders of magnitude lower than those used by conventional model architectures.
Furthermore, the architecture can be used to train instruction-based models, chat-based models, or a combination of both.
Its tensor processing via streaming enables an infinite context window, and its adaptive response calculations allow the model to generalize to inputs it was not explicitly trained on.

We named the network SCNet, an abbreviation of "Semantic Comparison Network", referring to the underlying algorithm (also authored by Ben-Hur Varriano) that originated the current code.
"""
# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
class SCNet():
    def __init__(self, device=None, user_id=0, parallel_prediction=False, minimum_probability_for_candidates=0.9, show_errors=True):
        try:
            self.__local_device = device.lower().strip() if type(device) == str else None
            self.user_id = int(user_id) if type(user_id) in (bool, int, float) else 0
            self.__parallel_prediction = bool(parallel_prediction) if type(parallel_prediction) in (bool, int, float) else False
            self.minimum_probability_for_candidates = min((1.0, max((0.0, float(minimum_probability_for_candidates))))) if type(minimum_probability_for_candidates) in (bool, int, float) else 0.9
            self.__show_errors = bool(show_errors) if type(show_errors) in (bool, int, float) else True
            from sys import platform
            from os.path import exists, splitext, basename, join, dirname, isdir, getsize, split
            from os import remove, sysconf, makedirs, replace, stat, fsync
            from pathlib import Path
            from tiktoken import encoding_for_model
            from unicodedata import normalize, category
            from tempfile import gettempdir, NamedTemporaryFile
            from psutil import virtual_memory
            from tqdm import tqdm
            from functools import partialmethod
            from urllib import request as urllib_request
            from urllib.request import urlopen
            from json import load as json_load
            from io import TextIOWrapper
            from csv import reader as csv_reader
            from ijson import items as json_items
            from mmap import mmap as MemoryMap, ACCESS_READ
            try:
                from numpy import mean, fromstring, array, asarray, zeros, empty, abs, inf, argmin, maximum, where
                from numpy.linalg import norm
                numpy_library_available = True
            except: numpy_library_available = False
            try:
                from torch import cuda, device as torch_device, backends, as_tensor, save, load
                from torch.nn.functional import cosine_similarity
                torch_library_available = True
            except: torch_library_available = False
            try:
                from torch_xla.core import xla_model
                xla_library_available = True
            except:
                apple = platform == 'darwin'
                if not apple and self.__local_device in ('tpu', 'xla'): print('Run "!pip install torch-xla" and try again.')
                xla_library_available, xla_model = False, None
            from math import sqrt
            from errno import EXDEV
            from ctypes import CDLL, c_uint64
            from semantic_comparison_network import SemanticComparisonNetwork
            from re import compile, sub, DOTALL
            from time import sleep
            from shutil import move
            from hurnet import HurNet
            self.__temporary_path = ''
            self.__exists = exists
            self.__remove = remove
            self.__model_path = ''
            self.__Path = Path
            self.__splitext = splitext
            self.__basename = basename
            self.__add_fit = False
            self.__possible_encoders = ('gpt2', 'gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo', 'text-davinci-001', 'text-davinci-002', 'text-davinci-003')
            self.__encoding_for_model = encoding_for_model
            self.__normalize = normalize
            self.__category = category
            self.__gettempdir = gettempdir
            self.__join = join
            self.__sysconf = sysconf
            self.__virtual_memory = virtual_memory
            self.__tqdm = tqdm
            self.__partialmethod = partialmethod
            self.__urlopen = urlopen
            self.__json_load = json_load
            self.__TextIOWrapper = TextIOWrapper
            self.__csv_reader = csv_reader
            self.__json_items = json_items
            self.__MemoryMap = MemoryMap
            self.__ACCESS_READ = ACCESS_READ
            self.__mean = mean
            self.__fromstring = fromstring
            self.__array = array
            self.__block_size = 50
            self.__NamedTemporaryFile = NamedTemporaryFile
            self.parameters_number = 0
            self.__candidates = []
            self.__torch_library_available = torch_library_available
            self.__numpy_library_available = numpy_library_available
            self.__cuda = cuda
            self.__device = torch_device
            self.__xla_library_available = xla_library_available
            self.__xla_model = xla_model
            self.__backends = backends
            self.__as_tensor = as_tensor
            self.__asarray = asarray
            self.__norm = norm
            self.__sqrt = sqrt
            self.__cosine_similarity = cosine_similarity
            self.__separators = ('?', '.', ';', '!', '\n')
            self.__zeros = zeros
            self.__empty = empty
            self.__abs = abs
            self.__inf = inf
            self.__argmin = argmin
            self.__maximum = maximum
            self.__where = where
            self.__dirname = dirname
            self.__isdir = isdir
            self.__makedirs = makedirs
            self.__replace = replace
            self.__EXDEV = EXDEV
            self.__stat = stat
            self.__platform = platform
            self.__CDLL = CDLL
            self.__c_uint64 = c_uint64
            self.__fsync = fsync
            self.__tokenizer = 'gpt-4'
            self.__inputs = []
            self.__outputs = []
            self.fit_probability = 0.0
            self.probability = 0.0
            self.__SemanticComparisonNetwork = SemanticComparisonNetwork
            self.__compile = compile
            self.__sleep = sleep
            self.__fine_tuning = False
            self.__fit_model_path = ''
            self.__hurnet_architecture = False
            self.__hur_net = None
            self.__trained = False
            self.__sub = sub
            self.__DOTALL = DOTALL
            self.__hidden_layers = []
            self.__string = ''
            self.__getsize = getsize
            self.__split = split
            self.__add_hur = False
            self.__save = save
            self.__move = move
            self.__load = load
            self.__HurNet = HurNet
            self.__loaded = False
        except Exception as error:
            if self.__show_errors: print('ERROR in __init__: '+str(error))
    def __del__(self):
        try:
            if len(self.__temporary_path) > 0 and self.__exists(self.__temporary_path):
                if not self.__temporary_path.endswith('.sccon') and not self.__temporary_path.endswith('.scnet'): self.__remove(self.__temporary_path)
            model_path = str(self.__model_path).strip()
            if len(model_path) > 0:
                def _list_model_files(model_directory_path=''):
                    directory, file_name = self.__split(model_directory_path)
                    model_directory = self.__Path(directory)
                    model_directory = model_directory if model_directory.is_dir() else self.__Path('./')
                    if not model_directory.is_dir(): return []
                    file_name, _ = self.__splitext(self.__basename(model_directory_path))
                    network_model_files = model_directory.glob(f'{file_name}.scnet')
                    fitting_model_files = model_directory.glob(f'{file_name}.scfit') if not self.__add_fit else []
                    return [str(file_path) for file_path in network_model_files] + [str(file_path) for file_path in fitting_model_files]
                list_model_files = _list_model_files(model_directory_path=model_path)
                for model_file in list_model_files: self.__overwriteWithHexadecimal(file_path=model_file)
                self.__model_path = ''
        except Exception as error:
            if self.__show_errors: print('ERROR in __del__: '+str(error))
    def __updateEncoder(self, encoder='gpt-4'):
        try:
            encoder = str(encoder).lower().strip()
            if encoder not in self.__possible_encoders:
                encoder = 'gpt2'
                if encoder.startswith('gpt'):
                    if 'turbo' in encoder:
                        if '3' in encoder: encoder = 'gpt-3.5-turbo'
                        elif '4' in encoder: encoder = 'gpt-4-turbo'
                    elif '4' in encoder: encoder = 'gpt-4'
                elif 'davinci' in encoder:
                    encoder = 'text-davinci-003'
                    if '1' in encoder: encoder = 'text-davinci-001'
                    elif '2' in encoder: encoder = 'text-davinci-002'
            return encoder
        except Exception as error:
            if self.__show_errors: print('ERROR in __updateEncoder: '+str(error))
            return 'gpt2'
    def __embeddingForText(self, embedding=[], encoder='gpt-4', strip=True):
        try:
            embedding = list(embedding) if type(embedding) in (tuple, list) else []
            encoder = self.__updateEncoder(encoder=encoder)
            strip = bool(strip) if type(strip) in (bool, int, float) else True
            encoding = self.__encoding_for_model(encoder)
            decoder = encoding.decode(embedding)
            return decoder.strip() if strip else decoder
        except Exception as error:
            if self.__show_errors: print('ERROR in __embeddingForText: '+str(error))
            return ''
    def __loadJSON(self, file_path='', string_content=''):
        try:
            json_content = {}
            file_path, string_content = str(file_path).strip(), str(string_content).strip()
            if len(file_path) > 0:
                if file_path.lower().startswith(('http://', 'https://', 'www.')):
                    from requests import get
                    return get(file_path).json()
                elif self.__exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as file: string_content = str(file.read()).strip()
            string_content = str(string_content)
            try:
                from json import loads
                json_content = loads(string_content)
            except:
                from ast import literal_eval
                json_content = literal_eval(string_content)
            return json_content
        except Exception as error:
            print('ERROR in __loadJSON: '+str(error))
            return {}
    def __normalization(self, input_text=''):
        try:
            input_text = str(input_text).strip()
            cleaned_text = ''.join(character for character in self.__normalize('NFD', input_text) if self.__category(character) != 'Mn' and not self.__category(character).startswith('P'))
            processed_words = []
            for each_word in cleaned_text.lower().strip().split():
                if len(each_word) > 5: processed_words.append(each_word[:-3])
                else: processed_words.append(each_word)
            final_text = ' '.join(processed_words)
            return final_text
        except Exception as error:
            if self.__show_errors: print('ERROR in __normalization: '+str(error))
            return input_text
    def __getID(self, user_id=0):
        try:
            temporary_directory = self.__gettempdir()
            filename = self.__join(temporary_directory, str(user_id))
            if not self.__exists(filename): return 0
            with open(filename, 'r') as file_handle: last_id = file_handle.read()
            return int(last_id)
        except Exception as error:
            if self.__show_errors: print('ERROR in __getID: '+str(error))
            return 0
    def __setID(self, user_id=0, last_id=0):
        try:
            temporary_directory = self.__gettempdir()
            filename = self.__join(temporary_directory, str(user_id))
            with open(filename, 'w') as file_handle: file_handle.write(str(last_id))
            return True
        except Exception as error:
            if self.__show_errors: print('ERROR in __setID: '+str(error))
            return False
    def __getBufferSize(self):
        try:
            buffer_size = 1048576
            try: buffer_size = int((self.__sysconf('SC_PAGE_SIZE') * self.__sysconf('SC_AVPHYS_PAGES')) * 0.1)
            except: buffer_size = int(self.__virtual_memory().available * 0.1)
            return buffer_size
        except Exception as error:
            if self.__show_errors: print('ERROR in __getBufferSize: '+str(error))
            return 1048576
    def __setTqdm(self, disable=True):
        try:
            disable = bool(disable) if type(disable) in (bool, int, float) else True
            self.__tqdm.__init__ = self.__partialmethod(self.__tqdm.__init__, disable=disable)
            return True
        except Exception as error:
            if self.__show_errors: print('ERROR in __setTqdm: '+str(error))
            return False
    def __updateTqdm(self, total=1, description=''):
        try:
            total = int(total) if type(total) in (int, float) else 1
            description = description.strip() if type(description) == str else str(description).strip()
            progress_bar = self.__tqdm(total=total, desc=description, position=0, leave=True)
            return progress_bar
        except Exception as error:
            if self.__show_errors: print('ERROR in __updateTqdm: '+str(error))
            return False    
    def __splitText(self, dataset_path='', end_tag=''):
        try:
            lower_path = dataset_path.lower()
            remote_flag = lower_path.startswith(('http://', 'https://'))
            if lower_path.endswith('.json'):
                data_stream = self.__urlopen(dataset_path) if remote_flag else open(dataset_path, 'rb')
                try:
                    parsed_data = self.__json_load(data_stream)
                    if isinstance(parsed_data, dict):
                        if 'data' in parsed_data and isinstance(parsed_data['data'], list): data_items = parsed_data['data']
                        else:
                            data_items = []
                            for value in parsed_data.values():
                                if isinstance(value, list):
                                    data_items = value
                                    break
                    elif isinstance(parsed_data, list): data_items = parsed_data
                    else: data_items = []
                    for entry in data_items:
                        if not isinstance(entry, dict): continue
                        input_text = ''
                        for field in ('input', 'prompt', 'question'):
                            if field in entry and isinstance(entry[field], str):
                                input_text = entry[field]
                                break
                        if not input_text:
                            first_key = next(iter(entry), None)
                            input_text = str(entry.get(first_key, '')) if first_key else ''
                        output_text = ''
                        for field in ('output', 'answer', 'response'):
                            if field in entry and isinstance(entry[field], str):
                                output_text = entry[field]
                                break
                        if not output_text:
                            last_key = None
                            for key in entry: last_key = key
                            output_text = str(entry.get(last_key, '')) if last_key else ''
                        input_text, output_text = input_text.strip(), output_text.strip()
                        if input_text == output_text: output_text = ''
                        yield str(f'{input_text}\n{output_text}').strip()
                finally: data_stream.close()
                return
            if lower_path.endswith('.csv'):
                if remote_flag:
                    remote_stream = self.__urlopen(dataset_path)
                    text_stream = self.__TextIOWrapper(remote_stream, encoding='utf-8')
                    csv_reader_object = self.__csv_reader(text_stream)
                else:
                    file_stream = open(dataset_path, 'r', encoding='utf-8', newline='')
                    csv_reader_object = self.__csv_reader(file_stream)
                try:
                    header_row = next(csv_reader_object, None)
                    if header_row:
                        input_index = next((header_row.index(name) for name in ('input', 'prompt', 'question') if name in header_row), 0)
                        output_index = next((header_row.index(name) for name in ('output', 'answer', 'response') if name in header_row), len(header_row) - 1)
                    else: input_index, output_index = 0, 0
                    for row_data in csv_reader_object:
                        if not row_data: continue
                        input_text = row_data[input_index] if input_index < len(row_data) else ''
                        output_text = row_data[output_index] if output_index < len(row_data) else ''
                        input_text, output_text = input_text.strip(), output_text.strip()
                        if input_text == output_text: output_text = ''
                        yield str(f'{input_text}\n{output_text}').strip()
                finally:
                    if remote_flag: text_stream.detach(), remote_stream.close()
                    else: file_stream.close()
                return
            separator_sequence = end_tag.encode('utf-8')
            sequence_length = len(separator_sequence)
            if remote_flag:
                remote_stream, buffer_capacity, data_buffer = self.__urlopen(dataset_path), self.__getBufferSize(), bytearray()
                while True:
                    chunk_bytes = remote_stream.read(buffer_capacity)
                    if not chunk_bytes: break
                    data_buffer.extend(chunk_bytes)
                    start_position = 0
                    while True:
                        position = data_buffer.find(separator_sequence, start_position)
                        if position == -1: break
                        yield str(data_buffer[start_position:position].decode('utf-8')).strip()
                        start_position = position + sequence_length
                    del data_buffer[:start_position]
                if data_buffer: yield str(data_buffer.decode('utf-8')).strip()
                remote_stream.close()
                return
            file_stream = open(dataset_path, 'rb')
            memory_map, start_position = self.__MemoryMap(file_stream.fileno(), 0, access=self.__ACCESS_READ), 0
            while True:
                position = memory_map.find(separator_sequence, start_position)
                if position == -1: break
                yield str(memory_map[start_position:position].decode('utf-8')).strip()
                start_position = position + sequence_length
            if start_position < len(memory_map): yield str(memory_map[start_position:].decode('utf-8')).strip()
            memory_map.close(), file_stream.close()
        except Exception as error:
            if self.__show_errors: print('ERROR in __splitText: '+str(error))
            yield ''
    def __textForEmbedding(self, text='', length=None, encoder='gpt-4'):
        try:
            text = str(text)
            encoder = self.__updateEncoder(encoder=encoder)
            encoding = self.__encoding_for_model(encoder)
            embedding = encoding.encode(text)
            if length is not None:
                embedding_length = len(embedding)
                length = int(length) if type(length) in (bool, int, float) else 50
                if embedding_length < length:
                    difference = length - embedding_length
                    new_embedding = encoding.encode(' ') * difference
                    embedding += new_embedding
                elif embedding_length > length:
                    difference = embedding_length - length
                    embedding_x = embedding[:-difference-1]
                    embedding_y = embedding[embedding_length-difference-1:]
                    new_embedding = [int(round(float(self.__mean(embedding_y))))]
                    embedding = embedding_x + new_embedding
            return embedding
        except Exception as error:
            if self.__show_errors: print('ERROR in __textForEmbedding: '+str(error))
            return []
    def __iterNumericVectors(self, model_path=''):
        try:
            if len(model_path) < 1: model_path = self.__temporary_path
            if self.__exists(model_path):
                buffering = self.__getBufferSize()
                buffering = min(buffering, 2147483647)
                with open(model_path, 'r', buffering=buffering) as open_file:
                    for line in open_file:
                        embeddings = self.__fromstring(line, dtype=int, sep=' ')
                        if embeddings.size == 0: continue
                        yield embeddings.tolist()
            else: yield []
        except Exception as error:
            if self.__show_errors:
                print('ERROR in __iterNumericVectors: '+str(error))
                print('model_path: '+str(model_path))
            yield []
    def __countTokens(self, text='', encoder='gpt-4'):
        try:
            text, encoder = str(text), str(encoder).lower().strip()
            encoder = self.__updateEncoder(encoder=encoder)
            return len(self.__encoding_for_model(encoder).encode(text))
        except Exception as error:
            if self.__show_errors: print('ERROR in __countTokens: '+str(error))
            return len(str(text))
    def __textSummary(self, text='', max_tokens=1000000, encoder='gpt-4'):
        try:
            text = str(text).strip()
            max_tokens = int(max_tokens) if type(max_tokens) in (bool, int, float) else 1000000
            encoder = str(encoder).lower().strip()
            encoder = self.__updateEncoder(encoder=encoder)
            model_encoding = self.__encoding_for_model(encoder)
            token_list = model_encoding.encode(text)
            if len(token_list) <= max_tokens: return text
            max_tokens -= 2
            segment_length = max_tokens // 3
            initial_tokens = token_list[:segment_length]
            middle_index = len(token_list) // 2
            half_segment = segment_length // 2
            middle_start_index = max(middle_index - half_segment, 0)
            middle_tokens = token_list[middle_start_index:middle_start_index + segment_length]
            final_tokens = token_list[-segment_length:]
            initial_tokens = model_encoding.decode(initial_tokens).strip()
            middle_tokens = model_encoding.decode(middle_tokens).strip()
            final_tokens = model_encoding.decode(final_tokens).strip()
            def _remove_leading_punctuation(input_text=''):
                punctuation_characters="!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
                if input_text == '' or input_text[0] not in punctuation_characters: return input_text.strip()
                return input_text[1:].strip()
            def _extract_text_until_last_punctuation(input_text=''):
                result_text = input_text
                punctuation_priorities = ('.', '?', '!', ';', ',')
                for punctuation in punctuation_priorities:
                    last_occurrence_index = input_text.rfind(punctuation)
                    if last_occurrence_index != -1: result_text = input_text[:last_occurrence_index + 1]
                last_space_index = input_text.rfind(' ')
                if last_space_index != -1: result_text = input_text[:last_space_index]
                _remove_leading_punctuation
                result_text = input_text
                return _remove_leading_punctuation(input_text=result_text)
            initial_tokens = _extract_text_until_last_punctuation(input_text=initial_tokens)
            middle_tokens = _extract_text_until_last_punctuation(input_text=middle_tokens)
            final_tokens = _extract_text_until_last_punctuation(input_text=final_tokens)
            combined_tokens = initial_tokens+' '+middle_tokens+' '+final_tokens
            return combined_tokens
        except Exception as error:
            if self.__show_errors: print('ERROR in __textSummary: '+str(error))
            return text
    def __vectorsValidation(self, first_vector=[], second_vector=[]):
        try:
            first_vector, second_vector = self.__array(first_vector, dtype=float), self.__array(second_vector, dtype=float)
            first_vector_length, second_vector_length = first_vector.size, second_vector.size
            minimum_length = min((first_vector_length, second_vector_length))
            if first_vector_length != second_vector_length: first_vector, second_vector = first_vector[:minimum_length], second_vector[:minimum_length]
            return first_vector, second_vector
        except Exception as error:
            if self.__show_errors: print('ERROR in __vectorsValidation: '+str(error))
            return [], []
    def __processDataset(self, dataset_path='', string='', precision=1.0, tokenizer='gpt-4', context_window=float('inf'), end_tag='', progress=True):
        try:
            self.__setTqdm(disable=not progress)
            progress_bar_1 = self.__updateTqdm(total=6, description='Tokenizing data')
            progress_bar_1.update(1)
            max_sentence_count, new_max_sentence_count = 0, 0
            total_bytes, arbitrary_total, bytes_count = 0, 1000000, 0
            has_dataset_path = len(dataset_path) > 0
            has_string, split_text, parts_number = len(string) > 0, [], 0
            progress_bar_1.update(1)
            if self.__parallel_prediction:
                if context_window < float('inf'): max_sentence_count = context_window
                else:
                    total_bytes = self.__getsize(self.__temporary_path) if self.__exists(self.__temporary_path) else arbitrary_total
                    total_bytes += len(string.encode('utf-8'))
                    if total_bytes < 1: total_bytes = arbitrary_total
                    progress_bar_2 = self.__updateTqdm(total=total_bytes, description='Reading data')
                    if has_dataset_path:
                        for piece in self.__splitText(dataset_path=dataset_path, end_tag=end_tag):
                            if len(piece.strip()) > 0:
                                piece = rf'{piece}'
                                sentence_count = len(piece.split())
                                if sentence_count > max_sentence_count: max_sentence_count = sentence_count
                                current_bytes = len(piece.encode('utf-8'))
                                progress_bar_2.update(current_bytes)
                                bytes_count += current_bytes
                        max_sentence_count = int(round(max_sentence_count + (max_sentence_count/1.5)))
                    if has_string:
                        split_text = string.split(end_tag)
                        for piece in split_text:
                            if len(piece.strip()) > 0:
                                piece = rf'{piece}'
                                sentence_count = len(piece.split())
                                if sentence_count > new_max_sentence_count: new_max_sentence_count = sentence_count
                                current_bytes = len(piece.encode('utf-8'))
                                progress_bar_2.update(current_bytes)
                                bytes_count += current_bytes
                        new_max_sentence_count = int(round(new_max_sentence_count + (new_max_sentence_count/1.5)))
                    max_sentence_count = max((max_sentence_count, new_max_sentence_count))
                    progress_bar_2.n = total_bytes
                    progress_bar_2.refresh()
                    progress_bar_2.close()
                max_sentence_count = max((1, int(round(max_sentence_count*precision))))
                self.__block_size = max_sentence_count
            else:
                progress_bar_2 = self.__updateTqdm(total=1, description='Reading data')
                progress_bar_2.n = 1
                progress_bar_2.refresh()
                progress_bar_2.close()
                max_sentence_count = None
            progress_bar_1.update(1)
            temporary_file = self.__NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix='.temp')
            temporary_path = temporary_file.name
            state = 'a' if self.__exists(temporary_path) else 'w'
            total_bytes, bytes_count = self.__getsize(temporary_path) if self.__exists(temporary_path) else arbitrary_total, 0
            total_bytes += len(string.encode('utf-8'))
            if total_bytes < 1: total_bytes = arbitrary_total
            progress_bar_3, embeddings = self.__updateTqdm(total=total_bytes, description='Embedding data'), [0]
            progress_bar_1.update(1)
            if has_dataset_path:
                with open(temporary_path, state, encoding='utf-8') as output_file:
                    for piece in self.__splitText(dataset_path=dataset_path, end_tag=end_tag):
                        if len(piece.strip()) > 0:
                            piece = rf'{piece}'
                            embeddings = self.__textForEmbedding(text=piece, length=max_sentence_count, encoder=tokenizer)
                            output_file.write(' '.join(map(str, embeddings))+'\n')
                            parts_number += 1
                            current_bytes = len(piece.encode('utf-8'))
                            progress_bar_3.update(current_bytes)
                            bytes_count += current_bytes
            state = 'a' if self.__exists(temporary_path) else 'w'
            progress_bar_1.update(1)
            if has_string:
                if len(split_text) < 1: split_text = string.split(end_tag)
                with open(temporary_path, state, encoding='utf-8') as output_file:
                    for piece in split_text:
                        if len(piece.strip()) > 0:
                            piece = rf'{piece}'
                            embeddings = self.__textForEmbedding(text=piece, length=max_sentence_count, encoder=tokenizer)
                            output_file.write(' '.join(map(str, embeddings))+'\n')
                            parts_number += 1
                            current_bytes = len(piece.encode('utf-8'))
                            progress_bar_3.update(current_bytes)
                            bytes_count += current_bytes
            progress_bar_3.n = total_bytes if total_bytes > 0 else bytes_count
            progress_bar_3.refresh()
            progress_bar_3.close()
            self.parameters_number = parts_number * (max_sentence_count if self.__parallel_prediction else len(embeddings))
            progress_bar_1.update(1)
            progress_bar_1.close()
            return temporary_path
        except Exception as error:
            if self.__show_errors: print('ERROR in __processDataset: '+str(error))
            return self.__temporary_path
    def __alternativeVectorComparison(self, input_vector=[], vector_matrix=[]):
        try:
            if not input_vector: return (-1, [])
            def _find_closest_element(element=0, vector_x=[]): return min(vector_x, key=lambda x: abs(x - element))
            length, maximum_probability, maximum_index, maximum_vector = len(input_vector), 0, 0, []
            for index, vector_x in enumerate(vector_matrix):
                search_vector, target_vector, probability = (vector_x, input_vector, 0) if len(input_vector) > len(vector_x) else (input_vector, vector_x, 0)
                for element in search_vector:
                    if element in target_vector: probability += 1
                    else:
                        closest = _find_closest_element(element=element, vector_x=vector_x)
                        probability += abs(element - closest) / max((element, closest))
                probability /= length
                if probability > maximum_probability: maximum_probability, maximum_index, maximum_vector = probability, index, vector_x
                elif probability > self.minimum_probability_for_candidates: self.__candidates.append(vector_x)
            return (maximum_index, maximum_vector)
        except Exception as error:
            if self.__show_errors: print('ERROR in __alternativeVectorComparison: '+str(error))
            return (-1, [])
    def __vectorComparison(self, input_vector=[], vector_matrix=[]):
        try:
            if not self.__parallel_prediction: return self.__alternativeVectorComparison(input_vector=input_vector, vector_matrix=vector_matrix)
            if not input_vector: return (-1, [])
            torch_available = getattr(self, '_HurModel__torch_library_available', False) or self.__torch_library_available
            vector_dimension, element_size_bytes = len(input_vector), 8
            numpy_available = not torch_available and self.__numpy_library_available
            try:
                if torch_available:
                    device_preference, selected_device = self.__local_device or '', None
                    if len(device_preference) > 0:
                        if device_preference in ('gpu', 'cuda') and self.__cuda.is_available(): selected_device = self.__device('cuda')
                        elif device_preference in ('tpu', 'xla') and self.__xla_library_available: selected_device = self.__xla_model.xla_device()
                        elif device_preference == 'mps' and getattr(self.__backends, 'mps', None) and self.__backends.mps.is_available(): selected_device = self.__device('mps')
                        else: selected_device = self.__device('cpu')
                    else:
                        if self.__cuda.is_available(): selected_device = self.__device('cuda')
                        elif self.__xla_library_available: selected_device = self.__xla_model.xla_device()
                        elif getattr(self.__backends, 'mps', None) and self.__backends.mps.is_available(): selected_device = self.__device('mps')
                        else: selected_device = self.__device('cpu')
                    computation_device = selected_device
                    device_properties = self.__cuda.get_device_properties(computation_device)
                    free_memory_bytes = device_properties.total_memory - self.__cuda.memory_allocated(computation_device) - self.__cuda.memory_reserved(computation_device)
                    available_memory_bytes = int(free_memory_bytes * 0.1)
                else: available_memory_bytes = self.__getBufferSize()
                batch_size = max(1, int(available_memory_bytes // (vector_dimension * element_size_bytes)))
            except: batch_size = 1024
            query_tensor, query_norm = [], []
            if torch_available: query_tensor = self.__as_tensor(input_vector, device=computation_device).float()
            elif numpy_available:
                query_array = self.__asarray(input_vector, float)
                query_norm = self.__norm(query_array) + 1e-12
            else: query_norm = self.__sqrt(sum(value * value for value in input_vector)) + 1e-12
            def _equalize_vectors(source_vector=[], target_vector=[]):
                source_length, target_length = len(source_vector), len(target_vector)
                if source_length < target_length:
                    missing_elements_count = target_length - source_length
                    source_vector.extend([0] * missing_elements_count)
                elif source_length > target_length: del source_vector[target_length:]
                return source_vector
            length_query_tensor, length_query_norm = len(query_tensor), len(query_norm)
            best_similarity_score, best_vector_index, global_index_counter, best_vector_match = -float('inf'), -1, 0, []
            if torch_available or numpy_available:
                vector_batch = []
                def _trim_vectors_to_smallest_length(vector_batch=[]):
                    minimal_length = min(len(vector) for vector in vector_batch)
                    return [vector[:minimal_length] for vector in vector_batch]
                for vector in vector_matrix:
                    length_vector = len(vector)
                    if length_query_tensor > 0 and length_query_tensor != length_vector: query_tensor = self.__as_tensor(_equalize_vectors(source_vector=query_tensor.tolist(), target_vector=vector), device=computation_device).float()
                    if length_query_norm > 0 and length_query_norm != length_vector: query_norm = self.__asarray(_equalize_vectors(source_vector=query_norm.tolist(), target_vector=vector), float)
                    vector_batch.append(vector)
                    if len(vector_batch) >= batch_size:
                        if torch_available:
                            try: tensor_batch = self.__as_tensor(vector_batch, device=computation_device).float()
                            except: tensor_batch = self.__as_tensor(_trim_vectors_to_smallest_length(vector_batch=vector_batch), device=computation_device).float()
                            similarity_tensor = self.__cosine_similarity(tensor_batch, query_tensor.unsqueeze(0), dim=1)
                            maximum_value, maximum_index = similarity_tensor.max(dim=0)
                            local_similarity_score, local_vector_index = float(maximum_value.item()), int(maximum_index.item())
                        else:
                            array_batch = self.__asarray(vector_batch, float)
                            similarity_array = (array_batch @ query_array) / (self.__norm(array_batch, axis=1) * query_norm + 1e-12)
                            local_vector_index, local_similarity_score = int(similarity_array.argmax()), float(similarity_array[local_vector_index])
                        if local_similarity_score > best_similarity_score: best_similarity_score, best_vector_index, best_vector_match = local_similarity_score, global_index_counter + local_vector_index, vector_batch[local_vector_index]
                        elif local_similarity_score > self.minimum_probability_for_candidates: self.__candidates.append(vector_batch[local_vector_index])
                        global_index_counter += len(vector_batch)
                        vector_batch.clear()
                if vector_batch:
                    if torch_available:
                        try: tensor_batch = self.__as_tensor(vector_batch, device=computation_device).float()
                        except: tensor_batch = self.__as_tensor(_trim_vectors_to_smallest_length(vector_batch=vector_batch), device=computation_device).float()
                        similarity_tensor = self.__cosine_similarity(tensor_batch, query_tensor.unsqueeze(0), dim=1)
                        maximum_value, maximum_index = similarity_tensor.max(dim=0)
                        local_similarity_score, local_vector_index = float(maximum_value.item()), int(maximum_index.item())
                    else:
                        array_batch = self.__asarray(vector_batch, float)
                        similarity_array = (array_batch @ query_array) / (self.__norm(array_batch, axis=1) * query_norm + 1e-12)
                        local_vector_index, local_similarity_score = int(similarity_array.argmax()), float(similarity_array[local_vector_index])
                    if local_similarity_score > best_similarity_score:
                        best_similarity_score = local_similarity_score
                        best_vector_index, best_vector_match = global_index_counter + local_vector_index, vector_batch[local_vector_index]
                    elif local_similarity_score > self.minimum_probability_for_candidates: self.__candidates.append(vector_batch[local_vector_index])
            else:
                for vector in vector_matrix:
                    length_vector = len(vector)
                    if length_query_norm > 0 and length_query_norm != length_vector: query_norm = self.__asarray(_equalize_vectors(source_vector=query_norm.tolist(), target_vector=vector), float)
                    dot_product = sum(query_value * vector_value for query_value, vector_value in zip(input_vector, vector))
                    vector_norm = self.__sqrt(sum(value * value for value in vector)) + 1e-12
                    similarity_score = dot_product / (query_norm * vector_norm)
                    if similarity_score > best_similarity_score: best_similarity_score, best_vector_index, best_vector_match = similarity_score, global_index_counter, vector
                    elif similarity_score > self.minimum_probability_for_candidates: self.__candidates.append(vector)
                    global_index_counter += 1
            return best_vector_index, best_vector_match
        except Exception as error:
            if self.__show_errors: print('ERROR in __vectorComparison: '+str(error))
            return (-1, [])
    def __extractResponse(self, prompt='', text=''):
        try:
            prompt, text = str(prompt).strip(), str(text).strip()
            if len(prompt) < 1 or len(text) < 1: return ''
            separators, input_segment = self.__separators, None
            for separator in separators:
                index_position = text.find(separator)
                if index_position != -1 and index_position > 0 and index_position < len(text) - 1:
                    input_segment = text[:index_position + 1]
                    break
            if input_segment is None: return text
            prompt_words = self.__normalization(input_text=prompt).split()
            total_words = len(prompt_words)
            if total_words == 0: return text
            lower_case_input, matching_count = self.__normalization(input_text=input_segment), 0
            for word in prompt_words:
                if word.lower() in lower_case_input: matching_count += 1
            if matching_count * 2 >= total_words: return text[len(input_segment):].strip()
            return text
        except Exception as error:
            if self.__show_errors: print('ERROR in __extractResponse: '+str(error))
            return text
    def __similarityBetweenVectors(self, first_vector=[], second_vector=[]):
        try:
            if first_vector == second_vector: return 1.0
            first_vector, second_vector = self.__vectorsValidation(first_vector=first_vector, second_vector=second_vector)
            minimum_value, maximum_value = min(first_vector.min(), second_vector.min()), max(first_vector.max(), second_vector.max())
            vector_length = first_vector.size
            is_used = self.__zeros(vector_length, dtype=bool)
            range_of_values = maximum_value - minimum_value
            similarity_scores = self.__empty(vector_length, dtype=float)
            for index_first, value_first in enumerate(first_vector):
                differences = self.__abs(second_vector - value_first)
                differences[is_used] = self.__inf
                best_index = int(self.__argmin(differences))
                best_difference = float(differences[best_index])
                is_used[best_index] = True
                numeric_distance_normalized = (best_difference / range_of_values if range_of_values > 0 else 0.0)
                index_distance_normalized = (abs(index_first - best_index) / (vector_length - 1) if vector_length > 1 else 0.0)
                similarity_score = 1.0 - (numeric_distance_normalized + index_distance_normalized) / 2.0
                similarity_scores[index_first] = similarity_score
            overall_similarity_score = float(similarity_scores.mean())
            return max(0.0, min(1.0, overall_similarity_score))
        except Exception as error:
            if self.__show_errors: print('ERROR in __similarityBetweenVectors: '+str(error))
            return 0.0
    def __euclideanSimilarity(self, first_vector=[], second_vector=[]):
        try:
            first_vector, second_vector = self.__vectorsValidation(first_vector=first_vector, second_vector=second_vector)
            differences = self.__abs(first_vector - second_vector)
            maximums = self.__maximum(first_vector, second_vector)
            maximums = self.__where(maximums == 0, 1, maximums)
            percentages = differences / maximums
            average_difference = float(self.__mean(percentages))
            similarity = 1.0-average_difference
            return similarity
        except Exception as error:
            if self.__show_errors: print('ERROR in __euclideanSimilarity: '+str(error))
            return 0.0
    def __changeExtension(self, model_path='', old_extension='scnet', new_extension='sccon'):
        try:
            if model_path.endswith('.'+old_extension):
                model_path_split = model_path.split('.')
                model_path_split[-1] = new_extension
                model_path = '.'.join(model_path_split)
            return model_path
        except Exception as error:
            if self.__show_errors: print('ERROR in __changeExtension: '+str(error))
            return model_path
    def __format_numbers(self, data_number=0, is_tokens=False):
        try:
            if data_number < 1_000: return data_number if is_tokens else f'{data_number}U'
            elif data_number < 1_000_000: return f'{data_number // 1_000}K'
            elif data_number < 1_000_000_000: return f'{data_number // 1_000_000}M'
            elif data_number < 1_000_000_000_000: return f'{data_number // 1_000_000_000}B'
            else: return f'{data_number // 1_000_000_000_000}T'
        except Exception as error:
            if self.__show_errors: print('ERROR in __format_numbers: '+str(error))
            return data_number
    def __moveAndRenameStream(self, source_path='', destination_path='', formatted_params='', progress=True):
        try:
            self.__setTqdm(disable=not progress)
            progress_bar = self.__updateTqdm(total=6, description=f'Generating {formatted_params} parameters')
            progress_bar.update(1)
            destination_directory = self.__dirname(destination_path)
            if destination_directory and not self.__isdir(destination_directory): self.__makedirs(destination_directory, exist_ok=True)
            try:
                self.__replace(source_path, destination_path)
                progress_bar.update(5)
                return True
            except OSError as error:
                if error.errno != self.__EXDEV: raise
            progress_bar.update(1)
            source_file = open(source_path, 'rb')
            destination_file = open(destination_path, 'wb')
            source_descriptor = source_file.fileno()
            total_size = self.__stat(source_path).st_size
            buffer_size = self.__getBufferSize()
            punch_function, offset = None, 0
            destination_descriptor = destination_file.fileno()
            progress_bar.update(1)
            if self.__platform.startswith('linux'):
                libc = self.__CDLL('libc.so.6', use_errno=True)
                punch_hole_flag, keep_size_flag = 0x02, 0x01
                def perform_punch(offset: int, length: int) -> None: libc.fallocate(source_descriptor, punch_hole_flag | keep_size_flag, self.__c_uint64(offset), self.__c_uint64(length))
                punch_function = perform_punch
            progress_bar.update(1)
            progress_bar_bytes = self.__updateTqdm(total=total_size, description='Processing data')
            while True:
                data_block = source_file.read(buffer_size)
                if not data_block: break
                destination_file.write(data_block)
                destination_file.flush()
                self.__fsync(destination_descriptor)
                if punch_function: punch_function(offset, len(data_block))
                offset += len(data_block)
                progress_bar_bytes.update(len(data_block))
            progress_bar_bytes.close()
            progress_bar.update(1)
            source_file.close()
            destination_file.close()
            self.__remove(source_path)
            self.__temporary_path = destination_path
            progress_bar.update(1)
            progress_bar.close()
            return True
        except Exception as error:
            if self.__show_errors: print('ERROR in __moveAndRenameStream: '+str(error))
            return False
    def __overwriteWithHexadecimal(self, file_path=''):
        try:
            file_path = str(file_path).strip()
            if not self.__exists(file_path):
                print(f'Overwrite: The path specified in {file_path} does not exist!!')
                return False
            temporary_file = self.__NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix='.temp')
            temporary_path = temporary_file.name
            chunk_size, current_line = self.__getBufferSize(), []
            with open(file_path, 'rb') as input_file, open(temporary_path, 'w') as output_file:
                while True:
                    chunk = input_file.read(chunk_size)
                    if not chunk: break
                    for byte in chunk:
                        current_line.append(f'{byte:04x}')
                        if len(current_line) == 8:
                            output_file.write(' '.join(current_line) + '\n')
                            current_line = []
                if current_line: output_file.write(' '.join(current_line))
            self.__replace(temporary_path, file_path)
            if self.__exists(temporary_path): self.__remove(temporary_path)
            return True
        except Exception as error:
            if self.__show_errors:
                print('ERROR in __overwriteWithHexadecimal: '+str(error))
                print('file_path: '+str(file_path))
            return False
    def __restoreOriginalFromHexadecimal(self, file_path=''):
        try:
            file_path = str(file_path).strip()
            if not self.__exists(file_path):
                print(f'Restore: The path specified in {file_path} does not exist!!')
                return False
            temporary_file = self.__NamedTemporaryFile(delete=False, mode='w', encoding='utf-8', suffix='.temp')
            temporary_path = temporary_file.name
            with open(file_path, 'r', errors='ignore') as input_file, open(temporary_path, 'wb') as output_file:
                for line in input_file:
                    tokens = line.strip().split()
                    byte_values = bytes(int(token, 16) & 0xFF for token in tokens)
                    output_file.write(byte_values)
            self.__replace(temporary_path, file_path)
            if self.__exists(temporary_path): self.__remove(temporary_path)
            return True
        except Exception as error:
            if self.__show_errors:
                print('ERROR in __restoreOriginalFromHexadecimal: '+str(error))
                print('file_path: '+str(file_path))
            return False
    def __setInputsAndOutputs(self, prompt='', answer=''):
        try:
            normalized_prompt = self.__normalization(input_text=prompt)
            input_embeddings = self.__textForEmbedding(text=normalized_prompt, length=self.__block_size, encoder=self.__tokenizer)
            output_embeddings = self.__textForEmbedding(text=str(answer).strip(), length=self.__block_size, encoder=self.__tokenizer)
            self.__inputs.append(input_embeddings), self.__outputs.append(output_embeddings)
            return True
        except Exception as error:
            if self.__show_errors: print('ERROR in __setInputsAndOutputs: '+str(error))
            return False
    def __standardAdjustmentForecast(self, input_prompt=[], vector_matrix=[]):
        try:
            result_dictionary = {'id': 0, 'relationship_id': 0, 'index': 0, 'prompt': '', 'answer': '', 'probability': 0.0}
            if vector_matrix in ((), []): return result_dictionary
            input_text_x = self.__embeddingForText(embedding=input_prompt, encoder=self.__tokenizer, strip=True) if type(input_prompt) in (tuple, list) else input_prompt
            input_text_x = self.__normalization(input_text=input_text_x)
            input_tokens_x = input_text_x.split()
            x_length = len(input_tokens_x)
            maximum_id, maximum_relationship_id = 0, 0
            maximum_probability, maximum_index, old_prompt, maximum_forecast = 0.0, 0, '', ''
            last_id = self.__getID(user_id=self.user_id)
            for index, vector in enumerate(vector_matrix):
                tokens = self.__embeddingForText(embedding=vector, encoder=self.__tokenizer, strip=True)
                if '<|end|>' not in tokens: continue
                id, relationship_id, input_text_y, output_text = tokens.split('<|end|>')
                id, relationship_id = int(id), int(relationship_id)
                if relationship_id == 0 or relationship_id == last_id:
                    input_text_z = input_text_y
                    input_text_y = self.__normalization(input_text=input_text_y)
                    input_tokens_y = input_text_y.split()
                    y_length = len(input_tokens_y)
                    if x_length < y_length: target, search = input_tokens_x, input_tokens_y
                    else: target, search = input_tokens_y, input_tokens_x
                    coincidences = 0
                    for token in target:
                        if token in search: coincidences += 1
                    probability = coincidences / max(1, len(target))
                    if probability > maximum_probability: maximum_id, maximum_relationship_id, maximum_probability, maximum_index, old_prompt, maximum_forecast = id, relationship_id, probability, index, input_text_z, output_text
            result_dictionary = {'id': maximum_id, 'relationship_id': maximum_relationship_id, 'index': maximum_index, 'prompt': old_prompt, 'answer': maximum_forecast, 'probability': maximum_probability}
            self.__setID(user_id=self.user_id, last_id=maximum_id)
            return result_dictionary
        except Exception as error:
            if self.__show_errors: print('ERROR in __standardAdjustmentForecast: '+str(error))
            return {'id': 0, 'relationship_id': 0, 'index': 0, 'prompt': '', 'answer': '', 'probability': 0.0}
    def __outputAdaptedToInput(self, prompt='', original_input='', original_output=''):
        try:
            prompt, original_input, original_output = str(prompt).strip(), str(original_input).strip(), str(original_output).strip()
            prompt, original_input, original_output = rf'{prompt}', rf'{original_input}', rf'{original_output}'
            original_output = self.__SemanticComparisonNetwork().outputAdaptedToInput(Input=prompt, Output=original_output.replace('\t', '\\t'), hot=True, stream=False).replace('\\t', '\t')
            if len(original_input) < 1: return original_output
            def _filter(text=''): return self.__compile(r'[.?!;,¡¿]').sub('', text)
            prompt_x, original_input_x, original_output_x = _filter(text=prompt), _filter(text=original_input), _filter(text=original_output)
            prompt_tokens, original_input_tokens, original_output_tokens = prompt_x.split(), original_input_x.split(), original_output_x.split()
            intercambios, y, z = [], [y.lower() for y in original_output_tokens], [z.lower() for z in prompt_tokens]
            for index, original_input_token in enumerate(original_input_tokens):
                x = original_input_token.lower()
                try: previous = original_input_tokens[index-1]
                except: previous = ''
                if x in y and x not in z: intercambios.append((previous, original_input_token))
            for index, prompt_token in enumerate(prompt_tokens):
                for intercambio in intercambios:
                    _previous, _next = intercambio
                    if prompt_token.lower() == _previous.lower():
                        try: new = prompt_tokens[index+1]
                        except: new = _next
                        original_output = original_output.replace(_next, new)
            return original_output
        except Exception as error:
            if self.__show_errors: print('ERROR in __outputAdaptedToInput: '+str(error))
            return original_output
    def __truncateTokens(self, text='', max_tokens=1000000, encoder='gpt-4'):
        try:
            truncate_text = ''
            text = str(text).strip()
            max_tokens = int(max_tokens) if type(max_tokens) in (bool, int, float) else 1000000
            encoder = str(encoder).lower().strip()
            encoder = self.__updateEncoder(encoder=encoder)
            model_encoding = self.__encoding_for_model(encoder)
            token_list = model_encoding.encode(text)
            if len(token_list) <= max_tokens: return text
            token_list = token_list[:max_tokens]
            truncate_text = model_encoding.decode(token_list).strip()
            last_index = len(truncate_text)-1
            for separator in self.__separators:
                index = truncate_text.rfind(separator)
                if index not in (-1, 0, last_index): truncate_text = truncate_text[:index+1]
            return truncate_text.strip()
        except Exception as error:
            if self.__show_errors: print('ERROR in __truncateTokens: '+str(error))
            return text
    def __getStream(self, final_answer='', fit_probability=0.0, probability=0.0, interval=0.0):
        try:
            embeddings = self.__textForEmbedding(text=final_answer, length=None, encoder=self.__tokenizer)
            for embedding in embeddings:
                token = self.__embeddingForText(embedding=[embedding], encoder=self.__tokenizer, strip=False)
                yield {'answer': token, 'fit_probability': fit_probability, 'probability': probability}
                self.__sleep(interval)
        except Exception as error:
            if self.__show_errors: print('ERROR in __getStream: '+str(error))
            yield {'answer': '', 'fit_probability': fit_probability, 'probability': probability}
    def __predict(self, prompt='', max_tokens=None, min_fit_probability=0.7, min_probability=0.01, generalization=True, stream=False, interval=0.0):
        try:
            answer_dictionary = {'answer': '', 'fit_probability': 0.0, 'probability': 0.0}
            prompt, final_answer = str(prompt).strip(), ''
            max_tokens = int(max_tokens) if type(max_tokens) in (bool, int, float) else None
            min_fit_probability = float(min_fit_probability) if type(min_fit_probability) in (bool, int, float) else 0.7
            min_probability = min((1.0, max((0.0, float(min_probability))))) if type(min_probability) in (bool, int, float) else 0.01
            generalization = bool(generalization) if type(generalization) in (bool, int, float) else True
            stream = bool(stream) if type(stream) in (bool, int, float) else False
            interval = max((0.0, float(interval))) if type(interval) in (bool, int, float) else 0.0
            prompt, original_show_errors = rf'{prompt}', self.__show_errors
            self.__show_errors, probability, original_input, answer, adjusted, hurnet, fit_probability = False, 0.0, '', '', False, False, 0.0
            if self.__fine_tuning:
                standard_adjustment_forecast = self.__standardAdjustmentForecast(input_prompt=prompt, vector_matrix=self.__iterNumericVectors(model_path=self.__fit_model_path))
                probability, original_input, answer = standard_adjustment_forecast['probability'], standard_adjustment_forecast['prompt'], standard_adjustment_forecast['answer']
            normalized_prompt = self.__normalization(input_text=prompt)
            if probability >= min_fit_probability: final_answer, adjusted = answer, True
            elif self.__hurnet_architecture:
                model_path = self.__fit_model_path
                hurnet_path = self.__changeExtension(model_path=model_path, old_extension='scfit', new_extension='hurnet')
                input_layer = self.__textForEmbedding(text=normalized_prompt, length=self.__block_size, encoder=self.__tokenizer)
                output_vector = self.__hur_net.predict(input_layer=[input_layer], decimal_places=0)[0]
                probability = self.__similarityBetweenVectors(first_vector=input_layer, second_vector=output_vector)
                if probability >= min_fit_probability:
                    final_answer = self.__embeddingForText(embedding=output_vector, encoder=self.__tokenizer, strip=True)
                    adjusted, hurnet = True, len(final_answer.strip()) > 0
            block_size = None if not self.__parallel_prediction else self.__block_size
            fit_probability, question_removal, self.__show_errors = probability, False, original_show_errors
            if len(final_answer) < 1:
                if not self.__trained: return ''
                if not self.__loaded and len(self.__inputs) > 0 and len(self.__outputs) > 0:
                    vector_matrix, new_embedding = [], self.__textForEmbedding(text='\n', length=None, encoder=self.__tokenizer)
                    for _input, _output in zip(self.__inputs, self.__outputs): vector_matrix.append(_input+new_embedding+_output)
                    input_vector = self.__textForEmbedding(text=prompt, length=None, encoder=self.__tokenizer)
                    _, output_vector = self.__vectorComparison(input_vector=input_vector, vector_matrix=vector_matrix)
                else:
                    input_vector = self.__textForEmbedding(text=prompt, length=block_size, encoder=self.__tokenizer)
                    _, output_vector = self.__vectorComparison(input_vector=input_vector, vector_matrix=self.__iterNumericVectors())
                probability = self.__similarityBetweenVectors(first_vector=input_vector, second_vector=output_vector)
                if probability >= min_probability:
                    final_answer, list_of_answers = self.__embeddingForText(embedding=output_vector, encoder=self.__tokenizer, strip=True), []
                    if len(self.__candidates) > 0:
                        list_of_answers = [final_answer]
                        for candidate in self.__candidates: list_of_answers.append(self.__embeddingForText(embedding=candidate, encoder=self.__tokenizer, strip=True))
                        from random import shuffle
                        shuffle(list_of_answers)
                        final_answer = '\n\n'.join(list_of_answers)
                    final_answer, self.__candidates = final_answer.strip(), []
                if normalized_prompt in self.__normalization(input_text=final_answer): generalization = False
                if len(final_answer) > 0 and '?' in final_answer and prompt.endswith('?'):
                    question_and_answer = final_answer.split('?')
                    question, answer = question_and_answer[0].strip(), question_and_answer[-1].strip()
                    if len(question) > 0 and len(answer) > 0:
                        final_answer, question_removal = final_answer.replace(question, '').strip(), True
                        if final_answer.startswith('?'): final_answer = final_answer[1:].strip()
                final_answer_x = self.__extractResponse(prompt=prompt, text=final_answer) if not question_removal else final_answer
                if final_answer_x != final_answer: original_input = final_answer.replace(final_answer_x, '').strip()
            if adjusted and fit_probability > 0.7: generalization = False
            if not hurnet and (generalization and probability < 1.0): final_answer = self.__outputAdaptedToInput(prompt=prompt, original_input=original_input, original_output=final_answer)
            if not question_removal and not adjusted and len(final_answer) > 0: final_answer = self.__extractResponse(prompt=prompt, text=final_answer)
            if max_tokens is not None: final_answer = self.__truncateTokens(text=final_answer, max_tokens=max_tokens, encoder=self.__tokenizer)
            final_answer, self.fit_probability, self.probability = final_answer.strip(), fit_probability, probability
            answer_dictionary = {'answer': final_answer, 'fit_probability': fit_probability, 'probability': probability}
            if stream: return self.__getStream(final_answer=final_answer, fit_probability=fit_probability, probability=probability, interval=interval)
            else: return answer_dictionary
        except Exception as error:
            if self.__show_errors: print('ERROR in __predict: '+str(error))
            if stream == True: return self.__getStream(final_answer='', probability=0.0, interval=0.0)
            else: return {'answer': '', 'fit_probability': 0.0, 'probability': 0.0}
    def __getTrainingText(self, max_tokens=None):
        try:
            result_text = ''
            max_tokens, tokens_count = int(max_tokens) if type(max_tokens) in (bool, int, float) else None, 0
            if self.__exists(self.__temporary_path):
                for embedding in self.__iterNumericVectors():
                    text = self.__embeddingForText(embedding=embedding, encoder=self.__tokenizer, strip=True)
                    if '<|' in text or '|>' in text:
                        def _remove_between_markers(text=''): return self.__sub(r'<\|.*?\|>', '', text, flags=self.__DOTALL)
                        text = _remove_between_markers(text=text)
                    result_text += text.strip()+'\n\n'
                    tokens_count += self.countTokens(text=result_text, encoder=self.__tokenizer)
                    if max_tokens is not None and tokens_count >= max_tokens: return self.__textSummary(text=result_text, max_tokens=max_tokens, encoder=self.__tokenizer)
            if self.__exists(self.__fit_model_path):
                for embedding in self.__iterNumericVectors(model_path=self.__fit_model_path):
                    text = self.__embeddingForText(embedding=embedding, encoder=self.__tokenizer, strip=True)
                    pairs = text.strip().split('<|end|>')
                    question, answer = pairs[-2].strip(), pairs[-1].strip()
                    result_text += f'{question}\n{answer}\n\n'
                    tokens_count += self.__countTokens(text=result_text, encoder=self.__tokenizer)
                    if max_tokens is not None and tokens_count >= max_tokens: return self.__textSummary(text=result_text, max_tokens=max_tokens, encoder=self.__tokenizer)
            return result_text.strip()
        except Exception as error:
            if self.__show_errors: print('ERROR in __getTrainingText: '+str(error))
            return ''
    def __downloadFile(self, url_path='', file_path=''):
        try:
            url_path, file_path = str(url_path).strip(), str(file_path).strip()
            if len(url_path) < 1 or not url_path.lower().startswith(('http://', 'https://', 'www.')): return False
            from urllib.parse import urlparse
            response = self.__urlopen(url_path)
            original_file_name = self.__basename(urlparse(url_path).path)
            if not file_path: target_file_path = original_file_name
            else:
                candidate_name = self.__basename(file_path)
                if not candidate_name or file_path.endswith('/') or file_path.endswith('\\'): target_file_path = self.__join(file_path, original_file_name)
                else: target_file_path = file_path
            directory = self.__dirname(target_file_path)
            if directory: self.__makedirs(directory, exist_ok=True)
            if self.__isdir(target_file_path) and not target_file_path.endswith('/') and not target_file_path.endswith('\\'): target_file_path = file_path+'/'+original_file_name
            with open(target_file_path,'wb') as file_handle: file_handle.write(response.read())
            return self.__exists(target_file_path)
        except Exception as error:
            print('ERROR in __downloadFile: '+str(error))
            return False
    def __addHiddenLayer(self, num_neurons=0):
        try:
            self.__hidden_layers.append(num_neurons)
            return True
        except Exception as error:
            if self.__show_errors: print('ERROR in __addHiddenLayer: '+str(error))
            return False
    def __train(self, dataset_path='', string='', precision=1.0, tokenizer='gpt-4', context_window=float('inf'), end_tag='\n\n', validate=0.0, progress=True):
        try:
            training_metrics, infinite = {'val_loss': 0.0, 'loss': 1.0, 'generalization_rate': 0.0, 'precision': 0.0}, float('inf')
            dataset_path = str(dataset_path).strip()
            string = str(string).strip()
            precision = min((1.0, max((0.0, float(precision))))) if type(precision) in (bool, int, float) else 1.0
            tokenizer = str(tokenizer).lower().strip()
            context_window = max((1, float(context_window))) if type(context_window) in (bool, int, float) else infinite
            end_tag = str(end_tag)
            validate = min((1.0, max((0.0, float(validate))))) if type(validate) in (bool, int, float) else 0.0
            progress = bool(progress) if type(progress) in (bool, int, float) else True
            string = rf'{string}'
            self.__setTqdm(disable=not progress)
            progress_bar = self.__updateTqdm(total=7, description='Training model')
            if len(end_tag) < 1: end_tag = '\n\n'
            progress_bar.update(1)
            self.__string = str(self.__string).strip()
            progress_bar.update(1)
            if len(self.__string) > 0: self.__string = self.__string.replace('<|context|>', '\n').replace('<|end|>', end_tag).strip()
            progress_bar.update(1)
            string = str(self.__string+'\n\n'+string).strip()
            progress_bar.update(1)
            self.__temporary_path = self.__processDataset(dataset_path=dataset_path, string=string, precision=precision, tokenizer=tokenizer, context_window=context_window, end_tag=end_tag, progress=progress)
            if validate > 0 and self.__exists(self.__temporary_path):
                probabilities_x, probabilities_y = [], []
                total_bytes, bytes_count = self.__getsize(self.__temporary_path), 0
                if total_bytes > 0:
                    bytes_limit = int(total_bytes * validate)
                    progress_bar_val = self.__updateTqdm(total=bytes_limit, description='Validating model')
                    for token_generator in self.__iterNumericVectors(model_path=self.__temporary_path):
                        prompt = answer = input_output = self.__embeddingForText(embedding=token_generator, encoder=self.__tokenizer, strip=True)
                        for separator in self.__separators:
                            if separator in input_output:
                                chunks = input_output.strip().split(separator)
                                prompt = chunks[0].strip()+separator
                                chunks = chunks[1:]
                                answer = separator.join(chunks).strip()
                                break
                        input_vector = self.__textForEmbedding(text=prompt, length=self.__block_size, encoder=self.__tokenizer)
                        output_vector = self.__textForEmbedding(text=answer, length=self.__block_size, encoder=self.__tokenizer)
                        _, approximate_output = self.__vectorComparison(input_vector=input_vector, vector_matrix=self.__iterNumericVectors(model_path=self.__temporary_path))
                        approximate_text = self.__embeddingForText(embedding=approximate_output, encoder=self.__tokenizer, strip=True)
                        approximate_text = self.__extractResponse(prompt=prompt, text=approximate_text)
                        approximate_output = self.__textForEmbedding(text=approximate_text, length=self.__block_size, encoder=self.__tokenizer)
                        probability_x = self.__similarityBetweenVectors(first_vector=output_vector, second_vector=approximate_output)
                        probability_y = self.__euclideanSimilarity(first_vector=output_vector, second_vector=approximate_output)
                        probabilities_x.append(probability_x), probabilities_y.append(1.0-((probability_x+probability_y)/2))
                        token_generator_str = ' '.join(map(str, token_generator))+'\n'
                        current_bytes = len(token_generator_str.encode('utf-8'))
                        progress_bar_val.update(current_bytes)
                        bytes_count += current_bytes
                        if bytes_count >= bytes_limit:
                            progress_bar_val.n = bytes_limit
                            progress_bar_val.refresh()
                            break
                    progress_bar_val.close()
                    loss_probability = float(self.__mean(probabilities_x))
                    val_loss = float(self.__mean(probabilities_y))
                    loss = 1.0-loss_probability
                    generalization_rate = 1.0-val_loss
                    training_metrics['val_loss'] = val_loss
                    training_metrics['loss'] = loss
                    training_metrics['generalization_rate'] = generalization_rate
                    training_metrics['precision'] = loss_probability
            else: training_metrics = {'val_loss': 0.0, 'loss': 1.0-precision, 'generalization_rate': precision/2, 'precision': precision}
            progress_bar.update(1)
            self.__tokenizer = tokenizer
            progress_bar.update(1)
            self.__trained = True
            progress_bar.update(1)
            progress_bar.close()
            self.__setTqdm(disable=True)
            return training_metrics
        except Exception as error:
            if self.__show_errors: print('ERROR in __train: '+str(error))
            try:
                self.__setTqdm(disable=True)
                return training_metrics
            except: return {'val_loss': 1.0, 'loss': 1.0, 'generalization_rate': 0.0, 'precision': 0.0}
    def __saveModel(self, model_path='', progress=True):
        try:
            model_path = file_name = str(model_path).strip()
            progress = bool(progress) if type(progress) in (bool, int, float) else True
            self.__setTqdm(disable=not progress)
            progress_bar = self.__updateTqdm(total=5, description='Saving model')
            progress_bar.update(1)
            model_path = self.__changeExtension(model_path=model_path, old_extension='scnet', new_extension='sccon')
            if len(model_path) > 0:
                directory, file_name = self.__split(model_path)
                if not file_name: file_name = 'model.sccon'
                elif not file_name.endswith('.sccon'):
                    point_count, index = file_name.count('.'), file_name.find('.')
                    if point_count > 1: file_name = file_name[:file_name.rfind('.')]
                    elif point_count > 0 and index > 0: file_name = file_name[:index]
                    file_name += '.sccon'
            else: directory, file_name = str(model_path), 'model.sccon'
            progress_bar.update(1)
            if directory and not self.__exists(directory): self.__makedirs(directory)
            save_path = self.__join(directory, file_name)
            save_dict = {
                'tokenizer': str(self.__tokenizer).lower().strip(),
                'block_size': max((1, int(self.__block_size))) if type(self.__block_size) in (bool, int, float) else 50,
                'parameters_number': max((0, int(self.parameters_number))) if type(self.parameters_number) in (bool, int, float) else 0,
                'parallel_prediction': int(self.__parallel_prediction) if type(self.__parallel_prediction) in (bool, int, float) else 0,
                'minimum_probability_for_candidates': float(self.minimum_probability_for_candidates) if type(self.minimum_probability_for_candidates) in (bool, int, float) else 0.9,
                'model_state_dict': []

            }
            progress_bar.update(1)
            if len(self.__temporary_path.strip()) > 0 and not self.__add_hur:
                destination_path = self.__changeExtension(model_path=save_path, old_extension='sccon', new_extension='scnet')
                formatted_params = self.__format_numbers(data_number=self.parameters_number, is_tokens=False)
                self.__moveAndRenameStream(source_path=self.__temporary_path, destination_path=destination_path, formatted_params=formatted_params, progress=progress)
                self.__overwriteWithHexadecimal(file_path=destination_path)
            self.__save(save_dict, save_path)
            progress_bar.update(1)
            source, save_path = 'model.hurnet', self.__changeExtension(model_path=save_path, old_extension='sccon', new_extension='hurnet')
            if len(self.__inputs) > 0 and len(self.__outputs) > 0 and self.__exists(source): self.__move(source, save_path)
            self.__trained = True
            progress_bar.update(1)
            progress_bar.close()
            return True
        except Exception as error:
            if self.__show_errors: print('ERROR in __saveModel: '+str(error))
            self.__setTqdm(disable=True)
            return False
    def __loadModel(self, model_path='', progress=True):
        try:
            model_path = str(model_path).strip()
            progress = bool(progress) if type(progress) in (bool, int, float) else True
            self.__setTqdm(disable=not progress)
            progress_bar = self.__updateTqdm(total=7, description='Loading model')
            progress_bar.update(1)
            model_path = self.__changeExtension(model_path=model_path, old_extension='scnet', new_extension='sccon')
            if len(model_path) > 0:
                directory, file_name = self.__split(model_path)
                if not file_name: file_name = 'model.sccon'
                elif not file_name.endswith('.sccon'):
                    point_count, index = file_name.count('.'), file_name.find('.')
                    if point_count > 1: file_name = file_name[:file_name.rfind('.')]
                    elif point_count > 0 and index > 0: file_name = file_name[:index]
                    file_name += '.sccon'
            else:
                def _find_first_sccon_file(directory='.'):
                    directory_path = self.__Path(directory)
                    if not directory_path.is_dir(): return 'model.sccon'
                    sccon_file_list = sorted(file_path for file_path in directory_path.iterdir() if file_path.is_file() and file_path.suffix.lower() == '.sccon')
                    return sccon_file_list[0] if sccon_file_list else 'model.sccon'
                directory, file_name = '', _find_first_sccon_file()
            model_path = self.__join(directory, file_name)
            progress_bar.update(1)
            if not self.__exists(model_path):
                progress_bar.update(5)
                return False
            checkpoint = self.__load(model_path, map_location=self.__device)
            try: self.__tokenizer = str(checkpoint['tokenizer']).lower().strip()
            except: self.__tokenizer = 'gpt-4'
            try: self.__block_size = max((1, int(checkpoint['block_size'])))
            except: self.__block_size = 50
            try: self.parameters_number = max((0, int(checkpoint['parameters_number']))) if type(checkpoint['parameters_number']) in (bool, int, float) else 0
            except: self.parameters_number = 0
            try: parallel_prediction = bool(checkpoint['parallel_prediction']) if type(checkpoint['parallel_prediction']) in (bool, int, float) else False
            except: parallel_prediction = False
            if parallel_prediction: self.__parallel_prediction = parallel_prediction
            try: self.minimum_probability_for_candidates = float(checkpoint['minimum_probability_for_candidates']) if type(checkpoint['minimum_probability_for_candidates']) in (bool, int, float) else 0.9
            except: self.minimum_probability_for_candidates = 0.9
            progress_bar.update(1)
            model_path = self.__changeExtension(model_path=model_path, old_extension='sccon', new_extension='scnet')
            self.__restoreOriginalFromHexadecimal(file_path=model_path)
            progress_bar.update(1)
            self.__fit_model_path = self.__changeExtension(model_path=model_path, old_extension='scnet', new_extension='scfit')
            if self.__exists(self.__fit_model_path): self.__restoreOriginalFromHexadecimal(file_path=self.__fit_model_path)
            progress_bar.update(1)
            hurnet_path1 = self.__changeExtension(model_path=model_path, old_extension='scnet', new_extension='hurnet')
            hurnet_path2 = self.__join(directory, 'model.hurnet')
            if self.__exists(self.__fit_model_path): self.__fine_tuning = True
            if self.__exists(hurnet_path1) or self.__exists(hurnet_path2):
                hurnet_path = hurnet_path1 if self.__exists(hurnet_path1) else hurnet_path2
                self.__hur_net = self.__HurNet(architecture='multi_layer', fx=True)
                self.__hur_net.loadModel(model_path=hurnet_path)
                self.__hurnet_architecture = True
            progress_bar.update(1)
            self.__temporary_path, self.__model_path, self.__trained, self.__loaded = model_path, model_path, True, True
            progress_bar.update(1)
            progress_bar.close()
            return True
        except Exception as error:
            if self.__show_errors: print('ERROR in __loadModel: '+str(error))
            self.__setTqdm(disable=True)
            return False
    def __addFit(self, prompt='', answer='', id=0, relationship_id=0):
        try:
            prompt, answer = str(prompt).strip(), str(answer).strip()
            prompt, answer = rf'{prompt}', rf'{answer}'
            id = int(id) if type(id) in (bool, int, float) else 0
            relationship_id = int(relationship_id) if type(relationship_id) in (bool, int, float) else 0
            if self.__trained:
                if not self.__loaded: return self.__setInputsAndOutputs(prompt=prompt, answer=answer)
                if len(self.__hidden_layers) > 0 and (id <= 0 and relationship_id <= 0):
                    self.__setInputsAndOutputs(prompt=prompt, answer=answer)
                    self.__add_hur = True
                else:
                    if len(prompt) < 1 or len(answer) < 1: return False
                    input_output = str(id)+'<|end|>'+str(relationship_id)+'<|end|>'+prompt+'<|end|>'+answer
                    model_path = self.__fit_model_path
                    state, restore = 'a' if self.__exists(model_path) else 'w', True
                    if state == 'a' and self.__add_fit: restore = self.__restoreOriginalFromHexadecimal(file_path=model_path)
                    if restore:
                        write = False
                        with open(model_path, state, encoding='utf-8') as open_file:
                            embeddings = self.__textForEmbedding(text=input_output, length=None, encoder=self.__tokenizer)
                            open_file.write(' '.join(map(str, embeddings))+'\n')
                            write = True
                        if write: self.__overwriteWithHexadecimal(file_path=model_path)
                        self.__add_fit = True
            else: self.__string += prompt+'<|context|>'+answer+'<|end|>'
            return True
        except Exception as error:
            if self.__show_errors: print('ERROR in __addFit: '+str(error))
            return False
    def __fit(self, interaction=True, activation_function='linear', bias=0.0, learning_rate=1.0, stochastic_factor=False, progress=True):
        try:
            if len(self.__hidden_layers) <= 0: return False
            progress = bool(progress) if type(progress) in (bool, int, float) else True
            self.__setTqdm(disable=not progress)
            progress_bar = self.__updateTqdm(total=4, description='Fitting model')
            progress_bar.update(1)
            if not self.__trained and len(self.__string) > 0 and '<|end|>' in self.__string:
                inputs_outputs = self.__string.split('<|end|>')
                progress_bar_text = self.__updateTqdm(total=len(inputs_outputs), description='Converting data')
                x, y, main_x_y = [], [], 0
                for input_output in inputs_outputs:
                    if len(input_output.strip()) > 0 and '<|context|>' in input_output:
                        prompt, answer = input_output.split('<|context|>')
                        x.append(prompt), y.append(answer)
                        max_x_y = max((len(prompt.split()), len(answer.split())))
                        if max_x_y > main_x_y: main_x_y = max_x_y
                    progress_bar_text.update(1)
                    progress_bar_text.close()
                self.__block_size = main_x_y*2
                for a, b in zip(x, y): self.__setInputsAndOutputs(prompt=a, answer=b)
            progress_bar.update(1)
            if len(self.__inputs) < 1 or len(self.__outputs) < 1:
                progress_bar.update(2)
                return False
            hur_net = self.__HurNet(architecture='multi_layer', fx=True)
            for hidden_layer in self.__hidden_layers: hur_net.addHiddenLayer(num_neurons=hidden_layer)
            train_result = hur_net.train(input_layer=self.__inputs, output_layer=self.__outputs, interaction=interaction, activation_function=activation_function, bias=bias, learning_rate=learning_rate, stochastic_factor=stochastic_factor)
            progress_bar.update(1)
            if train_result:
                model_path = self.__fit_model_path
                model_path = self.__changeExtension(model_path=model_path, old_extension='scfit', new_extension='hurnet')
                progress_bar.update(1)
                progress_bar.close()
                return hur_net.saveModel(model_path=model_path)
            else:
                progress_bar.update(1)
                progress_bar.close()
                return False
        except Exception as error:
            if self.__show_errors: print('ERROR in __fit: '+str(error))
            self.__setTqdm(disable=True)
            return False
    def __print_predict(self, prompt='', max_tokens=None, min_fit_probability=0.7, min_probability=0.01, generalization=True, stream=False, interval=0.0):
        try:
            if stream == True:
                tokens_generator = self.__predict(prompt=prompt, max_tokens=max_tokens, min_fit_probability=min_fit_probability, min_probability=min_probability, generalization=generalization, stream=stream, interval=interval)
                for answer_dictionary in tokens_generator:
                    answer = answer_dictionary['answer']
                    print(answer, end='', flush=True)
                print()
            else: print(self.__predict(prompt=prompt, max_tokens=max_tokens, min_fit_probability=min_fit_probability, min_probability=min_probability, generalization=generalization, stream=stream, interval=interval)['answer'])
        except Exception as error:
            if self.__show_errors: print('ERROR in __print_predict: '+str(error))
    def loadJSON(self, file_path='', string_content='', key_name=''):
        try:
            key_name = str(key_name).strip()
            json_loaded = self.__loadJSON(file_path=file_path, string_content=string_content)
            return json_loaded[key_name] if len(key_name) > 0 else json_loaded
        except Exception as error:
            print('ERROR in loadJSON: '+str(error))
            return {}
    def normalization(self, input_text=''):
        try: return self.__normalization(input_text=input_text)
        except Exception as error:
            if self.__show_errors: print('ERROR in normalization: '+str(error))
            return input_text
    def textForEmbedding(self, text='', length=None, encoder='gpt-4'):
        try: return self.__textForEmbedding(text=text, length=length, encoder=encoder)
        except Exception as error:
            if self.__show_errors: print('ERROR in textForEmbedding: '+str(error))
            return []
    def embeddingForText(self, embedding=[], encoder='gpt-4', strip=True):
        try: return self.__embeddingForText(embedding=embedding, encoder=encoder, strip=strip)
        except Exception as error:
            if self.__show_errors: print('ERROR in embeddingForText: '+str(error))
            return ''
    def countTokens(self, text='', encoder='gpt-4'):
        try: return self.__countTokens(text=text, encoder=encoder)
        except Exception as error:
            if self.__show_errors: print('ERROR in countTokens: '+str(error))
            return len(str(text))
    def truncateTokens(self, text='', max_tokens=1000000, encoder='gpt-4'):
        try: return self.__truncateTokens(text=text, max_tokens=max_tokens, encoder=encoder)
        except Exception as error:
            if self.__show_errors: print('ERROR in truncateTokens: '+str(error))
            return text
    def textSummary(self, text='', max_tokens=1000000, encoder='gpt-4'):
        try: return self.__textSummary(text=text, max_tokens=max_tokens, encoder=encoder)
        except Exception as error:
            if self.__show_errors: print('ERROR in textSummary: '+str(error))
            return text
    def getTrainingText(self, max_tokens=None):
        try: return self.__getTrainingText(max_tokens=max_tokens)
        except Exception as error:
            if self.__show_errors: print('ERROR in getTrainingText: '+str(error))
            return ''
    def alternativeVectorComparison(self, input_vector=[], vector_matrix=[]):
        try: return self.__alternativeVectorComparison(input_vector=input_vector, vector_matrix=vector_matrix)
        except Exception as error:
            if self.__show_errors: print('ERROR in alternativeVectorComparison: '+str(error))
            return (-1, [])
    def vectorComparison(self, input_vector=[], vector_matrix=[], stream=True):
        try:
            stream = bool(stream) if type(stream) in (bool, int, float) else True
            def _matrix_loop():
                for vector in vector_matrix: yield vector
            return self.__vectorComparison(input_vector=input_vector, vector_matrix=_matrix_loop() if stream else vector_matrix)
        except Exception as error:
            if self.__show_errors: print('ERROR in vectorComparison: '+str(error))
            return (-1, [])
    def similarityBetweenVectors(self, first_vector=[], second_vector=[]):
        try: return self.__similarityBetweenVectors(first_vector=first_vector, second_vector=second_vector)
        except Exception as error:
            if self.__show_errors: print('ERROR in similarityBetweenVectors: '+str(error))
            return 0.0
    def euclideanSimilarity(self, first_vector=[], second_vector=[]):
        try: return self.__euclideanSimilarity(first_vector=first_vector, second_vector=second_vector)
        except Exception as error:
            if self.__show_errors: print('ERROR in euclideanSimilarity: '+str(error))
            return 0.0
    def overwriteWithHexadecimal(self, file_path=''):
        try: return self.__overwriteWithHexadecimal(file_path=file_path)
        except Exception as error:
            if self.__show_errors: print('ERROR in overwriteWithHexadecimal: '+str(error))
            return False
    def restoreOriginalFromHexadecimal(self, file_path=''):
        try: return self.__restoreOriginalFromHexadecimal(file_path=file_path)
        except Exception as error:
            if self.__show_errors: print('ERROR in restoreOriginalFromHexadecimal: '+str(error))
            return False
    def outputAdaptedToInput(self, prompt='', original_input='', original_output=''):
        try: return self.__outputAdaptedToInput(prompt=prompt, original_input=original_input, original_output=original_output)
        except Exception as error:
            if self.__show_errors: print('ERROR in outputAdaptedToInput: '+str(error))
            return original_output
    def downloadFile(self, url_path='', file_path=''):
        try: return self.__downloadFile(url_path=url_path, file_path=file_path)
        except Exception as error:
            if self.__show_errors: print('ERROR in downloadFile: '+str(error))
            return False        
    def addHiddenLayer(self, num_neurons=0):
        try: return self.__addHiddenLayer(num_neurons=num_neurons)
        except Exception as error:
            if self.__show_errors: print('ERROR in addHiddenLayer: '+str(error))
            return False
    def train(self, dataset_path='', string='', precision=1.0, tokenizer='gpt-4', context_window=float('inf'), end_tag='\n\n', validate=0.0, progress=True):
        try: return self.__train(dataset_path=dataset_path, string=string, precision=precision, tokenizer=tokenizer, context_window=context_window, end_tag=end_tag, validate=validate, progress=progress)
        except Exception as error:
            if self.__show_errors: print('ERROR in train: '+str(error))
            return {'val_loss': 1.0, 'loss': 1.0, 'generalization_rate': 0.0, 'precision': 0.0}
    def saveModel(self, model_path='', progress=True):
        try: return self.__saveModel(model_path=model_path, progress=progress)
        except Exception as error:
            if self.__show_errors: print('ERROR in saveModel: '+str(error))
            return False
    def loadModel(self, model_path='', progress=True):
        try: return self.__loadModel(model_path=model_path, progress=progress)
        except Exception as error:
            if self.__show_errors: print('ERROR in loadModel: '+str(error))
            return False
    def addFit(self, prompt='', answer='', id=0, relationship_id=0):
        try: return self.__addFit(prompt=prompt, answer=answer, id=id, relationship_id=relationship_id)
        except Exception as error:
            if self.__show_errors: print('ERROR in addFit: '+str(error))
            return False
    def fit(self, interaction=True, activation_function='linear', bias=0.0, learning_rate=1.0, stochastic_factor=False, progress=True):
        try: return self.__fit(interaction=interaction, activation_function=activation_function, bias=bias, learning_rate=learning_rate, stochastic_factor=stochastic_factor, progress=progress)
        except Exception as error:
            if self.__show_errors: print('ERROR in fit: '+str(error))
            return False
    def predict(self, prompt='', max_tokens=None, min_fit_probability=0.7, min_probability=0.01, generalization=True, stream=False, interval=0.0):
        try: return self.__predict(prompt=prompt, max_tokens=max_tokens, min_fit_probability=min_fit_probability, min_probability=min_probability, generalization=generalization, stream=stream, interval=interval)
        except Exception as error:
            if self.__show_errors: print('ERROR in predict: '+str(error))
            if stream == True: return self.__getStream(final_answer='', probability=0.0, interval=0.0)
            else: return {'answer': '', 'fit_probability': 0.0, 'probability': 0.0}
    def print_predict(self, prompt='', max_tokens=None, min_fit_probability=0.7, min_probability=0.01, generalization=True, stream=False, interval=0.0):
        try: self.__print_predict(prompt=prompt, max_tokens=max_tokens, min_fit_probability=min_fit_probability, min_probability=min_probability, generalization=generalization, stream=stream, interval=interval)
        except Exception as error:
            if self.__show_errors: print('ERROR in print_predict: '+str(error))
"""
This code was architected, developed, and programmed by Ben-Hur Varriano for Sapiens Technology®️ (as well as all other AI algorithms of the company),
and any unauthorized alteration, adaptation, and/or distribution, as well as public comments and/or postings regarding the operation and/or mathematics involved in the algorithm, are strictly prohibited.
Failure to comply with these rules may result in legal action against the author by our team of attorneys.

The module in question comprises a sophisticated mathematical algorithm operated by a set of advanced applied mathematics functions, equations,
and calculations that collaboratively develop large language models (LLMs) with a novel approach and a revolutionary concept.
It differentiates itself from other architectures due to its ease of construction and efficiency in model training and inference.
The parameterization, training, and inference processes are significantly faster and require computational resources several orders of magnitude lower than those used by conventional model architectures.
Furthermore, the architecture can be used to train instruction-based models, chat-based models, or a combination of both.
Its tensor processing via streaming enables an infinite context window, and its adaptive response calculations allow the model to generalize to inputs it was not explicitly trained on.

We named the network SCNet, an abbreviation of "Semantic Comparison Network", referring to the underlying algorithm (also authored by Ben-Hur Varriano) that originated the current code.
"""
# --------------------------> A SAPIENS TECHNOLOGY®️ PRODUCTION) <--------------------------
