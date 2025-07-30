import pytest
import re
from evolvishub_ollama_adapter.text_utils import (
    clean_text,
    normalize_text,
    tokenize_text,
    remove_stopwords,
    stem_text,
    lemmatize_text,
    extract_keywords,
    calculate_similarity,
    format_text,
    truncate_text,
    split_text,
    join_text,
    count_words,
    count_characters,
    count_sentences,
    count_paragraphs,
    get_text_statistics,
    extract_entities,
    extract_phrases,
    extract_sentences,
    extract_paragraphs,
    extract_words,
    extract_characters,
    extract_numbers,
    extract_urls,
    extract_emails,
    extract_hashtags,
    extract_mentions,
    extract_dates,
    extract_times,
    extract_currencies,
    extract_measurements,
    extract_phone_numbers,
    extract_addresses,
    extract_names,
    extract_titles,
    extract_organizations,
    extract_locations,
    extract_languages,
    extract_topics,
    extract_summary,
    extract_keywords_tfidf,
    extract_keywords_rake,
    extract_keywords_yake,
    extract_keywords_textrank,
    extract_keywords_bert,
    extract_keywords_roberta,
    extract_keywords_xlnet,
    extract_keywords_albert,
    extract_keywords_distilbert,
    extract_keywords_electra,
    extract_keywords_gpt2,
    extract_keywords_t5,
    extract_keywords_bart,
    extract_keywords_pegasus,
    extract_keywords_mt5,
    extract_keywords_mbart,
    extract_keywords_prophetnet,
    extract_keywords_reformer,
    extract_keywords_longformer,
    extract_keywords_bigbird,
    extract_keywords_led,
    extract_keywords_m2m100,
    extract_keywords_marian,
    extract_keywords_mbart50,
    extract_keywords_nllb
)

@pytest.fixture
def sample_text():
    """Create a sample text for testing."""
    return """
    Hello, World! This is a sample text for testing.
    It contains multiple sentences and paragraphs.
    
    Here's another paragraph with some numbers: 123, 456, 789.
    And some URLs: https://example.com, http://test.org.
    
    Contact us at test@example.com or call +1-234-567-8900.
    Follow us on Twitter @example and #testing.
    
    The meeting is scheduled for 2024-03-20 at 14:30.
    The price is $99.99 and the weight is 2.5 kg.
    
    Dr. John Smith works at Acme Corp. in New York.
    The project is led by Prof. Jane Doe from MIT.
    """

def test_clean_text(sample_text):
    """Test text cleaning."""
    cleaned = clean_text(sample_text)
    assert isinstance(cleaned, str)
    assert len(cleaned) > 0
    assert not cleaned.startswith('\n')
    assert not cleaned.endswith('\n')
    
    # Test with empty text
    assert clean_text('') == ''
    
    # Test with None
    with pytest.raises(ValueError):
        clean_text(None)

def test_normalize_text(sample_text):
    """Test text normalization."""
    normalized = normalize_text(sample_text)
    assert isinstance(normalized, str)
    assert len(normalized) > 0
    
    # Test with empty text
    assert normalize_text('') == ''
    
    # Test with None
    with pytest.raises(ValueError):
        normalize_text(None)

