### Environment Setup ###

require(boxr)
require(stringi)
require(tidyverse)
require(tm)
require(tidytext)
require(textdata)
require(quanteda)

setwd("C:/Users/abhis/Documents/CollegeDocs/Data+/Sentiment Analysis")

### Load Data From Box ###

client_info <- read.table("./app.cfg",
                          sep = "\n", 
                          header = FALSE, 
                          row.names = c("client_id","client_secret"),
                          col.names = c("tokens"))

box_auth(client_id = client_info["client_id",],
         client_secret = client_info["client_secret",])

#use A1 for testing

data <- box_search("A1_P4.csv") %>%
  box_read()

### Data Cleaning ###

date_fixer <- function(date) {
  
  if (!(is.integer(date))) {
    
    date <- date %>%
      substring(3,6) %>%
      as.integer()
    
  }
  
  return(date)
  
}

data$date <- data$date %>%
  sapply(date_fixer) %>%
  as.data.frame()

data$decade <- (data$date %/% 10) * 10

data[,c("author","publisher","index")] <- list(NULL)

data <- data %>%
  data.table::data.table()

data <- data %>%
  mutate(
    title_length = stri_length(title) - stri_count_fixed(title, " ")
  )

### Compute Sentiment Scores ###

title_tokens <- data %>%
  group_by(date) %>%
  ungroup() %>%
  unnest_tokens(word,text)

score_sentiment <- function(dictionary, df) {
  
  sent_scores <- df %>%
    inner_join(get_sentiments(dictionary)) %>%
    count(title, sentiment) %>%
    pivot_wider(names_from = sentiment, values_from = n, values_fill = 0) %>% 
    mutate(sentiment = (positive - negative)/(positive + negative))
  
  return(sent_scores)
  
}

bing_sent <- score_sentiment("bing",title_tokens)
nrc_sent <- score_sentiment("nrc",title_tokens)
#afinn_sent <- score_sentiment("afinn", title_tokens)

data <- data %>% 
  inner_join(bing_sent, by = c("title")) %>%
  rename(sentiment_bing = sentiment)

data <- data %>%
  inner_join(nrc_sent, by = c("title")) %>%
  rename(sentiment_nrc = sentiment)

data[,c("negative.x","negative.y",
        "positive.x","positive.y",
        "anger","anticipation",
        "disgust","fear","joy",
        "sadness","surprise",
        "trust")] <- list(NULL)
  
data_long <- data %>%
  pivot_longer(cols = starts_with("sentiment"),
               names_to = "sentiment_type",
               names_prefix = "sentiment_",
               values_to = "sentiment_score")

sent_by_decade <- data %>%
  group_by(decade) %>%
  summarise_at(vars(sentiment_bing,sentiment_nrc),
               mean) %>%
  ungroup()

sent_by_decade_long <- sent_by_decade %>%
  pivot_longer(cols = starts_with("sentiment"),
               names_to = "sentiment_type",
               names_prefix = "sentiment_",
               values_to = "sentiment_score")

ggplot(data = data_long,
       mapping = aes(x = title_length, 
                     y = sentiment_score)) +
  geom_point() +
  labs(title = "Sentiment vs Title Length") +
  xlab("Number of Characters per Title") +
  ylab("Sentiment Score")

ggplot(data = data_long,
       mapping = aes(x = title_length, 
                     y = sentiment_score)) +
  geom_point(aes(color = sentiment_type)) +
  labs(title = "Sentiment vs Title Length", color = "Dictionary Used") +
  xlab("Number of Characters per Title") +
  ylab("Sentiment Score")

ggplot(data = sent_by_decade_long,
       mapping = aes(x = factor(decade), 
                     y = sentiment_score)) +
  geom_col(mapping = aes(fill = sentiment_type),
           position = "dodge2",
           na.rm = TRUE) +
  labs(title = "Average Sentiment by Decade", fill = "Dictionary Used") +
  xlab("Decade") +
  ylab("Sentiment Score")




