from utility_pack.vector_storage_helper import ShardedLmdbStorage
import numpy as np, faiss, pickle, os, threading
from operator import gt, ge, lt, le, ne
from collections import defaultdict
import traceback, math, pymongo

class MiniVectorDB:
    def __init__(self, storage_file='db.pkl'):
        self.embedding_size = None
        self.storage_file = storage_file
        self.embeddings = None
        self.metadata = []  # Stores dictionaries of metadata
        self.id_map = {}  # Maps embedding row number to unique id
        self.inverse_id_map = {}  # Maps unique id to embedding row number
        self.inverted_index = defaultdict(set)  # Inverted index for metadata
        self.index = None
        self._embeddings_changed = False
        self.lock = threading.Lock()
        self._load_database()

    def _convert_ndarray_float32(self, ndarray):
        return np.array(ndarray, dtype=np.float32)

    def _convert_ndarray_float32_batch(self, ndarrays):
        return [np.array(arr, dtype=np.float32) for arr in ndarrays]

    def _load_database(self):
        if os.path.exists(self.storage_file):
            with self.lock:
                with open(self.storage_file, 'rb') as f:
                    data = pickle.load(f)
                    self.embeddings = data['embeddings']
                    self.embedding_size = data['embeddings'].shape[1] if data['embeddings'] is not None else None
                    self.metadata = data['metadata']
                    self.id_map = data['id_map']
                    self.inverse_id_map = data['inverse_id_map']
                    self.inverted_index = data.get('inverted_index', defaultdict(set))
                if self.embedding_size is not None:
                    self._build_index()

    def _build_index(self):
        self.index = faiss.IndexFlatIP(self.embedding_size)
        if self.embeddings.shape[0] > 0:
            faiss.normalize_L2(self.embeddings)  # Normalize for cosine similarity
            self.index.add(self.embeddings)
            self._embeddings_changed = False

    def get_vector(self, unique_id):
        with self.lock:
            if unique_id not in self.inverse_id_map:
                raise ValueError("Unique ID does not exist.")
            
            row_num = self.inverse_id_map[unique_id]
            return self.embeddings[row_num]

    def store_embedding(self, unique_id, embedding, metadata_dict={}):
        with self.lock:
            if unique_id in self.inverse_id_map:
                raise ValueError("Unique ID already exists.")

            embedding = self._convert_ndarray_float32(embedding)

            if self.embedding_size is None:
                self.embedding_size = embedding.shape[0]

            if self.embeddings is None:
                self.embeddings = np.zeros((0, self.embedding_size), dtype=np.float32)

            row_num = self.embeddings.shape[0]

            self.embeddings = np.vstack([self.embeddings, embedding])
            self.metadata.append(metadata_dict)
            self.id_map[row_num] = unique_id
            self.inverse_id_map[unique_id] = row_num

            # Update the inverted index
            for key, _ in metadata_dict.items():
                self.inverted_index[key].add(unique_id)

            self._embeddings_changed = True

    def store_embeddings_batch(self, unique_ids, embeddings, metadata_dicts=[]):
        with self.lock:
            for uid in unique_ids:
                if uid in self.inverse_id_map:
                    raise ValueError("Unique ID already exists.")
            
            # Convert all embeddings to float32
            embeddings = self._convert_ndarray_float32_batch(embeddings)

            if self.embedding_size is None:
                self.embedding_size = embeddings[0].shape[0]
            
            if self.embeddings is None:
                self.embeddings = np.zeros((0, self.embedding_size), dtype=np.float32)
            
            if len(metadata_dicts) < len(unique_ids) and len(metadata_dicts) > 0:
                raise ValueError("Metadata dictionaries must be provided for all unique IDs.")

            if metadata_dicts == []:
                metadata_dicts = [{} for _ in range(len(unique_ids))]

            row_nums = list(range(self.embeddings.shape[0], self.embeddings.shape[0] + len(embeddings)))
            
            # Stack the embeddings with a single operation
            self.embeddings = np.vstack([self.embeddings, embeddings])
            self.metadata.extend(metadata_dicts)
            self.id_map.update({row_num: unique_id for row_num, unique_id in zip(row_nums, unique_ids)})
            self.inverse_id_map.update({unique_id: row_num for row_num, unique_id in zip(row_nums, unique_ids)})

            # Update the inverted index
            for i, metadata_dict in enumerate(metadata_dicts):
                for key, _ in metadata_dict.items():
                    self.inverted_index[key].add(unique_ids[i])

            self._embeddings_changed = True

    def delete_embedding(self, unique_id):
        if unique_id not in self.inverse_id_map:
            raise ValueError("Unique ID does not exist.")

        with self.lock:
            row_num = self.inverse_id_map[unique_id]
            # Delete the embedding and metadata
            self.embeddings = np.delete(self.embeddings, row_num, 0)
            metadata_to_delete = self.metadata.pop(row_num)

            # Update the inverted index
            for key, _ in metadata_to_delete.items():
                self.inverted_index[key].discard(unique_id)
                if not self.inverted_index[key]:  # If the set is empty, remove the key
                    del self.inverted_index[key]

            # Delete from inverse_id_map
            del self.inverse_id_map[unique_id]

            # Re-index id_map and inverse_id_map
            new_id_map = {}
            new_inverse_id_map = {}

            current_index = 0
            for old_index in sorted(self.id_map.keys()):
                uid = self.id_map[old_index]
                if uid == unique_id:
                    continue  # Skip the deleted unique_id
                new_id_map[current_index] = uid
                new_inverse_id_map[uid] = current_index
                current_index += 1

            self.id_map = new_id_map
            self.inverse_id_map = new_inverse_id_map

            # Since we've modified the embeddings, we must rebuild the index before the next search
            self._embeddings_changed = True

    def _apply_or_filter(self, or_filters):
        result_indices = set()
        for filter in or_filters:
            key_indices = set()
            for key, value in filter.items():
                # Check if the value is a dictionary containing operators
                if isinstance(value, dict):
                    op = next(iter(value))  # Get the operator
                    op_value = value[op]  # Get the value for the operator
                    op_func = {
                        "$gt": gt,
                        "$gte": ge,
                        "$lt": lt,
                        "$lte": le,
                        "$ne": ne,
                        "$in": lambda x, y: y in x,
                    }.get(op, None)
                    if op_func is None:
                        raise ValueError(f"Invalid operator: {op}")

                    try:
                        # Create a copy of the set for iteration
                        inverted_index_copy = self.inverted_index.get(key, set()).copy()

                        key_indices_update = set()

                        # Iterate over each user ID in the inverted index copy
                        for uid in inverted_index_copy:
                            # Get the corresponding index for the user ID from the inverse_id_map
                            if uid not in self.inverse_id_map:
                                continue

                            inverse_id = self.inverse_id_map[uid]

                            metadata = self.metadata[inverse_id]

                            # Get the value for the key from the metadata, if it doesn't exist, return None
                            metadata_value = metadata.get(key, None)

                            # Check if the operation function returns True when applied to the metadata value and the operation value
                            if op_func(metadata_value, op_value):
                                # If it does, add the index to the key_indices_update set
                                key_indices_update.add(inverse_id)

                        # Update the key_indices set with the key_indices_update set
                        key_indices.update(key_indices_update)
                    except KeyError:
                        continue
                else:
                    try:
                        # Create a copy of the set for iteration
                        inverted_index_copy = self.inverted_index.get(key, set()).copy()

                        key_indices_update = set()

                        # Iterate over each user ID in the inverted index copy
                        for uid in inverted_index_copy:
                            # Get the corresponding index for the user ID from the inverse_id_map
                            if uid not in self.inverse_id_map:
                                continue

                            inverse_id = self.inverse_id_map[uid]

                            metadata = self.metadata[inverse_id]

                            # Get the value for the key from the metadata, if it doesn't exist, return None
                            metadata_value = metadata.get(key, None)

                            # Check if the metadata value matches the given value
                            if metadata_value == value:
                                # If it does, add the index to the key_indices_update set
                                key_indices_update.add(inverse_id)

                        # Update the key_indices set with the key_indices_update set
                        key_indices.update(key_indices_update)
                    except KeyError:
                        continue
            result_indices |= key_indices

        return result_indices

    def _apply_and_filter(self, and_filters, filtered_indices):
        for metadata_filter in and_filters:
            for key, value in metadata_filter.items():
                # Check if the value is a dictionary containing operators
                if isinstance(value, dict):
                    op = next(iter(value))  # Get the operator
                    op_value = value[op]  # Get the value for the operator
                    op_func = {
                        "$gt": gt,
                        "$gte": ge,
                        "$lt": lt,
                        "$lte": le,
                        "$ne": ne,
                        "$in": lambda x, y: y in x,
                    }.get(op, None)
                    if op_func is None:
                        raise ValueError(f"Invalid operator: {op}")

                    try:
                        indices = set()

                        # Get the set of user IDs from the inverted index for the given key. If the key is not present, return an empty set.
                        uids = self.inverted_index.get(key, set())

                        # Iterate over each user ID in the set
                        for uid in uids:
                            # Get the corresponding index for the user ID from the inverse_id_map
                            if uid not in self.inverse_id_map:
                                continue

                            inverse_id = self.inverse_id_map[uid]

                            metadata = self.metadata[inverse_id]

                            # Get the value for the key from the metadata, if it doesn't exist, return None
                            metadata_value = metadata.get(key, None)

                            # Check if the operation function returns True when applied to the metadata value and the operation value
                            if op_func(metadata_value, op_value):
                                # If it does, add the index to the indices set
                                indices.add(inverse_id)
                    except KeyError:
                        indices = set()
                else:
                    try:
                        indices = set()

                        # Get the set of user IDs from the inverted index for the given key. If the key is not present, return an empty set.
                        uids = self.inverted_index.get(key, set())

                        # Iterate over each user ID in the set
                        for uid in uids:

                            # Get the corresponding index for the user ID from the inverse_id_map
                            if uid not in self.inverse_id_map:
                                continue

                            inverse_id = self.inverse_id_map[uid]

                            metadata = self.metadata[inverse_id]

                            # Check if the key exists in the metadata and if its value matches the given value
                            if metadata.get(key, None) == value:
                                # If it does, add the index to the indices set
                                indices.add(inverse_id)

                    except KeyError:
                        indices = set()

                if filtered_indices is None:
                    filtered_indices = indices
                else:
                    # Create a copy of filtered_indices for iteration
                    for index in filtered_indices.copy():
                        if index not in indices:
                            filtered_indices.remove(index)

                if not filtered_indices:
                    break
        
        return filtered_indices
    
    def _apply_exclude_filter(self, exclude_filter, filtered_indices):
        for exclude in exclude_filter:
            for key, value in exclude.items():
                try:
                    # Create a copy of the set for iteration
                    inverted_index_copy = self.inverted_index.get(key, set()).copy()

                    exclude_indices = set()

                    # Iterate over each user ID in the inverted index copy
                    for uid in inverted_index_copy:
                        # Get the corresponding index for the user ID from the inverse_id_map
                        if uid not in self.inverse_id_map:
                            continue

                        inverse_id = self.inverse_id_map[uid]

                        metadata = self.metadata[inverse_id]

                        # Get the value for the key from the metadata, if it doesn't exist, return None
                        metadata_value = metadata.get(key, None)

                        # Check if the metadata value matches the given value
                        if metadata_value == value:
                            # If it does, add the index to the exclude_indices set
                            exclude_indices.add(inverse_id)
                except KeyError:
                    exclude_indices = set()
                filtered_indices -= exclude_indices
                if not filtered_indices:
                    break

        return filtered_indices

    def _get_filtered_indices(self, metadata_filters, exclude_filter, or_filters):
        # Initialize filtered_indices with all indices if metadata_filters is not provided
        filtered_indices = set(self.inverse_id_map.values()) if not metadata_filters else None

        # Check if metadata_filters is a dict, if so, convert to list of dicts
        if isinstance(metadata_filters, dict):
            metadata_filters = [metadata_filters]

        # Apply metadata_filters (AND)
        if metadata_filters:
            filtered_indices = self._apply_and_filter(metadata_filters, filtered_indices)

        # Apply OR filters
        if or_filters:
            # Remove all empty dictionaries from or_filters
            if isinstance(or_filters, dict):
                or_filters = [or_filters]
            or_filters = [or_filter for or_filter in or_filters if or_filter]
            if or_filters:
                temp_indices = self._apply_or_filter(or_filters)
                if filtered_indices is None:
                    filtered_indices = temp_indices
                else:
                    filtered_indices &= temp_indices

        # Apply exclude_filter
        if exclude_filter:
            # Check if exclude_filter is a dict, if so, convert to list of dicts
            if isinstance(exclude_filter, dict):
                exclude_filter = [exclude_filter]
            filtered_indices = self._apply_exclude_filter(exclude_filter, filtered_indices)

        return filtered_indices if filtered_indices is not None else set()

    def find_most_similar(self, embedding, metadata_filter=None, exclude_filter=None, or_filters=None, k=5, autocut=False):
        """ or_filters could be a list of dictionaries, where each dictionary contains key-value pairs for OR filters.
        or it could be a single dictionary, which will be equivalent to a list with a single dictionary."""

        if self.embeddings is None:
            return [], [], []

        embedding = self._convert_ndarray_float32(embedding)
        embedding = np.array([embedding])
        faiss.normalize_L2(embedding)

        if self._embeddings_changed:
            with self.lock:
                self._build_index()
        
        with self.lock:
            filtered_indices = self._get_filtered_indices(metadata_filter, exclude_filter, or_filters)

        # If no filtered indices, return empty results
        if not filtered_indices:
            return [], [], []

        # Determine the maximum number of possible matches
        max_possible_matches = min(k, len(filtered_indices))

        found_results = []
        search_k = max_possible_matches

        # Check if filtered_indices corresponds to all possible matches
        if len(filtered_indices) == self.embeddings.shape[0]:
            # Simply perform the search
            distances, indices = self.index.search(embedding, search_k)

            for idx, dist in zip(indices[0], distances[0]):
                if idx == -1:
                    continue  # Skip processing for non-existent indices

                if idx in self.id_map:
                    try:
                        found_results.append((self.id_map[idx], dist, self.metadata[idx]))
                    except KeyError:
                        pass
        else:
            # Otherwise, we create a new index with only the filtered indices
            filtered_embeddings = self.embeddings[list(filtered_indices)]
            filtered_index = faiss.IndexFlatIP(self.embedding_size)
            filtered_index.add(filtered_embeddings)

            distances, indices = filtered_index.search(embedding, search_k)

            for idx, dist in zip(indices[0], distances[0]):
                if idx == -1:
                    continue  # Skip processing for non-existent indices

                try:
                    found_results.append((self.id_map[list(filtered_indices)[idx]], dist, self.metadata[list(filtered_indices)[idx]]))
                except KeyError:
                    pass

        # Unzip the results into separate lists
        ids, distances, metadatas = zip(*found_results) if found_results else ([], [], [])

        return ids, distances, metadatas

    def persist_to_disk(self):
        with self.lock:
            with open(self.storage_file, 'wb') as f:
                data = {
                    'embeddings': self.embeddings,
                    'metadata': self.metadata,
                    'id_map': self.id_map,
                    'inverse_id_map': self.inverse_id_map,
                    'inverted_index': self.inverted_index
                }
                pickle.dump(data, f)