def test_tokenize_text(sample_text):
    """Test text tokenization."""
    tokens = tokenize_text(sample_text)
    assert isinstance(tokens, list)
    assert len(tokens) > 0
    assert all(isinstance(token, str) for token in tokens)
    
    # Test with empty text
    assert tokenize_text('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        tokenize_text(None)

def test_remove_stopwords(sample_text):
    """Test stopword removal."""
    tokens = tokenize_text(sample_text)
    filtered = remove_stopwords(tokens)
    assert isinstance(filtered, list)
    assert len(filtered) <= len(tokens)
    assert all(isinstance(token, str) for token in filtered)
    
    # Test with empty list
    assert remove_stopwords([]) == []
    
    # Test with None
    with pytest.raises(ValueError):
        remove_stopwords(None)

def test_stem_text(sample_text):
    """Test text stemming."""
    tokens = tokenize_text(sample_text)
    stemmed = stem_text(tokens)
    assert isinstance(stemmed, list)
    assert len(stemmed) == len(tokens)
    assert all(isinstance(token, str) for token in stemmed)
    
    # Test with empty list
    assert stem_text([]) == []
    
    # Test with None
    with pytest.raises(ValueError):
        stem_text(None)

def test_lemmatize_text(sample_text):
    """Test text lemmatization."""
    tokens = tokenize_text(sample_text)
    lemmatized = lemmatize_text(tokens)
    assert isinstance(lemmatized, list)
    assert len(lemmatized) == len(tokens)
    assert all(isinstance(token, str) for token in lemmatized)
    
    # Test with empty list
    assert lemmatize_text([]) == []
    
    # Test with None
    with pytest.raises(ValueError):
        lemmatize_text(None)

def test_extract_keywords(sample_text):
    """Test keyword extraction."""
    keywords = extract_keywords(sample_text)
    assert isinstance(keywords, list)
    assert len(keywords) > 0
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords(None)

def test_calculate_similarity():
    """Test text similarity calculation."""
    text1 = "This is a test"
    text2 = "This is another test"
    similarity = calculate_similarity(text1, text2)
    assert isinstance(similarity, float)
    assert 0 <= similarity <= 1
    
    # Test with empty texts
    assert calculate_similarity('', '') == 1.0
    assert calculate_similarity('', 'test') == 0.0
    
    # Test with None
    with pytest.raises(ValueError):
        calculate_similarity(None, text2)
    with pytest.raises(ValueError):
        calculate_similarity(text1, None)

def test_format_text(sample_text):
    """Test text formatting."""
    formatted = format_text(sample_text)
    assert isinstance(formatted, str)
    assert len(formatted) > 0
    
    # Test with empty text
    assert format_text('') == ''
    
    # Test with None
    with pytest.raises(ValueError):
        format_text(None)

def test_truncate_text(sample_text):
    """Test text truncation."""
    truncated = truncate_text(sample_text, 50)
    assert isinstance(truncated, str)
    assert len(truncated) <= 50
    
    # Test with empty text
    assert truncate_text('', 50) == ''
    
    # Test with None
    with pytest.raises(ValueError):
        truncate_text(None, 50)

def test_split_text(sample_text):
    """Test text splitting."""
    splits = split_text(sample_text)
    assert isinstance(splits, list)
    assert len(splits) > 0
    assert all(isinstance(split, str) for split in splits)
    
    # Test with empty text
    assert split_text('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        split_text(None)

def test_join_text():
    """Test text joining."""
    texts = ['Hello', 'World', '!']
    joined = join_text(texts)
    assert isinstance(joined, str)
    assert joined == 'Hello World !'
    
    # Test with empty list
    assert join_text([]) == ''
    
    # Test with None
    with pytest.raises(ValueError):
        join_text(None)

def test_count_words(sample_text):
    """Test word counting."""
    count = count_words(sample_text)
    assert isinstance(count, int)
    assert count > 0
    
    # Test with empty text
    assert count_words('') == 0
    
    # Test with None
    with pytest.raises(ValueError):
        count_words(None)

def test_count_characters(sample_text):
    """Test character counting."""
    count = count_characters(sample_text)
    assert isinstance(count, int)
    assert count > 0
    
    # Test with empty text
    assert count_characters('') == 0
    
    # Test with None
    with pytest.raises(ValueError):
        count_characters(None)

def test_count_sentences(sample_text):
    """Test sentence counting."""
    count = count_sentences(sample_text)
    assert isinstance(count, int)
    assert count > 0
    
    # Test with empty text
    assert count_sentences('') == 0
    
    # Test with None
    with pytest.raises(ValueError):
        count_sentences(None)

def test_count_paragraphs(sample_text):
    """Test paragraph counting."""
    count = count_paragraphs(sample_text)
    assert isinstance(count, int)
    assert count > 0
    
    # Test with empty text
    assert count_paragraphs('') == 0
    
    # Test with None
    with pytest.raises(ValueError):
        count_paragraphs(None)

def test_get_text_statistics(sample_text):
    """Test text statistics."""
    stats = get_text_statistics(sample_text)
    assert isinstance(stats, dict)
    assert 'words' in stats
    assert 'characters' in stats
    assert 'sentences' in stats
    assert 'paragraphs' in stats
    
    # Test with empty text
    stats = get_text_statistics('')
    assert stats['words'] == 0
    assert stats['characters'] == 0
    assert stats['sentences'] == 0
    assert stats['paragraphs'] == 0
    
    # Test with None
    with pytest.raises(ValueError):
        get_text_statistics(None)

def test_extract_entities(sample_text):
    """Test entity extraction."""
    entities = extract_entities(sample_text)
    assert isinstance(entities, list)
    assert all(isinstance(entity, str) for entity in entities)
    
    # Test with empty text
    assert extract_entities('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_entities(None)

def test_extract_phrases(sample_text):
    """Test phrase extraction."""
    phrases = extract_phrases(sample_text)
    assert isinstance(phrases, list)
    assert all(isinstance(phrase, str) for phrase in phrases)
    
    # Test with empty text
    assert extract_phrases('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_phrases(None)

def test_extract_sentences(sample_text):
    """Test sentence extraction."""
    sentences = extract_sentences(sample_text)
    assert isinstance(sentences, list)
    assert all(isinstance(sentence, str) for sentence in sentences)
    
    # Test with empty text
    assert extract_sentences('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_sentences(None)

def test_extract_paragraphs(sample_text):
    """Test paragraph extraction."""
    paragraphs = extract_paragraphs(sample_text)
    assert isinstance(paragraphs, list)
    assert all(isinstance(paragraph, str) for paragraph in paragraphs)
    
    # Test with empty text
    assert extract_paragraphs('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_paragraphs(None)

def test_extract_words(sample_text):
    """Test word extraction."""
    words = extract_words(sample_text)
    assert isinstance(words, list)
    assert all(isinstance(word, str) for word in words)
    
    # Test with empty text
    assert extract_words('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_words(None)

def test_extract_characters(sample_text):
    """Test character extraction."""
    characters = extract_characters(sample_text)
    assert isinstance(characters, list)
    assert all(isinstance(char, str) for char in characters)
    
    # Test with empty text
    assert extract_characters('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_characters(None)

def test_extract_numbers(sample_text):
    """Test number extraction."""
    numbers = extract_numbers(sample_text)
    assert isinstance(numbers, list)
    assert all(isinstance(num, str) for num in numbers)
    
    # Test with empty text
    assert extract_numbers('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_numbers(None)

def test_extract_urls(sample_text):
    """Test URL extraction."""
    urls = extract_urls(sample_text)
    assert isinstance(urls, list)
    assert all(isinstance(url, str) for url in urls)
    assert all(url.startswith(('http://', 'https://')) for url in urls)
    
    # Test with empty text
    assert extract_urls('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_urls(None)

def test_extract_emails(sample_text):
    """Test email extraction."""
    emails = extract_emails(sample_text)
    assert isinstance(emails, list)
    assert all(isinstance(email, str) for email in emails)
    assert all('@' in email for email in emails)
    
    # Test with empty text
    assert extract_emails('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_emails(None)

def test_extract_hashtags(sample_text):
    """Test hashtag extraction."""
    hashtags = extract_hashtags(sample_text)
    assert isinstance(hashtags, list)
    assert all(isinstance(tag, str) for tag in hashtags)
    assert all(tag.startswith('#') for tag in hashtags)
    
    # Test with empty text
    assert extract_hashtags('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_hashtags(None)

def test_extract_mentions(sample_text):
    """Test mention extraction."""
    mentions = extract_mentions(sample_text)
    assert isinstance(mentions, list)
    assert all(isinstance(mention, str) for mention in mentions)
    assert all(mention.startswith('@') for mention in mentions)
    
    # Test with empty text
    assert extract_mentions('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_mentions(None)

def test_extract_dates(sample_text):
    """Test date extraction."""
    dates = extract_dates(sample_text)
    assert isinstance(dates, list)
    assert all(isinstance(date, str) for date in dates)
    
    # Test with empty text
    assert extract_dates('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_dates(None)

def test_extract_times(sample_text):
    """Test time extraction."""
    times = extract_times(sample_text)
    assert isinstance(times, list)
    assert all(isinstance(time, str) for time in times)
    
    # Test with empty text
    assert extract_times('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_times(None)

def test_extract_currencies(sample_text):
    """Test currency extraction."""
    currencies = extract_currencies(sample_text)
    assert isinstance(currencies, list)
    assert all(isinstance(currency, str) for currency in currencies)
    assert all(currency.startswith('$') for currency in currencies)
    
    # Test with empty text
    assert extract_currencies('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_currencies(None)

def test_extract_measurements(sample_text):
    """Test measurement extraction."""
    measurements = extract_measurements(sample_text)
    assert isinstance(measurements, list)
    assert all(isinstance(measurement, str) for measurement in measurements)
    
    # Test with empty text
    assert extract_measurements('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_measurements(None)

def test_extract_phone_numbers(sample_text):
    """Test phone number extraction."""
    numbers = extract_phone_numbers(sample_text)
    assert isinstance(numbers, list)
    assert all(isinstance(number, str) for number in numbers)
    
    # Test with empty text
    assert extract_phone_numbers('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_phone_numbers(None)

def test_extract_addresses(sample_text):
    """Test address extraction."""
    addresses = extract_addresses(sample_text)
    assert isinstance(addresses, list)
    assert all(isinstance(address, str) for address in addresses)
    
    # Test with empty text
    assert extract_addresses('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_addresses(None)

def test_extract_names(sample_text):
    """Test name extraction."""
    names = extract_names(sample_text)
    assert isinstance(names, list)
    assert all(isinstance(name, str) for name in names)
    
    # Test with empty text
    assert extract_names('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_names(None)

def test_extract_titles(sample_text):
    """Test title extraction."""
    titles = extract_titles(sample_text)
    assert isinstance(titles, list)
    assert all(isinstance(title, str) for title in titles)
    
    # Test with empty text
    assert extract_titles('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_titles(None)

def test_extract_organizations(sample_text):
    """Test organization extraction."""
    organizations = extract_organizations(sample_text)
    assert isinstance(organizations, list)
    assert all(isinstance(org, str) for org in organizations)
    
    # Test with empty text
    assert extract_organizations('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_organizations(None)

def test_extract_locations(sample_text):
    """Test location extraction."""
    locations = extract_locations(sample_text)
    assert isinstance(locations, list)
    assert all(isinstance(location, str) for location in locations)
    
    # Test with empty text
    assert extract_locations('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_locations(None)

def test_extract_languages(sample_text):
    """Test language extraction."""
    languages = extract_languages(sample_text)
    assert isinstance(languages, list)
    assert all(isinstance(lang, str) for lang in languages)
    
    # Test with empty text
    assert extract_languages('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_languages(None)

def test_extract_topics(sample_text):
    """Test topic extraction."""
    topics = extract_topics(sample_text)
    assert isinstance(topics, list)
    assert all(isinstance(topic, str) for topic in topics)
    
    # Test with empty text
    assert extract_topics('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_topics(None)

def test_extract_summary(sample_text):
    """Test text summarization."""
    summary = extract_summary(sample_text)
    assert isinstance(summary, str)
    assert len(summary) < len(sample_text)
    
    # Test with empty text
    assert extract_summary('') == ''
    
    # Test with None
    with pytest.raises(ValueError):
        extract_summary(None)

def test_extract_keywords_tfidf(sample_text):
    """Test TF-IDF keyword extraction."""
    keywords = extract_keywords_tfidf(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_tfidf('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_tfidf(None)

def test_extract_keywords_rake(sample_text):
    """Test RAKE keyword extraction."""
    keywords = extract_keywords_rake(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_rake('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_rake(None)

def test_extract_keywords_yake(sample_text):
    """Test YAKE keyword extraction."""
    keywords = extract_keywords_yake(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_yake('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_yake(None)

def test_extract_keywords_textrank(sample_text):
    """Test TextRank keyword extraction."""
    keywords = extract_keywords_textrank(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_textrank('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_textrank(None)

def test_extract_keywords_bert(sample_text):
    """Test BERT keyword extraction."""
    keywords = extract_keywords_bert(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_bert('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_bert(None)

def test_extract_keywords_roberta(sample_text):
    """Test RoBERTa keyword extraction."""
    keywords = extract_keywords_roberta(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_roberta('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_roberta(None)

def test_extract_keywords_xlnet(sample_text):
    """Test XLNet keyword extraction."""
    keywords = extract_keywords_xlnet(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_xlnet('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_xlnet(None)

def test_extract_keywords_albert(sample_text):
    """Test ALBERT keyword extraction."""
    keywords = extract_keywords_albert(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_albert('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_albert(None)

def test_extract_keywords_distilbert(sample_text):
    """Test DistilBERT keyword extraction."""
    keywords = extract_keywords_distilbert(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_distilbert('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_distilbert(None)

def test_extract_keywords_electra(sample_text):
    """Test ELECTRA keyword extraction."""
    keywords = extract_keywords_electra(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_electra('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_electra(None)

def test_extract_keywords_gpt2(sample_text):
    """Test GPT-2 keyword extraction."""
    keywords = extract_keywords_gpt2(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_gpt2('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_gpt2(None)

def test_extract_keywords_t5(sample_text):
    """Test T5 keyword extraction."""
    keywords = extract_keywords_t5(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_t5('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_t5(None)

def test_extract_keywords_bart(sample_text):
    """Test BART keyword extraction."""
    keywords = extract_keywords_bart(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_bart('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_bart(None)

def test_extract_keywords_pegasus(sample_text):
    """Test PEGASUS keyword extraction."""
    keywords = extract_keywords_pegasus(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_pegasus('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_pegasus(None)

def test_extract_keywords_mt5(sample_text):
    """Test mT5 keyword extraction."""
    keywords = extract_keywords_mt5(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_mt5('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_mt5(None)

def test_extract_keywords_mbart(sample_text):
    """Test mBART keyword extraction."""
    keywords = extract_keywords_mbart(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_mbart('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_mbart(None)

def test_extract_keywords_prophetnet(sample_text):
    """Test ProphetNet keyword extraction."""
    keywords = extract_keywords_prophetnet(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_prophetnet('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_prophetnet(None)

def test_extract_keywords_reformer(sample_text):
    """Test Reformer keyword extraction."""
    keywords = extract_keywords_reformer(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_reformer('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_reformer(None)

def test_extract_keywords_longformer(sample_text):
    """Test Longformer keyword extraction."""
    keywords = extract_keywords_longformer(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_longformer('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_longformer(None)

def test_extract_keywords_bigbird(sample_text):
    """Test BigBird keyword extraction."""
    keywords = extract_keywords_bigbird(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_bigbird('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_bigbird(None)

def test_extract_keywords_led(sample_text):
    """Test LED keyword extraction."""
    keywords = extract_keywords_led(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_led('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_led(None)

def test_extract_keywords_m2m100(sample_text):
    """Test M2M100 keyword extraction."""
    keywords = extract_keywords_m2m100(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_m2m100('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_m2m100(None)

def test_extract_keywords_marian(sample_text):
    """Test Marian keyword extraction."""
    keywords = extract_keywords_marian(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_marian('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_marian(None)

def test_extract_keywords_mbart50(sample_text):
    """Test mBART50 keyword extraction."""
    keywords = extract_keywords_mbart50(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_mbart50('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_mbart50(None)

def test_extract_keywords_nllb(sample_text):
    """Test NLLB keyword extraction."""
    keywords = extract_keywords_nllb(sample_text)
    assert isinstance(keywords, list)
    assert all(isinstance(keyword, str) for keyword in keywords)
    
    # Test with empty text
    assert extract_keywords_nllb('') == []
    
    # Test with None
    with pytest.raises(ValueError):
        extract_keywords_nllb(None) 