import MetaRagTool.Constants as Constants
import pandas as pd
from datasets import load_from_disk,load_dataset





def loadWikiFaQa(sample_size=-1, multi_hop = False,
                 random_seed=50, multi_hop_hardness_factor=0,custom_path=None,qa_sample_size=-1):

    if Constants.local_mode:
        path = 'D:\Library\MSc Ai\Thesis\Persian RAG\Datasets\synthetic data\\final\WikiFaQA'
        if multi_hop:
            path = f'D:\Library\MSc Ai\Thesis\Persian RAG\Datasets\synthetic data\\final\WikiFaQA_multiHop'

        existing_dataset = load_from_disk(path)
    else:
        path = 'codersan/WikiFaQA'
        if multi_hop:
            path = 'codersan/WikiFaQA_multiHop'
        if custom_path is not None:
            path = custom_path

        dataset_dict = load_dataset(path)
        existing_dataset = dataset_dict["train"]




    if sample_size != -1 and sample_size < len(existing_dataset):
        existing_dataset = existing_dataset.shuffle(seed=random_seed)
        existing_dataset = existing_dataset.select(range(sample_size))

    contexts = existing_dataset['context']
    exactPairs = existing_dataset['exactPairs']

    qa_data = []
    for pair_list in exactPairs:
        for pair in pair_list:
            if multi_hop:
                qa_data.append({
                    'question': pair['question'],
                    'answer1': pair['answer1'],
                    'answer2': pair['answer2'],
                    'distance': pair['distance'],
                })
            else:
                qa_data.append({
                    'question': pair['question'],
                    'answer': pair['answer']
                })

    qa = pd.DataFrame(qa_data)
    if multi_hop_hardness_factor==1:
        # top half of qa
        qa = qa[qa['distance'] >1077]


    elif multi_hop_hardness_factor==2:
        # top quarter of qa
        qa = qa[qa['distance'] > 4963]

    if qa_sample_size != -1 and qa_sample_size < len(qa):
        qa = qa.sample(qa_sample_size, random_state=random_seed)


    return contexts, qa





def loadFarSick(relatedness_score_threshold=4.5, sample_size=-1):
    file_path = 'D:\Library\MSc Ai\Thesis\Persian RAG\Datasets\FarSick.txt'
    data = pd.read_csv(file_path, sep='\t')
    data = data.drop_duplicates()
    data = data[data['relatedness_score'] >= relatedness_score_threshold]

    if sample_size != -1 and sample_size < len(data):
        data = data.sample(sample_size)

    allSentences = pd.concat([data['sentence_A'], data['sentence_B']], ignore_index=True)
    allSentences = allSentences.drop_duplicates()

    sentencePairs = data[['sentence_A', 'sentence_B']]

    print("dataset loaded successfully")

    return allSentences, sentencePairs


def loadPersianQa():
    file_path = 'D:\Library\MSc Ai\Thesis\Persian RAG\Datasets\persian_qa_cleaned.csv'
    data = pd.read_csv(file_path)
    data = data.drop_duplicates()
    data = data[['question', 'context', 'answers_raw']]

    print("dataset loaded successfully")

    return data
