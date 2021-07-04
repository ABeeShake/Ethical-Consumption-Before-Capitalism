library(tidyverse)
library(tidytext)
library(readtext)
library(x13binary)
library(x12)
library(quanteda)
library(tm)
library(textmineR)
library(topicmodels)
library(lda)

library(plyr)
setwd("~/Downloads")
mydir = "ethics_csv"
myfiles = list.files(path=mydir, pattern="*.csv", full.names=TRUE)
raw_data = ldply(myfiles, read_csv)

wordsonly <- raw_data %>%
  select(title, text) 

wordsonly <- wordsonly %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words)

detach(package:plyr,unload=TRUE)
library(dplyr)
words_dtm <- wordsonly %>%
  count(title, word) %>%
  cast_dtm(title, word, n)

library(topicmodels)

words_lda <- LDA(words_dtm, k = 16, control = list(seed = 1234))

text_topics <- tidy(words_lda, matrix = "beta")

top_terms <- text_topics %>%
  group_by(topic) %>%
  slice_max(beta, n = 5) %>%
  ungroup() %>%
  arrange(topic, -beta)

top_terms

top_terms %>%
  mutate(term = reorder_within(term, beta, topic)) %>%
  ggplot(aes(beta, term, fill = factor(topic))) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  scale_y_reordered()

