options(echo=TRUE)
arg <- commandArgs(trailingOnly = TRUE)
library(tools)
withoutExt = file_path_sans_ext(arg)

library(tidyverse)
library(tidytext)
library(readtext)
library(x13binary)
library(x12)
library(quanteda)
library(tm)
library(textmineR)
library(topicmodels)
library(readr)
library(tidyverse)
library(lda)
library(sjmisc)
library(sjlabelled)
library(insight)

# setwd("~/Downloads")
# mydir = "ethics_csv"
# myfiles = list.files(path=mydir, pattern="*.csv", full.names=TRUE)
# raw_data = ldply(myfiles, read_csv)
myfile = paste("C:/Users/slp70/Downloads/ethics_csv",arg,sep="/")
raw_data = read.csv(myfile)

wordsonly <- raw_data %>%
  select(title, text) 

wordsonly <- wordsonly %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words)

library(dplyr)
words_dtm <- wordsonly %>%
  count(title, word) %>%
  cast_dtm(title, word, n)

library(topicmodels)

words_lda <- LDA(words_dtm, k = 4, control = list(seed = 1234))

text_topics <- tidy(words_lda, matrix = "beta")

top_terms <- text_topics %>%
  group_by(topic) %>%
  slice_max(beta, n = 5) %>%
  ungroup() %>%
  arrange(topic, -beta)

top_terms

termstable = as.data.frame(top_terms)

outFile1 = paste("C:/Users/slp70/Downloads/ethics_csv",withoutExt,sep="/")
outFile = paste(outFile1,".txt",sep="")
termsstring = toString(termstable$term, width = NULL)
capture.output(termsstring, file=outFile, append=TRUE)

# isRelevant = ""
# if (str_contains(termsstring,"god")){
#   isRelevant = "true"
# } else {
#   isRelevant = "false"
# }

# top_terms %>%
#   mutate(term = reorder_within(term, beta, topic)) %>%
#   ggplot(aes(beta, term, fill = factor(topic))) +
#   geom_col(show.legend = FALSE) +
#   facet_wrap(~ topic, scales = "free") +
#   scale_y_reordered()