class VectorDB:
    def __init__(self, mongo_uri: str, mongo_database: str, mongo_collection: str, vector_storage: ShardedLmdbStorage, text_storage: ShardedLmdbStorage):
        self.mongo_uri = mongo_uri
        self.mongo_database = mongo_database
        self.mongo_collection = mongo_collection
        self.mongo_reference = pymongo.MongoClient(self.mongo_uri)[self.mongo_database][self.mongo_collection]
        self.vector_storage = vector_storage
        self.text_storage = text_storage

    def check_counts(self):
        print(f"Semantic storage count: {self.vector_storage.get_data_count()}")
        print(f"Text storage count: {self.text_storage.get_data_count()}")
        print(f"MongoDB count: {self.mongo_reference.count_documents({})}")
    
    def get_total_count(self):
        return self.text_storage.get_data_count()

    def ensure_embeddings_typing(self, embeddings):
        # Ensure embeddings is a numpy array
        if type(embeddings) is not np.ndarray:
            # Convert embeddings to numpy array 32-bit float
            embeddings = np.array(embeddings, dtype=np.float32)
        return embeddings

    def store_embeddings_batch(self, unique_ids: list, embeddings, metadata_dicts=[], text_field=None):
        payload = []

        embeddings = self.ensure_embeddings_typing(embeddings)

        if len(metadata_dicts) < len(unique_ids):
            metadata_dicts.extend([{} for _ in range(len(unique_ids) - len(metadata_dicts))])
        
        if text_field is not None:
            texts = [ m.pop(text_field, '') for m in metadata_dicts ]
        else:
            texts = [ '' for _ in range(len(unique_ids)) ]

        for uid, metadata_dict in zip(unique_ids, metadata_dicts):
            payload.append({**{ '_id': uid }, **metadata_dict})

        self.vector_storage.store_vectors(embeddings, unique_ids)
        self.text_storage.store_data(texts, unique_ids)
        self.mongo_reference.insert_many(payload)
    
    def delete_embeddings_batch(self, unique_ids):
        self.mongo_reference.delete_many({'_id': {'$in': unique_ids}})
        self.vector_storage.delete_data(unique_ids)
        self.text_storage.delete_data(unique_ids)
    
    def delete_embeddings_by_metadata(self, metadata_filters):
        identifiers = list(self.mongo_reference.find(metadata_filters, {'_id': 1}))
        self.mongo_reference.delete_many(metadata_filters)
        self.vector_storage.delete_data([i['_id'] for i in identifiers])
        self.text_storage.delete_data([i['_id'] for i in identifiers])
    
    def get_vector_by_metadata(self, metadata_filters):
        try:
            first_result = self.mongo_reference.find_one({**metadata_filters})
            if first_result is None:
                return None
            return self.vector_storage.get_vectors([first_result['_id']])[0]
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
        return None

    def search_faiss(self, query_embeddings, corpus_embeddings, top_k):
        faiss.normalize_L2(corpus_embeddings)
        faiss.normalize_L2(query_embeddings)
        
        index = faiss.IndexFlatL2(corpus_embeddings.shape[1])
    
        index.add(corpus_embeddings)
    
        distances, indices = index.search(query_embeddings, top_k)
    
        results = []
        
        # Zip the indices and distances together
        for idx, dist in zip(indices[0], distances[0]):
            if idx == -1:
                continue
    
            results.append({
                "corpus_id": idx,
                "score": dist
            })
        
        return results

    def find_most_similar(self, embedding, filters={}, output_fields=[], k=5, use_find_one=False):
        """
        Main entry point to find the most similar documents based on the given embedding.
        """
        try:
            # Step 1: Get documents from MongoDB
            results = self._fetch_mongo_documents(filters, output_fields, use_find_one)
            if not results:
                return [], [], []
        
            # Step 2: Prepare embeddings
            vector_ids, vectors, query_embedding, = self._prepare_embeddings(results, embedding)

            if not vector_ids:
                return [], [], []
            
            # Create a vector_id to index mapping
            vector_id_to_index = { idx: i for idx, i in enumerate(vector_ids) }
            # Step 3: Perform similarity search
            semantic_results = self.search_faiss(
                query_embeddings = query_embedding, 
                corpus_embeddings = vectors,
                top_k = k
            )
            ids = [ r['corpus_id'] for r in semantic_results if r['corpus_id'] != -1 ]
            scores =  [ r['score'] for r in semantic_results if r['corpus_id'] != -1 ]
            translated_ids = [ vector_id_to_index[i] for i in ids ]

            db_ids = translated_ids
            scores = scores

            # Iterate db_ids and scores together. If a duplicate db_id is found, remove it and its score
            seen_ids = set()
            
            # Iterate from inverse order to prevent errors on removal during iteration
            for i in range(len(db_ids) - 1, -1, -1):
                if db_ids[i] in seen_ids:
                    db_ids.pop(i)
                    scores.pop(i)
                else:
                    seen_ids.add(db_ids[i])

            # Step 4: Prepare final results
            return self._prepare_final_results(db_ids, scores, results)

        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            return [], [], []

    def find_most_similar_in_batches(self, embedding, filters={}, output_fields=[], k=5, use_find_one=False, max_ram_usage_gb=2):
        """
        Main entry point to find the most similar documents based on the given embedding.
        This function performs the search in batches if the estimated memory usage exceeds the specified limit.
        """
        try:
            # Estimate the total number of documents
            total_count = self.mongo_reference.count_documents(filters) if filters else self.mongo_reference.estimated_document_count()

            # Estimate the average document size in bytes
            avg_doc_size = 1024 * 300 # assuming an average document size of 300 KB

            # Estimate the total memory required for the documents
            doc_memory_usage = total_count * avg_doc_size

            # Estimate the memory required for the semantic vectors
            embedding_fixed_typing = self.ensure_embeddings_typing(embedding)
            vector_dim = embedding_fixed_typing.shape[0]
            vector_memory_usage = total_count * vector_dim * 4  # 4 bytes per float

            # Calculate the total estimated memory usage in GB
            total_memory_usage_gb = (doc_memory_usage + vector_memory_usage) / (1024 ** 3)

            # Check if the estimated memory usage exceeds the specified limit
            if total_memory_usage_gb > max_ram_usage_gb:

                # Perform the search in batches
                batch_size = math.ceil(total_count / (max_ram_usage_gb / (avg_doc_size + vector_dim * 4) / (1024 ** 3)))

                if batch_size < 1:
                    batch_size = 1
                
                if batch_size > 500000:
                    batch_size = 500000

                final_db_ids = []
                final_scores = []
                final_mongo_results = []

                for i in range(0, total_count, batch_size):
                    skip = i
                    limit = batch_size

                    batch_results = self._fetch_mongo_documents(filters, output_fields, use_find_one, limit, skip)

                    # Process the batch
                    if batch_results:
                        vector_ids, vectors, query_embedding = self._prepare_embeddings(batch_results, embedding)

                        # Create a vector_id to index mapping
                        vector_id_to_index = { idx: i for idx, i in enumerate(vector_ids) }

                        results = self.search_faiss(query_embedding, vectors, k)

                        ids = [ r['corpus_id'] for r in results if r['corpus_id'] != -1 ]
                        scores =  [ r['score'] for r in results if r['corpus_id'] != -1 ]
                        translated_ids = [ vector_id_to_index[i] for i in ids ]

                        db_ids = translated_ids
                        scores = scores

                        # Iterate db_ids and scores together. If a duplicate db_id is found, remove it and its score
                        seen_ids = set()
                        
                        # Iterate from inverse order to prevent errors on removal during iteration
                        for i in range(len(db_ids) - 1, -1, -1):
                            if db_ids[i] in seen_ids:
                                db_ids.pop(i)
                                scores.pop(i)
                            else:
                                seen_ids.add(db_ids[i])

                        # Consolidate the results
                        final_db_ids.extend(db_ids)
                        final_scores.extend(scores)
                        final_mongo_results.extend(batch_results)

                # Zip together ids and scores, sort by score desc
                final_db_ids, final_scores = zip(*sorted(zip(final_db_ids, final_scores), key=lambda x: x[1], reverse=False))

                # Cut off to k
                final_db_ids = final_db_ids[:k]
                final_scores = final_scores[:k]

                # Prepare final results
                return self._prepare_final_results(final_db_ids, final_scores, final_mongo_results)

            else:
                # Perform the search without batching
                return self.find_most_similar(embedding, filters, output_fields, k, use_find_one)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            return [], [], []

    def _fetch_mongo_documents(self, filters, output_fields, use_find_one, limit=None, skip=None):
        """Handle MongoDB document retrieval"""
        if output_fields == 'all':
            projection = {}
        else:
            output_fields = list(set(output_fields)) + ['_id', 'index']
            projection = {field: 1 for field in output_fields}

        if use_find_one:
            doc = self.mongo_reference.find_one(filters, projection)
            return [doc] if doc else []
        
        cursor = self.mongo_reference.find(filters, projection)
        if limit is not None:
            cursor = cursor.limit(limit)
        if skip is not None:
            cursor = cursor.skip(skip)
        result = list(cursor)
        return result

    def _prepare_embeddings(self, results, query_embedding):
        """Prepare embeddings for similarity search"""
        vector_ids = [r['_id'] for r in results]

        retrieved_vectors = self.vector_storage.get_vectors(vector_ids)
        # Some vectors could be None, zip together with vector_ids and remove the indices on both lists where the value is None
        zipped_vectors = zip(vector_ids, retrieved_vectors)
        filtered_vectors = [v for v in zipped_vectors if v[1] is not None]
        if not filtered_vectors:
            return [], [], []
        vector_ids, retrieved_vectors = zip(*filtered_vectors)

        lmdb_vectors = np.array(retrieved_vectors, dtype=np.float32)
        query_embedding = np.array([query_embedding], dtype=np.float32)
        
        return vector_ids, lmdb_vectors, query_embedding

    def _prepare_final_results(self, db_ids, scores, mongo_results):
        """Prepare the final results with texts and metadata"""
        texts = self.text_storage.get_data(db_ids)
        id_mapped_results = {r['_id']: r for r in mongo_results}
        
        metadatas = [
            id_mapped_results[db_id] if db_id in id_mapped_results else {}
            for db_id in db_ids
        ]

        for metadata, text in zip(metadatas, texts):
            metadata['text'] = text

        return db_ids, list(scores), metadatas
