import math
import re

class Bayes_Classifier:

    def __init__(self):
        self.prior_positive = 0
        self.prior_negative = 0
        self.words_all = set()
        self.bigrams_all = set()
        self.words_and_count_positive = {}
        self.words_and_count_negative = {}
        self.bigrams_and_count_positive = {}
        self.bigrams_and_count_negative = {}
        self.log_probability_positive = {}
        self.log_probability_negative = {}
        self.bigrams_log_probability_positive = {}
        self.bigrams_log_probability_negative = {}

    def train(self, lines):
        # separate to positive and negative reviews
        review_positive, review_negative = self.get_line(lines)

        # clean reviews words
        cleaned_positive = self.clean(review_positive)
        cleaned_negative = self.clean(review_negative)

        # total words in each class
        total_words_positive = 0
        total_words_negative = 0
        # total bigrams in each class
        total_bigrams_positive = 0
        total_bigrams_negative = 0

        # total unique words in each class
        total_unique_words_positive = 0
        total_unique_words_negative = 0
        # total unique bigrams in each class
        total_unique_bigrams_positive = 0
        total_unique_bigrams_negative = 0

        # count frequency of every word in positive review and add into word:count dict
        for line in cleaned_positive:
            words = line.split(' ')
            for word in words:
                if word not in self.words_all:
                    self.words_and_count_positive[word] = 1
                    self.words_and_count_negative[word] = 0
                    self.words_all.add(word)
                else:
                    self.words_and_count_positive[word] += 1
                total_words_positive += 1

        # count frequency of every bigram in positive review and add into bigram:count dict
        for line in cleaned_positive:
            words = line.split(' ')
            for i in range(1, len(words)):
                if words[i] > words[i - 1]:
                    bigram = words[i - 1] + " " + words[i]
                else:
                    bigram = words[i] + " " + words[i -1]
                if bigram not in self.bigrams_all:
                    self.bigrams_and_count_positive[bigram] = 1
                    self.bigrams_and_count_negative[bigram] = 0
                    self.bigrams_all.add(bigram)
                else:
                    self.bigrams_and_count_positive[bigram] += 1
                total_bigrams_positive += 1

        # count frequency of every word in negative review and add into word:count dict
        for line in cleaned_negative:
            words = line.split(' ')
            for word in words:
                if word not in self.words_all:
                    self.words_and_count_negative[word] = 1
                    self.words_and_count_positive[word] = 0
                    self.words_all.add(word)
                else:
                    self.words_and_count_negative[word] += 1
                total_words_negative += 1

        # count frequency of every bigram in negative review and add into bigram:count dict
        for line in cleaned_negative:
            words = line.split(' ')
            for i in range(1, len(words)):
                if words[i] > words[i - 1]:
                    bigram = words[i - 1] + " " + words[i]
                else:
                    bigram = words[i] + " " + words[i - 1]
                if bigram not in self.bigrams_all:
                    self.bigrams_and_count_negative[bigram] = 1
                    self.bigrams_and_count_positive[bigram] = 0
                    self.bigrams_all.add(bigram)
                else:
                    self.bigrams_and_count_negative[bigram] += 1
                total_bigrams_negative += 1

        # calculate total unique words for each class
        for word, count in self.words_and_count_positive.items():
            if count > 0:
                total_unique_words_positive += 1
        for word, count in self.words_and_count_negative.items():
            if count > 0:
                total_unique_words_negative += 1

        # calculate total unique bigrams for each class
        for word, count in self.bigrams_and_count_positive.items():
            if count > 0:
                total_unique_bigrams_positive += 1
        for word, count in self.bigrams_and_count_negative.items():
            if count > 0:
                total_unique_bigrams_negative += 1

        # smoothing factor
        # After testing with 0.01, 0.1, 0.5, 1, found out 0.1 generated the highest F score
        smoothing_factor = 0.1

        # calculate priors
        total_review = len(review_positive) + len(review_negative)
        self.prior_positive = math.log10(len(review_positive) / total_review)
        self.prior_negative = math.log10(len(review_negative) / total_review)

        # calculate log probabilities for all words
        # add smoothing factor to smooth the value for word count, to ensures that we don't multiply by 0 if the word doesn't exists
        # add total unique words multiply smoothing factor to smooth the denominator
        for word in self.words_and_count_positive:
            self.log_probability_positive.update({word: math.log10((self.words_and_count_positive[word] + smoothing_factor) / (total_words_positive + (total_unique_words_positive * smoothing_factor)))})
        for word in self.words_and_count_negative:
            self.log_probability_negative.update({word: math.log10((self.words_and_count_negative[word] + smoothing_factor) / (total_words_negative + (total_unique_words_negative * smoothing_factor)))})

        # calculate log probabilities for all bigrams
        # add smoothing factor to smooth the value for bigram count, to ensures that we don't multiply by 0 if the bigram doesn't exists
        # add total unique bigrams multiply smoothing factor to smooth the denominator
        for word in self.bigrams_and_count_positive:
            self.bigrams_log_probability_positive.update({word: math.log10((self.bigrams_and_count_positive[word] + smoothing_factor) / (total_bigrams_positive + (total_unique_bigrams_positive * smoothing_factor)))})

        for word in self.bigrams_and_count_negative:
             self.bigrams_log_probability_negative.update({word: math.log10((self.bigrams_and_count_negative[word] + smoothing_factor) / (total_bigrams_negative + (total_unique_bigrams_negative * smoothing_factor)))})

    def classify(self, lines):
        test_reviews = []
        predictions = []

        for line in lines:
            line = line.replace('\n', '')
            fields = line.split('|')
            test_reviews.append(fields[2])

        # clean test reviews words
        cleaned_test_reviews = self.clean(test_reviews)

        for review in cleaned_test_reviews:
            # add each prior to each sum of log probability
            sum_of_log_probability_positive = self.prior_positive
            sum_of_log_probability_negative = self.prior_negative
            words = review.split(' ')

            # calculate the likelihood of words for each class
            for word in words:
                # add log probability only if word exists in train set
                if word in self.words_all:
                    sum_of_log_probability_positive += self.log_probability_positive[word]
                    sum_of_log_probability_negative += self.log_probability_negative[word]

            # calculate the likelihood of bigrams for each class
            for i in range(1, len(words)):
                if words[i] > words[i - 1]:
                    bigram = words[i - 1] + " " + words[i]
                else:
                    bigram = words[i] + " " + words[i - 1]
                # add log probability only if bigram exists in train set
                if bigram in self.bigrams_all:
                    sum_of_log_probability_positive += self.bigrams_log_probability_positive[bigram]
                    sum_of_log_probability_negative += self.bigrams_log_probability_negative[bigram]

            # predict class
            if sum_of_log_probability_positive > sum_of_log_probability_negative:
                predictions.append('5')
            else:
                predictions.append('1')

        return predictions

    def get_line(self, lines):
        review_positive = []
        review_negative = []

        # separate review to positive or negative class
        for line in lines:
            line = line.replace('\n', '')
            fields = line.split('|')
            if fields[0] == '5':
                review_positive.append(fields[2])
            else:
                review_negative.append(fields[2])

        return review_positive, review_negative

    def clean(self, reviews):
        cleaned_reviews = []

        re_pattern = r'([^a-zA-Z ]+?)'

        stop_words = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'as',
                      'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can',
                      'did', 'do', 'does', 'doing', 'don', 'down', 'during', 'each', 'few', 'for', 'from', 'further',
                      'had', 'has', 'have', 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his',
                      'how', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'itself', 'just', 'me', 'more', 'most', 'my',
                      'myself', 'no', 'nor', 'not', 'now', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our',
                      'ours', 'ourselves', 'out', 'over', 'own', 's', 'same', 'she', 'should', 'so', 'some', 'such',
                      't', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these',
                      'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'we',
                      'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'you',
                      'your', 'yours', 'yourself', 'yourselves']

        for review in reviews:
            cleaned_review = ""
            first = True
            words = review.split(' ')

            for word in words:
                # make all lowercase
                word = word.lower()
                # filter out all(punctuation and numbers), except alpha words
                word = re.sub(re_pattern, "", word)
                # filter out all stop words
                if word not in stop_words:
                    if not first:
                        cleaned_review = cleaned_review + ' ' + word
                    else:
                        cleaned_review = word
                        first = False
            cleaned_reviews.append(cleaned_review)

        return cleaned_reviews
